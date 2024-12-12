from PyQt5.QtWidgets import QMenuBar, QMenu, QAction, QMessageBox
from src.fs_constants import FsConstants

class MenuBar:
    def __init__(self, parent):
        self.parent = parent
        self.menu_bar = QMenuBar(self.parent)

        self._create_help_menu()

    def _create_help_menu(self):
        """创建帮助菜单"""
        help_menu = QMenu(FsConstants.TOOLBAR_HELP_TITLE, self.parent)

        # 创建菜单项
        readme_action = QAction(FsConstants.TOOLBAR_README_TITLE, self.parent)
        readme_action.triggered.connect(self.open_readme)

        author_action = QAction(FsConstants.TOOLBAR_AUTHOR_TITLE, self.parent)
        author_action.triggered.connect(self.open_author)

        # 将菜单项添加到“帮助”菜单中
        help_menu.addAction(readme_action)
        help_menu.addAction(author_action)

        # 添加帮助菜单到菜单栏
        self.menu_bar.addMenu(help_menu)

        # 设置菜单栏
        self.parent.setMenuBar(self.menu_bar)



    def open_readme(self):
        readme_text = FsConstants.APP_TOOLBAR_README_TEXT
        QMessageBox.information(self.parent, FsConstants.TOOLBAR_README_TITLE, readme_text)

    def open_author(self):
        author_text = FsConstants.APP_TOOLBAR_AUTHOR_TEXT
        QMessageBox.information(self.parent, FsConstants.TOOLBAR_AUTHOR_TITLE, author_text)