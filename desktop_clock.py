import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt, QTimer
from loguru import logger
from path_util import PathUtil

class DesktopClockApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        logger.info("---- 初始化透明时间 ----")
        # 设置窗口无边框、无标题栏
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置窗口背景透明
        self.setWindowTitle("透明时间")

        # 设置窗口透明度
        self.setWindowOpacity(0.8)
        self.setWindowIcon(QIcon(PathUtil.get_resource_path("resources/app.ico")))


        self.setGeometry(0, 0, 200, 80)  # 设置窗口初始位置和大小，这里定位在桌面左上角并设置合适尺寸
        self.setStyleSheet("""
                    QWidget {
                        background-color: rgba(240, 240, 240, 0);
                    }
                    QLabel {
                        font-family: Arial;
                        font-size: 24px;
                        color: white;
                    }
                """)

        layout = QVBoxLayout()
        self.label_time = QLabel(self)
        self.label_time.setFont(QFont('Arial', 24))
        self.label_time.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_time)

        # 创建定时器，设置时间间隔为1000毫秒（即1秒）
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.setLayout(layout)

    def update_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.label_time.setText(current_time)


