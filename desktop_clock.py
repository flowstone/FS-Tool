import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer


class DesktopClockApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口无边框、无标题栏
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 设置窗口透明度
        self.setWindowOpacity(0.8)

        # 设置窗口背景透明，这里采用的方式是将背景色设置为透明色，需要配合样式表实现
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0, 0))
        self.setPalette(palette)

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
        self.setLayout(layout)

        self.update_time()

    def update_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.label_time.setText(current_time)
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)


