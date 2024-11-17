import sys
import os
import datetime

from fs_constants import FsConstants


class CommonUtil:

    # 获取资源（如图片等）的实际路径，处理打包后资源路径的问题
    @staticmethod
    def get_resource_path(relative_path):
        """
        获取资源（如图片等）的实际路径，处理打包后资源路径的问题
        """
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

    # 当前系统是Win 返回True
    @staticmethod
    def check_win_os():
        return sys.platform.startswith('win')


    #获得应用图标全路径
    @staticmethod
    def get_ico_full_path():
        return CommonUtil.get_resource_path(FsConstants.APP_ICON_PATH)

    # 获得应用小图标全路径
    @staticmethod
    def get_mini_ico_full_path():
        return CommonUtil.get_resource_path(FsConstants.APP_MINI_ICON_PATH)

    # 获得数据库文件全路径
    @staticmethod
    def get_db_full_path():
        # 判断系统
        data_path = FsConstants.SAVE_FILE_PATH_WIN if CommonUtil.check_win_os() else CommonUtil.get_mac_user_path()
        # 构建数据库文件的相对路径,假设数据库文件名为database.db
        return os.path.join(data_path, FsConstants.DATABASE_FILE)

    # 静止外部类调用这个方法
    @staticmethod
    def get_mac_user_path():
        return os.path.expanduser(FsConstants.SAVE_FILE_PATH_MAC)

    # 获得当前日期
    @staticmethod
    def get_today():
        # 获取当前日期（是一个date对象）
        current_date = datetime.date.today()
        # 使用strftime方法按照指定格式进行格式化
        return current_date.strftime('%Y-%m-%d')

    # 获得当前指定格式的时间
    # %Y-%m-%d %H:%M:%S
    @staticmethod
    def get_current_time(format:str='%Y-%m-%d %H:%M:%S'):
        # 获取当前日期和时间
        current_datetime = datetime.datetime.now()

        # 格式化时间为指定格式
        return current_datetime.strftime(format)