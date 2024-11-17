import sys
import os

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
        data_path = FsConstants.SAVE_FILE_PATH_WIN if CommonUtil.check_win_os() else FsConstants.SAVE_FILE_PATH_MAC
        # 构建数据库文件的相对路径,假设数据库文件名为database.db
        return os.path.join(data_path, FsConstants.DATABASE_FILE)
