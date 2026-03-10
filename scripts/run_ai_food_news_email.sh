#!/bin/zsh
set -euo pipefail

export PATH="/Users/ming/.nvm/versions/node/v24.13.0/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

export AI_FOOD_NEWS_SMTP_HOST="${AI_FOOD_NEWS_SMTP_HOST:-smtp.gmail.com}"
export AI_FOOD_NEWS_SMTP_PORT="${AI_FOOD_NEWS_SMTP_PORT:-587}"
export AI_FOOD_NEWS_AGENT="${AI_FOOD_NEWS_AGENT:-ai-food-news}"
export AI_FOOD_NEWS_TO="${AI_FOOD_NEWS_TO:-+8613900000013}"
export AI_FOOD_NEWS_SUBJECT_PREFIX="${AI_FOOD_NEWS_SUBJECT_PREFIX:-今日 AI+餐饮观察}"
export AI_FOOD_NEWS_STATE_FILE="${AI_FOOD_NEWS_STATE_FILE:-$HOME/.openclaw/state/ai-food-news-last-sent.txt}"

if [[ -f "$HOME/.zshrc" ]]; then
  # shellcheck disable=SC1090
  source "$HOME/.zshrc"
fi

/usr/bin/python3 /Users/ming/CaiHub/scripts/send_ai_food_news_email.py
