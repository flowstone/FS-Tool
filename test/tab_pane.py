import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QPushButton,QMenuBar,QMenu,QAction
from PyQt5.QtGui import QIcon
from src.fs_constants import FsConstants

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # ---- 工具栏 START
        menu_bar = QMenuBar(self)
        help_menu = QMenu(FsConstants.TOOLBAR_HELP_TITLE, self)
        menu_bar.addMenu(help_menu)

        # 创建”说明"菜单项
        readme_action = QAction(FsConstants.TOOLBAR_README_TITLE, self)
#        readme_action.triggered.connect(self.open_readme)

        # 创建"作者"菜单项
        author_action = QAction(FsConstants.TOOLBAR_AUTHOR_TITLE, self)
        #author_action.triggered.connect(self.open_author)
        # 将菜单项添加到文件菜单
        help_menu.addAction(readme_action)
        help_menu.addAction(author_action)
        layout.addWidget(menu_bar)
        # ---- 工具栏 END
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
                    QTabWidget::pane {
                        border: 1px solid #C2C7CB;  /* Tab页内容区域边框 */
                        background-color: white;  /* Tab页内容区域背景色 */
                    }
                    QTabBar::tab {
                        background-color: #E0E0E0;  /* 未选中Tab标签的背景色 */
                        color: #333333;  /* 未选中Tab标签的字体颜色 */
                        padding: 8px 12px;  /* 内边距 */
                    }
                    QTabBar::tab:selected {
                        background-color: #4CAF50;  /* 选中Tab标签的背景色 */
                        color: white;  /* 选中Tab标签的字体颜色 */
                    }
                    
                    QPushButton {
                        background-color: #4CAF50;  /* 按钮背景色 */
                        color: white;  /* 按钮字体颜色 */
                        border: none;  /* 无边框 */
                        border-radius: 5px;  /* 圆角半径 */
                        padding: 8px 16px;  /* 内边距 */
                    }
                    QPushButton:hover {
                        background-color: #45a049;  /* 鼠标悬停时的背景色 */
                    }
                    QPushButton:pressed {
                        background-color: #3e8e41;  /* 按钮按下时的背景色 */
                    }
                """)
        # 创建第一个Tab页面
        tab1_widget = QWidget()
        tab1_layout = QVBoxLayout()
        button1_1 = QPushButton("按钮1-1")
        button1_2 = QPushButton("按钮1-2")
        button1_3 = QPushButton("按钮1-3")
        tab1_layout.addWidget(button1_1)
        tab1_layout.addWidget(button1_2)
        tab1_layout.addWidget(button1_3)
        tab1_widget.setLayout(tab1_layout)
        tab1_icon = QIcon("../resources/icon/folder-icon.svg")

        self.tab_widget.addTab(tab1_widget,tab1_icon, "Tab 1")

        # 创建第二个Tab页面
        tab2_widget = QWidget()
        tab2_layout = QVBoxLayout()
        button2_1 = QPushButton("按钮2-1")
        button2_2 = QPushButton("按钮2-2")
        button2_3 = QPushButton("按钮2-3")
        tab2_layout.addWidget(button2_1)
        tab2_layout.addWidget(button2_2)
        tab2_layout.addWidget(button2_3)
        tab2_widget.setLayout(tab2_layout)
        self.tab_widget.addTab(tab2_widget, "Tab 2")

        # 创建第三个Tab页面
        tab3_widget = QWidget()
        tab3_layout = QVBoxLayout()
        button3_1 = QPushButton("按钮3-1")
        button3_2 = QPushButton("按钮3-2")
        button3_3 = QPushButton("按钮3-3")
        tab3_layout.addWidget(button3_1)
        tab3_layout.addWidget(button3_2)
        tab3_layout.addWidget(button3_3)
        tab3_widget.setLayout(tab3_layout)
        self.tab_widget.addTab(tab3_widget, "Tab 3")

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("QTabWidget示例")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())