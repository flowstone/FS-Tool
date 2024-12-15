import sys
import random
import string

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QSpinBox
)
from loguru import logger

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from src.fs_constants import FsConstants
from src.common_util import CommonUtil

class PasswordGeneratorApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal =  pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle(FsConstants.PASSWORD_GENERATOR_TITLE)
        self.setFixedSize(500, 350)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

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

        self.label.setFont(QFont("Arial", 16, QFont.Bold))
        self.label.setStyleSheet("color: #0078d7;")
        self.generated_password.setFont(QFont("Courier", 14))
        self.exclude_input.setFont(QFont("Courier", 12))

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec_())
