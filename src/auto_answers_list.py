import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from loguru import logger
import math


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont, QColor, QBrush
import sqlite3

from src.fs_constants import FsConstants
from src.common_util import CommonUtil


class AutoAnswersList(QWidget):
    def __init__(self):
        super().__init__()
        self.page_size = 10  # 每页显示的数据条数，这里调整为更合理的值，可按需修改
        self.current_page = 1  # 当前页码
        self.total_pages = 1  # 总页数，初始化为1，后续会根据实际数据量计算更新
        self.init_ui()
        self.load_data()
        self.update_total_pages()  # 初始化时先计算总页数

    def init_ui(self):
        layout = QVBoxLayout()
        self.setFixedSize(730, 600)  # 设置窗口固定大小为宽700像素，高600像素
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        self.table = QTableWidget()

        BTN_STYLE = """
            QPushButton {
                background-color: gray;  /* 将表头背景色设置为淡蓝色 */
                border: none;
                color: black;
                padding: 5px 10px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 14px;
                margin: 4px 2px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #bbb;
            }
        """
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                background-color: #f9f9f9;
                gridline-color: #e0e0e0;
                alternate-background-color: #f0f0f0;
                selection-background-color: #007BFF;
                selection-color: white;
            }
            QTableWidget QHeaderView::section {
                background-color: #ADD8E6;  /* 将表头背景色设置为淡蓝色 */
                border: 1px solid #ccc;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
                color: black;
            }
            QTableWidget::item {
                color: black;
                padding: 6px;
            }
        """)
        layout.addWidget(self.table)

        button_layout = QHBoxLayout()

        prev_button = QPushButton('上一页')
        prev_button.clicked.connect(self.prev_page)
        prev_button.setStyleSheet(BTN_STYLE)
        button_layout.addWidget(prev_button)

        self.page_label = QLabel(f'第 {self.current_page} 页')
        self.page_label.setFont(QFont("Arial", 12))
        button_layout.addWidget(self.page_label)

        next_button = QPushButton('下一页')
        next_button.clicked.connect(self.next_page)
        next_button.setStyleSheet(BTN_STYLE)
        button_layout.addWidget(next_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setWindowTitle('自动答题日志')
        self.show()

    def load_data(self):
        conn = sqlite3.connect(CommonUtil.get_db_full_path())
        cursor = conn.cursor()
        sql = f"SELECT * FROM {FsConstants.AUTO_ANSWERS_TABLE_NAME}"
        if self.page_size and self.current_page:
            offset = (self.current_page - 1) * self.page_size
            sql += f" ORDER BY id DESC LIMIT {self.page_size} OFFSET {offset}"
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        # 获取列名（假设表结构固定，这里从第一条记录获取列名，实际可根据数据库元数据更灵活获取）
        if results:
            column_names = ["序列", "错误", "正确", "日期", "创建时间", "更新时间"]
            self.table.setColumnCount(len(column_names))
            self.table.setHorizontalHeaderLabels(column_names)

        self.table.setRowCount(len(results))

        for row_idx, row_data in enumerate(results):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                if col_idx % 2 == 0:
                    item.setBackground(QBrush(QColor("#f0f0f0")))
                else:
                    item.setBackground(QBrush(QColor("#f9f9f9")))
                self.table.setItem(row_idx, col_idx, item)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_data()
            self.page_label.setText(f'第 {self.current_page} 页')
        else:
            QMessageBox.information(self, "提示", "已经是第一页了，没有上一页哦！")
            logger.warning("已经是第一页了，没有上一页哦！")

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_data()
            self.page_label.setText(f'第 {self.current_page} 页')
        else:
            QMessageBox.information(self, "提示", "已经是最后一页了，没有下一页了！")
            logger.warning("已经是最后一页了，没有下一页了！")

    def update_total_pages(self):
        """
        通过查询数据库中数据的总记录数来计算总页数
        """
        conn = sqlite3.connect(CommonUtil.get_db_full_path())
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {FsConstants.AUTO_ANSWERS_TABLE_NAME}")
        total_records = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        #self.total_pages = total_records
        self.total_pages = math.ceil(total_records / self.page_size)
        #self.page_size + (1 if total_records % self.page_size > 0 else 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = AutoAnswersList()
    main_window.show()
    sys.exit(app.exec_())