import sqlite3
import os
from fs_constants import FsConstants
import sys
from common_util import CommonUtil

class InitDB:
    def __init__(self, db_name):
        """
        初始化数据库连接和游标
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        """
        创建users表，如果不存在的话
        """
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def drop_table(self):
        drop_table_sql = "DROP TABLE IF EXISTS users"
        self.cursor.execute(drop_table_sql)
        self.conn.commit()
    def close_connection(self):
        """
        关闭数据库连接
        """
        self.cursor.close()
        self.conn.close()
# 示例用法
if __name__ == "__main__":

    db_tool = InitDB(CommonUtil.get_db_full_path())
    db_tool.create_table()
    #db_tool.drop_table()
    # 关闭连接
    db_tool.close_connection()