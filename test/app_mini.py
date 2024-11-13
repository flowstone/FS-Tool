import sys
import time
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout,QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter


class TransparentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口无边框、无标题栏，并始终保持在最顶层
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 设置窗口透明度为半透明（这里透明度值为0.8，可根据需求调整）
        self.setWindowOpacity(0.8)

        # 设置窗口的初始位置和大小
        self.setGeometry(100, 100, 200, 100)

        layout = QVBoxLayout()

        label = QLabel("这是一个透明的应用示例", self)
        label.setFont(QFont('Arial', 16))
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self.windowOpacity())
        painter.setBrush(Qt.transparent)
        painter.drawRect(self.rect())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TransparentApp()
    window.show()
    sys.exit(app.exec_())