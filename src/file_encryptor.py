import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QWidget, QMessageBox,
    QComboBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from src.fs_constants import FsConstants

class FileEncryptorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(FsConstants.FILE_ENCRYPTOR_WINDOW_TITLE)
        self.setFixedSize(500, 450)


        layout = QVBoxLayout()

        # 应用标题
        title_label = QLabel("批量文件加密")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2E86C1;")
        layout.addWidget(title_label)

        # 应用说明
        desc_label = QLabel("通过 AES 加密算法加密或解密指定文件夹内的所有文件。\n"
                            "支持密钥长度 128/192/256 位，请输入密码进行加密操作。")
        desc_label.setFont(QFont("Arial", 12))
        desc_label.setAlignment(Qt.AlignCenter)
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
        key = password.encode("utf-8").ljust(key_length // 8)[:key_length // 8]

        try:
            for root, _, files in os.walk(self.selected_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as f:
                        data = f.read()

                    # 使用 AES 加密
                    cipher = AES.new(key, AES.MODE_CBC)
                    ciphertext = cipher.encrypt(pad(data, AES.block_size))

                    # 保存加密文件
                    encrypted_file = file_path + ".enc"
                    with open(encrypted_file, "wb") as f:
                        f.write(cipher.iv)  # 写入初始化向量
                        f.write(ciphertext)

                    # 可选：删除原文件
                    os.remove(file_path)

            QMessageBox.information(self, "成功", f"文件夹内的文件已成功加密！")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"加密失败：{str(e)}")

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
        key = password.encode("utf-8").ljust(key_length // 8)[:key_length // 8]

        try:
            for root, _, files in os.walk(self.selected_folder):
                for file in files:
                    if not file.endswith(".enc"):
                        continue

                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as f:
                        iv = f.read(16)  # 读取初始化向量
                        ciphertext = f.read()

                    # 使用 AES 解密
                    cipher = AES.new(key, AES.MODE_CBC, iv)
                    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

                    # 保存解密文件
                    decrypted_file = file_path.replace(".enc", "")
                    with open(decrypted_file, "wb") as f:
                        f.write(plaintext)

                    # 可选：删除加密文件
                    os.remove(file_path)

            QMessageBox.information(self, "成功", f"文件夹内的文件已成功解密！")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"解密失败：{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileEncryptorApp()
    window.show()
    sys.exit(app.exec_())
