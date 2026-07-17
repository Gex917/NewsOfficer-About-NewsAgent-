# NewsOfficer - AI 资讯收集助手

[中文](#中文) | [English](#english)

---

## 中文

### 📖 简介

NewsOfficer 是一款 AI 驱动的每日资讯收集助手，自动收集世界军事和金融新闻，生成结构化报告。支持 OpenAI、Claude、MiMo 等多种 AI API。带有现代化的 GUI 界面。

### ✨ 功能特性

- 🤖 **多 AI 支持** - OpenAI / Claude / MiMo API
- 🖥️ **现代化 GUI** - PyQt6 深色主题界面
- 🎖️ **军事新闻** - 地区冲突、军事演习、武器装备、国防政策
- 💰 **金融新闻** - 股市动态、货币政策、并购交易、宏观经济
- ⏰ **定时收集** - 每日自动收集（默认 08:00 / 12:00 / 18:00）
- 📊 **智能分析** - AI 自动生成综合分析和要点总结
- 📄 **双格式报告** - Markdown + HTML 精美报告
- 🔔 **系统托盘** - 后台运行，双击打开
- 🌐 **主流媒体** - 优先从 BBC、纽约时报、路透社、卫报、CNN、CNBC 获取新闻
- 📅 **日期过滤** - 仅保留今日最新新闻

### 🚀 快速开始

#### 方式一：使用安装包（推荐）

1. 下载 `NewsOfficer_Setup.exe`
2. 双击运行安装程序
3. 按照提示完成安装
4. 从桌面快捷方式或开始菜单启动

#### 方式二：从源码运行

```bash
# 1. 克隆或下载项目
cd G:\mimo-work\NewsOfficer

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行程序
python main.py
```

### ⚙️ 配置说明

#### AI API 配置

编辑 `config.py` 或在 GUI 设置面板中配置：

```python
# 选择 AI 提供商
AI_PROVIDER = "openai"  # "openai" | "claude" | "mimo"

# OpenAI 配置
OPENAI_API_KEY = "sk-your-key-here"
OPENAI_BASE_URL = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-4o"

# Claude 配置
CLAUDE_API_KEY = "sk-ant-your-key-here"

# MiMo 配置
MIMO_API_KEY = "your-mimo-key-here"
MIMO_BASE_URL = "https://token-plan-cn.xiaomimimo.com/v1"
```

#### 网络配置

```python
# 请求超时时间（秒）
REQUEST_TIMEOUT = 20

# 重试次数
RETRY_COUNT = 3

# 重试延迟（秒）
RETRY_DELAY = 2
```

#### 日期过滤配置

```python
# 日期过滤模式
DATE_FILTER_MODE = "today_only"  # "today_only" | "today_and_yesterday"
```

### 🖥️ 界面说明

程序启动后会显示以下界面：

```
┌────────────────────────────────────────────────────────────┐
│  NEWSAGENT                                    [▶ COLLECT]   │
├────────────────────────────────────────────────────────────┤
│  [NEWS] [ANALYSIS] [LOG] [SETTINGS]                         │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  ◆ MILITARY                                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Title     │ Source │ Region │ Time │ Priority │ Imp   │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ ...       │ ...    │ ...    │ ...  │ ...      │ ...   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ◆ FINANCE                                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Title     │ Source │ Region │ Time │ Priority │ Imp   │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ ...       │ ...    │ ...    │ ...  │ ...      │ ...   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Status: Military: 12 | Finance: 12 | Time: 69.4s           │
└────────────────────────────────────────────────────────────┘
```

### 📁 项目结构

```
NewsOfficer/
├── main.py              # 主程序入口
├── config.py            # 配置文件
├── build.py             # 打包脚本
├── requirements.txt     # 依赖包
├── README.md            # 说明文档
├── agent/
│   ├── ai_provider.py   # AI API 抽象层
│   ├── news_agent.py    # 新闻收集 Agent
│   ├── web_search.py    # 网络搜索模块
│   └── prompts.py       # 提示词模板
├── report/
│   └── generator.py     # 报告生成器
├── scheduler/
│   └── task.py          # 任务调度器
├── gui/
│   ├── main_window.py   # 主窗口 UI
│   └── tray.py          # 系统托盘
├── reports/             # 生成的报告
└── dist/                # 打包输出
    └── NewsOfficer.exe    # 可执行文件
```

### 🔧 API Key 获取

| AI 服务 | 获取地址 |
|---------|----------|
| OpenAI | https://platform.openai.com/api-keys |
| Claude | https://console.anthropic.com/ |
| MiMo | 请参考小米开发者文档 |

### 📰 新闻来源

| 来源 | 类型 | 优先级 |
|------|------|--------|
| BBC | 国际 | 高 |
| 纽约时报 | 国际 | 高 |
| 路透社 | 国际 | 高 |
| 卫报 | 国际 | 高 |
| CNN | 国际 | 高 |
| CNBC | 国际 | 高 |
| 新华网 | 国内 | 中 |
| 环球网 | 国内 | 中 |
| 东方财富 | 国内 | 中 |

### ⚠️ 注意事项

- 需要有效的 AI API Key
- API 调用会产生费用
- 建议先手动测试一次，确认正常后再启用定时任务
- 部分新闻源可能需要科学上网

### 📝 更新日志

#### v1.1.0 (2026-07-16)
- ✨ 新增主流媒体优先收集（BBC、纽约时报、路透社等）
- ✨ 新增日期过滤功能（仅保留今日新闻）
- ✨ 新增网络配置（超时、重试）
- ✨ 新增 GUI 设置面板
- 🐛 修复日期解析问题
- 🐛 修复编码问题

#### v1.0.0 (2026-07-15)
- 🎉 初始版本
- ✨ 支持 OpenAI、Claude、MiMo API
- ✨ PyQt6 现代化 GUI
- ✅ 定时收集功能
- ✅ Markdown + HTML 报告生成

---

## English

### 📖 Introduction

NewsOfficer is an AI-powered daily news collection assistant that automatically collects world military and financial news and generates structured reports. Supports OpenAI, Claude, MiMo and other AI APIs. Features a modern GUI interface.

### ✨ Features

- 🤖 **Multi-AI Support** - OpenAI / Claude / MiMo API
- 🖥️ **Modern GUI** - PyQt6 dark theme interface
- 🎖️ **Military News** - Regional conflicts, military exercises, weapons, defense policy
- 💰 **Financial News** - Stock markets, monetary policy, M&A, macroeconomics
- ⏰ **Scheduled Collection** - Auto-collect daily (default: 08:00 / 12:00 / 18:00)
- 📊 **AI Analysis** - Auto-generated comprehensive analysis and summary
- 📄 **Dual Format Reports** - Markdown + HTML beautiful reports
- 🔔 **System Tray** - Run in background, double-click to open
- 🌐 **Premium Sources** - Prioritize BBC, NYT, Reuters, Guardian, CNN, CNBC
- 📅 **Date Filter** - Only keep today's latest news

### 🚀 Quick Start

#### Option 1: Use Installer (Recommended)

1. Download `NewsOfficer_Setup.exe`
2. Double-click to run the installer
3. Follow the prompts to complete installation
4. Launch from desktop shortcut or start menu

#### Option 2: Run from Source

```bash
# 1. Clone or download the project
cd G:\mimo-work\NewsOfficer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the program
python main.py
```

### 🔧 API Key Sources

| AI Service | URL |
|------------|-----|
| OpenAI | https://platform.openai.com/api-keys |
| Claude | https://console.anthropic.com/ |
| MiMo | Refer to Xiaomi developer docs |

### 📰 News Sources

| Source | Type | Priority |
|--------|------|----------|
| BBC | International | High |
| New York Times | International | High |
| Reuters | International | High |
| The Guardian | International | High |
| CNN | International | High |
| CNBC | International | High |
| Xinhua | Domestic | Medium |
| Huanqiu | Domestic | Medium |
| Eastmoney | Domestic | Medium |

### ⚠️ Notes

- Valid AI API Key required
- API calls will incur costs
- Test manually first before enabling scheduled tasks
- Some news sources may require VPN

---

## 📄 License

MIT License

---

## 🤝 Contributing

Welcome contributions! Please feel free to submit issues and pull requests.

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.
