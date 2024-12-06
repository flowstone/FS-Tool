import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QCheckBox, QFileDialog, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from loguru import logger
from common_util import CommonUtil
from fs_constants import FsConstants
from progress_tool import ProgressTool

class PicConversionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info("---- 初始化图片格式转换应用 ----")
        self.setWindowTitle(FsConstants.PIC_CONVERSION_WINDOW_TITLE)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        self.setFixedSize(FsConstants.PIC_CONVERSION_WINDOW_WIDTH, FsConstants.PIC_CONVERSION_WINDOW_HEIGHT)


        # 用于存储上传的图片路径
        self.image_path = None
        self.preview_image = None

        layout = QVBoxLayout()

        # 创建上传图片按钮
        self.upload_button = QPushButton("上传图片")
        self.upload_button.setObjectName("browse_button")
        self.upload_button.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)
        # 创建用于显示上传图片的标签
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # 创建复选框框架（这里使用水平布局让复选框在一行显示）
        self.checkbox_frame = QWidget(self)
        checkbox_layout = QHBoxLayout()
        self.checkbox_frame.setLayout(checkbox_layout)

        # 定义支持的目标格式
        self.target_formats = ["JPEG", "PNG", "GIF", "BMP", "WEBP", "ICO"]
        self.selected_formats = []

        # 创建复选框并添加到水平布局中
        for format in self.target_formats:
            checkbox = QCheckBox(format)
            checkbox.stateChanged.connect(lambda state, f=format: self.toggle_format(f, state))
            checkbox_layout.addWidget(checkbox)

        layout.addWidget(self.checkbox_frame)

        # 创建按钮所在的水平布局（用于放置转换按钮和关闭按钮）
        button_layout = QHBoxLayout()

        # 创建转换按钮
        self.convert_button = QPushButton("转换")
        self.convert_button.setEnabled(False)
        self.convert_button.setObjectName("start_button")
        self.convert_button.clicked.connect(self.convert_image)
        button_layout.addWidget(self.convert_button)

        # 创建关闭按钮
        self.close_button = QPushButton("关闭")
        self.close_button.setObjectName("exit_button")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)




    def upload_image(self):
        logger.info("---- 开始上传图片 ----")
        self.image_path = QFileDialog.getOpenFileName(self, "选择图片", "", "图片文件 (*.jpg *.png *.gif *.bmp *.webp *.ico)")[0]
        if self.image_path:
            logger.info(f"已上传图片: {self.image_path}")
            try:
                self.preview_image = Image.open(self.image_path)
                pixmap = QPixmap(self.image_path)
                self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(), aspectRatioMode=1))
            except Exception as e:
                logger.error(f"显示图片时出错: {e}")

    def toggle_format(self, format, state):
        if state == 2:  # 表示选中状态（PyQt中选中为2，未选中为0）
            self.selected_formats.append(format)
        else:
            self.selected_formats.remove(format) if format in self.selected_formats else None
        logger.info(f"----{self.selected_formats}")
        # 根据是否有复选框被选中来更新转换按钮的状态
        if len(self.selected_formats) > 0:
            self.convert_button.setEnabled(True)
        else:
            self.convert_button.setEnabled(False)

    def convert_image(self):
        self.progress_tool = ProgressTool(self)

        if not self.image_path:
            logger.warning("---- 请先上传图片! ----")
            return

        self.setEnabled(False)
        self.worker_thread = ImageConversionThread(self.image_path, self.selected_formats, self.progress_tool)
        self.worker_thread.finished_signal.connect(self.conversion_finished)
        self.worker_thread.error_signal.connect(self.conversion_error)
        self.worker_thread.start()
        self.progress_tool.show()

    def conversion_finished(self):
        logger.info("---- 图片转换完成 ----")
        self.progress_tool.hide()
        self.setEnabled(True)
        logger.info(
            f"图片已成功转换为所选格式，保存路径分别为: {[f'{os.path.splitext(self.image_path)[0]}.{f.lower()}' for f in self.selected_formats]}")
        QMessageBox.information(self, "提示", "移动文件完成！")


    def conversion_error(self, error_msg):
        logger.error(f"转换图片时出错: {error_msg}")
        self.progress_tool.hide()
        self.setEnabled(True)
        QMessageBox.information(self, "警告", "遇到异常停止工作")

class ImageConversionThread(QThread):
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, image_path, selected_formats, progress_tool):
        super().__init__()
        self.image_path = image_path
        self.selected_formats = selected_formats
        self.progress_tool = progress_tool

    def run(self):
        try:

            self.progress_tool.set_range(0, 0)

            image = Image.open(self.image_path)
            for target_format in self.selected_formats:
                base_name, ext = os.path.splitext(self.image_path)
                new_image_path = f"{base_name}.{target_format.lower()}"
                if target_format == "JPEG":
                    image = image.convert('RGB')
                elif target_format == "ICO":
                    image = image.convert('RGB') if image.mode!= 'RGB' else image
                    image.save(new_image_path, format='ICO')
                    continue
                elif target_format == "WEBP":
                    image = image.convert('RGB') if image.mode!= 'RGB' else image
                image.save(new_image_path)

            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PicConversionApp()
    window.show()
    sys.exit(app.exec_())