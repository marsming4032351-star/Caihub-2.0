# OpenClaw 日报补发方案

这个方案用于解决：

- 早上 9 点电脑没开机
- 开机后希望自动补发
- 一天内允许多个兜底触发点
- 但同一天只真正发 1 次

## 1. 实现思路

```text
launchd 开机触发 + 多时段触发
  -> run_ai_food_news_email.sh
  -> send_ai_food_news_email.py
  -> 检查今天是否已经发送
  -> 没发过才真正发送
```

## 2. 当前去重机制

`send_ai_food_news_email.py` 已内置“今日只发一次”逻辑。

状态文件默认位置：

```text
~/.openclaw/state/ai-food-news-last-sent.txt
```

如果今天已经发过，再次触发会直接输出：

```text
Skip sending: already sent today to ...
```

## 3. 启动脚本

使用：

```text
/Users/ming/CaiHub/scripts/run_ai_food_news_email.sh
```

这个脚本会：

- 补 PATH
- 读取 `~/.zshrc`
- 读取 `~/.openclaw/ai-food-news.env`（由 Python 脚本加载）
- 调用 Python 发信脚本

## 4. 推荐触发策略

### 开机触发

电脑一开机就检查：

- 如果今天没发过，立即补发
- 如果今天已经发过，直接跳过

### 多时段兜底

建议加这 3 个时间点：

- 09:00
- 12:00
- 18:00

## 5. 推荐 LaunchAgent 配置

把下面内容保存到：

```text
~/Library/LaunchAgents/ai.caihub.ai-food-news.plist
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>ai.caihub.ai-food-news</string>

  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>/Users/ming/CaiHub/scripts/run_ai_food_news_email.sh</string>
  </array>

  <key>RunAtLoad</key>
  <true/>

  <key>StartCalendarInterval</key>
  <array>
    <dict>
      <key>Hour</key>
      <integer>9</integer>
      <key>Minute</key>
      <integer>0</integer>
    </dict>
    <dict>
      <key>Hour</key>
      <integer>12</integer>
      <key>Minute</key>
      <integer>0</integer>
    </dict>
    <dict>
      <key>Hour</key>
      <integer>18</integer>
      <key>Minute</key>
      <integer>0</integer>
    </dict>
  </array>

  <key>StandardOutPath</key>
  <string>/Users/ming/.openclaw/logs/ai-food-news-email.log</string>

  <key>StandardErrorPath</key>
  <string>/Users/ming/.openclaw/logs/ai-food-news-email.err.log</string>
</dict>
</plist>
```

## 6. 加载方式

```bash
launchctl unload ~/Library/LaunchAgents/ai.caihub.ai-food-news.plist 2>/dev/null || true
launchctl load ~/Library/LaunchAgents/ai.caihub.ai-food-news.plist
launchctl start ai.caihub.ai-food-news
```

## 7. 为什么比纯 crontab 更适合你

- 支持开机触发
- 更适合 macOS 常驻任务
- 可以同时配多个兜底时间
- 配合“今日只发一次”逻辑，更符合你的使用习惯

## 8. 建议

你已经装了 `crontab`，但如果你真的希望：

- 错过 9 点也补发
- 开机就检查

建议最终改用这套 `launchd` 方案。
