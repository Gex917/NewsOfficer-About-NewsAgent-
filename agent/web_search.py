"""
网络搜索模块 - 获取当日实时新闻
优先从 BBC、纽约时报、路透社等主流新闻机构获取
"""

import requests
from typing import List, Dict
from datetime import datetime, timezone, timedelta


class NewsSearcher:
    """新闻搜索器 - 从多个来源获取当日实时新闻"""

    # 主流新闻机构 RSS 源（优先级高）
    PREMIUM_RSS_FEEDS = {
        'military': [
            # BBC 军事/防务
            'http://feeds.bbci.co.uk/news/world/rss.xml',
            # 纽约时报 世界新闻
            'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
            # 路透社 世界新闻
            'https://feeds.reuters.com/reuters/topNews',
            # 卫报 世界新闻
            'https://www.theguardian.com/world/rss',
            # CNN 世界新闻
            'http://rss.cnn.com/rss/edition_world.rss',
        ],
        'finance': [
            # BBC 商业新闻
            'http://feeds.bbci.co.uk/news/business/rss.xml',
            # 纽约时报 商业新闻
            'https://rss.nytimes.com/services/xml/rss/nyt/Business.xml',
            # 路透社 商业新闻
            'https://feeds.reuters.com/reuters/businessNews',
            # 卫报 商业新闻
            'https://www.theguardian.com/uk/business/rss',
            # CNBC 新闻
            'https://www.cnbc.com/id/100003114/device/rss/rss.html',
        ]
    }

    # 国内新闻源
    DOMESTIC_RSS_FEEDS = {
        'military': [
            # 新华网军事
            'http://www.xinhuanet.com/politics/news_politics.xml',
            # 环球网军事
            'https://rss.huanqiu.com/rss/military',
        ],
        'finance': [
            # 新华网财经
            'http://www.xinhuanet.com/fortune/news_fortune.xml',
            # 东方财富
            'https://rss.eastmoney.com/rss_caijing.xml',
        ]
    }

    def __init__(self, timeout=20, retry_count=3, retry_delay=2, date_filter_mode="today_only"):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, */*',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8',
        }
        self.timeout = timeout  # 请求超时时间（秒）
        self.retry_count = retry_count  # 重试次数
        self.retry_delay = retry_delay  # 重试延迟（秒）
        self.date_filter_mode = date_filter_mode  # 日期过滤模式
        # 当前日期（北京时间）
        beijing_tz = timezone(timedelta(hours=8))
        self.today = datetime.now(beijing_tz).strftime('%Y-%m-%d')
        self.today_short = datetime.now(beijing_tz).strftime('%m-%d')

    def search_military_news(self) -> List[Dict]:
        """搜索当日军事新闻（优先主流媒体）"""
        all_news = []

        # 第一优先级：主流国际媒体 RSS
        print("[*] 从 BBC、纽约时报、路透社等获取军事新闻...")
        premium_news = self._fetch_rss_feeds('military', self.PREMIUM_RSS_FEEDS)
        all_news.extend(premium_news)
        print(f"[✓] 主流媒体获取 {len(premium_news)} 条")

        # 添加延迟避免请求过快
        import time
        time.sleep(1)

        # 第二优先级：国内媒体 RSS
        print("[*] 从国内媒体获取军事新闻...")
        domestic_news = self._fetch_rss_feeds('military', self.DOMESTIC_RSS_FEEDS)
        all_news.extend(domestic_news)
        print(f"[✓] 国内媒体获取 {len(domestic_news)} 条")

        # 第三优先级：Google News 补充
        if len(all_news) < 8:
            time.sleep(1)
            print("[*] 从 Google News 补充军事新闻...")
            google_news = self._search_google_news("world military news today")
            all_news.extend(google_news)
            print(f"[✓] Google News 补充 {len(google_news)} 条")

        # 去重和严格过滤今日新闻
        all_news = self._deduplicate(all_news)
        today_news = self._filter_today(all_news)
        print(f"[✓] 过滤后保留 {len(today_news)} 条今日新闻")

        # 标记来源类型
        today_news = self._mark_source_type(today_news)

        return today_news[:12]

    def search_finance_news(self) -> List[Dict]:
        """搜索当日金融新闻（优先主流媒体）"""
        all_news = []

        # 第一优先级：主流国际媒体 RSS
        print("[*] 从 BBC、纽约时报、路透社等获取金融新闻...")
        premium_news = self._fetch_rss_feeds('finance', self.PREMIUM_RSS_FEEDS)
        all_news.extend(premium_news)
        print(f"[✓] 主流媒体获取 {len(premium_news)} 条")

        # 添加延迟避免请求过快
        import time
        time.sleep(1)

        # 第二优先级：国内媒体 RSS
        print("[*] 从国内媒体获取金融新闻...")
        domestic_news = self._fetch_rss_feeds('finance', self.DOMESTIC_RSS_FEEDS)
        all_news.extend(domestic_news)
        print(f"[✓] 国内媒体获取 {len(domestic_news)} 条")

        # 第三优先级：Google News 补充
        if len(all_news) < 8:
            time.sleep(1)
            print("[*] 从 Google News 补充金融新闻...")
            google_news = self._search_google_news("global financial news today")
            all_news.extend(google_news)
            print(f"[✓] Google News 补充 {len(google_news)} 条")

        # 去重和严格过滤今日新闻
        all_news = self._deduplicate(all_news)
        today_news = self._filter_today(all_news)
        print(f"[✓] 过滤后保留 {len(today_news)} 条今日新闻")

        # 标记来源类型
        today_news = self._mark_source_type(today_news)

        return today_news[:12]

    def _fetch_rss_feeds(self, category: str, feeds_dict: Dict[str, List[str]]) -> List[Dict]:
        """从 RSS 源获取新闻（带重试机制）"""
        results = []
        feeds = feeds_dict.get(category, [])

        for feed_url in feeds:
            for attempt in range(self.retry_count):
                try:
                    news_items = self._parse_rss_feed(feed_url)
                    results.extend(news_items)
                    break  # 成功则跳出重试循环
                except Exception as e:
                    if attempt < self.retry_count - 1:
                        print(f"RSS 获取失败 (尝试 {attempt + 1}/{self.retry_count}): {feed_url[:50]}...")
                        import time
                        time.sleep(self.retry_delay)
                    else:
                        print(f"RSS 获取失败 (已重试 {self.retry_count} 次): {feed_url[:50]}: {e}")

        return results

    def _parse_rss_feed(self, feed_url: str) -> List[Dict]:
        """解析单个 RSS 源"""
        results = []
        try:
            response = requests.get(feed_url, headers=self.headers, timeout=self.timeout)

            if response.status_code == 200:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.text)

                # 获取来源名称
                source_name = self._extract_source_name(feed_url, root)

                # 处理 RSS 2.0 格式 - 增加到10条
                for item in root.findall('.//item')[:10]:
                    news = self._parse_rss_item(item, source_name)
                    if news:
                        results.append(news)

                # 处理 Atom 格式 - 增加到10条
                if not results:
                    ns = {'atom': 'http://www.w3.org/2005/Atom'}
                    for entry in root.findall('.//atom:entry', ns)[:10]:
                        news = self._parse_atom_entry(entry, ns, source_name)
                        if news:
                            results.append(news)
        except Exception as e:
            print(f"RSS 解析失败 {feed_url[:50]}: {e}")

        return results

    def _extract_source_name(self, url: str, root) -> str:
        """从 URL 或 XML 提取来源名称"""
        # 尝试从 XML 提取
        channel_title = root.find('.//channel/title')
        if channel_title is not None and channel_title.text:
            return channel_title.text

        # 从 URL 推断
        source_map = {
            'bbc': 'BBC',
            'nytimes': '纽约时报',
            'reuters': '路透社',
            'theguardian': '卫报',
            'cnn': 'CNN',
            'cnbc': 'CNBC',
            'xinhuanet': '新华网',
            'huanqiu': '环球网',
            'eastmoney': '东方财富',
        }

        url_lower = url.lower()
        for key, name in source_map.items():
            if key in url_lower:
                return name

        return url.split('/')[2]

    def _parse_rss_item(self, item, source_name: str) -> Dict:
        """解析 RSS 2.0 item"""
        title = item.find('title')
        link = item.find('link')
        pub_date = item.find('pubDate')
        description = item.find('description')

        if title is None or not title.text:
            return None

        # 提取摘要
        summary = ''
        if description is not None and description.text:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(description.text, 'html.parser')
            summary = soup.get_text(strip=True)[:200]

        # 获取原始日期字符串
        raw_time = pub_date.text if pub_date is not None else ''
        parsed_time = self._parse_date(raw_time)

        # 调试日志
        if parsed_time != self.today:
            print(f"  [DEBUG] {source_name}: {title.text[:30]}... | 原始日期: {raw_time} | 解析后: {parsed_time}")

        return {
            'title': title.text.strip(),
            'source': source_name,
            'time': parsed_time,
            'url': link.text if link is not None else '',
            'summary': summary,
            'priority': 'high'  # 主流媒体标记为高优先级
        }

    def _parse_atom_entry(self, entry, ns: dict, source_name: str) -> Dict:
        """解析 Atom 格式 entry"""
        title = entry.find('atom:title', ns)
        link = entry.find('atom:link', ns)
        updated = entry.find('atom:updated', ns)
        summary = entry.find('atom:summary', ns)

        if title is None or not title.text:
            return None

        summary_text = ''
        if summary is not None and summary.text:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(summary.text, 'html.parser')
            summary_text = soup.get_text(strip=True)[:200]

        # 获取原始日期字符串
        raw_time = updated.text if updated is not None else ''
        parsed_time = self._parse_date(raw_time)

        # 调试日志
        if parsed_time != self.today:
            print(f"  [DEBUG] {source_name}: {title.text[:30]}... | 原始日期: {raw_time} | 解析后: {parsed_time}")

        return {
            'title': title.text.strip(),
            'source': source_name,
            'time': parsed_time,
            'url': link.get('href', '') if link is not None else '',
            'summary': summary_text,
            'priority': 'high'
        }

    def _mark_source_type(self, news_list: List[Dict]) -> List[Dict]:
        """标记新闻来源类型"""
        domestic_keywords = ['中国', '北京', '上海', '新华网', '环球网', '东方财富', '人民币']

        for news in news_list:
            # 如果已经有 source_type，跳过
            if 'source_type' in news:
                continue

            source = news.get('source', '')
            title = news.get('title', '')
            text = source + title

            if any(kw in text for kw in domestic_keywords):
                news['source_type'] = 'domestic'
            else:
                news['source_type'] = 'international'

        return news_list

    def _search_google_news(self, query: str) -> List[Dict]:
        """从 Google News 搜索（补充来源，带重试机制）"""
        results = []
        for attempt in range(self.retry_count):
            try:
                url = f"https://news.google.com/rss/search?q={query}&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
                response = requests.get(url, headers=self.headers, timeout=self.timeout)

                if response.status_code == 200:
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(response.text)

                    # 增加到15条
                    for item in root.findall('.//item')[:15]:
                        title = item.find('title')
                        link = item.find('link')
                        pub_date = item.find('pubDate')
                        source = item.find('source')

                        if title is not None:
                            raw_time = pub_date.text if pub_date is not None else ''
                            parsed_time = self._parse_date(raw_time)
                            results.append({
                                'title': title.text or '',
                                'source': source.text if source is not None else 'Google News',
                                'time': parsed_time,
                                'url': link.text if link is not None else '',
                                'summary': '',
                                'priority': 'normal'
                            })
                    break  # 成功则跳出重试循环
            except Exception as e:
                if attempt < self.retry_count - 1:
                    print(f"Google News 搜索超时 (尝试 {attempt + 1}/{self.retry_count}): {query[:20]}...")
                    import time
                    time.sleep(self.retry_delay)
                else:
                    print(f"Google News 搜索失败 (已重试 {self.retry_count} 次): {query[:20]}...")

        return results

    def _search_baidu_news(self, query: str) -> List[Dict]:
        """从百度新闻搜索"""
        results = []
        try:
            url = f"https://www.baidu.com/s?tn=news&word={query}"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # 解析百度新闻结果
                for item in soup.select('.result')[:10]:
                    title_elem = item.select_one('.news-title a')
                    if title_elem:
                        results.append({
                            'title': title_elem.get_text(strip=True),
                            'source': '百度新闻',
                            'time': datetime.now().strftime('%Y-%m-%d'),
                            'url': title_elem.get('href', ''),
                            'summary': ''
                        })
        except Exception as e:
            print(f"百度新闻搜索失败: {e}")

        return results

    def _parse_date(self, date_str: str) -> str:
        """解析日期，返回 YYYY-MM-DD 格式"""
        if not date_str:
            return ''  # 返回空字符串，让过滤器处理

        # 先检查是否包含相对时间关键词（只有这些才认为是今日）
        relative_keywords = ['今天', '今日', 'today', 'Today', '刚刚', '小时前', '分钟前', 'hours ago', 'minutes ago', 'just now']
        if any(kw in date_str for kw in relative_keywords):
            return self.today

        # 尝试从 RFC 2822 格式解析 (RSS 标准格式)
        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(date_str)
            return dt.strftime('%Y-%m-%d')
        except:
            pass

        # 尝试 ISO 8601 格式 (Atom 标准格式)
        try:
            # 处理 2026-07-16T10:30:00Z 或 2026-07-16T10:30:00+08:00
            if 'T' in date_str:
                date_part = date_str.split('T')[0]
                dt = datetime.strptime(date_part, '%Y-%m-%d')
                return dt.strftime('%Y-%m-%d')
        except:
            pass

        # 尝试其他格式
        parsed = self._parse_news_date(date_str)
        if parsed:
            return parsed

        return ''

    def _merge_ratio(self, list_a: List[Dict], list_b: List[Dict],
                     ratio_a: int, ratio_b: int, max_total: int = 15) -> List[Dict]:
        """按比例合并两个列表"""
        result = []
        idx_a = 0
        idx_b = 0
        count_a = 0
        count_b = 0

        # 计算每组应取的数量
        total_parts = ratio_a + ratio_b
        max_a = int(max_total * ratio_a / total_parts)
        max_b = int(max_total * ratio_b / total_parts)

        while len(result) < max_total:
            # 添加 list_a 的项
            if count_a < max_a and idx_a < len(list_a):
                result.append(list_a[idx_a])
                idx_a += 1
                count_a += 1

            # 添加 list_b 的项
            if count_b < max_b and idx_b < len(list_b):
                result.append(list_b[idx_b])
                idx_b += 1
                count_b += 1

            # 如果两个列表都用完了，退出
            if idx_a >= len(list_a) and idx_b >= len(list_b):
                break

            # 如果其中一个列表用完，从另一个补充
            if idx_a >= len(list_a) and count_b < max_b and idx_b < len(list_b):
                continue
            if idx_b >= len(list_b) and count_a < max_a and idx_a < len(list_a):
                continue

        return result

    def _filter_today(self, news_list: List[Dict]) -> List[Dict]:
        """根据配置过滤新闻"""
        today_news = []
        yesterday = (datetime.now(timezone(timedelta(hours=8))) - timedelta(days=1)).strftime('%Y-%m-%d')

        print(f"[*] 过滤新闻，今日: {self.today}, 昨日: {yesterday}, 模式: {self.date_filter_mode}, 待过滤: {len(news_list)} 条")

        for news in news_list:
            news_time = news.get('time', '')

            # 标准化时间
            if not news_time or not news_time.strip():
                # 没有时间信息，跳过（不保留）
                continue

            # 检查是否包含今日日期
            if self.today in news_time:
                news['time'] = self.today
                today_news.append(news)
                continue

            # 检查是否是"今天"、"今日"等关键词
            today_keywords = ['今天', '今日', 'today', 'Today', '刚刚', '小时前', '分钟前', 'hours ago', 'minutes ago', 'just now']
            if any(kw in news_time for kw in today_keywords):
                news['time'] = self.today
                today_news.append(news)
                continue

            # 解析日期检查
            try:
                parsed_date = self._parse_news_date(news_time)
                if parsed_date == self.today:
                    news['time'] = self.today
                    today_news.append(news)
                elif self.date_filter_mode == "today_and_yesterday" and parsed_date == yesterday:
                    # 如果配置允许，也保留昨天的新闻
                    news['time'] = self.today
                    today_news.append(news)
            except:
                # 解析失败，跳过
                continue

        print(f"[*] 过滤完成，保留 {len(today_news)} 条新闻")
        return today_news

    def _parse_news_date(self, date_str: str) -> str:
        """解析新闻日期，返回 YYYY-MM-DD 格式"""
        if not date_str:
            return None

        # 清理日期字符串
        date_str = date_str.strip()

        # 尝试多种日期格式
        formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%b %d, %Y',  # Jul 16, 2026
            '%d %b %Y',   # 16 Jul 2026
            '%B %d, %Y',  # July 16, 2026
            '%d %B %Y',   # 16 July 2026
            '%Y-%m-%dT%H:%M:%S',  # ISO 8601
            '%Y-%m-%dT%H:%M:%SZ', # ISO 8601 UTC
            '%Y-%m-%dT%H:%M:%S%z', # ISO 8601 with timezone
        ]

        # 移除时间部分（保留日期）
        if 'T' in date_str:
            date_str = date_str.split('T')[0]
        if ' ' in date_str and ':' in date_str:
            # 可能是 "2026-07-16 10:30:00" 格式
            parts = date_str.split(' ')
            if len(parts) >= 2 and '-' in parts[0]:
                date_str = parts[0]

        # 尝试解析
        for fmt in formats:
            try:
                # 对于英文月份格式，需要完整匹配
                if '%b' in fmt or '%B' in fmt:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%Y-%m-%d')
                else:
                    dt = datetime.strptime(date_str[:10], fmt[:len(date_str[:10])])
                    return dt.strftime('%Y-%m-%d')
            except Exception as e:
                continue

        # 尝试从 RFC 2822 格式解析
        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(date_str)
            return dt.strftime('%Y-%m-%d')
        except:
            pass

        return None

    def _deduplicate(self, news_list: List[Dict]) -> List[Dict]:
        """去重"""
        seen_titles = set()
        unique_news = []

        for news in news_list:
            title = news.get('title', '').strip()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(news)

        return unique_news


class RSSFeedParser:
    """RSS 订阅源解析器"""

    FEEDS = {
        'military': [
            'https://www.mod.go.jp/news/rss.xml',  # 日本防卫省
            'https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=1&max=10',  # 美国国防部
        ],
        'finance': [
            'https://feeds.reuters.com/reuters/businessNews',  # 路透社商业
            'https://feeds.reuters.com/reuters/topNews',  # 路透社头条
        ]
    }

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def parse_feed(self, url: str) -> List[Dict]:
        """解析 RSS 源"""
        results = []
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.text)

                # 处理 RSS 2.0
                for item in root.findall('.//item')[:10]:
                    title = item.find('title')
                    link = item.find('link')
                    desc = item.find('description')
                    pub_date = item.find('pubDate')

                    if title is not None:
                        results.append({
                            'title': title.text or '',
                            'source': url.split('/')[2],
                            'time': self._parse_date(pub_date.text if pub_date is not None else ''),
                            'url': link.text if link is not None else '',
                            'summary': desc.text[:200] if desc is not None and desc.text else ''
                        })
        except Exception as e:
            print(f"RSS 解析失败 {url}: {e}")

        return results

    def _parse_date(self, date_str: str) -> str:
        """解析日期"""
        if not date_str:
            return datetime.now().strftime('%Y-%m-%d')
        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(date_str)
            return dt.strftime('%Y-%m-%d')
        except:
            return datetime.now().strftime('%Y-%m-%d')

    def get_all_news(self, category: str) -> List[Dict]:
        """获取指定类别的所有新闻"""
        feeds = self.FEEDS.get(category, [])
        all_news = []

        for feed_url in feeds:
            news = self.parse_feed(feed_url)
            all_news.extend(news)

        return all_news
