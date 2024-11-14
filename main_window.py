import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSystemTrayIcon, QMenu, QAction, QToolBar, QMainWindow
from PyQt5.QtGui import QFont, QPalette, QColor
from desktop_clock import DesktopClockApp
from pic_conversion import PicConversionApp
from batch_file_renamer import RenameFileApp
from batch_create_folder import CreateFolderApp
from PyQt5.QtGui import QIcon
from app_mini import FloatingBall
import  os
from loguru import logger
from path_util import PathUtil
from app_menu_bar import AppMenuBar


class MainWindow(QMainWindow):
    def __init__(self, tray_icon_visible=False):
        super().__init__()
        # 任务栏托盘标志位，False没有创建  True已创建
        self.is_tray_icon_visible = tray_icon_visible

        self.init_ui()

    def init_ui(self):
        logger.info(f"调用了主界面的初始化,任务栏托盘标志位 = {self.is_tray_icon_visible}")
        self.setWindowTitle("流体石头的工具箱")
        self.setGeometry(100, 100, 300, 250)
        self.setStyleSheet("background-color: #F5F5F5;")  # 设置窗口背景色为淡灰色

        layout = QVBoxLayout()

        # ---- 导入外部的工具栏
        self.app_menu_bar = AppMenuBar(self)
        layout.addWidget(self.app_menu_bar)
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        # ++++ 导入外部的工具栏

        # 悬浮球可见状态，false可以创建悬浮球，反之。。。
        self.is_floating_ball_visible = False
        self.setWindowIcon(QIcon(PathUtil.get_resource_path("resources/app.ico")))

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
        # 初始化应用托盘图标
        self.init_tray_menu()


        # 处理窗口关闭事件，使其最小化到托盘
        self.closeEvent = self.handle_close_event




    # 初始化应用托盘图标
    def init_tray_menu(self):
        logger.info("---- 初始化任务栏图标 ----")

        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(
            QIcon(PathUtil.get_resource_path("resources/app_mini.ico")))  # 这里需要一个名为icon.png的图标文件，可以替换为真实路径
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



    # 从托盘菜单点击显示窗口
    def tray_menu_show_main(self):
        logger.info("---- 托盘菜单点击显示窗口 ----")

        self.show()
        # 悬浮球退出
        if  self.is_floating_ball_visible:
            self.floating_ball.close()
            self.is_floating_ball_visible = False


    # 处理窗口关闭事件
    def handle_close_event(self, event):
        logger.info(f"开始关闭主窗口，任务栏托盘标志位 = ,{self.is_tray_icon_visible}")

        event.ignore()
        self.hide()

        if not self.is_tray_icon_visible:
            self.tray_icon.show()
            self.is_tray_icon_visible = True


        if not self.is_floating_ball_visible:
            self.create_floating_ball()

        logger.info(f"成功关闭主窗口，任务栏托盘标志位 = ,{self.is_tray_icon_visible}")

    def create_floating_ball(self):
        logger.info("---- 创建悬浮球 ----")
        self.floating_ball = FloatingBall()
        self.floating_ball.show()
        self.is_floating_ball_visible = True



    # 双击托盘，打开窗口
    def tray_icon_activated(self, reason):
        logger.info("---- 双击任务栏托盘，打开窗口 ----")
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            # 悬浮球退出
            if self.is_floating_ball_visible:
                self.floating_ball.close()
                self.is_floating_ball_visible = False

    def time_btn_clicked(self):
        logger.info("---- 按钮<透明时间>被点击了 ----")
        self.desktop_clock = DesktopClockApp()
        self.desktop_clock.show()

    def img_conv_btn_clicked(self):
        logger.info("---- 按钮<图转大师>被点击了 ----")
        self.pic_conversion=PicConversionApp()
        self.pic_conversion.show()

    def create_folder_btn_clicked(self):
        logger.info("---- 按钮<文件夹创建师>被点击了 ----")
        self.create_folder = CreateFolderApp()
        self.create_folder.show()

    def rename_file_btn_clicked(self):
        logger.info("---- 按钮<重命名使者>被点击了 ----")
        self.rename_file = RenameFileApp()
        self.rename_file.show()

