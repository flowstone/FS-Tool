import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QMessageBox, QMenuBar
from loguru import logger
from fs_constants import FsConstants

class AppMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        logger.info("---- 初始化工具栏 ----")
        # 创建"文件"菜单
        self.help_menu = self.create_help_menu()
        # 将创建好的菜单添加到菜单栏
        self.addMenu(self.help_menu)

        #self.setGeometry(100, 100, 800, 600)

    def create_help_menu(self):
        """
        创建文件菜单及其包含的菜单项
        """
        help_menu = QMenu(FsConstants.TOOLBAR_HELP_TITLE, self)

        # 创建”说明"菜单项
        readme_action = QAction(FsConstants.TOOLBAR_README_TITLE, self)
        readme_action.triggered.connect(self.open_readme)

        # 创建"作者"菜单项
        author_action = QAction(FsConstants.TOOLBAR_AUTHOR_TITLE, self)
        author_action.triggered.connect(self.open_author)
        # 将菜单项添加到文件菜单
        help_menu.addAction(readme_action)
        help_menu.addAction(author_action)
        return help_menu

    def open_readme(self):
        readme_text = FsConstants.APP_TOOLBAR_README_TEXT
        QMessageBox.information(self, FsConstants.TOOLBAR_README_TITLE, readme_text)

    def open_author(self):
        author_text = FsConstants.APP_TOOLBAR_AUTHOR_TEXT
        QMessageBox.information(self, FsConstants.TOOLBAR_AUTHOR_TITLE, author_text)


#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    window = AppMenuBar()
#    window.show()
#    sys.exit(app.exec_())