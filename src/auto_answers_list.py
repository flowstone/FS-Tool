import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QProgressBar
from PyQt5.QtGui import QIcon, QColor, QBrush, QFont
from PyQt5.QtCore import Qt
from loguru import logger
import math
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel
import sqlite3
from src.fs_constants import FsConstants
from src.common_util import CommonUtil


class AutoAnswersList(QWidget):
    def __init__(self):
        super().__init__()
        self.page_size = 10  # 每页显示的数据条数
        self.current_page = 1  # 当前页码
        self.total_pages = 1  # 总页数，初始化为1
        self.init_ui()
        self.load_data()
        self.update_total_pages()  # 初始化时先计算总页数

    def init_ui(self):
        layout = QVBoxLayout()

        # 设置窗口大小和图标
        self.setFixedSize(730, 600)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setWindowTitle('自动答题日志')



        # 创建表格控件
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # 创建进度条控件
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # 设置为无限进度条
        self.progress_bar.setVisible(False)  # 默认不显示
        layout.addWidget(self.progress_bar)

        # 翻页按钮布局
        button_layout = QHBoxLayout()

        prev_button = QPushButton('上一页')
        prev_button.clicked.connect(self.prev_page)
        #prev_button.setIcon(QIcon("icons/prev.png"))  # 设置图标（需要提供prev.png）
        button_layout.addWidget(prev_button)

        self.page_label = QLabel(f'第 {self.current_page} 页')
        self.page_label.setFont(QFont("Arial", 12, QFont.Bold))
        button_layout.addWidget(self.page_label, alignment=Qt.AlignCenter)  # 将标签居中

        next_button = QPushButton('下一页')
        next_button.clicked.connect(self.next_page)
        #next_button.setIcon(QIcon("icons/next.png"))  # 设置图标（需要提供next.png）
        button_layout.addWidget(next_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.show()

    def load_data(self):
        """加载数据，并在表格中显示"""
        self.progress_bar.setVisible(True)  # 显示进度条
        self.progress_bar.setValue(0)  # 设置进度条为0
        QApplication.processEvents()  # 刷新界面

        try:
            conn = sqlite3.connect(CommonUtil.get_db_full_path())
            cursor = conn.cursor()
            sql = f"SELECT * FROM {FsConstants.AUTO_ANSWERS_TABLE_NAME}"
            if self.page_size and self.current_page:
                offset = (self.current_page - 1) * self.page_size
                sql += f" ORDER BY id DESC LIMIT {self.page_size} OFFSET {offset}"
            cursor.execute(sql)
            results = cursor.fetchall()
        except sqlite3.DatabaseError as e:
            QMessageBox.critical(self, "数据库错误", f"数据库错误: {e}")
            logger.error(f"数据库错误: {e}")
            return
        finally:
            if conn:
                conn.close()

        if results:
            column_names = ["序列", "错误", "正确", "日期", "创建时间", "更新时间"]
            if not self.table.columnCount():
                self.table.setColumnCount(len(column_names))  # 只在第一次设置列名
                self.table.setHorizontalHeaderLabels(column_names)

            self.table.setRowCount(len(results))

            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    # 设置行背景色交替
                    item.setBackground(QBrush(QColor("#f0f0f0") if col_idx % 2 == 0 else QColor("#f9f9f9")))
                    self.table.setItem(row_idx, col_idx, item)

        self.progress_bar.setVisible(False)  # 隐藏进度条
        self.progress_bar.setValue(0)

    def prev_page(self):
        """上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_data()
            self.page_label.setText(f'第 {self.current_page} 页')
        else:
            QMessageBox.information(self, "提示", "已经是第一页了，没有上一页哦！")
            logger.warning("已经是第一页了，没有上一页哦！")

    def next_page(self):
        """下一页"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_data()
            self.page_label.setText(f'第 {self.current_page} 页')
        else:
            QMessageBox.information(self, "提示", "已经是最后一页了，没有下一页了！")
            logger.warning("已经是最后一页了，没有下一页了！")

    def update_total_pages(self):
        """计算总页数"""
        try:
            conn = sqlite3.connect(CommonUtil.get_db_full_path())
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {FsConstants.AUTO_ANSWERS_TABLE_NAME}")
            total_records = cursor.fetchone()[0]
        except sqlite3.DatabaseError as e:
            QMessageBox.critical(self, "数据库错误", f"数据库错误: {e}")
            logger.error(f"数据库错误: {e}")
            return
        finally:
            if conn:
                conn.close()

        self.total_pages = math.ceil(total_records / self.page_size)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = AutoAnswersList()
    sys.exit(app.exec_())
