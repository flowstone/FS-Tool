import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton,QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
import time


class LoadingMaskExample(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setFixedSize(500,600)
        # 创建按钮
        self.button = QPushButton('点击触发加载')
        self.button.clicked.connect(self.show_loading_mask)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.setWindowTitle('点击按钮触发遮罩示例')
        self.show()

    def show_loading_mask(self):
        print("----------------")
        # 创建遮罩层窗口（QWidget），设置为半透明且覆盖整个父窗口
        self.mask_widget = QWidget()
        self.mask_widget.setGeometry(self.geometry())
        self.mask_widget.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.mask_widget.setAttribute(Qt.WA_TranslucentBackground)

        # 创建布局用于放置加载动画的QLabel
        mask_layout = QVBoxLayout()

        # 创建QLabel用于显示加载动画
        self.loading_label = QLabel(self.mask_widget)
        movie = QMovie('loading.gif')
        movie.start()
        self.loading_label.setMovie(movie)

        # 将QLabel添加到布局中，并使其在中间显示
        mask_layout.addWidget(self.loading_label, 0, Qt.AlignCenter)
        self.mask_widget.setLayout(mask_layout)

        # 禁用整个窗口的交互（除了遮罩层本身关闭等相关操作）
        #self.setEnabled(False)

        # 显示遮罩层
        self.mask_widget.show()

        # 模拟耗时操作，实际应用中可替换为真实的耗时任务，比如网络请求、文件读取等
        time.sleep(3)

        # 操作完成后，移除遮罩层并恢复窗口交互
        #self.mask_widget.hide()
        #self.setEnabled(True)
        #self.mask_widget.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoadingMaskExample()
    sys.exit(app.exec_())