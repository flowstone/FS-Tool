from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar
from PyQt5.QtCore import pyqtSignal, QObject


class ProgressTool:
    def __init__(self):
        # 创建用于承载进度条的窗口部件
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        # 创建进度条实例
        self.progress_bar = QProgressBar(self.widget)
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_bar)

    def show(self):
        """显示包含进度条的窗口"""
        self.widget.show()

    def hide(self):
        """隐藏包含进度条的窗口"""
        self.widget.hide()

    def set_value(self, value):
        """设置进度条的值"""
        self.progress_bar.setValue(value)

    def set_range(self, min_value, max_value):
        """设置进度条的范围"""
        self.progress_bar.setRange(min_value, max_value)

    def set_format(self, format_str):
        """设置进度条显示的格式文本"""
        self.progress_bar.setFormat(format_str)

    def connect_update_function(self, func):
        """连接外部的更新函数，当需要更新进度时调用该函数"""
        self.progress_bar.valueChanged.connect(func)


class ProgressSignalEmitter(QObject):
    progress_signal = pyqtSignal(int)
    """用于在有进度更新时发出信号的类，方便在不同任务中触发进度更新"""
    def update_progress(self, value):
        self.progress_signal.emit(value)