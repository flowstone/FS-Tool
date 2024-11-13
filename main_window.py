import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from desktop_clock import DesktopClockApp
from pic_conversion import PicConversionApp
from batch_file_renamer import RenameFileApp
from batch_create_folder import CreateFolderApp

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PyQt示例应用")
        self.setGeometry(100, 100, 300, 250)
        self.setStyleSheet("background-color: #F5F5F5;")  # 设置窗口背景色为淡灰色

        layout = QVBoxLayout()

        # 透明时间
        time_btn = QPushButton("透明时间")
        time_btn.setFont(QFont('Arial', 14))  # 设置字体
        time_btn.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #007B9A;
            }
        """)
        time_btn.clicked.connect(self.time_btn_clicked)
        layout.addWidget(time_btn)

        # 图转大师
        img_conv_btn = QPushButton("图转大师")
        img_conv_btn.setFont(QFont('Arial', 14))
        img_conv_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        img_conv_btn.clicked.connect(self.img_conv_btn_clicked)
        layout.addWidget(img_conv_btn)

        # 文件夹创建师
        create_folder_btn = QPushButton("文件夹创建师")
        create_folder_btn.setFont(QFont('Arial', 14))
        create_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        create_folder_btn.clicked.connect(self.create_folder_btn_clicked)
        layout.addWidget(create_folder_btn)

        # 重命名使者
        rename_file_btn = QPushButton("重命名使者")
        rename_file_btn.setFont(QFont('Arial', 14))
        rename_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #8E24AA;
            }
        """)
        rename_file_btn.clicked.connect(self.rename_file_btn_clicked)
        layout.addWidget(rename_file_btn)

        self.setLayout(layout)

    def time_btn_clicked(self):
        print("按钮<透明时间>被点击了")
        self.desktop_clock = DesktopClockApp()
        self.desktop_clock.show()

    def img_conv_btn_clicked(self):
        print("按钮<图转大师>被点击了")
        self.pic_conversion=PicConversionApp()
        self.pic_conversion.show()

    def create_folder_btn_clicked(self):
        print("按钮<文件夹创建师>被点击了")
        self.rename_file = RenameFileApp()
        self.rename_file.show()

    def rename_file_btn_clicked(self):
        print("按钮<重命名使者>被点击了")
        self.create_folder = CreateFolderApp()
        self.create_folder.show()

