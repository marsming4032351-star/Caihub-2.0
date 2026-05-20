from __future__ import annotations

import os
import shutil
import smtplib
import subprocess
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from glob import glob


DEFAULT_PROMPT = """请帮我生成一封可直接发送的「今日 AI+餐饮观察」邮件正文。

要求如下：

1. 搜索今天与“AI + 餐饮”高度相关的公开资讯，优先关注：
- 餐饮数字化
- 智能厨房 / 后厨自动化
- 餐饮机器人
- 餐饮 SaaS
- 外卖 / 配送智能化
- 餐饮供应链数字化
- 餐饮营销与会员智能化
- 餐饮行业中的 AI 产品、融资、合作、技术落地

2. 只保留最相关的 5 条，不要泛科技新闻，也不要低相关内容凑数。

3. 邮件正文结构固定为：

标题：今日 AI+餐饮观察 | YYYY-MM-DD

开头导语：
- 用 1 段话总结今天最值得关注的核心变化，不超过 120 字。

今日值得关注的 5 条资讯：
1. 标题
摘要：
为什么值得关注：
链接：

2. 标题
摘要：
为什么值得关注：
链接：

3. 标题
摘要：
为什么值得关注：
链接：

4. 标题
摘要：
为什么值得关注：
链接：

5. 标题
摘要：
为什么值得关注：
链接：

一句话总结：
- 用一句话总结今天 AI+餐饮赛道的核心趋势。

4. 全文用中文输出，风格专业、简洁、像一位长期关注 AI+餐饮行业的人写给创业者/投资人的每日观察。
5. 不要输出多余说明，不要解释过程，不要说“如果你愿意我可以继续”，只输出最终邮件正文。"""


@dataclass
class Settings:
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    recipients: list[str]
    alert_recipients: list[str]
    openclaw_bin: str
    openclaw_agents: list[str]
    openclaw_to: str
    openclaw_session_id: str
    subject_prefix: str
    prompt_file: str | None
    state_file: str
    max_retries: int


def load_env_file() -> None:
    shared_env_file = Path(
        os.getenv(
            "AI_FOOD_NEWS_SHARED_ENV_FILE",
            str(Path.home() / ".openclaw" / "ai-food-news-shared.env"),
        )
    ).expanduser()
    env_file = Path(
        os.getenv(
            "AI_FOOD_NEWS_ENV_FILE",
            str(Path.home() / ".openclaw" / "ai-food-news.env"),
        )
    ).expanduser()

    for file_path in (shared_env_file, env_file):
        if not file_path.exists():
            continue
        for raw_line in file_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def get_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def load_recipients() -> list[str]:
    recipients_value = os.getenv("AI_FOOD_NEWS_RECIPIENTS", "").strip()
    if recipients_value:
        recipients = [item.strip() for item in recipients_value.split(",") if item.strip()]
        if recipients:
            return recipients
    return [get_required_env("AI_FOOD_NEWS_RECIPIENT")]


def load_alert_recipients(smtp_username: str) -> list[str]:
    recipients_value = os.getenv("AI_FOOD_NEWS_ALERT_RECIPIENTS", "").strip()
    if recipients_value:
        recipients = [item.strip() for item in recipients_value.split(",") if item.strip()]
        if recipients:
            return recipients
    return [smtp_username]


def load_openclaw_agents() -> list[str]:
    raw = os.getenv("AI_FOOD_NEWS_AGENT", "ai-food-news").strip()
    agents = [item.strip() for item in raw.split(",") if item.strip()]
    if not agents:
        raise RuntimeError("Missing OpenClaw agent configuration: AI_FOOD_NEWS_AGENT")
    return agents


def resolve_openclaw_bin() -> str:
    configured = os.getenv("AI_FOOD_NEWS_OPENCLAW_BIN", "").strip()
    if configured:
        return str(Path(configured).expanduser())

    resolved = shutil.which("openclaw")
    if resolved:
        return resolved

    candidates = sorted(
        glob(str(Path.home() / ".nvm" / "versions" / "node" / "*" / "bin" / "openclaw"))
    )
    if candidates:
        return candidates[-1]

    raise RuntimeError(
        "Unable to locate the 'openclaw' binary. Set AI_FOOD_NEWS_OPENCLAW_BIN explicitly."
    )


def derive_session_target(base_to: str) -> str:
    scope = os.getenv("AI_FOOD_NEWS_SESSION_SCOPE", "daily").strip().lower()
    if scope != "daily":
        return base_to

    digits = "".join(ch for ch in base_to if ch.isdigit())
    if not digits:
        return base_to

    today_suffix = datetime.now().strftime("%y%m%d")
    derived_digits = f"{digits[:-6]}{today_suffix}" if len(digits) > 6 else today_suffix
    return f"+{derived_digits}"


def derive_session_id(agent: str) -> str:
    scope = os.getenv("AI_FOOD_NEWS_SESSION_SCOPE", "daily").strip().lower()
    if scope in {"per-run", "run", "retry-safe"}:
        return str(uuid.uuid4())

    if scope != "daily":
        return str(uuid.uuid4())

    seed = f"{agent}:{datetime.now().strftime('%Y-%m-%d')}"
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))


def load_settings() -> Settings:
    openclaw_agents = load_openclaw_agents()
    smtp_username = get_required_env("AI_FOOD_NEWS_SMTP_USERNAME")
    return Settings(
        smtp_host=os.getenv("AI_FOOD_NEWS_SMTP_HOST", "smtp.gmail.com"),
        smtp_port=int(os.getenv("AI_FOOD_NEWS_SMTP_PORT", "587")),
        smtp_username=smtp_username,
        smtp_password=get_required_env("AI_FOOD_NEWS_SMTP_PASSWORD"),
        recipients=load_recipients(),
        alert_recipients=load_alert_recipients(smtp_username),
        openclaw_bin=resolve_openclaw_bin(),
        openclaw_agents=openclaw_agents,
        openclaw_to=derive_session_target(os.getenv("AI_FOOD_NEWS_TO", "+8613900000013")),
        openclaw_session_id=derive_session_id(openclaw_agents[0]),
        subject_prefix=os.getenv("AI_FOOD_NEWS_SUBJECT_PREFIX", "今日 AI+餐饮观察"),
        prompt_file=os.getenv("AI_FOOD_NEWS_PROMPT_FILE") or None,
        state_file=os.getenv(
            "AI_FOOD_NEWS_STATE_FILE",
            str(Path.home() / ".openclaw" / "state" / "ai-food-news-last-sent.txt"),
        ),
        max_retries=int(os.getenv("AI_FOOD_NEWS_MAX_RETRIES", "3")),
    )


def load_prompt(prompt_file: str | None) -> str:
    if not prompt_file:
        return DEFAULT_PROMPT

    path = Path(prompt_file).expanduser()
    return path.read_text(encoding="utf-8").strip()


def sanitize_openclaw_output(raw_output: str) -> str:
    body = raw_output.strip()
    if not body:
        raise RuntimeError("OpenClaw returned empty output.")

    # Drop tool/debug chatter before the actual mail body.
    title_index = body.find("标题：")
    if title_index != -1:
        body = body[title_index:].strip()

    error_markers = (
        "Codex error:",
        '"type":"server_error"',
        "OpenClaw agent command failed.",
    )
    if any(marker in body for marker in error_markers):
        raise RuntimeError(f"OpenClaw returned an invalid response:\n{body}")

    required_markers = (
        "标题：",
        "开头导语：",
        "一句话总结：",
        "今日值得关注的 5 条资讯：",
        "本周总览：",
        "本周 7 条重点资讯：",
        "本周一句结论：",
    )
    blocked_markers = (
        "--final",
        "写入输出文件",
        "提交 git",
        "新增提交",
        "关键提交",
        "我继续把",
        "做完我会跑一遍",
        "继续做完了",
        "终端预览效果",
        "脚本多了一个",
        "以后你基本只要说一句",
    )
    if any(marker in body for marker in blocked_markers):
        raise RuntimeError(f"OpenClaw output contains blocked workflow chatter:\n{body}")

    if not body.startswith("标题：") and "今日 AI+餐饮" not in body and "本周 AI+餐饮" not in body:
        raise RuntimeError(f"OpenClaw output does not look like a newsletter body:\n{body}")

    if not any(marker in body for marker in required_markers):
        raise RuntimeError(f"OpenClaw output is missing expected newsletter sections:\n{body}")

    return body


def run_openclaw(
    openclaw_bin: str,
    agent: str,
    to: str,
    session_id: str,
    prompt: str,
    max_retries: int,
) -> str:
    command = [
        openclaw_bin,
        "agent",
        "--agent",
        agent,
        "--session-id",
        session_id,
        "--to",
        to,
        "--message",
        prompt,
    ]
    last_error: RuntimeError | None = None
    for attempt in range(1, max_retries + 1):
        attempt_session_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{session_id}:attempt:{attempt}"))
        attempt_command = command.copy()
        session_id_index = attempt_command.index("--session-id") + 1
        attempt_command[session_id_index] = attempt_session_id
        result = subprocess.run(
            attempt_command,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            try:
                return sanitize_openclaw_output(result.stdout)
            except RuntimeError as exc:
                last_error = exc
        else:
            last_error = RuntimeError(
                "OpenClaw agent command failed.\n"
                f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )

        if attempt < max_retries:
            time.sleep(2 * attempt)

    assert last_error is not None
    raise last_error


def run_openclaw_with_fallbacks(settings: Settings, prompt: str) -> str:
    errors: list[str] = []
    for agent in settings.openclaw_agents:
        try:
            return run_openclaw(
                openclaw_bin=settings.openclaw_bin,
                agent=agent,
                to=settings.openclaw_to,
                session_id=derive_session_id(agent),
                prompt=prompt,
                max_retries=settings.max_retries,
            )
        except RuntimeError as exc:
            errors.append(f"[{agent}] {exc}")

    raise RuntimeError("All OpenClaw agents failed.\n" + "\n\n".join(errors))


def send_email(settings: Settings, body: str) -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    send_email_message(
        settings=settings,
        recipients=settings.recipients,
        subject=f"{settings.subject_prefix} | {today}",
        body=body,
    )


def send_email_message(settings: Settings, recipients: list[str], subject: str, body: str) -> None:
    message = EmailMessage()
    message["From"] = settings.smtp_username
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as server:
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(message, to_addrs=recipients)


def send_failure_alert(settings: Settings, error: Exception) -> None:
    now = datetime.now()
    next_retry = now.replace(hour=9, minute=5, second=0, microsecond=0)
    body = "\n".join(
        [
            "今日 AI+餐饮日报自动发送失败。",
            "",
            f"失败时间：{now.strftime('%Y-%m-%d %H:%M:%S')}",
            f"尝试 Agent：{', '.join(settings.openclaw_agents)}",
            f"主收件人：{', '.join(settings.recipients)}",
            "",
            "错误摘要：",
            str(error),
            "",
            f"系统会继续按既有调度自动重试；最近一次补跑时间是 {next_retry.strftime('%Y-%m-%d %H:%M')}。",
        ]
    )
    send_email_message(
        settings=settings,
        recipients=settings.alert_recipients,
        subject=f"[告警] {settings.subject_prefix} 发送失败 | {now.strftime('%Y-%m-%d %H:%M')}",
        body=body,
    )


def already_sent_today(state_file: str) -> bool:
    path = Path(state_file).expanduser()
    if not path.exists():
        return False
    return path.read_text(encoding="utf-8").strip() == datetime.now().strftime("%Y-%m-%d")


def mark_sent_today(state_file: str) -> None:
    path = Path(state_file).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(datetime.now().strftime("%Y-%m-%d"), encoding="utf-8")


def main() -> None:
    load_env_file()
    settings = load_settings()
    recipients_label = ", ".join(settings.recipients)
    if already_sent_today(settings.state_file):
        print(f"Skip sending: already sent today to {recipients_label}")
        return
    try:
        prompt = load_prompt(settings.prompt_file)
        body = run_openclaw_with_fallbacks(settings, prompt)
        send_email(settings, body)
        mark_sent_today(settings.state_file)
        print(f"Email sent to {recipients_label}")
    except Exception as exc:
        try:
            send_failure_alert(settings, exc)
            print(f"Failure alert sent to {', '.join(settings.alert_recipients)}")
        except Exception as alert_exc:
            print(f"Failure alert also failed: {alert_exc}")
        raise


if __name__ == "__main__":
    main()
