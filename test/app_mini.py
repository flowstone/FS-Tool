import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, pyqtProperty, QParallelAnimationGroup
from PyQt5.QtGui import QIcon, QCursor, QMouseEvent, QPixmap, QColor, QBrush, QPainter, QLinearGradient
from PyQt5 import QtCore

class FloatingBall(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.original_size = 80  # 记录原始大小，用于特效还原
        self.original_opacity = 0.8  # 记录原始透明度，用于特效还原
        self.is_hovered = False  # 标记是否鼠标悬停

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setGeometry(0, 0, self.original_size, self.original_size)  # 设置悬浮球大小
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置窗口背景透明
        self.setWindowOpacity(self.original_opacity)  # 设置透明度

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


        # 连接鼠标进入和离开事件，用于触发特效
        #self.enterEvent = self.on_enter_event
        #self.leaveEvent = self.on_leave_event



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

    def on_enter_event(self, event):
        self.is_hovered = True
        self.start_hover_effect()

    def on_leave_event(self, event):
        self.is_hovered = False
        self.start_leave_effect()

    def start_hover_effect(self):
        self.animate_size(100, 0.9)  # 鼠标悬停时放大到100x100大小，透明度变为0.9

    def start_leave_effect(self):
        self.animate_size(self.original_size, self.original_opacity)  # 鼠标离开时还原大小和透明度

    def animate_size(self, target_size, target_opacity, duration=200):
        size_animation = QPropertyAnimation(self, b'size')
        size_animation.setDuration(duration)
        size_animation.setStartValue(self.size())
        size_animation.setEndValue(QtCore.QSize(target_size, target_size))

        opacity_animation = QPropertyAnimation(self, b'opacity')
        opacity_animation.setDuration(duration)
        opacity_animation.setStartValue(self.windowOpacity())
        opacity_animation.setEndValue(target_opacity)

        group_animation = QParallelAnimationGroup()
        group_animation.addAnimation(size_animation)
        group_animation.addAnimation(opacity_animation)

        group_animation.finished.connect(self.on_animation_finished)
        group_animation.start()

    def on_animation_finished(self):
        if not self.is_hovered:
            self.setGeometry(0, 0, self.original_size, self.original_size)
            self.setWindowOpacity(self.original_opacity)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(255, 255, 255, 100))
        gradient.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(gradient))
        painter.drawRect(self.rect())

