import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QMessageBox, QMenuBar
from loguru import logger


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

        self.setGeometry(100, 100, 800, 600)

    def create_help_menu(self):
        """
        创建文件菜单及其包含的菜单项
        """
        help_menu = QMenu("帮助", self)

        # 创建"打开"菜单项
        readme_action = QAction("说明", self)
        readme_action.triggered.connect(self.open_readme)

        # 创建"保存"菜单项
        author_action = QAction("作者", self)
        author_action.triggered.connect(self.open_author)
        # 将菜单项添加到文件菜单
        help_menu.addAction(readme_action)
        help_menu.addAction(author_action)
        return help_menu

    def open_readme(self):
        readme_text = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>HTML Editor-LDDGO.NET</title><link rel="stylesheet"href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/styles/default.min.css"type="text/css"></head><body><h2 style="text-align: center;">说明</h2><p>作者开发的小工具，目前只有Win端，如果有问题，可以去项目中提Issues，有时间会修复小问题。</p><h3><strong>功能</strong></h3><p><span style="color: #e03e2d;"><strong>【透明时间】</strong></span></p><p>主要为直播开发的小应用，在桌面左上角生成一个时间控件</p><p><strong><span style="color: #e03e2d;">【</span>图转大师<span style="color: #e03e2d;">】</span></strong></p><p>图片的格式转换，目前有很大问题，暂未修复</p><p><strong><span style="color: #e03e2d;">【</span>文件夹创建师<span style="color: #e03e2d;">】</span></strong></p><p>选择文件夹，找出相同部分的文件名，以它进行切割，如abc_123，以_分割的话，会创建abc文件夹，把abc相关的文件全部移动到文件夹中，不支持递归</p><p><span style="color: #3598db;"><strong><span style="color: #e03e2d;">【</span>重命名使者<span style="color: #e03e2d;">】</span></strong></span></p><p>选择文件夹，批量修改文件名，包括后缀，前缀，替换指定字符，不支持递归</p><p>&nbsp;</p><h3>项目地址</h3><p><span style="color: #e03e2d;">【</span><a href="https://github.com/flowstone/FS-Tool"target="_blank"rel="noopener">FS-Tool</a><span style="color: #e03e2d;">】</span><span>https://github.com/flowstone/FS-Tool</span></p><script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/highlight.min.js"type="text/javascript"></script><script type="text/javascript">hljs.highlightAll();</script></body></html>'
        QMessageBox.information(self, "说明", readme_text)

    def open_author(self):
        author_text = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>HTML Editor-LDDGO.NET</title><link rel="stylesheet"href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/styles/default.min.css"type="text/css"></head><body><h2 style="text-align: center;">作者</h2><p>没有特长的吗喽，哈哈哈</p><h3><strong>地址</strong></h3><p><span style="color: #e03e2d;"><strong>【<a href="https://github.com/flowstone">Github</a>】<span style="color: #000000;">https://github.com/flowstone/FS-Tool</span></strong></span></p><p><strong><span style="color: #e03e2d;">【</span><a href="http://blog.xueyao.tech/"><span style="color: #e03e2d;">博客</span></a><span style="color: #e03e2d;">】<span style="color: #000000;"></span></span></strong>文章基本不更新，但是域名注册了10年，到2034年结束</p><p><strong><span style="color: #e03e2d;">【</span>邮箱<span style="color: #e03e2d;">】<span style="color: #000000;"></span></span></strong>略，太多了不知道写哪个</p><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p><h4><span style="color: #3598db;"><strong>欢迎你的关注!</strong></span></h4><p><span style="color: #e03e2d;"><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;于202411.14&nbsp;&nbsp;23:45</strong></span></p><p>&nbsp;</p><script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/highlight.min.js"type="text/javascript"></script><script type="text/javascript">hljs.highlightAll();</script></body></html>'
        QMessageBox.information(self, "作者", author_text)


#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    window = AppMenuBar()
#    window.show()
#    sys.exit(app.exec_())