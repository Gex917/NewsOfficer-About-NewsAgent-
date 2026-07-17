"""
配置文件 - 支持多种 AI API
"""

AI_PROVIDER = "mimo"

OPENAI_API_KEY = ""
OPENAI_BASE_URL = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-4o"

CLAUDE_API_KEY = ""
CLAUDE_BASE_URL = "https://api.anthropic.com"
CLAUDE_MODEL = "claude-sonnet-4-20250514"

MIMO_API_KEY = ""
MIMO_BASE_URL = "https://token-plan-cn.xiaomimimo.com/v1"
MIMO_MODEL = "mimo-v2.5-pro"

SCHEDULE_TIMES = ["08:00", "12:00", "18:00"]
CATEGORIES = ["军事", "金融"]
MAX_NEWS_PER_CATEGORY = 10
REPORT_DIR = "reports"
SHOW_TRAY = True
SHOW_NOTIFICATION = True
AUTO_OPEN_REPORT = True

# 网络请求配置
REQUEST_TIMEOUT = 20
RETRY_COUNT = 3
RETRY_DELAY = 2

# 日期过滤模式
DATE_FILTER_MODE = "today_only"
