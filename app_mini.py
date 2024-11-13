import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, pyqtProperty, QParallelAnimationGroup,QTimer, QEasingCurve
from PyQt5.QtGui import QIcon, QCursor, QMouseEvent, QPixmap, QColor, QBrush, QPainter, QLinearGradient,QTransform
from PyQt5 import QtCore
import os


class FloatingBall(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()



    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setGeometry(0, 0, 90, 90)  # 设置悬浮球大小
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置窗口背景透明

        self.setWindowOpacity(0.8)  # 设置透明度

        self.setup_background_image()
        self.move_to_top_right()

        self.dragPosition = None
        self.setMouseTracking(True)

        # 连接鼠标进入和离开事件，用于触发特效
        #self.enterEvent = self.on_enter_event
        #self.leaveEvent = self.on_leave_event


        # 启动呼吸灯效果（透明度周期性变化）
        self.breathing_light_window()

    def breathing_light_window(self):
        # 初始透明度
        self.opacity = 0.2
        # 透明度每次变化的值，控制呼吸的速度和节奏
        self.direction = 0.02
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_opacity)
        # 设置定时器间隔为50毫秒，可根据需要调整呼吸节奏快慢
        self.timer.start(50)

    # 更新透明度
    def update_opacity(self):
        self.opacity += self.direction
        if self.opacity >= 1.0:
            self.direction = -0.02  # 达到最大透明度后开始减小透明度
        elif self.opacity <= 0.2:
            self.direction = 0.02  # 达到最小透明度后开始增大透明度
        self.setWindowOpacity(self.opacity)


    def setup_background_image(self):
        layout = QVBoxLayout()


        # 这里使用一个示例图片路径，你可以替换为真实路径
        pixmap = QPixmap("resources/pic_conversion.png")
        pixmap = pixmap.scaled(self.size())
        self.background_label = QLabel(self)
        self.background_label.setPixmap(pixmap)
        self.background_label.resize(self.size())
        layout.addWidget(self.background_label)
        self.setLayout(layout)


    def move_to_top_right(self):
        print("悬浮球初始化位置")
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
        print("鼠标移动到悬浮球")
        self.is_hovered = True
        self.start_hover_effect()

    def on_leave_event(self, event):
        print("鼠标离开了悬浮球")
        self.is_hovered = False
        self.start_leave_effect()

    def start_hover_effect(self):
        self.animate_rotation(360, 1000)  # 鼠标悬停时旋转360度，持续1000毫秒

    def start_leave_effect(self):
        self.stop_rotation()  # 鼠标离开时停止旋转

    def on_mouse_press_event(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            self.start_click_effect()  # 点击时启动点击特效
            event.accept()

    def start_click_effect(self):
        self.animate_size(100, 0.9, duration=100, easing=QEasingCurve.OutElastic)  # 点击时放大并改变透明度，添加弹性效果
        QTimer.singleShot(100, self.reset_size)  # 100毫秒后还原大小和透明度

    def reset_size(self):
        self.animate_size(self.original_size, self.original_opacity, duration=200)

    def animate_size(self, target_size, target_opacity, duration=200, easing=QEasingCurve.Linear):
        size_animation = QPropertyAnimation(self, b'size')
        size_animation.setDuration(duration)
        size_animation.setStartValue(self.size())
        size_animation.setEndValue(QtCore.QSize(target_size, target_size))
        size_animation.setEasingCurve(easing)

        opacity_animation = QPropertyAnimation(self, b'opacity')
        opacity_animation.setDuration(duration)
        opacity_animation.setStartValue(self.windowOpacity())
        opacity_animation.setEndValue(target_opacity)
        opacity_animation.setEasingCurve(easing)

        group_animation = QParallelAnimationGroup()
        group_animation.addAnimation(size_animation)
        group_animation.addAnimation(opacity_animation)

        group_animation.start()

    def animate_rotation(self, angle, duration):
        print("开始进入旋转动画")
        self.rotation_animation = QPropertyAnimation(self, b'rotation_angle')
        self.rotation_animation.setDuration(duration)
        self.rotation_animation.setStartValue(0)
        self.rotation_animation.setEndValue(angle)
        self.rotation_animation.setEasingCurve(QEasingCurve.Linear)
        self.rotation_animation.valueChanged.connect(self.update_rotation)
        self.rotation_animation.start()

    def stop_rotation(self):
        print("开始停止旋转动画")
        if hasattr(self, 'rotation_animation'):
            self.rotation_animation.stop()

    def update_rotation(self, value):
        transform = QTransform()
        transform.rotate(value)
        self.setTransform(transform)

    def start_breathing_effect(self):
        self.breathing_timer = QTimer(self)
        self.breathing_timer.timeout.connect(self.toggle_opacity)
        self.breathing_timer.start(500)  # 每500毫秒切换一次透明度

    def toggle_opacity(self):
        current_opacity = self.windowOpacity()
        target_opacity = self.original_opacity + 0.1 if current_opacity <= self.original_opacity else self.original_opacity - 0.1
        self.setWindowOpacity(target_opacity)

