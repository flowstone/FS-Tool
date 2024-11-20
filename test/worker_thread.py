import sys
import time
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class Worker(QObject):
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)  # 新增信号，用于发送错误信息

    def do_work(self):
        try:
            # 模拟耗时任务，如网络请求或大数据处理
            time.sleep(3)
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))  # 如果出现异常，发送异常信息

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 创建按钮
        self.button = QPushButton('点击我')
        self.button.clicked.connect(self.start_worker)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: lightblue;
                color: black;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:disabled {
                background-color: gray;
                color: white;
            }
        """)  # 设置按钮样式，使禁用和启用状态更直观
        layout.addWidget(self.button)

        # 创建用于显示提示信息的标签
        self.status_label = QLabel(self)
        self.status_label.setAlignment(Qt.AlignCenter)
        font = QFont('Microsoft YaHei', 10, QFont.Normal)
        self.status_label.setFont(font)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.setWindowTitle('示例窗口')
        self.show()

    def start_worker(self):
        self.button.setEnabled(False)
        self.status_label.setText('任务正在执行，请稍候...')  # 显示任务执行提示信息

        self.worker = Worker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        self.worker.finished_signal.connect(self.worker_finished)
        self.worker.error_signal.connect(self.worker_error)  # 连接异常信号处理方法
        self.thread.started.connect(self.worker.do_work)

        self.thread.start()

    def worker_finished(self):
        self.status_label.setText('任务完成')
        self.button.setEnabled(True)
        self.thread.quit()  # 任务完成后，退出线程
        self.thread.wait()  # 等待线程真正结束，释放资源

    def worker_error(self, error_msg):
        self.status_label.setText(f'任务出现错误: {error_msg}')
        self.button.setEnabled(True)
        self.thread.quit()
        self.thread.wait()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())