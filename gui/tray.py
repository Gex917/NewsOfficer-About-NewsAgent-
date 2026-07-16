"""
系统托盘图标
"""

import os
import sys
import webbrowser
from typing import Callable, Optional

try:
    import pystray
    from pystray import MenuItem as Item
    from PIL import Image, ImageDraw
    HAS_TRAY = True
except ImportError:
    HAS_TRAY = False


class TrayIcon:
    """系统托盘图标"""

    def __init__(self, app_name: str = "NewsOfficer"):
        self.app_name = app_name
        self.icon = None
        self.on_collect: Optional[Callable] = None
        self.on_open_report: Optional[Callable] = None
        self.on_quit: Optional[Callable] = None
        self.last_report_path: Optional[str] = None

    def create_icon_image(self, color: str = "blue") -> "Image.Image":
        """创建图标"""
        if not HAS_TRAY:
            return None

        # 创建一个简单的图标
        width = 64
        height = 64
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # 画一个圆形背景
        colors = {
            "blue": (70, 130, 180),
            "green": (46, 204, 113),
            "red": (231, 76, 60)
        }
        fill_color = colors.get(color, colors["blue"])

        draw.ellipse([4, 4, width-4, height-4], fill=fill_color)

        # 画一个 "N" 字
        draw.text((20, 15), "N", fill="white")

        return image

    def setup(self, on_collect: Callable = None, on_open_report: Callable = None,
              on_quit: Callable = None):
        """设置回调"""
        self.on_collect = on_collect
        self.on_open_report = on_open_report
        self.on_quit = on_quit

    def _create_menu(self):
        """创建菜单"""
        if not HAS_TRAY:
            return None

        return pystray.Menu(
            Item('📰 立即收集', self._on_collect),
            Item('📂 打开报告', self._on_open_report),
            pystray.Menu.SEPARATOR,
            Item('❌ 退出', self._on_quit)
        )

    def _on_collect(self, icon=None, item=None):
        """收集回调"""
        if self.on_collect:
            self.on_collect()

    def _on_open_report(self, icon=None, item=None):
        """打开报告回调"""
        if self.on_open_report:
            self.on_open_report()
        elif self.last_report_path:
            webbrowser.open(self.last_report_path)

    def _on_quit(self, icon=None, item=None):
        """退出回调"""
        if self.on_quit:
            self.on_quit()
        if self.icon:
            self.icon.stop()

    def show_notification(self, title: str, message: str):
        """显示通知"""
        if HAS_TRAY and self.icon:
            try:
                self.icon.notify(message, title)
            except Exception:
                pass

    def update_last_report(self, report_path: str):
        """更新最后报告路径"""
        self.last_report_path = report_path

    def run(self):
        """运行托盘图标"""
        if not HAS_TRAY:
            print("[!] pystray 或 Pillow 未安装，系统托盘不可用")
            print("[!] 请运行: pip install pystray Pillow")
            return

        image = self.create_icon_image("blue")
        menu = self._create_menu()

        self.icon = pystray.Icon(
            name=self.app_name,
            icon=image,
            title=self.app_name,
            menu=menu
        )

        print(f"[✓] 系统托盘已启动: {self.app_name}")
        self.icon.run()

    def stop(self):
        """停止托盘"""
        if self.icon:
            self.icon.stop()
