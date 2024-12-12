import sys
import os
import random
import string
import json
import csv

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QLabel, \
    QWidget, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont, QColor
from PIL import Image, ImageDraw, ImageFont  # 用于生成图片文件
from loguru import logger

class FileGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.folder_path = None

        self.setWindowTitle("批量生成文件")
        self.setFixedSize(450, 400)


        layout = QVBoxLayout()
        # 标题标签
        title_label = QLabel("批量生成文件")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("color: #4CAF50;")
        layout.addWidget(title_label)

        browse_layout = QHBoxLayout()
        # 输出目录选择
        self.output_folder_label = QLabel("输出目录")
        self.output_folder_label.setFont(QFont("Arial", 12))
        self.output_folder_label.setAlignment(Qt.AlignCenter)
        self.folder_path_entry = QLineEdit()
        self.folder_path_entry.setPlaceholderText("请选择要生成文件的目录")
        self.folder_path_entry.setObjectName("folder_path_input")
        self.select_folder_button = QPushButton("浏览")
        self.select_folder_button.setObjectName("browse_button")
        self.select_folder_button.clicked.connect(self.select_folder)
        browse_layout.addWidget(self.output_folder_label)
        browse_layout.addWidget(self.folder_path_entry)
        browse_layout.addWidget(self.select_folder_button)
        layout.addLayout(browse_layout)

        # 文件数量输入
        self.file_count_label = QLabel("文件数量：")
        layout.addWidget(self.file_count_label)

        self.file_count_input = QLineEdit()
        self.file_count_input.setPlaceholderText("请输入文件数量")

        layout.addWidget(self.file_count_input)

        # 文件大小输入
        self.file_size_label = QLabel("文件大小 (KB)：")
        layout.addWidget(self.file_size_label)

        self.file_size_input = QLineEdit()
        self.file_size_input.setPlaceholderText("请输入每个文件的大小")
        layout.addWidget(self.file_size_input)

        # 文件类型选择
        self.file_type_label = QLabel("文件类型：")
        layout.addWidget(self.file_type_label)

        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems(["文本文件", "图片文件", "JSON文件", "CSV文件"])
        self.file_type_combo.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #4CAF50;")
        layout.addWidget(self.file_type_combo)


        button_layout = QHBoxLayout()

        # 生成文件按钮
        self.generate_button = QPushButton("生成文件")
        self.generate_button.setObjectName("start_button")
        self.generate_button.clicked.connect(self.generate_files)
        button_layout.addWidget(self.generate_button)

        self.exit_button = QPushButton("退出")
        self.exit_button.setObjectName("exit_button")
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # 为了让控件不挤在一起，我们可以加入一些空间
        layout.addStretch(1)

    def select_folder(self):
        """打开文件夹选择对话框"""
        self.folder_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        logger.info(f"选择的输出目录：{self.folder_path}")

    def generate_files(self):
        """生成指定数量的文件"""
        file_count = self.file_count_input.text()
        file_size = self.file_size_input.text()

        # 校验输入
        if not file_count.isdigit() or not file_size.isdigit():
            logger.warning("请输入有效的文件数量和文件大小！")
            self.show_message("警告", "请输入有效的文件数量和文件大小！")
            return

        file_count = int(file_count)
        file_size = int(file_size) * 1024  # 转换为字节

        if file_count <= 0 or file_size <= 0:
            logger.warning("文件数量和文件大小必须大于零！")
            self.show_message("警告", "文件数量和文件大小必须大于零！")
            return

        if not self.folder_path:
            logger.warning("请先选择输出目录！")
            self.show_message("警告", "请先选择输出目录！")
            return

        file_type = self.file_type_combo.currentText()

        # 生成文件
        try:
            for i in range(file_count):
                if file_type == "文本文件":
                    self.generate_text_file(i + 1, file_size)
                elif file_type == "图片文件":
                    self.generate_image_file(i + 1, file_size)
                elif file_type == "JSON文件":
                    self.generate_json_file(i + 1, file_size)
                elif file_type == "CSV文件":
                    self.generate_csv_file(i + 1, file_size)

            logger.info(f"{file_count} 个文件已成功生成！")
            self.show_message("成功", f"{file_count} 个文件已成功生成！")
        except Exception as e:
            logger.warning(f"生成文件失败：{str(e)}")
            self.show_message("错误", f"生成文件失败：{str(e)}")

    def generate_text_file(self, index, size):
        """生成文本文件"""
        file_name = f"file_{index}.txt"
        file_path = os.path.join(self.folder_path, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            random_content = self.generate_random_content(size)
            f.write(random_content)

    def generate_image_file(self, index, size):
        """生成图片文件"""
        file_name = f"file_{index}.png"
        file_path = os.path.join(self.folder_path, file_name)

        # 计算图片的尺寸，假设每KB为1024字节，1字节 = 1个像素
        width = int(size ** 0.5)
        height = int(size / width)

        # 创建图片
        image = Image.new('RGB', (width, height), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        image.save(file_path)

    def generate_json_file(self, index, size):
        """生成JSON文件"""
        file_name = f"file_{index}.json"
        file_path = os.path.join(self.folder_path, file_name)

        # 生成随机JSON数据
        data = {
            "id": index,
            "name": f"Random File {index}",
            "content": self.generate_random_content(size)
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def generate_csv_file(self, index, size):
        """生成CSV文件"""
        file_name = f"file_{index}.csv"
        file_path = os.path.join(self.folder_path, file_name)

        # 生成随机CSV数据
        headers = ["ID", "Name", "Content"]
        rows = [
            [index, f"Random File {index}", self.generate_random_content(size)]
        ]

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    def generate_random_content(self, size):
        """生成指定大小的随机内容"""
        characters = string.ascii_letters + string.digits + string.punctuation
        random_content = ''.join(random.choice(characters) for _ in range(size))
        return random_content

    def show_message(self, title, message):
        """显示信息框"""
        QMessageBox.information(self, title, message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileGeneratorApp()
    window.show()
    sys.exit(app.exec_())
