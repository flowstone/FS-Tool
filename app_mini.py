import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QCursor, QMouseEvent, QPixmap
from PyQt5.QtCore import Qt, QPoint

class FloatingBall(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setGeometry(0, 0, 80, 80)  # 设置悬浮球大小
        self.setWindowOpacity(0.8)  # 设置透明度
        # 这里使用一个示例图片路径，你可以替换为真实路径
        pixmap = QPixmap('resources/pic_conversion.png')
        pixmap = pixmap.scaled(self.size())
        layout = QVBoxLayout()
        self.background_label = QLabel(self)
        self.background_label.setPixmap(pixmap)
        self.background_label.resize(self.size())
        layout.addWidget(self.background_label)
        self.setLayout(layout)
        self.move_to_top_right()


        self.dragPosition = None
        self.setMouseTracking(True)

    def setup_background_image(self):
        # 这里使用一个示例图片路径，你可以替换为真实路径
        pixmap = QPixmap('resources/pic_conversion.png')
        pixmap = pixmap.scaled(self.size())
        self.background_label = QLabel(self)
        self.background_label.setPixmap(pixmap)
        self.background_label.resize(self.size())
        self.setLayout(self.background_label)

    def move_to_top_right(self):
        print("执行了移动操作")
        screen_geo = QApplication.desktop().screenGeometry()
        x = screen_geo.width() - self.width() - 10
        y = 10
        self.move(x, y)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self.dragPosition:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def show_main_window(self):
        from main_window import MainWindow
        main_window = MainWindow()
        main_window.show()
        self.close()

    # 鼠标双击，打开主界面
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.show_main_window()

