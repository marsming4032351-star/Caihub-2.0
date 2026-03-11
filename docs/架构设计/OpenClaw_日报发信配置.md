# OpenClaw 日报发信配置

这份说明用于把 `ai-food-news` 子智能体生成的日报，通过 Gmail 自动发送到指定邮箱。

## 1. 目标结构

```text
OpenClaw ai-food-news
  -> 搜索 AI+餐饮资讯
  -> 生成日报正文
  -> 本地脚本调用 Gmail SMTP
  -> 发送到你的 Gmail
```

## 2. 准备条件

- `OpenClaw` 已安装并可运行
- 已创建 `ai-food-news` 子智能体
- Gmail 已开启两步验证
- 已生成 Gmail App Password

## 3. 环境变量

推荐拆成两层：

- 共享文件：`~/.openclaw/ai-food-news-shared.env`
- 日报专属文件：`~/.openclaw/ai-food-news.env`

先写共享文件：

```bash
mkdir -p ~/.openclaw
cat > ~/.openclaw/ai-food-news-shared.env <<'EOF'
AI_FOOD_NEWS_SMTP_HOST=smtp.gmail.com
AI_FOOD_NEWS_SMTP_PORT=587
AI_FOOD_NEWS_SMTP_USERNAME=你的 Gmail 地址
AI_FOOD_NEWS_SMTP_PASSWORD=你的 Gmail App Password
AI_FOOD_NEWS_RECIPIENT=收件邮箱地址
AI_FOOD_NEWS_RECIPIENTS=你的 Gmail 地址,84369563@qq.com,605229578@qq.com,315865302@qq.com
EOF
```

再写日报专属文件：

```bash
cat > ~/.openclaw/ai-food-news.env <<'EOF'
AI_FOOD_NEWS_AGENT=ai-food-news
AI_FOOD_NEWS_TO=+8613900000013
AI_FOOD_NEWS_SUBJECT_PREFIX=今日 AI+餐饮观察
AI_FOOD_NEWS_MAX_RETRIES=3
EOF
```

也可以在本机 shell 配置中加入这些变量：

```bash
export AI_FOOD_NEWS_SHARED_ENV_FILE="$HOME/.openclaw/ai-food-news-shared.env"
export AI_FOOD_NEWS_AGENT="ai-food-news"
export AI_FOOD_NEWS_TO="+8613900000013"
export AI_FOOD_NEWS_SUBJECT_PREFIX="今日 AI+餐饮观察"
export AI_FOOD_NEWS_MAX_RETRIES="3"
```

说明：

- `AI_FOOD_NEWS_SMTP_USERNAME`
  用来发信的 Gmail 地址
- `AI_FOOD_NEWS_SMTP_PASSWORD`
  Gmail App Password，不是 Gmail 登录密码
- `AI_FOOD_NEWS_RECIPIENT`
  收件人邮箱，可以填你自己的 Gmail
- `AI_FOOD_NEWS_RECIPIENTS`
  多收件人模式，多个邮箱用英文逗号分隔；设置后会优先于 `AI_FOOD_NEWS_RECIPIENT`
- `AI_FOOD_NEWS_SHARED_ENV_FILE`
  共享配置文件，日报和周报都会先读取它；适合统一维护 SMTP 和收件人列表
- `AI_FOOD_NEWS_TO`
  OpenClaw 用来生成独立 session key 的占位号码；建议把这个号码专门留给自动化，不要在手动测试时复用
- `AI_FOOD_NEWS_MAX_RETRIES`
  OpenClaw 或 SMTP 瞬时失败时的自动重试次数

## 4. 手动测试发送

执行：

```bash
python3 /Users/ming/CaiHub/scripts/send_ai_food_news_email.py
```

成功后会输出：

```text
Email sent to your-email@example.com
```

说明：

- 脚本会先读取 `~/.openclaw/ai-food-news-shared.env`
- 再读取 `~/.openclaw/ai-food-news.env`
- 所以 `launchd` / `cron` 触发时也能拿到配置

## 5. 自定义 prompt

如果你想换成自己的日报 prompt，可以把 prompt 写到文件里，然后增加：

```bash
export AI_FOOD_NEWS_PROMPT_FILE="/path/to/prompt.txt"
```

脚本会优先读取该文件。

## 6. 定时发送

### 方案 A：用 OpenClaw cron

先确保脚本可以手动发送成功，再加 cron：

```bash
openclaw cron add \
  --name ai-food-news-email \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --system-event "run-ai-food-news-email" \
  --description "每日早上 9 点发送 AI+餐饮资讯日报"
```

注意：

- 这个命令只创建调度项
- 如果你要让 OpenClaw 直接调用脚本，还需要后续把 system event 和本地执行流程接起来

### 方案 B：先用系统 cron / launchd

对个人机器更简单，建议先这样做。

例如用 `crontab -e`：

```cron
0 9 * * * /usr/bin/python3 /Users/ming/CaiHub/scripts/send_ai_food_news_email.py >> /Users/ming/.openclaw/logs/ai-food-news-email.log 2>&1
```

## 7. 推荐顺序

1. 先手动执行脚本
2. 确认邮件格式满意
3. 再加定时任务

## 8. 会话隔离规则

- 自动化日报专用：`AI_FOOD_NEWS_TO=+8613900000013`
- 自动化周报专用：`AI_FOOD_NEWS_TO=+8613900000020`
- 手动测试时不要复用上面两个号码
- 手动实验建议单独使用一个测试号码，例如：`+8613900000099`
- 更稳的做法是拆两个 agent：
  - `ai-food-news-prod`：只给日报/周报自动化
  - `ai-food-news-lab`：平时实验、改 prompt、测试搜索时使用

## 9. 风险提示

- Gmail App Password 要妥善保存
- 不要把真实密码写入 Git 仓库
- 初期先发给自己，确认内容稳定后再扩大收件范围
- 如果邮件里出现“我继续把……”“提交 git”“--final 模式”这类过程性话术，说明自动化会话被污染，应立即更换测试 session
