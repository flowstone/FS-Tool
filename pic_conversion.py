import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QCheckBox, QFileDialog, QHBoxLayout,QDesktopWidget
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class PicConversionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("图片格式转换应用")
        self.setWindowIcon(QIcon(self.get_resource_path("resources/app.ico")))

        # 获取屏幕尺寸
        desktop = QDesktopWidget().availableGeometry()
        screen_width = desktop.width()
        screen_height = desktop.height()
        # 设置主应用窗口大小
        window_width = 500
        window_height = 400
        print(screen_width)
        # 计算窗口在屏幕中心的位置
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2

        self.setGeometry( x_pos, y_pos, window_width, window_height)
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
                width: 100px;  /* 设置按钮宽度 */
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QCheckBox {
                spacing: 10px;
            }
            QLabel {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

        # 用于存储上传的图片路径
        self.image_path = None
        self.preview_image = None

        layout = QVBoxLayout()

        # 创建上传图片按钮
        self.upload_button = QPushButton("上传图片")
        self.upload_button.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)
        # 创建用于显示上传图片的标签
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # 创建复选框框架（这里使用水平布局让复选框在一行显示）
        self.checkbox_frame = QWidget(self)
        checkbox_layout = QHBoxLayout()
        self.checkbox_frame.setLayout(checkbox_layout)

        # 定义支持的目标格式
        self.target_formats = ["JPEG", "PNG", "GIF", "BMP", "WEBP", "ICO"]
        self.selected_formats = []

        # 创建复选框并添加到水平布局中
        for format in self.target_formats:
            checkbox = QCheckBox(format)
            checkbox.stateChanged.connect(lambda state, f=format: self.toggle_format(f, state))
            checkbox_layout.addWidget(checkbox)

        layout.addWidget(self.checkbox_frame)

        # 创建按钮所在的水平布局（用于放置转换按钮和关闭按钮）
        button_layout = QHBoxLayout()

        # 创建转换按钮
        self.convert_button = QPushButton("转换")
        self.convert_button.clicked.connect(self.convert_image)
        self.convert_button.setEnabled(False)
        button_layout.addWidget(self.convert_button)

        # 创建关闭按钮
        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)


    def get_resource_path(self, relative_path):
        """
        获取资源（如图片等）的实际路径，处理打包后资源路径的问题
        """
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


    def upload_image(self):
        self.image_path = QFileDialog.getOpenFileName(self, "选择图片", "", "图片文件 (*.jpg *.png *.gif *.bmp *.webp *.ico)")[0]
        if self.image_path:
            print(f"已上传图片: {self.image_path}")
            try:
                self.preview_image = Image.open(self.image_path)
                pixmap = QPixmap(self.image_path)
                self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(), aspectRatioMode=1))
            except Exception as e:
                print(f"显示图片时出错: {e}")

    def toggle_format(self, format, state):
        if state == 2:  # 表示选中状态（PyQt中选中为2，未选中为0）
            self.selected_formats.append(format)
        else:
            self.selected_formats.remove(format) if format in self.selected_formats else None

        # 根据是否有复选框被选中来更新转换按钮的状态
        if len(self.selected_formats) > 0:
            self.convert_button.setEnabled(True)
        else:
            self.convert_button.setEnabled(False)

    def convert_image(self):
        if not self.image_path:
            print("请先上传图片!")
            return

        try:
            image = Image.open(self.image_path)

            for target_format in self.selected_formats:
                base_name, ext = os.path.splitext(self.image_path)
                new_image_path = f"{base_name}.{target_format.lower()}"
                if target_format == "JPEG":
                    image = image.convert('RGB')
                elif target_format == "ICO":
                    image = image.convert('RGB') if image.mode!= 'RGB' else image
                    image.save(new_image_path, format='ICO')
                    continue
                elif target_format == "WEBP":
                    image = image.convert('RGB') if image.mode!= 'RGB' else image
                image.save(new_image_path)

            print(f"图片已成功转换为所选格式，保存路径分别为: {[f'{base_name}.{f.lower()}' for f in self.selected_formats]}")
        except Exception as e:
            print(f"转换图片时出错: {e}")

