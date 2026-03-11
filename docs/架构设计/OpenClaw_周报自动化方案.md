# OpenClaw 周报自动化方案

这份说明用于在现有日报能力之上，再增加一条每周自动发送的周报链路。

## 1. 目标结构

```text
ai-food-news Agent (Gemini)
  -> 回顾最近 7 天 AI+餐饮资讯
  -> 生成中文周报
  -> Gmail 自动发信
  -> 每周固定时间触发
```

## 2. 已提供文件

- `prompts/ai_food_news_weekly_prompt.txt`
- `scripts/run_ai_food_news_weekly_email.sh`
- `deploy/ai.caihub.ai-food-news-weekly.plist`

## 3. 周报环境文件

建议只在共享文件里维护 SMTP 和收件人：

```bash
cat > ~/.openclaw/ai-food-news-shared.env <<'EOF'
AI_FOOD_NEWS_SMTP_HOST=smtp.gmail.com
AI_FOOD_NEWS_SMTP_PORT=587
AI_FOOD_NEWS_SMTP_USERNAME=你的 Gmail 地址
AI_FOOD_NEWS_SMTP_PASSWORD=你的 Gmail App Password
AI_FOOD_NEWS_RECIPIENT=你的 Gmail 地址
AI_FOOD_NEWS_RECIPIENTS=你的 Gmail 地址,84369563@qq.com,605229578@qq.com,315865302@qq.com
EOF
```

周报自己的文件只保留周报参数：

```bash
cat > ~/.openclaw/ai-food-news-weekly.env <<'EOF'
AI_FOOD_NEWS_AGENT=ai-food-news
AI_FOOD_NEWS_TO=+8613900000020
AI_FOOD_NEWS_SUBJECT_PREFIX=本周 AI+餐饮周报
AI_FOOD_NEWS_STATE_FILE=/Users/你的用户名/.openclaw/state/ai-food-news-weekly-last-sent.txt
AI_FOOD_NEWS_PROMPT_FILE=/Users/ming/CaiHub/prompts/ai_food_news_weekly_prompt.txt
EOF
```

## 4. 手动测试

```bash
AI_FOOD_NEWS_ENV_FILE="$HOME/.openclaw/ai-food-news-weekly.env" \
python3 /Users/ming/CaiHub/scripts/send_ai_food_news_email.py
```

## 5. 推荐发送时间

当前模板里默认设置为：

- 每周一 10:00

如果你更希望周日晚上发，也可以改 `plist`。

## 6. 安装 LaunchAgent

```bash
cp /Users/ming/CaiHub/deploy/ai.caihub.ai-food-news-weekly.plist ~/Library/LaunchAgents/ai.caihub.ai-food-news-weekly.plist
chmod +x /Users/ming/CaiHub/scripts/run_ai_food_news_weekly_email.sh
launchctl unload ~/Library/LaunchAgents/ai.caihub.ai-food-news-weekly.plist 2>/dev/null || true
launchctl load ~/Library/LaunchAgents/ai.caihub.ai-food-news-weekly.plist
```

## 7. 说明

- 日报和周报共用同一个 Python 发信脚本
- 两者会先读取 `~/.openclaw/ai-food-news-shared.env`
- 区别只在于：
  - 使用不同 env 文件
  - 使用不同 prompt 文件
  - 使用不同 state file
  - 使用不同 LaunchAgent
