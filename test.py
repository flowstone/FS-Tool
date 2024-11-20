import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.button = QPushButton('点击我')
        self.button.clicked.connect(self.change_button_text)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.setWindowTitle('示例窗口')
        self.show()

    def change_button_text(self):
        self.setEnabled(False)
        self.button.setText('已点击')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())