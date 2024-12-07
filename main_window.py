import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSystemTrayIcon, QMenu, QAction, QToolBar, QMainWindow
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.Qt import QStyle

from batch_heic_jpg import HeicToJpgApp
from desktop_clock import ColorSettingDialog
from pic_conversion import PicConversionApp
from batch_file_renamer import RenameFileApp
from batch_create_folder import CreateFolderApp
from auto_answers import AutoAnswersApp
from stick_note import StickyNoteApp
from PyQt5.QtGui import QIcon
from app_mini import FloatingBall
import  os
from loguru import logger
from common_util import CommonUtil
from app_menu_bar import AppMenuBar
from fs_constants import FsConstants

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.floating_ball = FloatingBall(self)
        # 悬浮球可见状态，false可以创建悬浮球，反之。。。
        self.is_floating_ball_visible = False

        self.init_ui()

    def init_ui(self):



        logger.info(f"调用了主界面的初始化,悬浮球标志位 = {self.is_floating_ball_visible}")
        self.setWindowTitle(FsConstants.APP_WINDOW_TITLE)
        #self.setFixedSize(FsConstants.APP_WINDOW_WIDTH, FsConstants.APP_WINDOW_HEIGHT)
        self.setFixedWidth(FsConstants.APP_WINDOW_WIDTH)

        layout = QVBoxLayout()

        # ---- 导入外部的工具栏
        self.app_menu_bar = AppMenuBar(self)
        layout.addWidget(self.app_menu_bar)
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        # ++++ 导入外部的工具栏


        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        # 透明时间
        time_btn = QPushButton(QIcon(CommonUtil.get_button_ico_path(FsConstants.BUTTON_TIME_ICON)),FsConstants.DESKTOP_CLOCK_WINDOW_TITLE)
        time_btn.setObjectName("feature")
        time_btn.clicked.connect(self.time_btn_clicked)
        layout.addWidget(time_btn)

        # 图转大师
        img_conv_btn = QPushButton(QIcon(CommonUtil.get_button_ico_path(FsConstants.BUTTON_PIC_ICON)),FsConstants.PIC_CONVERSION_WINDOW_TITLE)
        img_conv_btn.setObjectName("feature")
        img_conv_btn.clicked.connect(self.img_conv_btn_clicked)
        layout.addWidget(img_conv_btn)

        # 文件夹创建师
        create_folder_btn = QPushButton(QIcon(CommonUtil.get_button_ico_path(FsConstants.BUTTON_FOLDER_ICON)),FsConstants.CREATE_FOLDER_WINDOW_TITLE)
        create_folder_btn.setObjectName("feature")
        create_folder_btn.clicked.connect(self.create_folder_btn_clicked)
        layout.addWidget(create_folder_btn)

        # 重命名使者
        rename_file_btn = QPushButton(QIcon(CommonUtil.get_button_ico_path(FsConstants.BUTTON_FILE_ICON)),FsConstants.FILE_RENAMER_WINDOW_TITLE)
        rename_file_btn.setObjectName("feature")
        rename_file_btn.clicked.connect(self.rename_file_btn_clicked)
        layout.addWidget(rename_file_btn)

        # HEIC转JPG
        heic_jpg_btn = QPushButton(QIcon(CommonUtil.get_button_ico_path(FsConstants.BUTTON_HEIC_ICON)),FsConstants.HEIC_JPG_BUTTON_TITLE)
        heic_jpg_btn.setObjectName("feature")
        heic_jpg_btn.clicked.connect(self.heic_jpg_btn_clicked)
        layout.addWidget(heic_jpg_btn)

        # 自动答题
        auto_answers_btn = QPushButton(QIcon(CommonUtil.get_button_ico_path(FsConstants.BUTTON_ANSWERS_ICON)),FsConstants.AUTO_ANSWERS_WINDOW_TITLE)
        auto_answers_btn.setObjectName("feature")
        auto_answers_btn.clicked.connect(self.auto_answers_btn_clicked)
        layout.addWidget(auto_answers_btn)

        # 快捷便签
        stick_note_btn = QPushButton(QIcon(CommonUtil.get_button_ico_path(FsConstants.BUTTON_STICK_NOTE_ICON)),FsConstants.STICK_NOTE_WINDOW_TITLE)
        stick_note_btn.setObjectName("feature")
        stick_note_btn.clicked.connect(self.stick_note_btn_clicked)
        layout.addWidget(stick_note_btn)


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
            QIcon(CommonUtil.get_mini_ico_full_path()))  # 这里需要一个名为icon.png的图标文件，可以替换为真实路径
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
        # 悬浮球退出
        self.floating_ball.close()
        self.is_floating_ball_visible = False
        self.show()



    # 处理窗口关闭事件
    def handle_close_event(self, event):
        logger.info(f"开始关闭主窗口，悬浮球标志位 = ,{self.is_floating_ball_visible}")

        event.ignore()
        self.hide()
        self.tray_icon.show()


        if not self.is_floating_ball_visible:
            self.create_floating_ball()

        logger.info(f"成功关闭主窗口，悬浮球标志位 = ,{self.is_floating_ball_visible}")

    def create_floating_ball(self):
        logger.info("---- 创建悬浮球 ----")
        self.floating_ball.show()
        self.is_floating_ball_visible = True



    # 双击托盘，打开窗口
    def tray_icon_activated(self, reason):
        logger.info("---- 双击任务栏托盘，打开窗口 ----")
        # 悬浮球退出
        self.floating_ball.close()
        self.is_floating_ball_visible = False
        if reason == QSystemTrayIcon.DoubleClick:
           self.show()


    def time_btn_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.DESKTOP_CLOCK_WINDOW_TITLE}>被点击了 ----")
        self.desktop_clock = ColorSettingDialog()
        self.desktop_clock.show()

    def img_conv_btn_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.PIC_CONVERSION_WINDOW_TITLE}>被点击了 ----")
        self.pic_conversion=PicConversionApp()
        self.pic_conversion.show()

    def create_folder_btn_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.CREATE_FOLDER_WINDOW_TITLE}>被点击了 ----")
        self.create_folder = CreateFolderApp()
        self.create_folder.show()

    def rename_file_btn_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.FILE_RENAMER_WINDOW_TITLE}>被点击了 ----")
        self.rename_file = RenameFileApp()
        self.rename_file.show()

    def heic_jpg_btn_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.HEIC_JPG_WINDOW_TITLE}>被点击了 ----")
        self.heic_to_jpg = HeicToJpgApp()
        self.heic_to_jpg.show()

    def auto_answers_btn_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.AUTO_ANSWERS_WINDOW_TITLE}>被点击了 ----")
        self.auto_answers = AutoAnswersApp()
        self.auto_answers.show()

    def stick_note_btn_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.STICK_NOTE_WINDOW_TITLE}>被点击了 ----")
        self.stick_note = StickyNoteApp()
        self.stick_note.show()

