import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton,  QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QFont, QPalette, QColor
from desktop_clock import DesktopClockApp
from pic_conversion import PicConversionApp
from batch_file_renamer import RenameFileApp
from batch_create_folder import CreateFolderApp
from PyQt5.QtGui import QIcon
from app_mini import FloatingBall
import  os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        print("你调用了主界面的构造方法")
        self.setWindowTitle("流体石头的工具箱")
        self.setGeometry(100, 100, 300, 250)
        self.setStyleSheet("background-color: #F5F5F5;")  # 设置窗口背景色为淡灰色
        # 悬浮球可见状态，false可以创建悬浮球，反之。。。
        self.is_floating_ball_visible = False
        self.is_tray_icon_visible = False

        self.setWindowIcon(QIcon(self.get_resource_path("resources/app.ico")))

        layout = QVBoxLayout()
        # 透明时间
        time_btn = QPushButton("透明时间")
        time_btn.setFont(QFont('Arial', 14))  # 设置字体
        time_btn.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #007B9A;
            }
        """)
        time_btn.clicked.connect(self.time_btn_clicked)
        layout.addWidget(time_btn)

        # 图转大师
        img_conv_btn = QPushButton("图转大师")
        img_conv_btn.setFont(QFont('Arial', 14))
        img_conv_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        img_conv_btn.clicked.connect(self.img_conv_btn_clicked)
        layout.addWidget(img_conv_btn)

        # 文件夹创建师
        create_folder_btn = QPushButton("文件夹创建师")
        create_folder_btn.setFont(QFont('Arial', 14))
        create_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        create_folder_btn.clicked.connect(self.create_folder_btn_clicked)
        layout.addWidget(create_folder_btn)

        # 重命名使者
        rename_file_btn = QPushButton("重命名使者")
        rename_file_btn.setFont(QFont('Arial', 14))
        rename_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #8E24AA;
            }
        """)
        rename_file_btn.clicked.connect(self.rename_file_btn_clicked)
        layout.addWidget(rename_file_btn)

        self.setLayout(layout)

        # 处理窗口关闭事件，使其最小化到托盘
        self.closeEvent = self.handle_close_event

        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.get_resource_path("resources/app_mini.ico")))  # 这里需要一个名为icon.png的图标文件，可以替换为真实路径
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # 创建托盘菜单
        tray_menu = QMenu()
        show_action = QAction("主界面", self)
        show_action.triggered.connect(self.tray_menu_show_main)
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(sys.exit)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)

    def get_resource_path(self, relative_path):
        """
        获取资源（如图片等）的实际路径，处理打包后资源路径的问题
        """
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

    # 从托盘菜单点击显示窗口
    def tray_menu_show_main(self):
        self.show()
        # 悬浮球退出
        if  self.is_floating_ball_visible:
            self.floating_ball.close()
            self.is_floating_ball_visible = False


    # 处理窗口关闭事件
    def handle_close_event(self, event):
        event.ignore()
        self.hide()

        print(f"关闭窗口时，is_tray_icon_visible：,{self.is_tray_icon_visible}")
        if not self.is_tray_icon_visible:
            self.tray_icon.show()
            self.is_tray_icon_visible = True


        if not self.is_floating_ball_visible:
            self.create_floating_ball()

    def create_floating_ball(self):
        self.floating_ball = FloatingBall()
        # 连接子窗口的信号到主窗口的槽函数
        self.floating_ball.value_changed_signal.connect(self.update_tray_icon_visible)
        self.floating_ball.show()
        self.is_floating_ball_visible = True

    def update_tray_icon_visible(self, value):
        if value:
            print("信号状态: 已接收 - True")
        else:
            print("信号状态: 已接收 - False")
        # 更新主窗口is_tray_icon_visible值
        self.is_tray_icon_visible = value
        print(f"信号更新后，is_tray_icon_visible：{self.is_tray_icon_visible}")

    # 双击托盘，打开窗口
    def tray_icon_activated(self, reason):
        print("你双击了任务栏托盘，打开窗口")
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            # 悬浮球退出
            if self.is_floating_ball_visible:
                self.floating_ball.close()
                self.is_floating_ball_visible = False

    def time_btn_clicked(self):
        print("按钮<透明时间>被点击了")
        self.desktop_clock = DesktopClockApp()
        self.desktop_clock.show()

    def img_conv_btn_clicked(self):
        print("按钮<图转大师>被点击了")
        self.pic_conversion=PicConversionApp()
        self.pic_conversion.show()

    def create_folder_btn_clicked(self):
        print("按钮<文件夹创建师>被点击了")
        self.rename_file = RenameFileApp()
        self.rename_file.show()

    def rename_file_btn_clicked(self):
        print("按钮<重命名使者>被点击了")
        self.create_folder = CreateFolderApp()
        self.create_folder.show()

