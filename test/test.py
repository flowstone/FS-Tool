import os
import shutil
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox,QVBoxLayout, QHBoxLayout


class CreateFolderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("批量移动文件")
        self.setGeometry(100, 100, 450, 350)  # 设置窗口初始大小和位置
        self.setStyleSheet("background-color: #F5F5F5;")  # 设置窗口背景色

        # 整体垂直布局
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)  # 让内部部件顶部对齐

        # 标题样式设置
        title_font = QFont("黑体", 14)
        title_font.setBold(True)
        title_label = QLabel("批量移动文件工具", self)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # 说明文本
        info_font = QFont("楷体", 10)
        info_label = QLabel("说明：根据输入的分割字符，取前部分创建文件夹，符合相关的文件都移动到对应文件夹中", self)
        info_label.setFont(info_font)
        info_label.setStyleSheet("color: gray;")
        layout.addWidget(info_label)

        # 选择文件夹相关部件
        folder_path_group = QWidget(self)  # 使用一个容器部件方便布局管理
        folder_path_layout = QHBoxLayout()
        folder_path_group.setLayout(folder_path_layout)

        folder_path_label = QLabel("选择文件夹：", self)
        folder_path_label.setFont(info_font)
        folder_path_layout.addWidget(folder_path_label)

        self.folder_path_entry = QLineEdit(self)
        self.folder_path_entry.setFixedWidth(250)
        self.folder_path_entry.setFont(info_font)
        folder_path_layout.addWidget(self.folder_path_entry)

        browse_button = QPushButton("浏览", self)
        browse_button.setFont(info_font)
        browse_button.setFixedSize(80, 25)
        browse_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        browse_button.clicked.connect(self.browse_folder)
        folder_path_layout.addWidget(browse_button)

        layout.addWidget(folder_path_group)

        # 分割字符输入部件
        slice_group = QWidget(self)  # 同样使用容器部件
        slice_layout = QHBoxLayout()
        slice_group.setLayout(slice_layout)

        slice_label = QLabel("指定分割字符：", self)
        slice_label.setFont(info_font)
        slice_layout.addWidget(slice_label)

        self.slice_entry = QLineEdit(self)
        self.slice_entry.setFixedWidth(250)
        self.slice_entry.setFont(info_font)
        slice_layout.addWidget(self.slice_entry)

        layout.addWidget(slice_group)

        # 作者和Github信息文本
        author_font = QFont("楷体", 10)
        author_label = QLabel("Author：xueyao.me@gmail.com", self)
        author_label.setFont(author_font)
        author_label.setStyleSheet("color: blue;")
        layout.addWidget(author_label)

        github_label = QLabel("Github：https://github.com/flowstone/Tooool", self)
        github_label.setFont(author_font)
        github_label.setStyleSheet("color: blue;")
        layout.addWidget(github_label)

        # 操作按钮
        button_group = QWidget(self)
        button_layout = QHBoxLayout()
        button_group.setLayout(button_layout)

        start_button = QPushButton("开始", self)
        start_button.setFont(info_font)
        start_button.setFixedSize(80, 25)
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #03A9F4;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0288D1;
            }
        """)
        start_button.clicked.connect(self.start_operation)
        button_layout.addWidget(start_button)

        exit_button = QPushButton("退出", self)
        exit_button.setFont(info_font)
        exit_button.setFixedSize(80, 25)
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        layout.addWidget(button_group)

        self.setLayout(layout)

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.folder_path_entry.setText(folder_path)

    def start_operation(self):
        folder_path = self.folder_path_entry.text()
        slice_char = self.slice_entry.text()
        if folder_path:
            self.create_folder_move_files(folder_path, slice_char)
            QMessageBox.information(self, "提示", "移动文件完成！")
        else:
            QMessageBox.warning(self, "警告", "请选择要操作的文件夹！")

    # 创建文件夹，并移动到指定目录下
    def create_folder_move_files(self, folder_path, slice_char):
        # 遍历文件夹下的文件名
        for filename in os.listdir(folder_path):
            source_path = os.path.join(folder_path, filename)
            # 判断是否是文件
            if os.path.isfile(source_path):
                # 找到分割的位置，如'-'
                index = filename.find(slice_char)
                if index!= -1:
                    # 提取分割字符前面的部分作为文件夹名
                    folder_name = filename[:index]
                    # 如果文件夹不存在，则创建
                    target_folder = os.path.join(folder_path, folder_name)
                    if not os.path.exists(target_folder):
                        os.mkdir(target_folder)
                    # 将文件移动到对应的文件夹
                    destination_path = os.path.join(target_folder, filename)
                    shutil.move(source_path, destination_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CreateFolderApp()
    window.show()
    sys.exit(app.exec_())