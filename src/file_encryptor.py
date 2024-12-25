import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QWidget, QMessageBox,
    QComboBox, QHBoxLayout, QProgressBar
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QIcon
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from loguru import logger

from src.common_util import CommonUtil
from src.color_constants import RED, DARK_GRAY, BLUE, BLACK, DEEP_SKY_BLUE
from src.font_constants import FontConstants


class EncryptThread(QThread):
    progress = pyqtSignal(int)  # 信号用于传递进度
    finished = pyqtSignal()     # 信号用于标记加密完成
    error = pyqtSignal(str)    # 信号用于报告错误

    def __init__(self, folder_path, key, parent=None):
        super().__init__(parent)
        self.folder_path = folder_path
        self.key = key

    def run(self):
        try:
            total_files = sum([len(files) for _, _, files in os.walk(self.folder_path)])
            processed_files = 0

            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as f:
                        data = f.read()

                    # 使用 AES 加密
                    cipher = AES.new(self.key, AES.MODE_CBC)
                    ciphertext = cipher.encrypt(pad(data, AES.block_size))

                    encrypted_file = file_path + ".enc"
                    with open(encrypted_file, "wb") as f:
                        f.write(cipher.iv)  # 写入初始化向量
                        f.write(ciphertext)

                    # 删除原文件
                    os.remove(file_path)

                    processed_files += 1
                    self.progress.emit(int((processed_files / total_files) * 100))  # 更新进度条

            self.finished.emit()  # 加密完成信号

        except Exception as e:
            self.error.emit(str(e))  # 发送错误信息
            self.finished.emit()

class DecryptThread(QThread):
    progress = pyqtSignal(int)  # 信号用于传递进度
    finished = pyqtSignal()     # 信号用于标记解密完成
    error = pyqtSignal(str)    # 信号用于报告错误

    def __init__(self, folder_path, key, parent=None):
        super().__init__(parent)
        self.folder_path = folder_path
        self.key = key

    def run(self):
        try:
            total_files = sum([len(files) for _, _, files in os.walk(self.folder_path)])
            processed_files = 0

            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    if not file.endswith(".enc"):
                        continue

                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as f:
                        iv = f.read(16)  # 读取初始化向量
                        ciphertext = f.read()

                    # 使用 AES 解密
                    cipher = AES.new(self.key, AES.MODE_CBC, iv)
                    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

                    decrypted_file = file_path.replace(".enc", "")
                    with open(decrypted_file, "wb") as f:
                        f.write(plaintext)

                    # 删除加密文件
                    os.remove(file_path)

                    processed_files += 1
                    self.progress.emit(int((processed_files / total_files) * 100))  # 更新进度条

            self.finished.emit()  # 解密完成信号

        except Exception as e:
            logger.error(f"Exception = {e}")
            self.error.emit(str(e))  # 发送错误信息
            self.finished.emit()

class FileEncryptorApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("批量文件加密")
        #self.setFixedSize(500, 550)  # 调整窗口大小
        self.setFixedWidth(500)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        layout = QVBoxLayout()

        # 应用标题
        title_label = QLabel("批量文件加密")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {BLACK.name()};")
        title_label.setFont(FontConstants.H1)
        layout.addWidget(title_label)

        # 应用说明
        desc_label = QLabel("通过 AES 加密算法加密或解密指定文件夹内的所有文件。\n"
                            "支持密钥长度 128/192/256 位，请输入密码进行加密操作。")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet(f"color: {BLUE.name()};")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        browse_layout = QHBoxLayout()
        # 文件夹路径显示
        self.folder_label = QLabel("选择目录")
        self.folder_path_entry = QLineEdit()
        self.folder_path_entry.setPlaceholderText("请选择要加密的目录")
        self.folder_path_entry.setObjectName("folder_path_input")
        # 文件夹选择按钮
        self.select_folder_button = QPushButton("选择文件夹")
        self.select_folder_button.setObjectName("browse_button")
        self.select_folder_button.clicked.connect(self.select_folder)
        browse_layout.addWidget(self.folder_label)
        browse_layout.addWidget(self.folder_path_entry)
        browse_layout.addWidget(self.select_folder_button)
        layout.addLayout(browse_layout)

        # 密钥长度选择
        key_length_label = QLabel("选择密钥长度：")
        layout.addWidget(key_length_label)

        self.key_length_combo = QComboBox()
        self.key_length_combo.addItems(["128", "192", "256"])
        layout.addWidget(self.key_length_combo)

        # 密码输入
        password_label = QLabel("输入密码：")
        layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("请输入密码 (至少8位)")
        layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()

        # 加密按钮
        self.encrypt_button = QPushButton("加密文件")
        self.encrypt_button.setObjectName("start_button")
        self.encrypt_button.clicked.connect(self.encrypt_folder)
        button_layout.addWidget(self.encrypt_button)

        # 解密按钮
        self.decrypt_button = QPushButton("解密文件")
        self.decrypt_button.setObjectName("exit_button")
        self.decrypt_button.clicked.connect(self.decrypt_folder)
        button_layout.addWidget(self.decrypt_button)

        layout.addLayout(button_layout)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        # 当前选择的文件夹路径
        self.selected_folder = None

    def select_folder(self):
        """打开文件夹选择对话框"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.selected_folder = folder_path
        self.folder_path_entry.setText(folder_path)

    def encrypt_folder(self):
        """加密文件夹下的所有文件"""
        if not self.selected_folder:
            QMessageBox.warning(self, "警告", "请先选择一个文件夹！")
            return

        password = self.password_input.text()
        if len(password) < 8:
            QMessageBox.warning(self, "警告", "密码长度必须至少8个字符！")
            return

        key_length = int(self.key_length_combo.currentText())
        key = self.derive_key(password, key_length)
        self.progress_bar.show()
        self.setEnabled(False)
        self.encrypt_thread = EncryptThread(self.selected_folder, key)
        self.encrypt_thread.progress.connect(self.update_progress)  # 连接进度更新
        self.encrypt_thread.finished.connect(self.encryption_finished)  # 加密完成处理
        self.encrypt_thread.error.connect(self.encryption_error)  # 错误处理
        self.encrypt_thread.start()  # 启动加密线程

    def decrypt_folder(self):
        """解密文件夹下的所有加密文件"""
        if not self.selected_folder:
            QMessageBox.warning(self, "警告", "请先选择一个文件夹！")
            return

        password = self.password_input.text()
        if len(password) < 8:
            QMessageBox.warning(self, "警告", "密码长度必须至少8个字符！")
            return

        key_length = int(self.key_length_combo.currentText())
        key = self.derive_key(password, key_length)
        self.progress_bar.show()
        self.setEnabled(False)
        self.decrypt_thread = DecryptThread(self.selected_folder, key)
        self.decrypt_thread.progress.connect(self.update_progress)  # 连接进度更新
        self.decrypt_thread.finished.connect(self.decryption_finished)  # 解密完成处理
        self.decrypt_thread.error.connect(self.decryption_error)  # 错误处理
        self.decrypt_thread.start()  # 启动解密线程

    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)

    def encryption_finished(self):
        self.setEnabled(True)
        self.progress_bar.hide()

        """加密完成后的提示"""
        QMessageBox.information(self, "成功", "文件夹内的文件已成功加密！")

    def decryption_finished(self):
        self.setEnabled(True)
        self.progress_bar.hide()

        """解密完成后的提示"""
        QMessageBox.information(self, "成功", "文件夹内的文件已成功解密！")

    def encryption_error(self, error_msg):
        self.setEnabled(True)
        self.progress_bar.hide()

        """加密错误提示"""
        QMessageBox.critical(self, "错误", f"加密过程中发生错误: {error_msg}")

    def decryption_error(self, error_msg):
        self.setEnabled(True)
        self.progress_bar.hide()

        """解密错误提示"""
        QMessageBox.critical(self, "错误", f"解密过程中发生错误: {error_msg}")

    def derive_key(self, password: str, key_length: int):
        """通过 PBKDF2 生成密钥"""
        salt = b'fs_tool_salt'  # 可以随机生成并保存到文件中
        return PBKDF2(password, salt, dkLen=key_length // 8, count=100000, hmac_hash_module=SHA256)

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileEncryptorApp()
    window.show()
    sys.exit(app.exec_())
