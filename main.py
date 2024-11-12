import tkinter as tk
from tkinter import ttk
import win32gui
import win32con
from PIL import Image, ImageDraw
from desktop_clock import DesktopClock
from pic_conversion import PicConversion
from main_mini import MainMini
import pystray
from pystray import MenuItem
import os

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
        self.root.bind("<Unmap>", self.on_minimize)

        # 创建用于任务栏图标的图像
        self.icon_image = self.create_task_icon()

        # 创建pystray图标对象
        self.tray_icon = pystray.Icon(
            'app_icon',
            self.icon_image,
            'FSTool',
            menu=pystray.Menu(
                MenuItem('显示应用', self.show_application),
                MenuItem('退出', self.exit_application)
            )
        )

        self.root.mainloop()

    def create_task_icon(self):
        # 创建一个简单的圆形图标图像（这里你可以根据需要替换为自己的图标图像）
        image = Image.new('RGB', (32, 32), (255, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, 32, 32), fill=(0, 0, 255))
        return image

    # 显示主窗口
    def show_application(self):
        print("你点击了任务栏中的显示应用")

        # 显示主窗口
        self.root.deiconify()
        # 停止任务栏图标运行，隐藏图标
        self.tray_icon.stop()

    # 退出应用程序
    def exit_application(self):
        print("你点击了任务栏中的退出应用")
        self.root.destroy()
        os._exit(0)

    def on_minimize(self,event):
        print("你点击了主窗口的最小化")
        # 隐藏主窗口
        self.root.withdraw()
        #MainMini(self.root)

        # 在任务栏显示图标
        self.tray_icon.run()

    def desktop_clock(self):
        print("你点击了透明时间")
        DesktopClock(self.root)

    def pic_conversion(self):
        print("你点击了图转大师")
        PicConversion(self.root)

if __name__ == "__main__":
    app = MainApplication()
