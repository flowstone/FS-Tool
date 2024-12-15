import sys
import os

from PyQt5.QtWidgets import QApplication, QGroupBox, QRadioButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from loguru import logger

from src.common_util import CommonUtil
from src.fs_constants import FsConstants
from src.progress_widget import ProgressWidget

class RenameFileApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal =  pyqtSignal()
    def __init__(self):
        super().__init__()
        self.check_type_text = None
        self.check_serial_flag = False
        self.check_clear_flag = False
        self.init_ui()

    def init_ui(self):
        logger.info("---- 初始化文件名批量修改工具 ----")
        self.setWindowTitle(FsConstants.FILE_RENAMER_WINDOW_TITLE)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setWindowFlags(self.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)


        layout = QVBoxLayout()

        # 创建第一个单选按钮组（文件类型）
        group_box = QGroupBox('文件类型')
        radio_btn_layout = QHBoxLayout()
        self.radio_label = QLabel("*选择文件类型：")

        # 创建两个单选按钮
        self.file_rbtn = QRadioButton('文件')
        self.folder_rbtn = QRadioButton('文件夹')
        self.check_type_text = self.file_rbtn.text()
        self.file_rbtn.setChecked(True)  # 默认选中选项1
        self.file_rbtn.toggled.connect(self.radio_btn_toggled)
        self.folder_rbtn.toggled.connect(self.radio_btn_toggled)

        radio_btn_layout.addWidget(self.radio_label)
        radio_btn_layout.addWidget(self.file_rbtn)
        radio_btn_layout.addWidget(self.folder_rbtn)
        group_box.setLayout(radio_btn_layout)
        layout.addWidget(group_box)

        # 创建序号选择单选按钮组
        number_box = QGroupBox('序号')
        radio_asc_layout = QHBoxLayout()
        self.number_label = QLabel("选择序号：")
        self.number_rbtn = QRadioButton('数字，如1、2、3')
        self.number_rbtn.toggled.connect(self.radio_serial_toggled)

        radio_asc_layout.addWidget(self.number_label)
        radio_asc_layout.addWidget(self.number_rbtn)
        number_box.setLayout(radio_asc_layout)
        layout.addWidget(number_box)

        # 创建清空文件名单选按钮组
        radio_clear_layout = QHBoxLayout()
        self.name_label = QLabel("清空文件名：")
        self.name_clear_rbtn = QRadioButton('是')
        self.name_clear_rbtn.toggled.connect(self.radio_name_clear_toggled)

        radio_clear_layout.addWidget(self.name_label)
        radio_clear_layout.addWidget(self.name_clear_rbtn)
        layout.addLayout(radio_clear_layout)

        # 选择文件夹相关部件
        folder_path_layout = QHBoxLayout()
        self.folder_path_label = QLabel("*选择文件夹：")
        self.folder_path_entry = QLineEdit()
        self.folder_path_entry.setFixedWidth(300)
        self.folder_path_entry.setObjectName("folder_path_input")
        self.folder_path_entry.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #ccc;")

        self.browse_button = QPushButton("浏览")
        self.browse_button.setObjectName("browse_button")
        self.browse_button.clicked.connect(self.browse_folder)

        folder_path_layout.addWidget(self.folder_path_label)
        folder_path_layout.addWidget(self.folder_path_entry)
        folder_path_layout.addWidget(self.browse_button)
        layout.addLayout(folder_path_layout)

        # 文件名前缀输入部件
        prefix_layout = QHBoxLayout()
        self.prefix_label = QLabel("文件名前缀：")
        self.prefix_entry = QLineEdit()
        self.prefix_entry.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #ccc;")

        prefix_layout.addWidget(self.prefix_label)
        prefix_layout.addWidget(self.prefix_entry)
        layout.addLayout(prefix_layout)

        # 文件名后缀输入部件
        suffix_layout = QHBoxLayout()
        self.suffix_label = QLabel("文件名后缀：")
        self.suffix_entry = QLineEdit()
        self.suffix_entry.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #ccc;")

        suffix_layout.addWidget(self.suffix_label)
        suffix_layout.addWidget(self.suffix_entry)
        layout.addLayout(suffix_layout)

        # 查找字符输入部件
        char_to_find_layout = QHBoxLayout()
        self.char_to_find_label = QLabel("查找字符：")
        self.char_to_find_entry = QLineEdit()
        self.char_to_find_entry.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #ccc;")

        char_to_find_layout.addWidget(self.char_to_find_label)
        char_to_find_layout.addWidget(self.char_to_find_entry)
        layout.addLayout(char_to_find_layout)

        # 替换字符输入部件
        replace_char_layout = QHBoxLayout()
        self.replace_char_label = QLabel("替换字符：")
        self.replace_char_entry = QLineEdit()
        self.replace_char_entry.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #ccc;")

        replace_char_layout.addWidget(self.replace_char_label)
        replace_char_layout.addWidget(self.replace_char_entry)
        layout.addLayout(replace_char_layout)



        # 操作按钮
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("开始")
        self.start_button.setObjectName("start_button")
        self.start_button.clicked.connect(self.start_operation)


        self.exit_button = QPushButton("退出")
        self.exit_button.setObjectName("exit_button")
        self.exit_button.clicked.connect(self.close)


        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.exit_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)


    # 清空原名称，只限序号时使用
    def radio_name_clear_toggled(self):
        if self.name_clear_rbtn.isChecked():
            self.check_clear_flag = True
            logger.info(f'当前选中：{self.name_clear_rbtn.text()}')
        else:
            self.check_clear_flag = False
            logger.info(f'取消选中')

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
        self.progress_tool = ProgressWidget(self)

        folder_path = self.folder_path_entry.text()
        prefix = self.prefix_entry.text()
        suffix = self.suffix_entry.text()
        char_to_find = self.char_to_find_entry.text()
        replace_char = self.replace_char_entry.text()
        if self.check_clear_flag and self.check_serial_flag == False:
            logger.info(f"选择清空选项时，必须选择序号!")
            QMessageBox.warning(self, "警告", "选择清空选项时，选择序号必选！")
            return
        if self.check_serial_flag and (prefix != "" or suffix != "" or char_to_find != "" or replace_char != ""):
            logger.info(f"选择序号时，不能同时修改其它信息")
            QMessageBox.warning(self, "警告", "选择序号时，不能同时修改其它信息！")
            return
        if folder_path:
            self.setEnabled(False)
            self.worker_thread = FileRenameThread(folder_path, prefix, suffix, char_to_find, replace_char,
                                                  self.check_type_text, self.check_serial_flag,
                                                  self.check_clear_flag, self.progress_tool)
            self.worker_thread.finished_signal.connect(self.operation_finished)
            self.worker_thread.error_signal.connect(self.operation_error)
            self.worker_thread.start()
            self.progress_tool.show()

        else:
            QMessageBox.warning(self, "警告", "请选择要修改的文件夹！")
            logger.warning("请选择要修改的文件夹")

    def operation_finished(self):
        logger.info("---- 操作完成 ----")
        self.progress_tool.hide()
        self.setEnabled(True)
        QMessageBox.information(self, "提示", "批量改名完成！")

    def operation_error(self, error_msg):
        logger.error(f"出现异常：{error_msg}")
        self.progress_tool.hide()
        self.setEnabled(True)
        QMessageBox.information(self, "警告", "遇到异常停止工作")

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

class FileRenameThread(QThread):
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, folder_path, prefix, suffix, char_to_find, replace_char, check_type_text, check_serial_flag,
                 check_clear_flag, progress_tool):
        super().__init__()
        self.folder_path = folder_path
        self.prefix = prefix
        self.suffix = suffix
        self.char_to_find = char_to_find
        self.replace_char = replace_char
        self.check_type_text = check_type_text
        self.check_serial_flag = check_serial_flag
        self.check_clear_flag = check_clear_flag
        self.progress_tool = progress_tool

    def run(self):
        try:
            self.progress_tool.set_range(0, 0)

            if self.check_type_text == "文件":
                logger.info(f"你选择类型是:{FsConstants.FILE_RENAMER_TYPE_FILE}")
                self.rename_files()
            else:
                logger.info(f"你选择的类型是：{FsConstants.FILE_RENAMER_TYPE_FOLDER}")
                self.rename_folder()

            if self.check_serial_flag:
                logger.info(f"选择序号单独走其它方法")
                self.rename_serial()

            self.finished_signal.emit()
        except OSError as e:
            self.error_signal.emit(str(e))

    def rename_files(self):
        # 遍历文件夹下的文件名

        for filename in os.listdir(self.folder_path):
            old_path = os.path.join(self.folder_path, filename)
            # 判断是否是文件
            if os.path.isfile(old_path):
                new_filename = f"{self.prefix}{filename}{self.suffix}"
                # 判断是否需要进行文件替换操作
                if self.char_to_find and self.replace_char:
                    # 替换字符
                    new_filename = new_filename.replace(self.char_to_find, self.replace_char)
                new_path = os.path.join(self.folder_path, new_filename)
                os.rename(old_path, new_path)


    def rename_folder(self):

        for dir_name in os.listdir(self.folder_path):
            old_path = os.path.join(self.folder_path, dir_name)
            if os.path.isdir(old_path):
                new_folder_name = f"{self.prefix}{dir_name}{self.suffix}"
                # 判断是否需要进行文件替换操作
                if self.char_to_find and self.replace_char:
                    # 替换字符
                    new_folder_name = new_folder_name.replace(self.char_to_find, self.replace_char)
                new_path = os.path.join(self.folder_path, new_folder_name)
                os.rename(old_path, new_path)


    def rename_serial(self):
        # 用于记录重命名的序号，初始化为1
        index = 1
        if self.check_type_text == "文件夹":
            logger.info("---- 开始为文件夹创建序号 ----")
            # 获取当前文件夹下的所有子文件夹和文件
            sub_dirs = [os.path.join(self.folder_path, d) for d in os.listdir(self.folder_path) if
                        os.path.isdir(os.path.join(self.folder_path, d))]

            # 重命名当前文件夹下的子文件夹
            for dir_path in sub_dirs:
                dir_name = "" if self.check_clear_flag else os.path.basename(dir_path)
                new_dir_name = str(index) + dir_name
                new_dir_path = os.path.join(os.path.dirname(dir_path), new_dir_name)
                os.rename(dir_path, new_dir_path)
                index += 1

        if self.check_type_text == "文件":
            logger.info("---- 开始为文件创建序号 ----")
            files = [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path) if
                     os.path.isfile(os.path.join(self.folder_path, f))]
            # 重命名当前文件夹下的文件
            for file_path in files:
                file_name = os.path.basename(file_path)
                if self.check_clear_flag:
                    _, file_name = os.path.splitext(file_path)
                new_file_name = str(index) + file_name
                new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
                os.rename(file_path, new_file_path)
                index += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RenameFileApp()
    window.show()
    sys.exit(app.exec_())