import sys
import os
import whatimage
import pillow_heif
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog


class ImageConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 选择文件夹按钮
        self.select_folder_button = QPushButton('选择文件夹')
        self.select_folder_button.clicked.connect(self.selectFolder)
        # 设置按钮样式
        self.select_folder_button.setStyleSheet(
            "QPushButton {"
            "    background-color: #007BFF;"
            "    color: white;"
            "    border: none;"
            "    padding: 10px 20px;"
            "    border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #0056b3;"
            "}"
        )
        layout.addWidget(self.select_folder_button)

        # 开始转换按钮
        self.start_button = QPushButton('开始')
        self.start_button.clicked.connect(self.startConversion)
        self.start_button.setEnabled(False)
        # 设置按钮样式
        self.start_button.setStyleSheet(
            "QPushButton {"
            "    background-color: #28a745;"
            "    color: white;"
            "    border: none;"
            "    padding: 10px 20px;"
            "    border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #218838;"
            "}"
        )
        layout.addWidget(self.start_button)

        self.setLayout(layout)
        self.setWindowTitle('HEIC转JPG工具')
        # 设置窗口大小
        self.setFixedSize(400, 200)
        self.show()

        self.folder_path = None

    def selectFolder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, '选择包含HEIC图片的文件夹')
        if self.folder_path:
            self.start_button.setEnabled(True)

    def startConversion(self):
        if self.folder_path:
            for root, dirs, files in os.walk(self.folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                        fmt = whatimage.identify_image(file_data)
                        if fmt == 'heic':
                            try:
                                heif_file = pillow_heif.read_heif(file_path)
                                image = Image.frombytes(mode=heif_file.mode, size=heif_file.size, data=heif_file.data)
                                new_file_name = os.path.splitext(file)[0] + '.jpg'
                                new_file_path = os.path.join(root, new_file_name)
                                image.save(new_file_path, 'JPEG')
                                print(f'已将 {file_path} 转换为 {new_file_path}')
                            except Exception as e:
                                print(f'转换 {file_path} 时出错: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageConverter()
    sys.exit(app.exec_())