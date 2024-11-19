import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton,QLabel


# 子界面类
class SubWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("这是子界面")
        layout.addWidget(label)
        self.setLayout(layout)


# 主界面类
class MainWindow(QWidget):
    # 自定义一个信号，用于触发显示子界面的操作
    show_sub_widget_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        button = QPushButton("打开子界面")
        button.clicked.connect(self.emit_show_signal)
        layout.addWidget(button)
        self.setLayout(layout)

    def emit_show_signal(self):
        self.show_sub_widget_signal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sub_widget = SubWidget()

    # 将主界面的信号与显示子界面的槽函数连接起来
    main_window.show_sub_widget_signal.connect(sub_widget.show)

    main_window.show()
    sys.exit(app.exec_())