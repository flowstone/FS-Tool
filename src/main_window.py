import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget,QGridLayout, QSystemTrayIcon, QMenu, QAction, QMainWindow,QMessageBox, QMenuBar

from src.batch_heic_jpg import HeicToJpgApp
from src.desktop_clock import ColorSettingDialog
from src.pic_conversion import PicConversionApp
from src.batch_file_renamer import RenameFileApp
from src.batch_create_folder import CreateFolderApp
from src.auto_answers import AutoAnswersApp
from src.stick_note import StickyNoteApp
from src.password_generator import  PasswordGeneratorApp
from src.file_comparator import FileComparatorApp
from src.file_generator import FileGeneratorApp
from src.file_encryptor import FileEncryptorApp

from PyQt5.QtGui import QIcon
from src.app_mini import FloatingBall
from loguru import logger
from src.common_util import CommonUtil
from src.fs_constants import FsConstants
from src.app_icon_widget import AppIconWidget
from src.menu_bar import MenuBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.floating_ball = FloatingBall(self)
        self.is_floating_ball_visible = False
        self.desktop_clock = None
        self.stick_note = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        logger.info(f"调用了主界面的初始化,悬浮球标志位 = {self.is_floating_ball_visible}")
        self.setWindowTitle(FsConstants.APP_WINDOW_TITLE)
        #self.setFixedSize(FsConstants.APP_WINDOW_WIDTH, FsConstants.APP_WINDOW_HEIGHT)

        # ---- 工具栏 START
        self.menubar = MenuBar(self)
        # ---- 工具栏 END

        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))


        # 透明时间
        time_app = AppIconWidget(CommonUtil.get_button_ico_path(FsConstants.BUTTON_TIME_ICON)
                                 ,FsConstants.DESKTOP_CLOCK_WINDOW_TITLE)
        # 快捷便签按钮
        stick_note_app = AppIconWidget(CommonUtil.get_button_ico_path(FsConstants.BUTTON_STICK_NOTE_ICON)
                                       ,FsConstants.STICK_NOTE_WINDOW_TITLE)
        # 图转大师按钮
        img_conv_app = AppIconWidget(CommonUtil.get_button_ico_path(FsConstants.BUTTON_PIC_ICON)
                                     ,FsConstants.PIC_CONVERSION_WINDOW_TITLE)
        # 文件夹创建按钮
        folder_app = AppIconWidget(CommonUtil.get_button_ico_path(FsConstants.BUTTON_FOLDER_ICON),
                                        FsConstants.CREATE_FOLDER_WINDOW_TITLE)
        # 重命名按钮
        rename_file_app = AppIconWidget(CommonUtil.get_button_ico_path(FsConstants.BUTTON_FILE_ICON),
                                      FsConstants.FILE_RENAMER_WINDOW_TITLE)
        # HEIC转JPG按钮
        heic_jpg_app = AppIconWidget(CommonUtil.get_button_ico_path(FsConstants.BUTTON_HEIC_ICON),
                                   FsConstants.HEIC_JPG_BUTTON_TITLE)
        # 自动答题按钮
        auto_answers_app = AppIconWidget(CommonUtil.get_button_ico_path(FsConstants.BUTTON_ANSWERS_ICON),
                                       FsConstants.AUTO_ANSWERS_WINDOW_TITLE)
        # 密码生成器
        password_generator_app = AppIconWidget(CommonUtil.get_button_ico_path(FsConstants.BUTTON_PASSWORD_ICON),
                                       FsConstants.PASSWORD_GENERATOR_TITLE)


        # 批量生成文件
        file_generator_app = AppIconWidget(CommonUtil.get_button_ico_path(FsConstants.BUTTON_FILE_GENERATOR_ICON),
                                         FsConstants.FILE_GENERATOR_WINDOW_TITLE)
        # 文件比较
        file_comparator_app = AppIconWidget(CommonUtil.get_button_ico_path(FsConstants.BUTTON_FILE_COMPARATOR_ICON),
                                               FsConstants.FILE_COMPARATOR_WINDOW_TITLE)
        # 文件加密
        file_encryptor_app = AppIconWidget(CommonUtil.get_button_ico_path(FsConstants.BUTTON_FILE_ENCRYPTOR_ICON),
                                     FsConstants.FILE_ENCRYPTOR_WINDOW_TITLE)

        time_app.iconClicked.connect(self.time_app_clicked)
        stick_note_app.iconClicked.connect(self.stick_note_app_clicked)
        img_conv_app.iconClicked.connect(self.img_conv_app_clicked)
        folder_app.iconClicked.connect(self.create_folder_app_clicked)
        rename_file_app.iconClicked.connect(self.rename_file_app_clicked)
        heic_jpg_app.iconClicked.connect(self.heic_jpg_app_clicked)
        auto_answers_app.iconClicked.connect(self.auto_answers_app_clicked)
        password_generator_app.iconClicked.connect(self.password_generator_app_clicked)
        file_generator_app.iconClicked.connect(self.file_generator_app_clicked)
        file_comparator_app.iconClicked.connect(self.file_comparator_app_clicked)
        file_encryptor_app.iconClicked.connect(self.file_encryptor_app_clicked)
        # 创建主布局
        main_layout = QGridLayout()
        main_layout.setSpacing(0)  # 去除格子之间的间隙

        # 将每个图标放入网格布局
        main_layout.addWidget(time_app, 0, 0)  # 第一行第一列
        main_layout.addWidget(stick_note_app, 0, 1)  # 第一行第二列
        main_layout.addWidget(password_generator_app, 0, 2)  # 第一行第三列
        main_layout.addWidget(folder_app, 0, 3)  # 第一行第四列
        main_layout.addWidget(rename_file_app, 1, 0)  # 第二行第一列
        main_layout.addWidget(heic_jpg_app, 1, 1)  # 第二行第二列
        main_layout.addWidget(img_conv_app, 1, 2)  # 第二行第三列
        main_layout.addWidget(auto_answers_app, 1, 3)  # 第二行第四列
        main_layout.addWidget(file_generator_app, 2, 0)  # 第二行第四列
        main_layout.addWidget(file_comparator_app, 2, 1)  # 第二行第二列
        main_layout.addWidget(file_encryptor_app, 2, 2)  # 第二行第三列
        layout.addLayout(main_layout)
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


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


    def time_app_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.DESKTOP_CLOCK_WINDOW_TITLE}>被点击了 ----")
        if self.desktop_clock is None:
            self.desktop_clock = ColorSettingDialog()
            self.desktop_clock.show()
        else:
            self.desktop_clock.show()

    def img_conv_app_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.PIC_CONVERSION_WINDOW_TITLE}>被点击了 ----")
        self.pic_conversion=PicConversionApp()
        self.pic_conversion.show()

    def create_folder_app_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.CREATE_FOLDER_WINDOW_TITLE}>被点击了 ----")
        self.create_folder = CreateFolderApp()
        self.create_folder.show()

    def rename_file_app_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.FILE_RENAMER_WINDOW_TITLE}>被点击了 ----")
        self.rename_file = RenameFileApp()
        self.rename_file.show()

    def heic_jpg_app_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.HEIC_JPG_WINDOW_TITLE}>被点击了 ----")
        self.heic_to_jpg = HeicToJpgApp()
        self.heic_to_jpg.show()

    def auto_answers_app_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.AUTO_ANSWERS_WINDOW_TITLE}>被点击了 ----")
        self.auto_answers = AutoAnswersApp()
        self.auto_answers.show()

    def stick_note_app_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.STICK_NOTE_WINDOW_TITLE}>被点击了 ----")
        if self.stick_note is None or not self.stick_note.isVisible():
            self.stick_note = StickyNoteApp()
            self.stick_note.show()
        else:
            if self.stick_note.isMinimized():
                self.stick_note.showNormal()
            else:
                self.stick_note.show()
                self.stick_note.activateWindow()

    def password_generator_app_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.PASSWORD_GENERATOR_TITLE}>被点击了 ----")
        self.password_generator = PasswordGeneratorApp()
        self.password_generator.show()

    def file_generator_app_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.PASSWORD_GENERATOR_TITLE}>被点击了 ----")
        self.file_generator = FileGeneratorApp()
        self.file_generator.show()
    def file_comparator_app_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.PASSWORD_GENERATOR_TITLE}>被点击了 ----")
        self.file_comparator = FileComparatorApp()
        self.file_comparator.show()
    def file_encryptor_app_clicked(self):
        logger.info(f"---- 按钮<{FsConstants.PASSWORD_GENERATOR_TITLE}>被点击了 ----")
        self.file_encryptor = FileEncryptorApp()
        self.file_encryptor.show()

