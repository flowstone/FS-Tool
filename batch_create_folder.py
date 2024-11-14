import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMenuBar, QFileDialog
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from loguru import logger
from path_util import PathUtil

class CreateFolderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info("---- 初始化创建文件夹并移动文件 ----")
        self.setWindowTitle("批量移动文件")

        # 设置窗口背景色为淡灰色
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#F5F5F5"))
        self.setPalette(palette)

        self.setWindowIcon(QIcon(PathUtil.get_resource_path("resources/app.ico")))

        layout = QVBoxLayout()



        # 说明文本
        description_label = QLabel("说明：根据输入的分割字符，取前部分创建文件夹，符合相关的文件都移动到对应文件夹中")
        description_label.setFont(QFont("楷体", 10))
        description_label.setStyleSheet("color: white;")

        # 选择文件夹相关部件
        folder_path_layout = QHBoxLayout()
        folder_path_label = QLabel("选择文件夹：")
        folder_path_label.setStyleSheet("color: #333; font-size: 14px;")
        self.folder_path_entry = QLineEdit()
        self.folder_path_entry.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 2px 5px;
            }
        """)
        browse_button = QPushButton("浏览")
        browse_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 3px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        browse_button.clicked.connect(self.browse_folder)

        folder_path_layout.addWidget(folder_path_label)
        folder_path_layout.addWidget(self.folder_path_entry)
        folder_path_layout.addWidget(browse_button)

        # 指定分割字符相关部件
        slice_layout = QHBoxLayout()
        slice_label = QLabel("指定分割字符：")
        slice_label.setStyleSheet("color: #333; font-size: 14px;")
        self.slice_entry = QLineEdit()
        self.slice_entry.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 2px 5px;
            }
        """)

        slice_layout.addWidget(slice_label)
        slice_layout.addWidget(self.slice_entry)

        # 作者和Github信息文本
        author_font = QFont("楷体", 11)
        author_label = QLabel("Author：xueyao.me@gmail.com")
        author_label.setFont(author_font)
        author_label.setStyleSheet("color: #007BFF;")
        github_label = QLabel("Github：https://github.com/flowstone/Tooool")
        github_label.setFont(author_font)
        github_label.setStyleSheet("color: #007BFF;")

        info_layout = QVBoxLayout()
        info_layout.addWidget(author_label)
        info_layout.addWidget(github_label)

        # 操作按钮
        button_layout = QHBoxLayout()
        start_button = QPushButton("开始")
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;
                color: white;
                border-radius: 3px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #007B9A;
            }
        """)
        start_button.clicked.connect(self.start_operation)
        exit_button = QPushButton("退出")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border-radius: 3px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        exit_button.clicked.connect(self.close)

        button_layout.addWidget(start_button)
        button_layout.addWidget(exit_button)

        layout.addWidget(description_label)
        layout.addLayout(folder_path_layout)
        layout.addLayout(slice_layout)
        layout.addLayout(info_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)




    def browse_folder(self):
        logger.info("---- 开始选择文件夹 ----")
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.folder_path_entry.setText(folder_path)



    def start_operation(self):
        logger.info("---- 开始执行操作 ----")
        folder_path = self.folder_path_entry.text()
        slice_char = self.slice_entry.text()

        if folder_path:
            self.create_folder_move_files(folder_path, slice_char)
            QMessageBox.information(self, "提示", "移动文件完成！")
        else:
            QMessageBox.warning(self, "警告", "请选择要操作的文件夹！")

    # 创建文件夹，并移动到指定目录下
    @staticmethod
    def create_folder_move_files(self, folder_path, slice_char):

        # 遍历文件夹下的文件名
        for filename in os.listdir(folder_path):
            source_path = os.path.join(folder_path, filename)
            # 判断是否是文件
            if os.path.isfile(source_path):
                # 找到分割的位置，如'-'
                index = filename.find(slice_char)
                if index!= -1:
                    # 提取 '-' 前面的部分作为文件夹名
                    folder_name = filename[:index]
                    # 如果文件夹不存在，则创建
                    target_folder = os.path.join(folder_path, folder_name)
                    if not os.path.exists(target_folder):
                        os.mkdir(target_folder)
                    # 将文件移动到对应的文件夹
                    destination_path = os.path.join(target_folder, filename)
                    shutil.move(source_path, destination_path)


