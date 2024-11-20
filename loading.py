from PyQt5.Qt import *


class LoadingMask(QMainWindow):
    def __init__(self, parent, gif=None, tip=None):
        super(LoadingMask, self).__init__(parent)
        self.parent_enabled = parent.isEnabled()  # 记录父窗口初始可交互状态
        parent.setEnabled(False)  # 禁用父窗口交互

        self.label = QLabel()
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置窗口背景透明

        if not tip is None:
            self.label.setText(tip)
            font = QFont('Microsoft YaHei', 10, QFont.Normal)
            font_metrics = QFontMetrics(font)
            self.label.setFont(font)
            self.label.setFixedSize(font_metrics.width(tip, len(tip)) + 10, font_metrics.height() + 5)
            self.label.setAlignment(Qt.AlignCenter)

        if not gif is None:
            self.movie = QMovie(gif)
            self.label.setMovie(self.movie)
            self.label.setFixedSize(QSize(160, 160))
            self.label.setScaledContents(True)
            self.movie.start()

        layout = QHBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        layout.addWidget(self.label)

        self.setCentralWidget(widget)
        self.setWindowOpacity(0.8)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.hide()

    def eventFilter(self, widget, event):
        if widget == self.parent() and type(event) == QMoveEvent:
            self.moveWithParent()
            return True
        return super(LoadingMask, self).eventFilter(widget, event)

    def moveWithParent(self):
        if self.isVisible():
            self.move(self.parent().geometry().x(), self.parent().geometry().y())
            self.setFixedSize(QSize(self.parent().geometry().width(), self.parent().geometry().height()))

    def hide(self):
        super(LoadingMask, self).hide()
        self.parent().setEnabled(self.parent_enabled)  # 恢复父窗口可交互状态


    @staticmethod
    def showToast(window, tip='加载中...', duration=500):
        mask = LoadingMask(window, tip=tip)
        mask.show()
        # 一段时间后移除组件
        QTimer().singleShot(duration, lambda: mask.deleteLater())