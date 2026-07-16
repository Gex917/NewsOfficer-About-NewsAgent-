"""
NewsOfficer - AI 驱动的每日资讯收集助手
支持 OpenAI、Claude、MiMo API
带 PyQt6 GUI 界面
"""

import os
import sys
import io
import webbrowser
import threading
from datetime import datetime

# 修复 Windows 控制台编码
if sys.platform == 'win32':
    try:
        if sys.stdout and sys.stdout.buffer:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if sys.stderr and sys.stderr.buffer:
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from agent import NewsOfficer
from agent.ai_provider import create_provider
from report import ReportGenerator
from scheduler import TaskScheduler

from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import Qt
from gui.main_window import MainWindow


class NewsOfficerApp:
    """主应用"""

    def __init__(self):
        self.ai_provider = None
        self.agent = None
        self.report_gen = ReportGenerator(config.REPORT_DIR)
        self.scheduler = TaskScheduler()
        self.is_collecting = False

    def initialize(self):
        """初始化应用"""
        print("=" * 60)
        print("  🌍 NewsOfficer - AI 资讯收集助手")
        print("=" * 60)
        print(f"  当前 AI: {config.AI_PROVIDER}")
        print(f"  收集时间: {', '.join(config.SCHEDULE_TIMES)}")
        print(f"  新闻源: BBC、纽约时报、路透社、卫报、CNN、CNBC 等主流媒体")
        print(f"  网络配置: 超时 {config.REQUEST_TIMEOUT}秒, 重试 {config.RETRY_COUNT}次")
        print(f"  日期过滤: {config.DATE_FILTER_MODE}")
        print("=" * 60)
        print()

        # 初始化 AI Provider
        try:
            self.ai_provider = create_provider(config.AI_PROVIDER, config)
            self.agent = NewsOfficer(
                self.ai_provider,
                timeout=config.REQUEST_TIMEOUT,
                retry_count=config.RETRY_COUNT,
                retry_delay=config.RETRY_DELAY,
                date_filter_mode=config.DATE_FILTER_MODE
            )
            print(f"[✓] AI Provider 初始化成功: {config.AI_PROVIDER}")
        except Exception as e:
            print(f"[!] AI Provider 初始化失败: {e}")
            print("[!] 请检查 config.py 中的 API 配置")
            return False

        # 设置定时任务
        for time_str in config.SCHEDULE_TIMES:
            self.scheduler.add_scheduled_task(
                time_str,
                self._scheduled_collect,
                "news_collect"
            )

        return True

    def _scheduled_collect(self):
        """定时收集"""
        print(f"\n[*] 定时任务触发 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.collect_news()

    def collect_news(self) -> dict:
        """收集新闻"""
        if self.is_collecting:
            print("[*] 正在收集中，请稍候...")
            return {}

        self.is_collecting = True

        try:
            data = self.agent.collect_all()
            return data
        except Exception as e:
            print(f"[!] 收集失败: {e}")
            raise
        finally:
            self.is_collecting = False

    def start_scheduler(self):
        """启动调度器"""
        self.scheduler.start()


def create_icon():
    """创建应用图标"""
    pixmap = QPixmap(64, 64)
    pixmap.fill(QColor(0, 0, 0, 0))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # 背景圆
    painter.setBrush(QColor(137, 180, 250))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(4, 4, 56, 56)

    # 文字
    painter.setPen(QColor(30, 30, 46))
    painter.setFont(QFont("", 24, QFont.Weight.Bold))
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "N")

    painter.end()
    return QIcon(pixmap)


def main():
    """主函数"""
    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("NewsOfficer")
    app.setApplicationDisplayName("NewsOfficer - AI 资讯收集助手")

    # 设置图标
    icon = create_icon()
    app.setWindowIcon(icon)

    # 初始化后端
    backend = NewsOfficerApp()
    if not backend.initialize():
        print("[!] 初始化失败，程序退出")
        sys.exit(1)

    # 创建主窗口
    window = MainWindow(config, backend)
    window.setWindowIcon(icon)
    window.show()

    # 启动定时任务
    backend.start_scheduler()

    # 系统托盘
    if config.SHOW_TRAY and QSystemTrayIcon.isSystemTrayAvailable():
        tray = QSystemTrayIcon(icon, app)
        tray.setToolTip("NewsOfficer - AI 资讯收集助手")

        # 托盘菜单
        menu = QMenu()
        show_action = QAction("显示主窗口", app)
        show_action.triggered.connect(window.show)
        menu.addAction(show_action)

        collect_action = QAction("立即收集", app)
        collect_action.triggered.connect(window.start_collect)
        menu.addAction(collect_action)

        menu.addSeparator()

        quit_action = QAction("退出", app)
        quit_action.triggered.connect(app.quit)
        menu.addAction(quit_action)

        tray.setContextMenu(menu)
        tray.activated.connect(lambda reason: window.show() if reason == QSystemTrayIcon.ActivationReason.DoubleClick else None)
        tray.show()

    # 运行
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
