from PyQt5.QtWidgets import QMenuBar, QMenu, QAction, QMessageBox

from src.about_window import AboutWindow
from src.fs_constants import FsConstants
import sys,os
from src.common_util import CommonUtil
from loguru import logger
class MenuBar:
    def __init__(self, parent):
        self.parent = parent
        self.menu_bar = QMenuBar(self.parent)

        self._create_help_menu()
        self.about_window = AboutWindow()

    def _create_help_menu(self):
        """创建帮助菜单"""
        help_menu = QMenu(FsConstants.TOOLBAR_HELP_TITLE, self.parent)

        # 创建菜单项
        readme_action = QAction(FsConstants.TOOLBAR_README_TITLE, self.parent)
        readme_action.triggered.connect(open_readme)

        # 创建日志窗口菜单项
        about_action = QAction("关于", self.parent)
        about_action.triggered.connect(self.show_about_window)

        # 将菜单项添加到“帮助”菜单中
        help_menu.addAction(readme_action)
        help_menu.addAction(about_action)

        # 添加帮助菜单到菜单栏
        self.menu_bar.addMenu(help_menu)
        # 设置菜单栏
        self.parent.setMenuBar(self.menu_bar)

    def show_about_window(self):
         self.about_window.show()

def open_readme():
    try:
        file_path = CommonUtil.get_resource_path(FsConstants.HELP_PDF_FILE_PATH)
        # 使用系统默认的 PDF 阅读器打开文件
        if CommonUtil.check_win_os():
            os.startfile(file_path)  # Windows 平台
        else:
            os.system(f"open '{file_path}'")  # MacOS 平台

    except Exception as e:
        logger.error(f"无法打开 PDF 文件: {str(e)}")
