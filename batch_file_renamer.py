import sys
import os
from PyQt5.QtWidgets import QApplication, QGroupBox,QRadioButton,QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMenuBar,QFileDialog
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from loguru import logger
from select import select

from common_util import CommonUtil
from fs_constants import FsConstants

class RenameFileApp(QWidget):
    def __init__(self):
        super().__init__()
        # 选择文件类型
        self.check_type_text = None
        self.check_serial_flag = False
        self.init_ui()

    def init_ui(self):
        logger.info("---- 初始化文件名批量修改工具 ----")
        self.setWindowTitle(FsConstants.FILE_RENAMER_WINDOW_TITLE)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        layout = QVBoxLayout()
        # 创建第一个单选按钮组
        group_box = QGroupBox('文件类型')
        radio_btn_layout = QHBoxLayout()
        self.radio_label = QLabel("选择文件类型：")
        self.radio_label.setStyleSheet("color: #333; font-size: 14px;")

        # 创建两个单选按钮
        self.file_rbtn = QRadioButton('文件')
        self.folder_rbtn = QRadioButton('文件夹')
        # 将两个单选按钮设置为互斥
        self.check_type_text = self.file_rbtn.text()
        self.file_rbtn.setChecked(True)  # 默认选中选项1
        self.file_rbtn.toggled.connect(self.radio_btn_toggled)
        self.folder_rbtn.toggled.connect(self.radio_btn_toggled)
        radio_btn_layout.addWidget(self.radio_label)
        radio_btn_layout.addWidget(self.file_rbtn)
        radio_btn_layout.addWidget(self.folder_rbtn)
        group_box.setLayout(radio_btn_layout)
        layout.addWidget(group_box)


        radio_asc_layout = QHBoxLayout()
        self.number_label = QLabel("选择序号：")
        self.number_label.setStyleSheet("color: #333; font-size: 14px;")

        # 创建两个单选按钮
        self.number_rbtn = QRadioButton('数字，如1、2、3')
        self.number_rbtn.toggled.connect(self.radio_serial_toggled)
        radio_asc_layout.addWidget(self.number_label)
        radio_asc_layout.addWidget(self.number_rbtn)
        layout.addLayout(radio_asc_layout)




        # 选择文件夹相关部件
        folder_path_layout = QHBoxLayout()
        self.folder_path_label = QLabel("选择文件夹：")
        self.folder_path_label.setStyleSheet("color: #333; font-size: 14px;")
        self.folder_path_entry = QLineEdit()
        self.folder_path_entry.setFixedWidth(300)
        self.folder_path_entry.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 2px 5px;
            }
        """)
        self.browse_button = QPushButton("浏览")
        self.browse_button.setStyleSheet("""
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
        self.browse_button.clicked.connect(self.browse_folder)

        folder_path_layout.addWidget(self.folder_path_label)
        folder_path_layout.addWidget(self.folder_path_entry)
        folder_path_layout.addWidget(self.browse_button)
        layout.addLayout(folder_path_layout)

        # 文件名前缀输入部件
        prefix_layout = QHBoxLayout()
        self.prefix_label = QLabel("文件名前缀：")
        self.prefix_label.setStyleSheet("color: #333; font-size: 14px;")
        self.prefix_entry = QLineEdit()
        self.prefix_entry.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 2px 5px;
            }
        """)
        prefix_layout.addWidget(self.prefix_label)
        prefix_layout.addWidget(self.prefix_entry)
        layout.addLayout(prefix_layout)

        # 文件名后缀输入部件
        suffix_layout = QHBoxLayout()
        self.suffix_label = QLabel("文件名后缀：")
        self.suffix_label.setStyleSheet("color: #333; font-size: 14px;")
        self.suffix_entry = QLineEdit()
        self.suffix_entry.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 2px 5px;
            }
        """)
        suffix_layout.addWidget(self.suffix_label)
        suffix_layout.addWidget(self.suffix_entry)
        layout.addLayout(suffix_layout)

        # 查找字符输入部件
        char_to_find_layout = QHBoxLayout()
        self.char_to_find_label = QLabel("查找字符：")
        self.char_to_find_label.setStyleSheet("color: #333; font-size: 14px;")
        self.char_to_find_entry = QLineEdit()
        self.char_to_find_entry.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 2px 5px;
            }
        """)
        char_to_find_layout.addWidget(self.char_to_find_label)
        char_to_find_layout.addWidget(self.char_to_find_entry)
        layout.addLayout(char_to_find_layout)

        # 替换字符输入部件
        replace_char_layout = QHBoxLayout()
        self.replace_char_label = QLabel("替换字符：")
        self.replace_char_label.setStyleSheet("color: #333; font-size: 14px;")
        self.replace_char_entry = QLineEdit()
        self.replace_char_entry.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 2px 5px;
            }
        """)
        replace_char_layout.addWidget(self.replace_char_label)
        replace_char_layout.addWidget(self.replace_char_entry)
        layout.addLayout(replace_char_layout)

        # 作者和Github信息文本
        author_font = QFont("楷体", 11)
        self.author_label = QLabel(f"Author：{FsConstants.AUTHOR_BLOG}")
        self.author_label.setFont(author_font)
        self.author_label.setStyleSheet("color: #007BFF;")
        self.github_label = QLabel(f"Github：{FsConstants.PROJECT_ADDRESS}")
        self.github_label.setFont(author_font)
        self.github_label.setStyleSheet("color: #007BFF;")

        info_layout = QVBoxLayout()
        info_layout.addWidget(self.author_label)
        info_layout.addWidget(self.github_label)
        layout.addLayout(info_layout)

        # 操作按钮
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("开始")
        self.start_button.setStyleSheet("""
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
        self.start_button.clicked.connect(self.start_operation)
        self.exit_button = QPushButton("退出")
        self.exit_button.setStyleSheet("""
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
        self.exit_button.clicked.connect(self.close)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.exit_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)


    # 序号Radio
    def radio_serial_toggled(self):
        if self.number_rbtn.isChecked():
            self.check_serial_flag = True
            logger.info(f'当前选中：{self.number_rbtn.text()}')
        else:
            self.check_serial_flag = False
            logger.info(f'取消选中')


    # 文件类型Radio
    def radio_btn_toggled(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.check_type_text = radio_button.text()
            logger.info(f'当前选中：{radio_button.text()}')

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.folder_path_entry.setText(folder_path)



    def start_operation(self):
        folder_path = self.folder_path_entry.text()
        prefix = self.prefix_entry.text()
        suffix = self.suffix_entry.text()
        char_to_find = self.char_to_find_entry.text()
        replace_char = self.replace_char_entry.text()
        if self.check_serial_flag and (prefix != "" or suffix != "" or char_to_find != "" or replace_char != ""):
            logger.info(f"选择序号时，不能同时修改其它信息")
            QMessageBox.warning(self, "警告", "选择序号时，不能同时修改其它信息！")
            return
        if folder_path:
            if self.check_type_text == self.file_rbtn.text():
                logger.info(f"你选择类型是:{FsConstants.FILE_RENAMER_TYPE_FILE}")
                self.rename_files(folder_path, prefix, suffix, char_to_find, replace_char)
            else:
                logger.info(f"你选择的类型是：{FsConstants.FILE_RENAMER_TYPE_FOLDER}")
                self.rename_folder(folder_path, prefix, suffix, char_to_find, replace_char)

            if self.check_serial_flag:
                logger.info(f"选择序号单独走其它方法")
                self.rename_serial(folder_path)

            QMessageBox.information(self, "提示", "批量改名完成！")
            logger.info("批量改名完成")

        else:
            QMessageBox.warning(self, "警告", "请选择要修改的文件夹！")
            logger.warning("请选择要修改的文件夹")


    # 修改文件名
    @staticmethod
    def rename_files(folder_path, prefix, suffix, char_to_find, replace_char):
        # 遍历文件夹下的文件名
        for filename in os.listdir(folder_path):
            old_path = os.path.join(folder_path, filename)
            # 判断是否是文件
            if os.path.isfile(old_path):
                new_filename = f"{prefix}{filename}{suffix}"
                # 判断是否需要进行文件替换操作
                if char_to_find and replace_char:
                    # 替换字符
                    new_filename = new_filename.replace(char_to_find, replace_char)
                new_path = os.path.join(folder_path, new_filename)
                os.rename(old_path, new_path)


    # 修改文件夹名
    @staticmethod
    def rename_folder(folder_path, prefix, suffix, char_to_find, replace_char):
        for dir_name in os.listdir(folder_path):
            old_path = os.path.join(folder_path, dir_name)
            if os.path.isdir(old_path):
                new_folder_name = f"{prefix}{dir_name}{suffix}"
                # 判断是否需要进行文件替换操作
                if char_to_find and replace_char:
                    # 替换字符
                    new_folder_name = new_folder_name.replace(char_to_find, replace_char)
                new_path = os.path.join(folder_path, new_folder_name)
                os.rename(old_path, new_path)
    # 添加序号
    def rename_serial(self, folder_path):
        # 用于记录重命名的序号，初始化为1
        index = 1
        if self.check_type_text == self.folder_rbtn.text():
            logger.info("---- 开始为文件夹创建序号 ----")
            # 获取当前文件夹下的所有子文件夹和文件
            sub_dirs = [os.path.join(folder_path, d) for d in os.listdir(folder_path) if
                        os.path.isdir(os.path.join(folder_path, d))]

            # 重命名当前文件夹下的子文件夹
            for dir_path in sub_dirs:
                dir_name = os.path.basename(dir_path)
                new_dir_name = str(index) + dir_name
                new_dir_path = os.path.join(os.path.dirname(dir_path), new_dir_name)
                os.rename(dir_path, new_dir_path)
                index += 1


        if self.check_type_text == self.file_rbtn.text():
            logger.info("---- 开始为文件创建序号 ----")
            files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                     os.path.isfile(os.path.join(folder_path, f))]
            # 重命名当前文件夹下的文件
            for file_path in files:
                file_name = os.path.basename(file_path)
                new_file_name = str(index) + file_name
                new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
                os.rename(file_path, new_file_path)
                index += 1
