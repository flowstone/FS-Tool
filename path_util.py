import sys
import os


class PathUtil:

    # 获取资源（如图片等）的实际路径，处理打包后资源路径的问题
    @staticmethod
    def get_resource_path(relative_path):
        """
        获取资源（如图片等）的实际路径，处理打包后资源路径的问题
        """
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)