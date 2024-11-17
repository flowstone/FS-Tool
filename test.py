import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt

from fs_constants import FsConstants
from sqlite_util import SQLiteTool
from common_util import CommonUtil


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        button = QPushButton('打开数据展示界面')
        button.clicked.connect(self.open_data_window)

        layout.addWidget(button)

        self.setLayout(layout)
        self.setWindowTitle('主界面')
        self.show()

    def open_data_window(self):
        self.data_window = DataWindow()

class DataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.page_size = 1  # 每页显示的数据条数
        self.current_page = 1  # 当前页码
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        layout.addWidget(self.table)

        button_layout = QHBoxLayout()

        prev_button = QPushButton('上一页')
        prev_button.clicked.connect(self.prev_page)
        button_layout.addWidget(prev_button)

        self.page_label = QLabel(f'第 {self.current_page} 页')
        button_layout.addWidget(self.page_label)

        next_button = QPushButton('下一页')
        next_button.clicked.connect(self.next_page)
        button_layout.addWidget(next_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setWindowTitle('数据展示界面')
        self.show()

    def load_data(self):
        offset = (self.current_page - 1) * self.page_size

        results = sqlite.read_page(FsConstants.AUTO_ANSWERS_TABLE_NAME,page_size=self.page_size, page_num=offset)

        self.table.setRowCount(len(results))
        self.table.setColumnCount(len(results[0]))

        for row_idx, row_data in enumerate(results):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.table.setItem(row_idx, col_idx, item)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_data()
            self.page_label.setText(f'第 {self.current_page} 页')

    def next_page(self):
        self.current_page += 1
        self.load_data()
        self.page_label.setText(f'第 {self.current_page} 页')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sqlite = SQLiteTool(CommonUtil.get_db_full_path())
    main_window = MainWindow()
    sys.exit(app.exec_())