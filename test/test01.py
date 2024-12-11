import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsOpacityEffect, QVBoxLayout, QGridLayout, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve


class AppIconWidget(QWidget):
    # 定义一个信号，当图标被点击时发出
    iconClicked = pyqtSignal(str)  # 传递图标名称

    def __init__(self, icon_path, name, parent=None):
        super().__init__(parent)

        # 保存名称和图标路径
        self.icon_path = icon_path
        self.name = name

        # 创建布局
        layout = QVBoxLayout()
        layout.setSpacing(0)  # 去掉图标和名称之间的间距

        # 创建第一个 QLabel 用于显示图标
        self.icon_label = QLabel(self)
        pixmap = QPixmap(icon_path)  # 加载图片

        # 设置固定大小，确保图片自适应显示
        self.icon_label.setFixedSize(80, 80)  # 设置固定的图标显示大小
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignCenter)  # 图标居中显示
        self.icon_label.setScaledContents(True)  # 让图片按QLabel大小缩放

        # 创建第二个 QLabel 用于显示名称
        self.name_label = QLabel(name, self)
        self.name_label.setAlignment(Qt.AlignCenter)  # 名称居中显示
        self.name_label.setStyleSheet("font-size: 14px; color: #333;")  # 设置字体大小和颜色
        self.name_label.setMargin(0)  # 去除内边距，确保文字紧贴图标

        # 设置名称标签最大宽度为图片宽度
        self.name_label.setMaximumWidth(80)  # 设置最大宽度与图片一致

        # 将两个 QLabel 添加到布局中
        layout.addWidget(self.icon_label)
        layout.addWidget(self.name_label)

        # 设置布局
        self.setLayout(layout)

        # 设置鼠标样式
        self.setCursor(Qt.PointingHandCursor)  # 设置鼠标样式为手指图标

        # 设置固定大小
        self.setFixedSize(90, 120)  # 设置整个小部件的固定大小（宽度与图标相同，高度适合图标和名称）


        # 设置透明度效果
        self.opacity_effect = QGraphicsOpacityEffect(self.icon_label)
        self.icon_label.setGraphicsEffect(self.opacity_effect)

        # 创建透明度动画
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(200)
        self.opacity_animation.setStartValue(1.0)  # 初始不透明
        self.opacity_animation.setEndValue(0.5)  # 点击时变暗，透明度设置为0.5
        self.opacity_animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.is_animating = False  # 动画状态标志

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        # 当图标被点击时，发出信号
        self.iconClicked.emit(self.name)
        # 执行动画效果
        self.is_animating = True  # 设置动画状态为进行中
        # 执行透明度动画（变暗）
        self.opacity_animation.setDirection(QPropertyAnimation.Forward)  # 正向动画，变暗
        self.opacity_animation.start()


        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""

        # 执行恢复的透明度动画（恢复亮度）
        self.opacity_animation.setDirection(QPropertyAnimation.Backward)  # 反向动画，恢复亮度
        self.opacity_animation.start()

        self.opacity_animation.finished.connect(self.on_animation_finished)

        super().mouseReleaseEvent(event)

    def on_animation_finished(self):
        """动画完成后的处理"""
        self.is_animating = False  # 动画结束，允许新的点击

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("APP 图标模拟")
        #self.setFixedSize(430, 430)  # 设置窗口大小

        # 创建 APP 图标和名称
        app_icon1 = AppIconWidget("../resources/icon/home-icon.svg", "应用1")
        app_icon2 = AppIconWidget("../resources/icon/home-icon.svg", "应用2")
        app_icon3 = AppIconWidget("../resources/icon/home-icon.svg", "应用3")
        app_icon4 = AppIconWidget("../resources/icon/home-icon.svg", "应用4")
        app_icon5 = AppIconWidget("../resources/icon/home-icon.svg", "应用5")
        app_icon6 = AppIconWidget("../resources/icon/home-icon.svg", "应用6")
        app_icon7 = AppIconWidget("../resources/icon/home-icon.svg", "应用7")
        app_icon8 = AppIconWidget("../resources/icon/home-icon.svg", "应用8")

        # 连接信号
        app_icon1.iconClicked.connect(self.on_icon_clicked)
        app_icon2.iconClicked.connect(self.on_icon_clicked2)
        app_icon3.iconClicked.connect(self.on_icon_clicked2)
        app_icon4.iconClicked.connect(self.on_icon_clicked2)
        app_icon5.iconClicked.connect(self.on_icon_clicked2)
        app_icon6.iconClicked.connect(self.on_icon_clicked2)
        app_icon7.iconClicked.connect(self.on_icon_clicked2)
        app_icon8.iconClicked.connect(self.on_icon_clicked2)

        # 创建主布局
        main_layout = QGridLayout()
        main_layout.setSpacing(0)  # 去除格子之间的间隙

        # 将每个图标放入网格布局
        main_layout.addWidget(app_icon1, 0, 0)  # 第一行第一列
        main_layout.addWidget(app_icon2, 0, 1)  # 第一行第二列
        main_layout.addWidget(app_icon3, 0, 2)  # 第一行第三列
        main_layout.addWidget(app_icon4, 0, 3)  # 第一行第四列
        main_layout.addWidget(app_icon5, 1, 0)  # 第二行第一列
        main_layout.addWidget(app_icon6, 1, 1)  # 第二行第二列
        main_layout.addWidget(app_icon7, 1, 2)  # 第二行第三列
        main_layout.addWidget(app_icon8, 1, 3)  # 第二行第四列

        central_widget = QWidget(self)
        central_widget.setContentsMargins(0, 0, 0, 0)  # 去除整个布局的边缘间隙

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def on_icon_clicked(self):
        """图标点击事件的槽方法"""
        print(f"点击了 1 图标")
        # 在这里处理点击事件，执行相应的操作，例如打开新窗口等

    def on_icon_clicked2(self, name):
        """图标点击事件的槽方法"""
        print(f"点击了 2 图标")
        # 在这里处理点击事件，执行相应的操作，例如打开新窗口等

    # def paintEvent(self, event):
    #     """重载paintEvent，绘制自适应背景图片"""
    #     painter = QPainter(self)
    #     pixmap = QPixmap("../resources/bg.jpg")  # 加载背景图片
    #     painter.drawPixmap(self.rect(), pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding))  # 让背景图片自适应窗口大小
    #
    #     super().paintEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
