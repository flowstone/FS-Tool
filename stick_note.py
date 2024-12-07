import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from common_util import CommonUtil
from fs_constants import FsConstants

class StickyNoteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setWindowTitle(FsConstants.STICK_NOTE_WINDOW_TITLE)

        self.text_edit = QTextEdit(self)
        self.text_edit.setFont(QFont('SimSun', 12))
        self.text_edit.setStyleSheet("""
            QTextEdit {
                border: 2px solid lightgray;
                border-radius: 5px;
                padding: 10px;
                background-color: white;
            }
        """)

        self.save_button = QPushButton('保存', self)
        self.save_button.setObjectName("start_button")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_note)

        self.clear_button = QPushButton('清空', self)
        self.clear_button.setObjectName("exit_button")
        self.clear_button.clicked.connect(self.clear_text)

        # 创建水平布局放置两个按钮
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addLayout(button_layout)
        layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(layout)
        self.resize(FsConstants.STICK_NOTE_WINDOW_WIDTH, FsConstants.STICK_NOTE_WINDOW_HEIGHT)
        self.setMinimumSize(FsConstants.STICK_NOTE_WINDOW_MIN_WIDTH, FsConstants.STICK_NOTE_WINDOW_MIN_HEIGHT)

    def save_note(self):
        note_text = self.text_edit.toPlainText().strip()
        if note_text:
            print(f'保存便签内容: {note_text}')
            QMessageBox.information(self, '保存成功', '便签内容已成功保存！')
        else:
            QMessageBox.warning(self, '内容为空', '请输入便签内容后再保存哦！')

    def clear_text(self):
        self.text_edit.clear()
        QMessageBox.information(self, '已清空', '便签内容已清空。')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StickyNoteApp()
    window.show()
    sys.exit(app.exec())