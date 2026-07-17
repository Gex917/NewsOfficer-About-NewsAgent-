"""
配置文件 - 支持多种 AI API
请在使用前填入您的 API Key
"""

# ==================== AI API 配置 ====================

# 当前使用的 AI 提供商: "openai" | "claude" | "mimo"
AI_PROVIDER = "openai"

# OpenAI 配置
OPENAI_API_KEY = ""
OPENAI_BASE_URL = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-4o"

# Claude 配置
CLAUDE_API_KEY = ""
CLAUDE_BASE_URL = "https://api.anthropic.com"
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# MiMo 配置 (OpenAI 兼容格式)
MIMO_API_KEY = ""
MIMO_BASE_URL = "https://token-plan-cn.xiaomimimo.com/v1"
MIMO_MODEL = "mimo-v2.5-pro"

# ==================== 收集配置 ====================

# 定时收集时间 (24小时制)
SCHEDULE_TIMES = ["08:00", "12:00", "18:00"]

# 收集类别
CATEGORIES = ["军事", "金融"]

# 每个类别最大新闻条数
MAX_NEWS_PER_CATEGORY = 10

# 报告保存目录
REPORT_DIR = "reports"

# ==================== 网络配置 ====================

# 请求超时时间（秒）
REQUEST_TIMEOUT = 20

# 重试次数
RETRY_COUNT = 3

# 重试延迟（秒）
RETRY_DELAY = 2

# 日期过滤模式: "today_only" 仅今日, "today_and_yesterday" 今日和昨日
DATE_FILTER_MODE = "today_only"

# ==================== 系统配置 ====================

# 是否显示系统托盘
SHOW_TRAY = True

# 收集完成后是否弹出通知
SHOW_NOTIFICATION = True

# 自动打开报告
AUTO_OPEN_REPORT = True
