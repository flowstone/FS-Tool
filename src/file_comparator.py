import sys
import os
import hashlib
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QWidget, QComboBox,
    QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt


class FileComparatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件比较")
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        # 标签显示
        self.label = QLabel("请选择源目录和目标目录进行文件比较")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # 源目录标签
        self.source_label = QLabel("源目录: 未选择")
        self.source_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.source_label)

        # 目标目录标签
        self.target_label = QLabel("目标目录: 未选择")
        self.target_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.target_label)

        # 按钮布局，放置“选择源目录”和“选择目标目录”按钮
        button_layout = QHBoxLayout()
        self.source_button = QPushButton("选择源目录")
        self.source_button.setObjectName("browse_button")

        self.source_button.clicked.connect(self.select_source_directory)

        button_layout.addWidget(self.source_button)

        self.target_button = QPushButton("选择目标目录")
        self.target_button.setObjectName("browse_button")

        self.target_button.clicked.connect(self.select_target_directory)
        button_layout.addWidget(self.target_button)

        layout.addLayout(button_layout)

        # 添加“选择比较方法”标签
        self.method_label = QLabel("请选择比较方法:")
        layout.addWidget(self.method_label)

        # 比较方法选择框
        self.method_combo = QComboBox()
        self.method_combo.addItems(["文件大小比较", "哈希算法比较", "逐字节比较", "校验和比较"])
        layout.addWidget(self.method_combo)

        # 开始比较按钮
        self.compare_button = QPushButton("开始比较")
        self.compare_button.setObjectName("start_button")
        self.compare_button.clicked.connect(self.compare_files)
        layout.addWidget(self.compare_button)

        # 显示文件列表区域
        self.result_text = QTextEdit()
        self.result_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #388E3C;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QTextEdit:read-only {
                background-color: #f9f9f9;
            }
        """)
        self.result_text.setReadOnly(True)  # 只读
        layout.addWidget(self.result_text)
        self.setLayout(layout)
        # 当前选择的源目录和目标目录路径
        self.source_directory = None
        self.target_directory = None


    def select_source_directory(self):
        """选择源目录"""
        directory = QFileDialog.getExistingDirectory(self, "选择源目录")
        if directory:
            self.source_directory = directory
            self.source_label.setText(f"源目录: {directory}")

    def select_target_directory(self):
        """选择目标目录"""
        directory = QFileDialog.getExistingDirectory(self, "选择目标目录")
        if directory:
            self.target_directory = directory
            self.target_label.setText(f"目标目录: {directory}")

    def compare_files(self):
        """比较源目录和目标目录中的文件"""
        if not self.source_directory or not self.target_directory:
            QMessageBox.warning(self, "警告", "请先选择源目录和目标目录！")
            return

        method = self.method_combo.currentText()

        # 获取源目录和目标目录中的文件列表
        source_files = set(os.listdir(self.source_directory))
        target_files = set(os.listdir(self.target_directory))

        # 获取相同文件名的文件
        common_files = source_files.intersection(target_files)

        if not common_files:
            QMessageBox.information(self, "信息", "没有相同文件名的文件。")
            return

        total_same_files = 0
        total_diff_files = 0
        result = "文件比较结果:\n\n"

        for file_name in common_files:
            source_file_path = os.path.join(self.source_directory, file_name)
            target_file_path = os.path.join(self.target_directory, file_name)

            result += f"正在比较文件: {file_name}\n"

            if method == "文件大小比较":
                if self.compare_by_size(source_file_path, target_file_path):
                    total_same_files += 1
                    result += "  文件大小相同\n"
                else:
                    total_diff_files += 1
                    result += "  文件大小不匹配\n"

            elif method == "哈希算法比较":
                if self.compare_by_hash(source_file_path, target_file_path):
                    total_same_files += 1
                    result += "  哈希值相同\n"
                else:
                    total_diff_files += 1
                    result += "  哈希值不匹配\n"

            elif method == "逐字节比较":
                if self.compare_by_bytes(source_file_path, target_file_path):
                    total_same_files += 1
                    result += "  文件内容相同\n"
                else:
                    total_diff_files += 1
                    result += "  文件内容不匹配\n"

            elif method == "校验和比较":
                if self.compare_by_checksum(source_file_path, target_file_path):
                    total_same_files += 1
                    result += "  校验和相同\n"
                else:
                    total_diff_files += 1
                    result += "  校验和不匹配\n"

            result += "\n"

        result += f"\n相同文件数量: {total_same_files} 个文件\n"
        result += f"不同文件数量: {total_diff_files} 个文件\n"

        # 显示结果
        self.result_text.setText(result)

    def compare_by_size(self, file1, file2):
        """通过文件大小比较"""
        return os.path.getsize(file1) == os.path.getsize(file2)

    def compare_by_hash(self, file1, file2):
        """通过哈希算法比较"""

        def file_hash(file_path):
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()

        return file_hash(file1) == file_hash(file2)

    def compare_by_bytes(self, file1, file2):
        """逐字节比较"""
        with open(file1, "rb") as f1, open(file2, "rb") as f2:
            while True:
                byte1 = f1.read(4096)
                byte2 = f2.read(4096)
                if byte1 != byte2:
                    return False
                if not byte1:
                    return True

    def compare_by_checksum(self, file1, file2):
        """通过校验和比较"""

        def file_checksum(file_path):
            checksum = 0
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    checksum ^= hash(chunk)
            return checksum

        return file_checksum(file1) == file_checksum(file2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileComparatorApp()
    window.show()
    sys.exit(app.exec_())
