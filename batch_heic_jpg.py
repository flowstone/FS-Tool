import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMenuBar, QFileDialog
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt,pyqtSignal, QObject, QThread

from PyQt5.QtWidgets import QMessageBox
from loguru import logger
from common_util import CommonUtil
from fs_constants import FsConstants
import whatimage
import pillow_heif
from PIL import Image,ImageOps
from pillow_heif import register_heif_opener
import loading_util
# 注册HEIC文件 opener，使得PIL能够识别并打开HEIC格式文件，仅限V2方法使用
register_heif_opener()

class HeicToJpgApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info("---- 初始化HEIC转JPG ----")
        self.setWindowTitle(FsConstants.HEIC_JPG_WINDOW_TITLE)
        self.setWindowFlags(self.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)

        # 设置窗口背景色为淡灰色
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#F5F5F5"))
        self.setPalette(palette)

        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        layout = QVBoxLayout()





        # 选择文件夹相关部件
        folder_path_layout = QHBoxLayout()
        folder_path_label = QLabel("选择文件夹：")
        self.folder_path_input = QLineEdit()
        self.folder_path_input.setFixedWidth(300)
        self.folder_path_input.setObjectName("folder_path_input")


        browse_button = QPushButton("浏览")
        browse_button.setObjectName("browse_button")
        browse_button.clicked.connect(self.browse_folder)

        folder_path_layout.addWidget(folder_path_label)
        folder_path_layout.addWidget(self.folder_path_input)
        folder_path_layout.addWidget(browse_button)





        # 操作按钮
        button_layout = QHBoxLayout()
        start_button = QPushButton("开始")
        start_button.setObjectName("start_button")
        start_button.clicked.connect(self.start_operation)

        exit_button = QPushButton("退出")
        exit_button.setObjectName("exit_button")
        exit_button.clicked.connect(self.close)

        button_layout.addWidget(start_button)
        button_layout.addWidget(exit_button)

        layout.addLayout(folder_path_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)




    def browse_folder(self):
        logger.info("---- 开始选择文件夹 ----")
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.folder_path_input.setText(folder_path)



    def start_operation(self):
        logger.info("---- 开始执行操作 ----")
        folder_path = self.folder_path_input.text()


        if folder_path:
            logger.info("---- 有选择文件夹，开始执行操作 ----")
            self.setEnabled(False)  # 禁用按钮，防止多次点击

            self.worker = Worker()
            self.worker.folder_path = folder_path

            self.thread = QThread()
            self.worker.moveToThread(self.thread)
            self.worker.finished_signal.connect(self.worker_finished)
            self.worker.error_signal.connect(self.worker_error)  # 连接异常信号处理方法
            self.thread.started.connect(self.worker.do_work)

            self.thread.start()
        else:

            QMessageBox.warning(self, "警告", "请选择要操作的文件夹！")
    def worker_finished(self):
        self.setEnabled(True)
        self.thread.quit()  # 任务完成后，退出线程
        self.thread.wait()  # 等待线程真正结束，释放资源
        QMessageBox.information(self, "提示", "移动文件完成！")

    def worker_error(self, error_msg):
        logger.warning(f'任务出现错误: {error_msg}')
        self.setEnabled(True)
        self.thread.quit()
        self.thread.wait()
    # 创建文件夹，并移动到指定目录下
    # import whatimage
    # import pillow_heif
    # 但是个别HEIC图片无法识别
    @staticmethod
    def heic_to_jpg(folder_path):
        if folder_path:
            for root, dirs, files in os.walk(folder_path):
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
                                logger.info(f'已将 {file_path} 转换为 {new_file_path}')
                            except Exception as e:
                                logger.error(f'转换 {file_path} 时出错: {e}')




class Worker(QObject):
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)  # 新增信号，用于发送错误信息

    def do_work(self):
        try:
            self.heic_to_jpg_v2(self.folder_path)
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))  # 如果出现异常，发送异常信息

        # +++++ 最新方法 +++++
        # PIL导入Image
        # from PIL import Image,ImageOps
        # from pillow_heif import register_heif_opener
        # 注册HEIC文件 opener，使得PIL能够识别并打开HEIC格式文件
        # register_heif_opener()

    @staticmethod
    def heic_to_jpg_v2(folder_path):
        if folder_path:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.HEIC') or file.endswith('.heic'):
                        file_path = os.path.join(root, file)
                        try:
                            image = Image.open(file_path)
                            # 使用exif_transpose方法根据EXIF信息调整图像方向
                            image = ImageOps.exif_transpose(image)
                            file_name = file.split('.')[0] + '.jpg'
                            output_path = os.path.join(root, file_name)
                            image.convert('RGB').save(output_path, 'JPEG')
                            logger.info(f"{file_path} 已成功转换为 {output_path}")
                        except FileNotFoundError:
                            logger.error(f"文件 {file_path} 不存在，请检查路径。")
                        except IOError as e:
                            logger.warning(f"处理 {file_path} 时出现错误: {str(e)}")
            logger.info("所有HEIC图片转换完成！")