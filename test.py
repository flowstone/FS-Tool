from sqlite_util import SQLiteTool
from fs_constants import FsConstants
from common_util import CommonUtil
# 示例用法
if __name__ == "__main__":

    # 假设数据库文件名为test.db，可根据实际情况替换
    db_tool = SQLiteTool(CommonUtil.get_db_full_path())

    # 创建操作示例
    #data_to_create = {'name': 'Alice', 'age': 28}
    #db_tool.create('users', data_to_create)

    # 读取操作示例
    #result_read = db_tool.read('users')
    #print("读取到的记录:", result_read)

    # 更新操作示例
    #data_to_update = {'age': 29}
    #condition_update = "name = 'Alice'"
    #db_tool.update('users', data_to_update, condition_update)

    # 删除操作示例
    #condition_delete = "id = '1'"
    #db_tool.delete('users', condition_delete)

    db_tool.close()