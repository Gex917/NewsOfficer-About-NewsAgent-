"""
NewsOfficer - 主窗口 UI (现代化黑白主题)
"""

import os
import sys
import webbrowser
import threading
from datetime import datetime
from typing import Optional, List, Dict

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QComboBox, QLineEdit, QSpinBox,
    QTimeEdit, QGroupBox, QFormLayout, QStatusBar, QSystemTrayIcon,
    QMenu, QMessageBox, QProgressBar, QSplitter, QFrame, QDialog,
    QTextBrowser, QAbstractItemView
)
from PyQt6.QtCore import Qt, QTime, pyqtSignal, QObject, QSize, QTimer
from datetime import datetime, timezone, timedelta
from PyQt6.QtGui import QFont, QColor, QIcon, QAction, QPixmap, QPainter, QBrush


# ==================== 黑白主题样式 ====================

DARK_THEME = """
QMainWindow {
    background-color: #0a0a0a;
}
QWidget {
    background-color: #0a0a0a;
    color: #e0e0e0;
    font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
}
QTabWidget::pane {
    border: 1px solid #2a2a2a;
    background-color: #0a0a0a;
    border-radius: 8px;
}
QTabBar::tab {
    background-color: #1a1a1a;
    color: #808080;
    padding: 16px 32px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-size: 14px;
    letter-spacing: 1px;
}
QTabBar::tab:selected {
    background-color: #2a2a2a;
    color: #ffffff;
    font-weight: bold;
}
QTabBar::tab:hover {
    background-color: #222222;
    color: #cccccc;
}
QGroupBox {
    background-color: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    margin-top: 15px;
    padding-top: 20px;
    font-weight: bold;
    font-size: 13px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px;
    color: #ffffff;
}
QLineEdit, QSpinBox, QTimeEdit, QComboBox {
    background-color: #1a1a1a;
    color: #e0e0e0;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
}
QLineEdit:focus, QSpinBox:focus, QTimeEdit:focus, QComboBox:focus {
    border: 1px solid #ffffff;
}
QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #808080;
    margin-right: 5px;
}
QComboBox QAbstractItemView {
    background-color: #1a1a1a;
    color: #e0e0e0;
    border: 1px solid #333333;
    selection-background-color: #333333;
}
QPushButton {
    background-color: #1a1a1a;
    color: #e0e0e0;
    border: 1px solid #333333;
    border-radius: 8px;
    padding: 14px 28px;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #2a2a2a;
    border: 1px solid #555555;
}
QPushButton:pressed {
    background-color: #333333;
}
QPushButton:disabled {
    background-color: #111111;
    color: #444444;
    border: 1px solid #222222;
}
QProgressBar {
    border: 1px solid #333333;
    border-radius: 4px;
    text-align: center;
    background-color: #1a1a1a;
    color: #ffffff;
}
QProgressBar::chunk {
    background-color: #ffffff;
    border-radius: 3px;
}
QStatusBar {
    background-color: #111111;
    color: #808080;
    font-size: 12px;
    border-top: 1px solid #222222;
}
QTableWidget {
    background-color: #0f0f0f;
    color: #e0e0e0;
    border: 1px solid #222222;
    gridline-color: #1a1a1a;
    selection-background-color: #2a2a2a;
    font-size: 13px;
}
QTableWidget::item {
    padding: 0px 12px;
    border-bottom: 1px solid #1a1a1a;
}
QTableWidget::item:selected {
    background-color: #2a2a2a;
    color: #ffffff;
}
QTableWidget::item:hover {
    background-color: #1a1a1a;
}
QHeaderView::section {
    background-color: #141414;
    color: #ffffff;
    padding: 16px 12px;
    border: none;
    border-bottom: 2px solid #333333;
    font-weight: bold;
    font-size: 14px;
}
QHeaderView::section:hover {
    background-color: #1a1a1a;
}
QTextEdit {
    background-color: #0f0f0f;
    color: #e0e0e0;
    border: 1px solid #222222;
    border-radius: 8px;
    padding: 16px;
    font-size: 13px;
    line-height: 1.6;
}
QScrollBar:vertical {
    background-color: #0a0a0a;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background-color: #333333;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #555555;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background-color: #0a0a0a;
    height: 10px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal {
    background-color: #333333;
    border-radius: 5px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #555555;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
"""


class Communicate(QObject):
    """信号通信"""
    update_status = pyqtSignal(str)
    update_progress = pyqtSignal(int)
    news_collected = pyqtSignal(dict)
    show_error = pyqtSignal(str, str)


class DetailDialog(QDialog):
    """新闻详情对话框"""

    def __init__(self, news_data: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📰 新闻详情")
        self.setMinimumSize(600, 500)
        self.setup_ui(news_data)

    def setup_ui(self, news_data: dict):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # 标题
        title = news_data.get('title', '未知标题')
        title_label = QLabel(title)
        title_label.setFont(QFont("", 18, QFont.Weight.Bold))
        title_label.setWordWrap(True)
        title_label.setStyleSheet("color: #ffffff; padding: 8px 0;")
        layout.addWidget(title_label)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #333333; max-height: 1px;")
        layout.addWidget(line)

        # 元信息
        meta_layout = QHBoxLayout()

        source = news_data.get('source', '未知来源')
        time = news_data.get('time', '未知时间')
        importance = news_data.get('importance', '中')

        importance_colors = {'高': '#ff4444', '中': '#ffaa00', '低': '#44ff44'}
        imp_color = importance_colors.get(importance, '#808080')

        meta_text = f"📰 来源: {source}  |  🕐 时间: {time}  |  ⚡ 重要性: <span style='color:{imp_color}'>{importance}</span>"
        meta_label = QLabel(meta_text)
        meta_label.setStyleSheet("color: #999999; font-size: 13px;")
        meta_label.setTextFormat(Qt.TextFormat.RichText)
        meta_layout.addWidget(meta_label)

        layout.addLayout(meta_layout)

        # 详细内容
        content_label = QLabel("📋 详细内容")
        content_label.setFont(QFont("", 14, QFont.Weight.Bold))
        content_label.setStyleSheet("color: #ffffff; margin-top: 8px;")
        layout.addWidget(content_label)

        content_text = QTextEdit()
        content_text.setReadOnly(True)
        content_text.setStyleSheet("""
            QTextEdit {
                background-color: #141414;
                color: #cccccc;
                border: 1px solid #2a2a2a;
                border-radius: 8px;
                padding: 16px;
                font-size: 14px;
                line-height: 1.8;
            }
        """)

        # 获取详细内容
        summary = news_data.get('summary', '暂无详细内容')
        detail = news_data.get('detail', '')
        content = detail if detail else summary
        if not content:
            content = '暂无详细内容'

        content_text.setText(content)
        layout.addWidget(content_text)

        # 链接
        url = news_data.get('url', '')
        if url:
            link_btn = QPushButton("🔗 查看原文")
            link_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    color: #000000;
                    padding: 10px 24px;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #cccccc;
                }
            """)
            link_btn.clicked.connect(lambda: webbrowser.open(url))
            layout.addWidget(link_btn)

        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)


class SortableTable(QTableWidget):
    """可排序的新闻表格"""

    def __init__(self, category: str = "military"):
        super().__init__()
        self.category = category
        self.all_news: List[Dict] = []
        self.current_sort_col = -1
        self.current_sort_order = Qt.SortOrder.AscendingOrder
        self.setup_ui()

    def setup_ui(self):
        """设置表格"""
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["标题", "来源", "地区", "时间", "重要性", "优先级"])

        # 设置列宽
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        # 启用排序
        self.setSortingEnabled(True)
        header.sectionClicked.connect(self.on_header_clicked)

        # 选择行为
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.verticalHeader().setVisible(False)

        # 固定行高
        self.verticalHeader().setDefaultSectionSize(48)
        self.verticalHeader().setMinimumSectionSize(48)

        # 双击打开详情
        self.cellDoubleClicked.connect(self.on_row_double_clicked)

    def on_header_clicked(self, logical_index: int):
        """表头点击排序"""
        if self.current_sort_col == logical_index:
            # 切换排序方向
            if self.current_sort_order == Qt.SortOrder.AscendingOrder:
                self.current_sort_order = Qt.SortOrder.DescendingOrder
            else:
                self.current_sort_order = Qt.SortOrder.AscendingOrder
        else:
            self.current_sort_col = logical_index
            self.current_sort_order = Qt.SortOrder.AscendingOrder

        self.sortItems(logical_index, self.current_sort_order)

    def update_news(self, news_list: list):
        """更新新闻数据"""
        self.all_news = news_list
        self.setSortingEnabled(False)
        self.setRowCount(len(news_list))

        for row, news in enumerate(news_list):
            title = news.get("title", "")
            source = news.get("source", "")
            region = news.get("region", "国际")
            time = news.get("time", "")
            importance = news.get("importance", "中")
            priority = news.get("priority", "normal")

            # 标题
            title_item = QTableWidgetItem(title)
            title_item.setData(Qt.ItemDataRole.UserRole, news)
            title_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.setItem(row, 0, title_item)

            # 来源
            source_item = QTableWidgetItem(source)
            source_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.setItem(row, 1, source_item)

            # 地区
            region_item = QTableWidgetItem(region)
            region_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.setItem(row, 2, region_item)

            # 时间
            time_item = QTableWidgetItem(time)
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.setItem(row, 3, time_item)

            # 重要性（带颜色）
            imp_item = QTableWidgetItem(importance)
            imp_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            importance_colors = {'高': '#ff4444', '中': '#ffaa00', '低': '#44ff44'}
            imp_item.setForeground(QColor(importance_colors.get(importance, "#808080")))
            imp_item.setFont(QFont("", 11, QFont.Weight.Bold))
            self.setItem(row, 4, imp_item)

            # 优先级（主流媒体标记为高优先级）
            priority_item = QTableWidgetItem(priority.upper())
            priority_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            if priority == 'high':
                priority_item.setForeground(QColor("#44ff44"))
                priority_item.setFont(QFont("", 11, QFont.Weight.Bold))
            self.setItem(row, 5, priority_item)

        self.setSortingEnabled(True)

    def on_row_double_clicked(self, row: int, col: int):
        """双击行打开详情"""
        item = self.item(row, 0)
        if item:
            news_data = item.data(Qt.ItemDataRole.UserRole)
            if news_data:
                dialog = DetailDialog(news_data, self)
                dialog.exec()


class SettingsPanel(QWidget):
    """设置面板"""

    def __init__(self, config, on_save_callback=None):
        super().__init__()
        self.config = config
        self.on_save_callback = on_save_callback
        self.setup_ui()

    def _create_row(self, label_text: str, widget) -> QHBoxLayout:
        """创建一行：标签 + 输入框"""
        row = QHBoxLayout()
        row.setSpacing(16)

        label = QLabel(label_text)
        label.setFixedWidth(120)
        label.setStyleSheet("font-size: 15px; color: #bbbbbb;")
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        widget.setMinimumHeight(44)
        widget.setStyleSheet("""
            font-size: 15px;
            padding: 8px 14px;
            background-color: #1a1a1a;
            border: 1px solid #333333;
            border-radius: 6px;
            color: #e0e0e0;
        """)

        row.addWidget(label)
        row.addWidget(widget, 1)
        return row

    def _create_separator(self) -> QFrame:
        """创建分隔线"""
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #222222; max-height: 1px; margin: 15px 0;")
        sep.setFixedHeight(1)
        return sep

    def _create_section_title(self, text: str) -> QLabel:
        """创建分区标题"""
        label = QLabel(text)
        label.setStyleSheet("font-size: 14px; color: #666666; font-weight: bold; margin-bottom: 10px;")
        return label

    def setup_ui(self):
        """设置界面"""
        # 外层滚动
        from PyQt6.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(24)
        layout.setContentsMargins(50, 30, 50, 30)

        # ========== AI 设置 ==========
        ai_group = QGroupBox("🤖 AI 设置")
        ai_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                border: 1px solid #2a2a2a;
                border-radius: 10px;
                margin-top: 20px;
                padding: 30px;
                background-color: #111111;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                top: 5px;
                padding: 0 10px;
                color: #ffffff;
            }
        """)
        ai_layout = QVBoxLayout()
        ai_layout.setSpacing(18)

        # AI 提供商
        self.ai_combo = QComboBox()
        self.ai_combo.addItems(["openai", "claude", "mimo"])
        self.ai_combo.setCurrentText(self.config.AI_PROVIDER)
        ai_layout.addLayout(self._create_row("AI 提供商:", self.ai_combo))

        ai_layout.addWidget(self._create_separator())

        # ---- OpenAI ----
        ai_layout.addWidget(self._create_section_title("OpenAI"))

        self.openai_key = QLineEdit(self.config.OPENAI_API_KEY)
        self.openai_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_key.setPlaceholderText("sk-...")
        ai_layout.addLayout(self._create_row("API Key:", self.openai_key))

        self.openai_url = QLineEdit(self.config.OPENAI_BASE_URL)
        ai_layout.addLayout(self._create_row("Base URL:", self.openai_url))

        self.openai_model = QLineEdit(self.config.OPENAI_MODEL)
        ai_layout.addLayout(self._create_row("Model:", self.openai_model))

        ai_layout.addWidget(self._create_separator())

        # ---- Claude ----
        ai_layout.addWidget(self._create_section_title("Claude"))

        self.claude_key = QLineEdit(self.config.CLAUDE_API_KEY)
        self.claude_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.claude_key.setPlaceholderText("sk-ant-...")
        ai_layout.addLayout(self._create_row("API Key:", self.claude_key))

        self.claude_url = QLineEdit(self.config.CLAUDE_BASE_URL)
        ai_layout.addLayout(self._create_row("Base URL:", self.claude_url))

        self.claude_model = QLineEdit(self.config.CLAUDE_MODEL)
        ai_layout.addLayout(self._create_row("Model:", self.claude_model))

        ai_layout.addWidget(self._create_separator())

        # ---- MiMo ----
        ai_layout.addWidget(self._create_section_title("MiMo"))

        self.mimo_key = QLineEdit(self.config.MIMO_API_KEY)
        self.mimo_key.setEchoMode(QLineEdit.EchoMode.Password)
        ai_layout.addLayout(self._create_row("API Key:", self.mimo_key))

        self.mimo_url = QLineEdit(self.config.MIMO_BASE_URL)
        ai_layout.addLayout(self._create_row("Base URL:", self.mimo_url))

        self.mimo_model = QLineEdit(self.config.MIMO_MODEL)
        ai_layout.addLayout(self._create_row("Model:", self.mimo_model))

        ai_group.setLayout(ai_layout)
        layout.addWidget(ai_group)

        # ========== 定时设置 ==========
        schedule_group = QGroupBox("⏰ 定时设置")
        schedule_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                border: 1px solid #2a2a2a;
                border-radius: 10px;
                margin-top: 20px;
                padding: 30px;
                background-color: #111111;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                top: 5px;
                padding: 0 10px;
                color: #ffffff;
            }
        """)
        schedule_layout = QVBoxLayout()
        schedule_layout.setSpacing(18)

        self.time1 = QTimeEdit()
        self.time1.setTime(QTime(8, 0))
        schedule_layout.addLayout(self._create_row("收集时间 1:", self.time1))

        self.time2 = QTimeEdit()
        self.time2.setTime(QTime(12, 0))
        schedule_layout.addLayout(self._create_row("收集时间 2:", self.time2))

        self.time3 = QTimeEdit()
        self.time3.setTime(QTime(18, 0))
        schedule_layout.addLayout(self._create_row("收集时间 3:", self.time3))

        schedule_group.setLayout(schedule_layout)
        layout.addWidget(schedule_group)

        # ========== 网络设置 ==========
        network_group = QGroupBox("🌐 网络设置")
        network_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                border: 1px solid #2a2a2a;
                border-radius: 10px;
                margin-top: 20px;
                padding: 30px;
                background-color: #111111;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                top: 5px;
                padding: 0 10px;
                color: #ffffff;
            }
        """)
        network_layout = QVBoxLayout()
        network_layout.setSpacing(18)

        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(5, 60)
        self.timeout_spin.setValue(self.config.REQUEST_TIMEOUT)
        self.timeout_spin.setSuffix(" 秒")
        network_layout.addLayout(self._create_row("请求超时:", self.timeout_spin))

        self.retry_count_spin = QSpinBox()
        self.retry_count_spin.setRange(1, 10)
        self.retry_count_spin.setValue(self.config.RETRY_COUNT)
        self.retry_count_spin.setSuffix(" 次")
        network_layout.addLayout(self._create_row("重试次数:", self.retry_count_spin))

        self.retry_delay_spin = QSpinBox()
        self.retry_delay_spin.setRange(1, 10)
        self.retry_delay_spin.setValue(self.config.RETRY_DELAY)
        self.retry_delay_spin.setSuffix(" 秒")
        network_layout.addLayout(self._create_row("重试延迟:", self.retry_delay_spin))

        network_layout.addWidget(self._create_separator())

        # 日期过滤模式
        self.date_filter_combo = QComboBox()
        self.date_filter_combo.addItems(["today_only", "today_and_yesterday"])
        self.date_filter_combo.setCurrentText(self.config.DATE_FILTER_MODE)
        network_layout.addLayout(self._create_row("日期过滤:", self.date_filter_combo))

        network_group.setLayout(network_layout)
        layout.addWidget(network_group)

        # ========== 保存按钮 ==========
        btn_container = QWidget()
        btn_container.setStyleSheet("background: transparent;")
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 30, 0, 20)

        save_btn = QPushButton("💾  保存设置")
        save_btn.setFixedSize(260, 64)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #cccccc;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)

        layout.addWidget(btn_container)

        layout.addStretch()

        scroll.setWidget(content)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def save_settings(self):
        """保存设置"""
        self.config.AI_PROVIDER = self.ai_combo.currentText()
        self.config.OPENAI_API_KEY = self.openai_key.text()
        self.config.OPENAI_BASE_URL = self.openai_url.text()
        self.config.OPENAI_MODEL = self.openai_model.text()
        self.config.CLAUDE_API_KEY = self.claude_key.text()
        self.config.CLAUDE_BASE_URL = self.claude_url.text()
        self.config.CLAUDE_MODEL = self.claude_model.text()
        self.config.MIMO_API_KEY = self.mimo_key.text()
        self.config.MIMO_BASE_URL = self.mimo_url.text()
        self.config.MIMO_MODEL = self.mimo_model.text()

        # 保存网络设置
        self.config.REQUEST_TIMEOUT = self.timeout_spin.value()
        self.config.RETRY_COUNT = self.retry_count_spin.value()
        self.config.RETRY_DELAY = self.retry_delay_spin.value()
        self.config.DATE_FILTER_MODE = self.date_filter_combo.currentText()

        self._save_to_file()

        if self.on_save_callback:
            self.on_save_callback()

        QMessageBox.information(self, "保存成功", "设置已保存并生效！")

    def _save_to_file(self):
        """保存配置到文件"""
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        config_path = os.path.join(base_dir, 'config.py')

        content = f'''"""
配置文件 - 支持多种 AI API
"""

AI_PROVIDER = "{self.config.AI_PROVIDER}"

OPENAI_API_KEY = "{self.config.OPENAI_API_KEY}"
OPENAI_BASE_URL = "{self.config.OPENAI_BASE_URL}"
OPENAI_MODEL = "{self.config.OPENAI_MODEL}"

CLAUDE_API_KEY = "{self.config.CLAUDE_API_KEY}"
CLAUDE_BASE_URL = "{self.config.CLAUDE_BASE_URL}"
CLAUDE_MODEL = "{self.config.CLAUDE_MODEL}"

MIMO_API_KEY = "{self.config.MIMO_API_KEY}"
MIMO_BASE_URL = "{self.config.MIMO_BASE_URL}"
MIMO_MODEL = "{self.config.MIMO_MODEL}"

SCHEDULE_TIMES = ["08:00", "12:00", "18:00"]
CATEGORIES = ["军事", "金融"]
MAX_NEWS_PER_CATEGORY = 10
REPORT_DIR = "reports"
SHOW_TRAY = True
SHOW_NOTIFICATION = True
AUTO_OPEN_REPORT = True

# 网络请求配置
REQUEST_TIMEOUT = {self.config.REQUEST_TIMEOUT}
RETRY_COUNT = {self.config.RETRY_COUNT}
RETRY_DELAY = {self.config.RETRY_DELAY}

# 日期过滤模式
DATE_FILTER_MODE = "{self.config.DATE_FILTER_MODE}"
'''
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"保存配置失败: {e}")


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, config, app_instance):
        super().__init__()
        self.config = config
        self.app = app_instance
        self.comm = Communicate()
        self.setup_signals()
        self.setup_ui()

    def setup_signals(self):
        """设置信号连接"""
        self.comm.update_status.connect(self._update_status)
        self.comm.update_progress.connect(self._update_progress)
        self.comm.news_collected.connect(self._on_news_collected)
        self.comm.show_error.connect(self._show_error)

    def setup_ui(self):
        """设置界面"""
        self.setWindowTitle("NewsOfficer")
        self.setMinimumSize(1200, 850)

        # 应用深色主题
        self.setStyleSheet(DARK_THEME)

        # 中央部件
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # 顶部工具栏
        toolbar = QHBoxLayout()
        toolbar.setSpacing(16)

        # Logo
        logo_label = QLabel("NEWSAGENT")
        logo_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        logo_label.setStyleSheet("color: #ffffff; letter-spacing: 3px;")
        toolbar.addWidget(logo_label)

        # 版本标签
        version_label = QLabel("v1.0")
        version_label.setStyleSheet("color: #555555; font-size: 11px;")
        toolbar.addWidget(version_label)

        toolbar.addStretch()

        # 北京时间
        self.beijing_time_label = QLabel()
        self.beijing_time_label.setStyleSheet("""
            color: #cccccc;
            font-size: 13px;
            background-color: #1a1a1a;
            padding: 8px 16px;
            border-radius: 6px;
            border: 1px solid #2a2a2a;
        """)
        toolbar.addWidget(self.beijing_time_label)

        # 伦敦时间
        self.london_time_label = QLabel()
        self.london_time_label.setStyleSheet("""
            color: #cccccc;
            font-size: 13px;
            background-color: #1a1a1a;
            padding: 8px 16px;
            border-radius: 6px;
            border: 1px solid #2a2a2a;
        """)
        toolbar.addWidget(self.london_time_label)

        # 更新时间
        self._update_clock()
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self._update_clock)
        self.clock_timer.start(1000)

        toolbar.addSpacing(20)

        # 状态标签
        self.status_label = QLabel("READY")
        self.status_label.setStyleSheet("color: #666666; font-size: 12px; letter-spacing: 1px;")
        toolbar.addWidget(self.status_label)

        # 收集按钮
        self.collect_btn = QPushButton("▶ COLLECT")
        self.collect_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                padding: 12px 32px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #cccccc;
            }
            QPushButton:disabled {
                background-color: #333333;
                color: #666666;
            }
        """)
        self.collect_btn.clicked.connect(self.start_collect)
        toolbar.addWidget(self.collect_btn)

        main_layout.addLayout(toolbar)

        # 进度条
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setFixedHeight(3)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #1a1a1a;
            }
            QProgressBar::chunk {
                background-color: #ffffff;
            }
        """)
        main_layout.addWidget(self.progress)

        # 标签页
        tabs = QTabWidget()

        # 新闻标签页
        news_tab = QWidget()
        news_layout = QVBoxLayout(news_tab)
        news_layout.setSpacing(24)
        news_layout.setContentsMargins(16, 16, 16, 16)

        # 排序控制栏
        sort_bar = QHBoxLayout()
        sort_bar.setSpacing(12)

        sort_label = QLabel("SORT BY:")
        sort_label.setStyleSheet("color: #666666; font-size: 11px; letter-spacing: 1px;")
        sort_bar.addWidget(sort_label)

        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["默认", "来源", "地区", "时间", "重要性", "优先级"])
        self.sort_combo.setStyleSheet("""
            QComboBox {
                background-color: #1a1a1a;
                color: #e0e0e0;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 100px;
            }
        """)
        self.sort_combo.currentTextChanged.connect(self.on_sort_changed)
        sort_bar.addWidget(self.sort_combo)

        sort_bar.addStretch()

        # 统计信息
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet("color: #666666; font-size: 12px;")
        sort_bar.addWidget(self.stats_label)

        news_layout.addLayout(sort_bar)

        # 军事新闻
        military_header = QHBoxLayout()
        military_header.setSpacing(10)
        military_icon = QLabel("◆")
        military_icon.setStyleSheet("color: #ff4444; font-size: 20px;")
        military_header.addWidget(military_icon)
        military_label = QLabel("MILITARY")
        military_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        military_label.setStyleSheet("color: #ffffff; letter-spacing: 3px;")
        military_header.addWidget(military_label)
        military_header.addStretch()
        news_layout.addLayout(military_header)

        self.military_table = SortableTable("military")
        self.military_table.setMinimumHeight(200)
        self.military_table.setMaximumHeight(300)
        news_layout.addWidget(self.military_table)

        # 金融新闻
        finance_header = QHBoxLayout()
        finance_header.setSpacing(10)
        finance_icon = QLabel("◆")
        finance_icon.setStyleSheet("color: #44ff44; font-size: 20px;")
        finance_header.addWidget(finance_icon)
        finance_label = QLabel("FINANCE")
        finance_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        finance_label.setStyleSheet("color: #ffffff; letter-spacing: 3px;")
        finance_header.addWidget(finance_label)
        finance_header.addStretch()
        news_layout.addLayout(finance_header)

        self.finance_table = SortableTable("finance")
        self.finance_table.setMinimumHeight(200)
        self.finance_table.setMaximumHeight(300)
        news_layout.addWidget(self.finance_table)

        # 提示
        hint_label = QLabel("双击新闻条目查看详细内容")
        hint_label.setStyleSheet("color: #555555; font-size: 12px; font-style: italic; margin-top: 8px;")
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        news_layout.addWidget(hint_label)

        tabs.addTab(news_tab, "  NEWS  ")

        # 分析标签页
        analysis_tab = QWidget()
        analysis_layout = QVBoxLayout(analysis_tab)

        analysis_header = QLabel("AI ANALYSIS")
        analysis_header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        analysis_header.setStyleSheet("color: #ffffff; letter-spacing: 2px; margin-bottom: 8px;")
        analysis_layout.addWidget(analysis_header)

        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        analysis_layout.addWidget(self.analysis_text)

        tabs.addTab(analysis_tab, "  ANALYSIS  ")

        # 日志标签页
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)

        log_header = QLabel("SYSTEM LOG")
        log_header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        log_header.setStyleSheet("color: #ffffff; letter-spacing: 2px; margin-bottom: 8px;")
        log_layout.addWidget(log_header)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #050505;
                color: #808080;
                border: 1px solid #1a1a1a;
                border-radius: 8px;
                padding: 16px;
                font-family: "Consolas", "Courier New", monospace;
                font-size: 12px;
            }
        """)
        log_layout.addWidget(self.log_text)

        tabs.addTab(log_tab, "  LOG  ")

        # 设置标签页
        settings_tab = SettingsPanel(self.config, on_save_callback=self._on_settings_saved)
        tabs.addTab(settings_tab, "  SETTINGS  ")

        main_layout.addWidget(tabs)

        # 状态栏
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #0a0a0a;
                color: #555555;
                border-top: 1px solid #1a1a1a;
                padding: 4px;
            }
        """)

        # 初始日志
        self.log("NewsOfficer initialized")
        self.log(f"AI Provider: {self.config.AI_PROVIDER}")
        self.log(f"Schedule: {', '.join(self.config.SCHEDULE_TIMES)}")
        self.log("News Sources: BBC, NYT, Reuters, Guardian, CNN, CNBC")
        self.log(f"Network: Timeout {self.config.REQUEST_TIMEOUT}s, Retry {self.config.RETRY_COUNT}x")
        self.log(f"Date Filter: {self.config.DATE_FILTER_MODE}")
        self.log("Ready to collect")

    def _update_clock(self):
        """更新时钟显示"""
        # 北京时间 (UTC+8)
        beijing_tz = timezone(timedelta(hours=8))
        beijing_now = datetime.now(beijing_tz)
        self.beijing_time_label.setText(f"🇨🇳 北京 {beijing_now.strftime('%Y-%m-%d %H:%M:%S')}")

        # 伦敦时间 (UTC+0 / UTC+1 夏令时)
        london_tz = timezone(timedelta(hours=0))
        london_now = datetime.now(london_tz)
        self.london_time_label.setText(f"🇬🇧 伦敦 {london_now.strftime('%Y-%m-%d %H:%M:%S')}")

    def log(self, message: str):
        """添加日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"<span style='color:#555555'>[{timestamp}]</span> <span style='color:#aaaaaa'>{message}</span>")

    def start_collect(self):
        """开始收集"""
        self.collect_btn.setEnabled(False)
        self.collect_btn.setText("⏳ COLLECTING...")
        self.status_label.setText("COLLECTING...")
        self.status_label.setStyleSheet("color: #ffffff; font-size: 12px; letter-spacing: 1px;")
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.log("Starting news collection...")

        thread = threading.Thread(target=self._collect_thread, daemon=True)
        thread.start()

    def _collect_thread(self):
        """收集线程"""
        try:
            data = self.app.collect_news()
            self.comm.news_collected.emit(data)
        except Exception as e:
            self.comm.show_error.emit("Collection Failed", str(e))
        finally:
            self.comm.update_status.emit("READY")
            self.comm.update_progress.emit(100)

    def _update_status(self, status: str):
        """更新状态"""
        self.status_label.setText(status)
        self.status_label.setStyleSheet("color: #666666; font-size: 12px; letter-spacing: 1px;")
        self.collect_btn.setEnabled(True)
        self.collect_btn.setText("▶ COLLECT")
        self.progress.setVisible(False)

    def _update_progress(self, value: int):
        """更新进度"""
        if value >= 100:
            self.progress.setVisible(False)
        else:
            self.progress.setValue(value)

    def _on_news_collected(self, data: dict):
        """新闻收集完成"""
        military = data.get("military", [])
        finance = data.get("finance", [])
        summary = data.get("summary", "")
        elapsed_time = data.get("elapsed_time", 0)

        self.military_table.update_news(military)
        self.finance_table.update_news(finance)
        self.analysis_text.setText(summary)

        # 统计高优先级新闻
        high_priority_military = len([n for n in military if n.get('priority') == 'high'])
        high_priority_finance = len([n for n in finance if n.get('priority') == 'high'])

        # 统计今日新闻
        today_military = len([n for n in military if n.get('time') == datetime.now().strftime('%Y-%m-%d')])
        today_finance = len([n for n in finance if n.get('time') == datetime.now().strftime('%Y-%m-%d')])

        # 更新统计
        self.stats_label.setText(
            f"Military: {len(military)} ({today_military} today) | "
            f"Finance: {len(finance)} ({today_finance} today) | "
            f"Time: {elapsed_time:.1f}s"
        )

        self.log(f"Collection complete: Military {len(military)}, Finance {len(finance)}")
        self.log(f"Today's news: Military {today_military}, Finance {today_finance}")
        self.log(f"Collection time: {elapsed_time:.1f} seconds")
        self.statusBar().showMessage(
            f"Military: {len(military)} ({today_military} today) | "
            f"Finance: {len(finance)} ({today_finance} today) | "
            f"Time: {elapsed_time:.1f}s | "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )

        saved = self.app.report_gen.save_report(data)
        if "html" in saved:
            self.log(f"Report saved: {saved['html']}")

    def _show_error(self, title: str, message: str):
        """显示错误"""
        self.log(f"Error: {message}")
        QMessageBox.critical(self, title, message)

    def _on_settings_saved(self):
        """设置保存后的回调"""
        self.log("=" * 40)
        self.log("Settings saved!")
        self.log(f"AI Provider changed to: {self.config.AI_PROVIDER}")
        self.log(f"Network settings updated: Timeout {self.config.REQUEST_TIMEOUT}s, Retry {self.config.RETRY_COUNT}x")
        self.log(f"Date filter mode: {self.config.DATE_FILTER_MODE}")
        self.log("=" * 40)

        try:
            from agent.ai_provider import create_provider
            self.app.ai_provider = create_provider(self.config.AI_PROVIDER, self.config)
            self.app.agent.ai = self.app.ai_provider
            # 更新网络配置
            self.app.agent.searcher.timeout = self.config.REQUEST_TIMEOUT
            self.app.agent.searcher.retry_count = self.config.RETRY_COUNT
            self.app.agent.searcher.retry_delay = self.config.RETRY_DELAY
            self.app.agent.searcher.date_filter_mode = self.config.DATE_FILTER_MODE
            self.log(f"AI Provider initialized: {self.config.AI_PROVIDER}")
        except Exception as e:
            self.log(f"AI Provider init failed: {e}")

    def on_sort_changed(self, text: str):
        """排序方式改变"""
        sort_map = {
            "默认": -1,
            "来源": 1,
            "地区": 2,
            "时间": 3,
            "重要性": 4,
            "优先级": 5
        }
        col = sort_map.get(text, -1)
        if col >= 0:
            self.military_table.sortItems(col, Qt.SortOrder.AscendingOrder)
            self.finance_table.sortItems(col, Qt.SortOrder.AscendingOrder)
