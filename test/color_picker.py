import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QApplication
from PyQt5.QtGui import QColor, QPixmap, QPainter, QMouseEvent, QImage, QIcon
from PyQt5.QtCore import Qt
from common_util import CommonUtil
from fs_constants import FsConstants

class ImageColorPicker(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.selected_color = QColor(0, 0, 0)  # 初始颜色为黑色
        self.pixmap = None  # 用于存储加载的图片
        self.load_image()  # 直接加载指定图片

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setWindowTitle("颜色选择器")
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        # 图片显示区域
        self.image_display = QLabel(self)
        self.image_display.setFixedSize(240, 250)
        self.image_display.mousePressEvent = self.pick_color  # 绑定鼠标点击事件
        main_layout.addWidget(self.image_display, alignment=Qt.AlignCenter)

        # 滑块布局
        slider_layout = QHBoxLayout()

        # 红色滑块
        self.red_slider = QSlider(Qt.Horizontal, self)
        self.red_slider.setMinimum(0)
        self.red_slider.setMaximum(255)
        self.red_slider.setValue(0)
        self.red_slider.valueChanged.connect(self.update_color)
        slider_layout.addWidget(self.red_slider)

        # 绿色滑块
        self.green_slider = QSlider(Qt.Horizontal, self)
        self.green_slider.setMinimum(0)
        self.green_slider.setMaximum(255)
        self.green_slider.setValue(0)
        self.green_slider.valueChanged.connect(self.update_color)
        slider_layout.addWidget(self.green_slider)

        # 蓝色滑块
        self.blue_slider = QSlider(Qt.Horizontal, self)
        self.blue_slider.setMinimum(0)
        self.blue_slider.setMaximum(255)
        self.blue_slider.setValue(0)
        self.blue_slider.valueChanged.connect(self.update_color)
        slider_layout.addWidget(self.blue_slider)

        main_layout.addLayout(slider_layout)

        # RGB值显示标签
        self.rgb_label = QLabel(self)
        self.rgb_label.setText("RGB: (0, 0, 0)")
        main_layout.addWidget(self.rgb_label, alignment=Qt.AlignCenter)

        # 十六进制颜色值显示标签
        self.hex_label = QLabel(self)
        self.hex_label.setText("Hex: #000000")
        main_layout.addWidget(self.hex_label, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def load_image(self):
        """
        加载指定的图片
        """
        self.pixmap = QPixmap(CommonUtil.get_resource_path(FsConstants.BASE_COLOR_MAP))
        if not self.pixmap.isNull():
            self.image_display.setPixmap(self.pixmap)

    def pick_color(self, event: QMouseEvent):
        """
        通过鼠标点击图片获取颜色
        """
        if event.button() == Qt.LeftButton and self.pixmap:
            x = event.pos().x()
            y = event.pos().y()
            image = self.pixmap.toImage()
            if 0 <= x < image.width() and 0 <= y < image.height():
                color = QColor(image.pixel(x, y))
                self.set_selected_color(color)

    def set_selected_color(self, color: QColor):
        """
        设置选中的颜色，并更新界面显示
        """
        self.selected_color = color
        self.update_color()

    def update_color(self):
        """
        根据滑块值或选中的颜色更新界面显示的颜色、RGB值和十六进制值
        """
        if self.sender() in (self.red_slider, self.green_slider, self.blue_slider):
            red = self.red_slider.value()
            green = self.green_slider.value()
            blue = self.blue_slider.value()
            self.selected_color.setRgb(red, green, blue)
        color = self.selected_color
        self.rgb_label.setText(f"RGB: ({color.red()}, {color.green()}, {color.blue()})")
        hex_code = color.name().upper()
        self.hex_label.setText(f"Hex: #{hex_code}")
        if self.pixmap:
            painter = QPainter(self.pixmap)
            painter.setPen(color)
            painter.setBrush(color)
            painter.drawRect(0, 0, 25, 25)
            painter.end()
            self.image_display.setPixmap(self.pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageColorPicker()
    window.show()
    sys.exit(app.exec_())