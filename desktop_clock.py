import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QDialog, QComboBox, QHBoxLayout
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt, QTimer
from common_util import CommonUtil

class DesktopClockApp(QWidget):
    def __init__(self):
        super().__init__()
        self.elapsed_time = 0
        self.init_ui()
        self.selected_time_color = "white"
        self.selected_timer_color = "pink"

    def init_ui(self):
        # 设置窗口无边框、无标题栏
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置窗口背景透明
        self.setWindowTitle("桌面时钟")
        # 设置窗口透明度
        self.setWindowOpacity(0.8)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        self.setGeometry(0, 0, 200, 80)

        layout = QVBoxLayout()

        self.current_time = QLabel(self)
        self.current_time.setFont(QFont('Arial', 18))
        self.current_time.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.current_time)

        self.count_time = QLabel(self)
        self.count_time.setFont(QFont('Arial', 12, 75))
        self.count_time.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        layout.addWidget(self.count_time)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.setLayout(layout)

    def show_with_colors(self, time_color, timer_color):
        self.selected_time_color = time_color
        self.selected_timer_color = timer_color
        self.update_colors()
        self.timer.start(1000)
        self.show()

    def update_colors(self):
        """
         根据所选颜色更新时间显示文本的颜色
        """
        color_css = {
            "白色": "white",
            "粉色": "pink",
            "红色": "red",
            "绿色": "green",
            "blue": "blue"
        }
        self.current_time.setStyleSheet(f"color: {color_css[self.selected_time_color]};")
        self.count_time.setStyleSheet(f"color: {color_css[self.selected_timer_color]};")

    def update_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.current_time.setText(current_time)
        # 计时器
        self.elapsed_time += 1
        hours = self.elapsed_time // 3600
        minutes = (self.elapsed_time % 3600) // 60
        seconds = self.elapsed_time % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.count_time.setText(time_str)


class ColorSettingDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("颜色设置")
        self.setFixedSize(250, 150)  # 设置固定大小，让界面更规整
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        layout = QVBoxLayout()

        # 设置对话框整体的样式表，添加背景颜色等样式
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
            }
            QComboBox {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QPushButton {
                font-size: 14px;
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # 当前时间颜色选择行
        time_row_layout = QHBoxLayout()
        time_label = QLabel("时间")
        time_row_layout.addWidget(time_label)
        self.time_color_combobox = QComboBox(self)
        self.time_color_combobox.addItems(["白色", "粉色", "红色", "绿色", "蓝色"])
        time_row_layout.addWidget(self.time_color_combobox)
        layout.addLayout(time_row_layout)

        # 增加一些垂直间距，让布局更清晰
        layout.addSpacing(10)

        # 计时器颜色选择行
        timer_row_layout = QHBoxLayout()
        timer_label = QLabel("计时器")
        timer_row_layout.addWidget(timer_label)
        self.timer_color_combobox = QComboBox(self)
        self.timer_color_combobox.addItems(["白色", "粉色", "红色", "绿色", "蓝色"])
        timer_row_layout.addWidget(self.timer_color_combobox)
        layout.addLayout(timer_row_layout)

        layout.addSpacing(10)

        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.start_operation)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def get_selected_time_color(self):
        return self.time_color_combobox.currentText()

    def get_selected_timer_color(self):
        return self.timer_color_combobox.currentText()

    def start_operation(self):
        print("你点击了按钮")
        time_color = self.get_selected_time_color()
        timer_color = self.get_selected_timer_color()

        self.window = DesktopClockApp()
        self.window.show_with_colors(time_color, timer_color)
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    setting_dialog = ColorSettingDialog()
    setting_dialog.show()
    # if setting_dialog.exec_():
    #     time_color = setting_dialog.get_selected_time_color()
    #     timer_color = setting_dialog.get_selected_timer_color()
    #
    #     window = DesktopClockApp()
    #     window.show_with_colors(time_color, timer_color)

    sys.exit(app.exec_())