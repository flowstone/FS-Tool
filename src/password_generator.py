import sys
import random
import string
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QSpinBox
)
from loguru import logger

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("密码生成器")
        self.setGeometry(100, 100, 500, 350)

        # 初始化界面元素
        self.init_ui()

        # 应用样式表
        self.apply_styles()

    def init_ui(self):
        # 创建标签、输入框和按钮
        self.label = QLabel("生成的密码:")
        self.label.setAlignment(Qt.AlignCenter)
        self.generated_password = QLineEdit(self)
        self.generated_password.setReadOnly(True)

        # 排除字符输入框
        self.exclude_label = QLabel("排除字符:")
        self.exclude_input = QLineEdit(self)
        self.exclude_input.setText("0oO1iIlLq9g")

        # 选择字符类型
        self.include_digits = QCheckBox("包含数字")
        self.include_lowercase = QCheckBox("包含小写字母")
        self.include_uppercase = QCheckBox("包含大写字母")
        self.include_special = QCheckBox("包含特殊字符")

        # 设置默认选项
        self.include_digits.setChecked(True)
        self.include_lowercase.setChecked(True)
        self.include_uppercase.setChecked(True)

        # 密码长度输入框
        self.length_label = QLabel("密码长度:")
        self.password_length_input = QSpinBox(self)
        self.password_length_input.setRange(4, 64)  # 密码长度的范围
        self.password_length_input.setValue(16)  # 默认密码长度为 16

        # 生成密码按钮
        self.generate_button = QPushButton("生成密码", self)
        self.generate_button.clicked.connect(self.generate_password)

        # 布局
        layout = QVBoxLayout()
        options_layout = QHBoxLayout()
        options_layout.addWidget(self.include_digits)
        options_layout.addWidget(self.include_lowercase)
        options_layout.addWidget(self.include_uppercase)
        options_layout.addWidget(self.include_special)


        layout.addLayout(options_layout)
        layout.addWidget(self.exclude_label)
        layout.addWidget(self.exclude_input)
        layout.addWidget(self.length_label)
        layout.addWidget(self.password_length_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.label)
        layout.addWidget(self.generated_password)

        self.setLayout(layout)

    def generate_password(self):
        # 获取排除字符
        exclude_chars = self.exclude_input.text()

        # 获取选中的字符类型
        main_char_pool = ""
        special_char_pool = ""
        if self.include_digits.isChecked():
            main_char_pool += string.digits
        if self.include_lowercase.isChecked():
            main_char_pool += string.ascii_lowercase
        if self.include_uppercase.isChecked():
            main_char_pool += string.ascii_uppercase
        if self.include_special.isChecked():
            special_char_pool += string.punctuation

        # 去除排除字符后的字符池
        main_char_pool = ''.join(c for c in main_char_pool if c not in exclude_chars)
        special_char_pool = ''.join(c for c in special_char_pool if c not in exclude_chars)

        if not main_char_pool and not special_char_pool:
            logger.warning("字符池为空，请检查排除字符或选择字符类型")
            self.generated_password.setText("字符池为空，请检查排除字符或选择字符类型")
            return

        # 获取用户设置的密码长度
        password_length = self.password_length_input.value()

        # 确定特殊字符的数量（10%-40%）
        special_char_count = min(max(password_length // 10, 4), len(special_char_pool))
        main_char_count = password_length - special_char_count

        # 确保主字符池不为空
        if not main_char_pool:
            logger.warning("主字符池为空，请检查排除字符")
            self.generated_password.setText("主字符池为空，请检查排除字符")
            return

        # 随机生成密码
        password = (
            ''.join(random.choice(main_char_pool) for _ in range(main_char_count)) +
            ''.join(random.choice(special_char_pool) for _ in range(special_char_count))
        )

        # 打乱密码顺序
        password = ''.join(random.sample(password, len(password)))

        self.generated_password.setText(password)

    def apply_styles(self):
        """应用美化样式"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit {
                font-size: 14px;
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #fff;
            }
            QCheckBox {
                font-size: 14px;
                color: #555;
            }
            QSpinBox {
                font-size: 14px;
                padding: 4px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #fff;
            }
            QSpinBox::up-button {
                border: none;
                background-color: #8BC34A;
                height: 15px;
                width: 15px;
                border-radius: 5px;
            }
            
            QSpinBox::down-button {
                border: none;
                background-color: #F44336;
                height: 15px;
                width: 15px;
                border-radius: 5px;
            }
        
            QSpinBox::up-button:hover {
                background-color: #7CB342;
            }
        
            QSpinBox::down-button:hover {
                background-color: #E53935;
            }
            QPushButton {
                font-size: 14px;
                color: #fff;
                background-color: #0078d7;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
            QPushButton:pressed {
                background-color: #004a9b;
            }
        """)

        self.label.setFont(QFont("Arial", 16, QFont.Bold))
        self.label.setStyleSheet("color: #0078d7;")
        self.generated_password.setFont(QFont("Courier", 14))
        self.exclude_input.setFont(QFont("Courier", 12))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec_())
