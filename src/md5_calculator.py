import sys
import hashlib

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QLineEdit
)
from PyQt5.QtCore import Qt, pyqtSignal
from src.fs_constants import FsConstants
from src.common_util import CommonUtil

class MD5CalculatorApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal = pyqtSignal()
    """
    主窗口类，实现选择文件并计算其 MD5 值
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口属性
        self.setWindowTitle(FsConstants.RSA_MD5_CALCULATOR_WINDOW_TITLE)
        #self.setGeometry(400, 200, 500, 200)
        self.setFixedSize(500, 200)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

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

        # 结果显示布局
        result_layout = QHBoxLayout()
        self.result_label = QLabel("MD5 值:")
        self.md5_value_label = QLineEdit()
        self.md5_value_label.setReadOnly(True)
        self.md5_value_label.setAlignment(Qt.AlignCenter)

        result_layout.addWidget(self.result_label)
        result_layout.addWidget(self.md5_value_label)

        # 操作按钮
        button_layout = QHBoxLayout()
        calculate_button = QPushButton("计算 MD5")
        calculate_button.setObjectName("start_button")
        calculate_button.clicked.connect(self.calculate_md5)
        exit_button = QPushButton("退出")
        exit_button.setObjectName("exit_button")
        exit_button.clicked.connect(self.close)

        button_layout.addWidget(calculate_button)
        button_layout.addWidget(exit_button)

        # 将各个布局添加到主布局中
        layout.addLayout(file_layout)
        layout.addLayout(result_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def browse_file(self):
        """
        选择本地文件，并显示文件路径
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*.*)")
        if file_path:
            self.file_path_entry.setText(file_path)

    def calculate_md5(self):
        """
        计算选中文件的 MD5 值
        """
        file_path = self.file_path_entry.text()

        if not file_path:
            QMessageBox.warning(self, "警告", "请先选择一个文件！")
            return

        try:
            md5_value = self.get_md5_of_file(file_path)
            self.md5_value_label.setText(md5_value)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"计算 MD5 失败：{str(e)}")

    @staticmethod
    def get_md5_of_file(file_path):
        """
        计算文件的 MD5 值
        :param file_path: 文件路径
        :return: MD5 字符串
        """
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):  # 按 4KB 分块读取文件，适用于大文件
                md5_hash.update(chunk)
        return md5_hash.hexdigest()

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MD5CalculatorApp()
    window.show()
    sys.exit(app.exec_())
