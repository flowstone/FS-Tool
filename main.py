import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw
from desktop_clock import DesktopClock
from pic_conversion import PicConversion
import pystray
from pystray import MenuItem
import os
import threading
import sys

# 在模块顶层定义tray_thread变量，初始值设为None
tray_thread = None
tray_icon = None
running = True

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("FS Tool")
        # 设置窗口初始位置和大小
        self.root.geometry("240x500-100+100")

        # 创建两个按钮
        self.desktopClockBtn = ttk.Button(self.root, text="透明时间", command=self.desktop_clock)
        self.picConversionBtn = ttk.Button(self.root, text="图转大师", command=self.pic_conversion)
        # 布局按钮
        self.desktopClockBtn.pack(padx=0, pady=50)
        self.picConversionBtn.pack(padx=0, pady=5)

        # 禁止窗口在水平和垂直方向上调整大小
        self.root.resizable(False, False)
        # 绑定系统事件，监听窗口最小化操作
        #self.root.bind("<Unmap>", self.on_minimize)
        # 关闭窗口，隐藏窗口
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.root.iconify())

        # 用于创建任务栏托盘图标
        self.create_system_tray_icon()
        self.root.mainloop()

    # 处理打包后，应用无法正确找到图片资源
    def get_resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)


    def create_system_tray_icon(self):
        global tray_icon, tray_thread

        # 替换为自己的图标路径
        image = Image.open(self.get_resource_path("desktop_clock.ico"))
        # 创建pystray图标对象
        tray_icon = pystray.Icon(
            'app_icon',
            image,
            'FSTool',
            menu=pystray.Menu(
                MenuItem('打开应用', self.show_application),
                MenuItem('退出', self.exit_application)
            )
        )
        # 在单独的线程中运行托盘图标
        tray_thread = threading.Thread(target=self.run_tray_icon)
        tray_thread.start()

    def run_tray_icon(self):
        global running
        try:
            while running:
                tray_icon.run()

        except Exception as e:
            print(f"托盘线程运行出现异常: {e}")
            running = False
            # 可以根据具体情况决定是否要在这里直接设置tray_running为False等操作
            # 比如如果异常情况意味着线程无法继续正常运行，那就可以设置tray_running = False

    # 显示主窗口
    def show_application(self):
        print("你点击了任务栏中的显示应用")
        # 显示主窗口
        self.root.deiconify()



    # 退出应用程序
    def exit_application(self):
        print("你点击了任务栏中的退出应用")
        # 设置一个标志位来通知更新线程退出
        global running, tray_icon, tray_thread
        running = False
        # 关闭主窗口
        self.root.destroy()

        if tray_thread.is_alive():
            print("托盘线程还在运行")
            # 等待更新线程结束
            tray_thread.join()
            # 停止托盘图标
            tray_icon.stop()

        os._exit(0)

    def on_minimize(self):
        print("你点击了主窗口的最小化")
        # 停止系统托盘图标
        #self.tray_icon.stop()
        # 隐藏主窗口
        #self.root.withdraw()
        #最小化窗口
        self.root.iconify()
        #MainMini(self.root)



    def desktop_clock(self):
        print("你点击了透明时间")
        DesktopClock(self.root)

    def pic_conversion(self):
        print("你点击了图转大师")
        PicConversion(self.root)

if __name__ == "__main__":
    app = MainApplication()
