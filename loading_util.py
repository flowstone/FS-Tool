import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

from common_util import CommonUtil
from loading import LoadingMask

# Loading显示
def show_loading_mask(self):
    self.loading_mask = LoadingMask(self, CommonUtil.get_loading_full_path(), '加载中...')
    self.loading_mask.show()

# 示例方法，禁止使用
def do_task_with_loading_mask(self):
    self.show_loading_mask()  # 先显示加载遮罩

    # 模拟耗时任务，这里简单地使用QTimer延迟3秒来模拟
    from PyQt5.QtCore import QTimer
    QTimer.singleShot(3000, self.task_finished)

# Loading隐藏
def task_finished(self):
    if hasattr(self, 'loading_mask'):
        self.loading_mask.hide()  # 隐藏加载遮罩
        delattr(self, 'loading_mask')  # 删除属性，避免后续误操作
    # 此处可添加任务完成后的其他逻辑，比如更新界面显示等