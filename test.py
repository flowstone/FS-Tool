from sqlite_util import SQLiteTool
from fs_constants import FsConstants
from common_util import CommonUtil
import datetime

# 示例用法
if __name__ == "__main__":

    # 假设数据库文件名为test.db，可根据实际情况替换
    db_tool = SQLiteTool(CommonUtil.get_db_full_path())

    # 创建操作示例
    #data_to_create = {'error': 'Alice', 'age': 28}
    #data_to_create = {'error': 1,'today':'2022-01-01'}
    #db_tool.create('auto_answers_log', data_to_create)

    # 读取操作示例
    #result_read = db_tool.read_one('auto_answers_log',condition="today='2022-01-01'")
    #print(result_read[1])
    #print("读取到的记录:", result_read)

    # 更新操作示例
    #data_to_update = {'error': 4}
    #condition_update = "today = '2022-01-01'"
    #db_tool.update('auto_answers_log', data_to_update, condition_update)

    # 删除操作示例
    #condition_delete = "id = '1'"
    #db_tool.delete('users', condition_delete)
    today = "2024-11-18"
    update_dict = {'error': 1, 'success': 1, 'update_time': CommonUtil.get_current_time()}
    db_tool.update(FsConstants.AUTO_ANSWERS_TABLE_NAME, update_dict,
                       f"today = '{today}'")
    db_tool.close()
    print(CommonUtil.get_today())