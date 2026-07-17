"""
新闻收集 Agent - 使用网络搜索 + AI 总结
"""

import json
import os
import requests
from datetime import datetime
from typing import Dict, List, Optional

from .ai_provider import AIProvider
from .prompts import SYSTEM_PROMPT
from .web_search import NewsSearcher


class NewsOfficer:
    """新闻收集 Agent"""

    def __init__(self, ai_provider: AIProvider, timeout=20, retry_count=3, retry_delay=2, date_filter_mode="today_only"):
        self.ai = ai_provider
        self.searcher = NewsSearcher(
            timeout=timeout,
            retry_count=retry_count,
            retry_delay=retry_delay,
            date_filter_mode=date_filter_mode
        )
        self.last_result: Optional[Dict] = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # 打印当前日期信息用于调试
        print(f"[*] NewsOfficer 初始化 - 今日日期: {self.searcher.today}")
        print(f"[*] 网络配置 - 超时: {timeout}秒, 重试: {retry_count}次, 延迟: {retry_delay}秒")
        print(f"[*] 日期过滤模式: {date_filter_mode}")

    def collect_military_news(self) -> List[Dict]:
        """收集军事新闻（优先主流媒体，仅当日）"""
        print("[*] 正在搜索军事新闻...")

        # 从网络获取真实新闻（已按优先级排序，仅当日）
        real_news = self.searcher.search_military_news()
        print(f"[*] 获取到 {len(real_news)} 条今日军事新闻")

        # 处理：检测地区，设置默认重要性
        for news in real_news:
            news['region'] = self._detect_region(news.get('title', ''), news.get('summary', ''))
            # 主流媒体来源的重要性默认为高
            if news.get('priority') == 'high' and 'importance' not in news:
                news['importance'] = '高'
            elif 'importance' not in news:
                news['importance'] = '中'

        # 打印收集到的新闻日期
        if real_news:
            print("[*] 军事新闻日期检查:")
            for i, news in enumerate(real_news[:3], 1):
                print(f"  {i}. {news.get('title', '')[:30]}... | 日期: {news.get('time', '')}")

        return real_news

    def collect_finance_news(self) -> List[Dict]:
        """收集金融新闻（优先主流媒体，仅当日）"""
        print("[*] 正在搜索金融新闻...")

        # 从网络获取真实新闻（已按优先级排序，仅当日）
        real_news = self.searcher.search_finance_news()
        print(f"[*] 获取到 {len(real_news)} 条今日金融新闻")

        # 处理：检测地区，设置默认重要性
        for news in real_news:
            news['region'] = self._detect_region(news.get('title', ''), news.get('summary', ''))
            # 主流媒体来源的重要性默认为高
            if news.get('priority') == 'high' and 'importance' not in news:
                news['importance'] = '高'
            elif 'importance' not in news:
                news['importance'] = '中'

        # 打印收集到的新闻日期
        if real_news:
            print("[*] 金融新闻日期检查:")
            for i, news in enumerate(real_news[:3], 1):
                print(f"  {i}. {news.get('title', '')[:30]}... | 日期: {news.get('time', '')}")

        return real_news

    def collect_all(self) -> Dict:
        """收集所有新闻"""
        import time
        start_time = time.time()

        print("=" * 60)
        print(f"开始收集新闻 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"今日日期: {self.searcher.today}")
        print(f"超时设置: {self.searcher.timeout} 秒/请求")
        print(f"重试次数: {self.searcher.retry_count} 次")
        print("=" * 60)

        military = self.collect_military_news()
        finance = self.collect_finance_news()

        elapsed_time = time.time() - start_time

        print("=" * 60)
        print(f"收集完成 - 军事: {len(military)} 条, 金融: {len(finance)} 条")
        print(f"总耗时: {elapsed_time:.1f} 秒")
        print("=" * 60)

        # 验证所有新闻都是今日的
        all_news = military + finance
        non_today = [n for n in all_news if n.get('time') != self.searcher.today]
        if non_today:
            print(f"[!] 警告: 发现 {len(non_today)} 条非今日新闻:")
            for n in non_today[:3]:
                print(f"  - {n.get('title', '')[:30]}... | 日期: {n.get('time', '')}")
        else:
            print("[✓] 所有新闻都是今日的")

        result = {
            "timestamp": datetime.now().isoformat(),
            "military": military,
            "finance": finance,
            "summary": self._generate_summary(military, finance),
            "elapsed_time": elapsed_time
        }

        self.last_result = result
        return result

    def _fetch_detail(self, url: str) -> str:
        """获取新闻详细内容"""
        if not url:
            return ""

        try:
            from bs4 import BeautifulSoup
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # 移除脚本和样式
                for script in soup(["script", "style"]):
                    script.decompose()

                # 尝试获取文章内容
                article = soup.find('article') or soup.find('div', class_=['content', 'article', 'post', 'entry'])
                if article:
                    text = article.get_text(separator='\n', strip=True)
                else:
                    text = soup.get_text(separator='\n', strip=True)

                # 清理文本
                lines = [line.strip() for line in text.split('\n') if line.strip() and len(line.strip()) > 10]
                detail = '\n'.join(lines[:20])  # 取前20行

                # 限制长度
                if len(detail) > 1500:
                    detail = detail[:1500] + "..."

                return detail
        except Exception as e:
            print(f"获取详情失败 {url}: {e}")

        return ""

    def _detect_region(self, title: str, summary: str) -> str:
        """检测新闻地区"""
        text = (title + " " + summary).lower()

        region_keywords = {
            "中国": ["中国", "北京", "上海", "台湾", "香港", "china", "beijing", "taiwan"],
            "美国": ["美国", "华盛顿", "纽约", "美股", "美联储", "america", "us", "washington", "fed"],
            "欧洲": ["欧洲", "欧盟", "英国", "德国", "法国", "europe", "eu", "uk", "germany", "france"],
            "俄罗斯": ["俄罗斯", "莫斯科", "普京", "russia", "moscow", "putin"],
            "中东": ["中东", "以色列", "伊朗", "叙利亚", "伊拉克", "沙特", "middle east", "israel", "iran"],
            "亚洲": ["日本", "韩国", "印度", "东南亚", "japan", "korea", "india"],
            "非洲": ["非洲", "africa"],
            "拉美": ["巴西", "墨西哥", "南美", "brazil", "mexico"],
        }

        for region, keywords in region_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return region

        return "国际"

    def _ai_analyze(self, news_list: List[Dict], category: str) -> List[Dict]:
        """用 AI 分析新闻重要性"""
        if not news_list:
            return []

        # 构建新闻列表文本
        news_text = f"以下是今日{category}新闻标题，请分析每条新闻的重要性（高/中/低）：\n\n"
        for i, news in enumerate(news_list[:10], 1):
            title = news.get('title', '')
            news_text += f"{i}. {title}\n"

        prompt = f"""请分析以下{category}新闻的重要性，返回 JSON 数组。
每条包含：
- index: 序号
- importance: 重要性（高/中/低）
- reason: 简短原因（20字以内）

只返回 JSON 数组，不要其他内容。

{news_text}"""

        try:
            response = self.ai.chat(SYSTEM_PROMPT, prompt)
            importance_data = self._parse_json_response(response)

            # 应用分析结果
            for item in importance_data:
                idx = item.get('index', 0) - 1
                if 0 <= idx < len(news_list):
                    news_list[idx]['importance'] = item.get('importance', '中')
                    news_list[idx]['importance_reason'] = item.get('reason', '')
        except Exception as e:
            print(f"AI 分析失败: {e}")
            # 设置默认重要性
            for news in news_list:
                if 'importance' not in news:
                    news['importance'] = '中'

        return news_list

    def _parse_json_response(self, response: str) -> List[Dict]:
        """解析 AI 返回的 JSON"""
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]
            else:
                json_str = response

            json_str = json_str.strip()
            data = json.loads(json_str)

            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                for key in data:
                    if isinstance(data[key], list):
                        return data[key]
                return [data]
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}")

        return []

    def _generate_summary(self, military: List[Dict], finance: List[Dict]) -> str:
        """生成综合摘要（简化版，快速生成）"""
        if not military and not finance:
            return "暂无今日新闻数据"

        lines = []
        lines.append("📊 今日资讯要点")
        lines.append("=" * 40)
        lines.append(f"📅 日期: {self.searcher.today}")

        # 统计高优先级新闻
        high_priority_military = len([n for n in military if n.get('priority') == 'high'])
        high_priority_finance = len([n for n in finance if n.get('priority') == 'high'])
        lines.append(f"⭐ 高优先级新闻: 军事 {high_priority_military} 条, 金融 {high_priority_finance} 条")

        if military:
            lines.append(f"\n🎖️ 军事动态 ({len(military)} 条)")
            lines.append("-" * 30)
            for i, news in enumerate(military[:5], 1):
                title = news.get('title', '')
                source = news.get('source', '')
                region = news.get('region', '国际')
                lines.append(f"{i}. [{source}] [{region}] {title}")

        if finance:
            lines.append(f"\n💰 金融市场 ({len(finance)} 条)")
            lines.append("-" * 30)
            for i, news in enumerate(finance[:5], 1):
                title = news.get('title', '')
                source = news.get('source', '')
                region = news.get('region', '国际')
                lines.append(f"{i}. [{source}] [{region}] {title}")

        lines.append(f"\n📅 数据更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        return "\n".join(lines)
