import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from init_db import InitDB
from common_util import CommonUtil

def main():
    app = QApplication(sys.argv)
    # 初始化SQLite
    db_tool = InitDB(CommonUtil.get_db_full_path())
    db_tool.create_table()
    db_tool.close_connection()

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()