"""
报告生成器 - 生成 Markdown 和 HTML 报告
"""

import os
from datetime import datetime
from typing import Dict, List


class ReportGenerator:
    """报告生成器"""

    def __init__(self, report_dir: str = "reports"):
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)

    def generate_markdown(self, data: Dict) -> str:
        """生成 Markdown 报告"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        military = data.get("military", [])
        finance = data.get("finance", [])
        summary = data.get("summary", "")

        md = f"# 🌍 每日资讯简报\n\n"
        md += f"**生成时间**: {timestamp}\n\n"
        md += "---\n\n"

        # 综合分析
        if summary:
            md += "## 📊 今日要点\n\n"
            md += f"{summary}\n\n"
            md += "---\n\n"

        # 军事新闻
        md += "## 🎖️ 军事新闻\n\n"
        if military:
            for i, news in enumerate(military, 1):
                title = news.get("title", "未知标题")
                source = news.get("source", "未知来源")
                time = news.get("time", "今日")
                summary_text = news.get("summary", "暂无摘要")
                importance = news.get("importance", "中")

                importance_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(importance, "⚪")

                md += f"### {i}. {title}\n\n"
                md += f"- **来源**: {source} | **时间**: {time} | **重要性**: {importance_icon} {importance}\n"
                md += f"- {summary_text}\n\n"
        else:
            md += "*暂无军事新闻*\n\n"

        md += "---\n\n"

        # 金融新闻
        md += "## 💰 金融新闻\n\n"
        if finance:
            for i, news in enumerate(finance, 1):
                title = news.get("title", "未知标题")
                source = news.get("source", "未知来源")
                time = news.get("time", "今日")
                summary_text = news.get("summary", "暂无摘要")
                importance = news.get("importance", "中")

                importance_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(importance, "⚪")

                md += f"### {i}. {title}\n\n"
                md += f"- **来源**: {source} | **时间**: {time} | **重要性**: {importance_icon} {importance}\n"
                md += f"- {summary_text}\n\n"
        else:
            md += "*暂无金融新闻*\n\n"

        md += "---\n\n"
        md += f"*本报告由 AI Agent 自动生成 | {timestamp}*\n"

        return md

    def generate_html(self, data: Dict) -> str:
        """生成 HTML 报告"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        military = data.get("military", [])
        finance = data.get("finance", [])
        summary = data.get("summary", "")

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日资讯简报 - {timestamp}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            padding: 20px;
            color: #e0e0e0;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            padding: 30px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        .header h1 {{
            font-size: 2em;
            color: white;
            margin-bottom: 10px;
        }}
        .header .time {{
            color: rgba(255,255,255,0.8);
            font-size: 0.9em;
        }}
        .summary {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .summary h2 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        .section {{
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .section h2 {{
            font-size: 1.3em;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }}
        .military h2 {{ color: #e74c3c; }}
        .finance h2 {{ color: #2ecc71; }}
        .news-item {{
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 12px;
            border-left: 4px solid;
            transition: transform 0.2s;
        }}
        .news-item:hover {{
            transform: translateX(5px);
        }}
        .military .news-item {{ border-left-color: #e74c3c; }}
        .finance .news-item {{ border-left-color: #2ecc71; }}
        .news-title {{
            font-weight: bold;
            font-size: 1.05em;
            margin-bottom: 8px;
            color: #fff;
        }}
        .news-meta {{
            font-size: 0.8em;
            color: #888;
            margin-bottom: 8px;
        }}
        .news-meta span {{
            margin-right: 15px;
        }}
        .importance-high {{ color: #e74c3c; }}
        .importance-mid {{ color: #f39c12; }}
        .importance-low {{ color: #2ecc71; }}
        .news-summary {{
            font-size: 0.9em;
            color: #bbb;
            line-height: 1.5;
        }}
        .empty {{
            text-align: center;
            color: #666;
            padding: 20px;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.85em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌍 每日资讯简报</h1>
            <div class="time">🕐 {timestamp}</div>
        </div>
"""

        # 综合分析
        if summary:
            html += f"""
        <div class="summary">
            <h2>📊 今日要点</h2>
            <p style="line-height: 1.8; color: #ccc;">{summary}</p>
        </div>
"""

        # 军事新闻
        html += """
        <div class="section military">
            <h2>🎖️ 军事新闻</h2>
"""
        if military:
            for news in military:
                title = news.get("title", "未知标题")
                source = news.get("source", "未知来源")
                time = news.get("time", "今日")
                summary_text = news.get("summary", "暂无摘要")
                importance = news.get("importance", "中")

                imp_class = {"高": "importance-high", "中": "importance-mid", "低": "importance-low"}.get(importance, "")
                imp_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(importance, "⚪")

                html += f"""
            <div class="news-item">
                <div class="news-title">{title}</div>
                <div class="news-meta">
                    <span>📰 {source}</span>
                    <span>🕐 {time}</span>
                    <span class="{imp_class}">{imp_icon} {importance}</span>
                </div>
                <div class="news-summary">{summary_text}</div>
            </div>
"""
        else:
            html += '<div class="empty">暂无军事新闻</div>'

        html += "        </div>\n"

        # 金融新闻
        html += """
        <div class="section finance">
            <h2>💰 金融新闻</h2>
"""
        if finance:
            for news in finance:
                title = news.get("title", "未知标题")
                source = news.get("source", "未知来源")
                time = news.get("time", "今日")
                summary_text = news.get("summary", "暂无摘要")
                importance = news.get("importance", "中")

                imp_class = {"高": "importance-high", "中": "importance-mid", "低": "importance-low"}.get(importance, "")
                imp_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(importance, "⚪")

                html += f"""
            <div class="news-item">
                <div class="news-title">{title}</div>
                <div class="news-meta">
                    <span>📰 {source}</span>
                    <span>🕐 {time}</span>
                    <span class="{imp_class}">{imp_icon} {importance}</span>
                </div>
                <div class="news-summary">{summary_text}</div>
            </div>
"""
        else:
            html += '<div class="empty">暂无金融新闻</div>'

        html += "        </div>\n"

        # 页脚
        html += f"""
        <div class="footer">
            本报告由 AI Agent 自动生成 | {timestamp}
        </div>
    </div>
</body>
</html>
"""
        return html

    def save_report(self, data: Dict, format: str = "both") -> Dict[str, str]:
        """保存报告到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_files = {}

        if format in ("markdown", "both"):
            md_path = os.path.join(self.report_dir, f"report_{timestamp}.md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(self.generate_markdown(data))
            saved_files["markdown"] = md_path
            print(f"[✓] Markdown 报告已保存: {md_path}")

        if format in ("html", "both"):
            html_path = os.path.join(self.report_dir, f"report_{timestamp}.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(self.generate_html(data))
            saved_files["html"] = html_path
            print(f"[✓] HTML 报告已保存: {html_path}")

        return saved_files
