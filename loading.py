import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
import time


class LoadingApp:
    def __init__(self):
        super().__init__()


    # 打开Loading
    def open_loading(self):
        self.setEnabled(False)

        # 创建新窗口
        self.loading_widget = QWidget()
        self.loading_widget.setGeometry(self.geometry())
        self.loading_widget.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.loading_widget.setAttribute(Qt.WA_TranslucentBackground)

        # 为新窗口设置布局（这里使用简单的垂直布局示例）
        loading_layout = QVBoxLayout()

        # 在新窗口布局中添加一个标签作为示例内容，你可以添加更多组件
        label = QLabel('这是弹出的新窗口')
        movie = QMovie('./resources/loading.gif')
        movie.start()
        label.setMovie(movie)


        loading_layout.addWidget(label, 0, Qt.AlignCenter)

        self.loading_widget.setLayout(loading_layout)
        # 根据布局内的部件大小调整新窗口大小，使其自适应
        self.loading_widget.layout().activate()
        self.loading_widget.adjustSize()
        # 显示新窗口
        self.loading_widget.show()


    # 关闭Loading
    def close_loading(self):
        # 操作完成后，移除遮罩层并恢复窗口交互
        self.loading_widget.hide()
        self.setEnabled(True)
        self.loading_widget.deleteLater()