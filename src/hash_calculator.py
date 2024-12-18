import sys
import hashlib
import zlib
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QLineEdit, QTextEdit, QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from src.fs_constants import FsConstants
from src.common_util import CommonUtil


class HashCalculatorApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口属性
        self.setWindowTitle(FsConstants.HASH_CALCULATOR_WINDOW_TITLE)
        self.setFixedSize(500, 300)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        # 启用文件拖放功能
        self.setAcceptDrops(True)

        # 主布局
        layout = QVBoxLayout()

        # 文件路径布局
        file_layout = QHBoxLayout()
        self.file_label = QLabel("选择的文件:")
        self.file_path_entry = QLineEdit()
        self.file_path_entry.setReadOnly(True)
        browse_button = QPushButton("选择文件")
        browse_button.setObjectName("browse_button")
        browse_button.clicked.connect(self.browse_file)

        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_path_entry)
        file_layout.addWidget(browse_button)

        # 选择计算的哈希类型
        hash_selection_layout = QHBoxLayout()
        self.md5_checkbox = QCheckBox("MD5")
        self.md5_checkbox.setChecked(True)  # 默认勾选 MD5
        self.sha1_checkbox = QCheckBox("SHA1")
        self.sha1_checkbox.setChecked(True)  # 默认勾选 SHA1
        self.sha256_checkbox = QCheckBox("SHA256")
        self.sha256_checkbox.setChecked(True)  # 默认勾选 SHA256
        self.crc32_checkbox = QCheckBox("CRC32")
        self.crc32_checkbox.setChecked(True)  # 默认勾选 CRC32

        hash_selection_layout.addWidget(self.md5_checkbox)
        hash_selection_layout.addWidget(self.sha1_checkbox)
        hash_selection_layout.addWidget(self.sha256_checkbox)
        hash_selection_layout.addWidget(self.crc32_checkbox)

        # 操作按钮
        button_layout = QHBoxLayout()
        calculate_button = QPushButton("计算")
        calculate_button.setObjectName("calculate_button")
        calculate_button.clicked.connect(self.calculate_hashes)
        exit_button = QPushButton("退出")
        exit_button.setObjectName("exit_button")
        exit_button.clicked.connect(self.close)

        button_layout.addWidget(calculate_button)
        button_layout.addWidget(exit_button)

        # 文件信息显示框
        self.file_info_text = QTextEdit()
        self.file_info_text.setReadOnly(True)

        # 将各个布局添加到主布局中
        layout.addLayout(file_layout)
        layout.addLayout(hash_selection_layout)
        layout.addWidget(self.file_info_text)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def browse_file(self):
        """
        选择本地文件，并显示文件路径
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*.*)")
        if file_path:
            self.file_path_entry.setText(file_path)

    def dragEnterEvent(self, event):
        """
        拖入文件时的事件处理
        """
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        放置文件时的事件处理
        """
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            file_path = urls[0].toLocalFile()  # 获取第一个文件路径
            if os.path.isfile(file_path):  # 确保是文件而不是文件夹
                self.file_path_entry.setText(file_path)
            else:
                QMessageBox.warning(self, "警告", "拖入的不是有效文件！")

    def calculate_hashes(self):
        """
        计算选中文件的哈希值和文件信息
        """
        file_path = self.file_path_entry.text()

        if not file_path:
            QMessageBox.warning(self, "警告", "请先选择一个文件！")
            return

        # 获取文件信息
        try:
            file_info = self.get_file_info(file_path)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"读取文件信息失败：{str(e)}")
            return

        # 根据用户选择计算哈希值
        hashes = {}
        if self.md5_checkbox.isChecked():
            hashes["MD5"] = self.get_md5_of_file(file_path)
        if self.sha1_checkbox.isChecked():
            hashes["SHA1"] = self.get_sha1_of_file(file_path)
        if self.sha256_checkbox.isChecked():
            hashes["SHA256"] = self.get_sha256_of_file(file_path)
        if self.crc32_checkbox.isChecked():
            hashes["CRC32"] = self.get_crc32_of_file(file_path)

        # 显示结果
        self.display_file_info(file_info, hashes)

    @staticmethod
    def get_file_info(file_path):
        """
        获取文件的基本信息
        :param file_path: 文件路径
        :return: 文件名、大小、修改时间的字典
        """
        #file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        modification_time = os.path.getmtime(file_path)

        return {
            "文件名": file_path,
            "大小": f"{file_size} 字节",
            "修改时间": CommonUtil.format_time(modification_time)  # 假设格式化方法在 CommonUtil 中
        }

    @staticmethod
    def get_md5_of_file(file_path):
        """
        计算文件的 MD5 值
        """
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):  # 按 4KB 分块读取文件
                md5_hash.update(chunk)
        return md5_hash.hexdigest()

    @staticmethod
    def get_sha1_of_file(file_path):
        """
        计算文件的 SHA1 值
        """
        sha1_hash = hashlib.sha1()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha1_hash.update(chunk)
        return sha1_hash.hexdigest()

    @staticmethod
    def get_sha256_of_file(file_path):
        """
        计算文件的 SHA256 值
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    @staticmethod
    def get_crc32_of_file(file_path):
        """
        计算文件的 CRC32 值
        """
        crc32_hash = 0
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                crc32_hash = zlib.crc32(chunk, crc32_hash)
        return format(crc32_hash & 0xFFFFFFFF, "08x").upper()

    def display_file_info(self, file_info, hashes):
        """
        显示文件信息和计算结果
        """
        info_text = "\n".join([f"{key}: {value}" for key, value in file_info.items()])
        if hashes:
            hash_text = "\n".join([f"{key}: {value}" for key, value in hashes.items()])
            info_text += f"\n\n{hash_text}"

        self.file_info_text.setText(info_text)

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HashCalculatorApp()
    window.show()
    sys.exit(app.exec_())
