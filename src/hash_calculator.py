import sys
import hashlib
import zlib
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QLineEdit, QTextEdit, QCheckBox, QProgressBar
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread

from src.color_constants import BLACK, DEEP_SKY_BLUE
from src.font_constants import FontConstants
from src.fs_constants import FsConstants
from src.common_util import CommonUtil


class HashCalculatorThread(QThread):
    progress_signal = pyqtSignal(int)  # 用于更新进度条
    result_signal = pyqtSignal(dict, dict)  # 传递文件信息和哈希结果

    def __init__(self, file_path, hash_types):
        super().__init__()
        self.file_path = file_path
        self.hash_types = hash_types

    def run(self):
        try:
            # 获取文件信息
            file_info = HashCalculatorApp.get_file_info(self.file_path)

            # 计算哈希值
            hashes = {}
            file_size = os.path.getsize(self.file_path)
            processed_size = 0

            with open(self.file_path, "rb") as f:
                while chunk := f.read(4096):  # 按 4KB 分块读取文件
                    processed_size += len(chunk)

                    # 根据选择计算哈希
                    if "MD5" in self.hash_types:
                        if "md5" not in hashes:
                            hashes["md5"] = hashlib.md5()
                        hashes["md5"].update(chunk)

                    if "SHA1" in self.hash_types:
                        if "sha1" not in hashes:
                            hashes["sha1"] = hashlib.sha1()
                        hashes["sha1"].update(chunk)

                    if "SHA256" in self.hash_types:
                        if "sha256" not in hashes:
                            hashes["sha256"] = hashlib.sha256()
                        hashes["sha256"].update(chunk)

                    if "CRC32" in self.hash_types:
                        if "crc32" not in hashes:
                            hashes["crc32"] = 0
                        hashes["crc32"] = zlib.crc32(chunk, hashes["crc32"])

                    # 发出进度信号
                    progress = int((processed_size / file_size) * 100)
                    self.progress_signal.emit(progress)

            # 格式化哈希值
            results = {
                "MD5": hashes["md5"].hexdigest() if "md5" in hashes else None,
                "SHA1": hashes["sha1"].hexdigest() if "sha1" in hashes else None,
                "SHA256": hashes["sha256"].hexdigest() if "sha256" in hashes else None,
                "CRC32": format(hashes["crc32"] & 0xFFFFFFFF, "08x").upper() if "crc32" in hashes else None,
            }

            # 发出结果信号
            self.result_signal.emit(file_info, results)

        except Exception as e:
            QMessageBox.critical(None, "错误", f"计算哈希失败：{str(e)}")


class HashCalculatorApp(QWidget):
    closed_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(FsConstants.HASH_CALCULATOR_WINDOW_TITLE)
        self.setFixedSize(500, 350)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setAcceptDrops(True)

        layout = QVBoxLayout()

        # 文件选择布局
        file_layout = QHBoxLayout()
        title_label = QLabel("HASH校验")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {BLACK.name()};")
        title_label.setFont(FontConstants.H1)
        layout.addWidget(title_label)

        self.file_label = QLabel("选择的文件:")
        self.file_path_entry = QLineEdit()
        self.file_path_entry.setReadOnly(True)
        browse_button = QPushButton("选择文件")
        browse_button.setObjectName("browse_button")
        browse_button.clicked.connect(self.browse_file)

        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_path_entry)
        file_layout.addWidget(browse_button)

        # 哈希类型选择布局
        hash_selection_layout = QHBoxLayout()
        self.md5_checkbox = QCheckBox("MD5")
        self.md5_checkbox.setChecked(True)
        self.sha1_checkbox = QCheckBox("SHA1")
        self.sha1_checkbox.setChecked(True)
        self.sha256_checkbox = QCheckBox("SHA256")
        self.sha256_checkbox.setChecked(True)
        self.crc32_checkbox = QCheckBox("CRC32")
        self.crc32_checkbox.setChecked(True)

        hash_selection_layout.addWidget(self.md5_checkbox)
        hash_selection_layout.addWidget(self.sha1_checkbox)
        hash_selection_layout.addWidget(self.sha256_checkbox)
        hash_selection_layout.addWidget(self.crc32_checkbox)

        # 按钮布局
        button_layout = QHBoxLayout()
        self.calculate_button = QPushButton("计算")
        self.calculate_button.setObjectName("start_button")
        self.calculate_button.clicked.connect(self.start_hash_calculation)
        exit_button = QPushButton("退出")
        exit_button.setObjectName("exit_button")

        exit_button.clicked.connect(self.close)

        button_layout.addWidget(self.calculate_button)
        button_layout.addWidget(exit_button)

        # 文件信息显示框
        self.file_info_text = QTextEdit()
        self.file_info_text.setReadOnly(True)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # 布局组合
        layout.addLayout(file_layout)
        layout.addLayout(hash_selection_layout)
        layout.addWidget(self.file_info_text)
        layout.addWidget(self.progress_bar)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*.*)")
        if file_path:
            self.file_path_entry.setText(file_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            if os.path.isfile(file_path):
                self.file_path_entry.setText(file_path)
            else:
                QMessageBox.warning(self, "警告", "拖入的不是有效文件！")

    def start_hash_calculation(self):
        file_path = self.file_path_entry.text()
        if not file_path:
            QMessageBox.warning(self, "警告", "请先选择一个文件！")
            return

        hash_types = []
        if self.md5_checkbox.isChecked():
            hash_types.append("MD5")
        if self.sha1_checkbox.isChecked():
            hash_types.append("SHA1")
        if self.sha256_checkbox.isChecked():
            hash_types.append("SHA256")
        if self.crc32_checkbox.isChecked():
            hash_types.append("CRC32")

        if not hash_types:
            QMessageBox.warning(self, "警告", "请至少选择一种哈希类型！")
            return

        self.calculate_button.setEnabled(False)
        # 创建并启动线程
        self.thread = HashCalculatorThread(file_path, hash_types)
        self.thread.progress_signal.connect(self.progress_bar.setValue)
        self.thread.result_signal.connect(self.display_file_info)
        self.thread.start()

    def display_file_info(self, file_info, hashes):
        info_text = "\n".join([f"{key}: {value}" for key, value in file_info.items()])
        hash_text = "\n".join([f"{key}: {value}" for key, value in hashes.items() if value])
        self.file_info_text.setText(f"{info_text}\n\n{hash_text}")
        self.progress_bar.setValue(100)
        self.calculate_button.setEnabled(True)


    @staticmethod
    def get_file_info(file_path):
        file_size = os.path.getsize(file_path)
        modification_time = os.path.getmtime(file_path)

        return {
            "文件名": file_path,
            "大小": f"{file_size} 字节",
            "修改时间": CommonUtil.format_time(modification_time)
        }

    def closeEvent(self, event):
        self.closed_signal.emit()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HashCalculatorApp()
    window.show()
    sys.exit(app.exec_())
