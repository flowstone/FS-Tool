import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import QThread
from src.progress_widget import ProgressWidget, ProgressSignalEmitter

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("任务进度模拟")
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet("background-color: #f0f0f0;")  # 设置背景色

        # 布局
        layout = QVBoxLayout()

        # 创建进度条
        self.progress_tool1 = ProgressWidget(self)  # 传递父窗口
        self.progress_tool1.set_range(0, 100)  # 设置进度条范围
        layout.addWidget(self.progress_tool1)

        # 创建按钮
        self.start_button = QPushButton("开始任务", self)
        self.start_button.clicked.connect(self.start_task)  # 连接按钮点击信号
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        # 创建 ProgressSignalEmitter 实例
        self.progress_signal_emitter1 = ProgressSignalEmitter()

        # 连接进度信号
        self.progress_signal_emitter1.progress_signal.connect(self.progress_tool1.set_value)

    def start_task(self):
        # 启动任务并更新进度条
        self.start_button.setEnabled(False)  # 禁用按钮防止重复点击
        self.progress_tool1.show()  # 显示进度条窗口

        # 创建并启动任务线程
        self.task_thread = TaskThread(self.progress_signal_emitter1)
        self.task_thread.finished.connect(self.on_task_finished)
        self.task_thread.start()

    def on_task_finished(self):
        # 任务完成后的处理
        self.start_button.setEnabled(True)  # 启用按钮
        self.progress_tool1.hide()  # 隐藏进度条窗口
        print("任务完成！")


class TaskThread(QThread):
    def __init__(self, progress_signal_emitter):
        super().__init__()
        self.progress_signal_emitter = progress_signal_emitter

    def run(self):
        # 模拟任务执行并更新进度
        for i in range(101):
            time.sleep(0.1)  # 模拟任务执行
            self.progress_signal_emitter.update_progress(i)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建主窗口
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
