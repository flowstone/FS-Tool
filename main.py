import tkinter as tk
from tkinter import ttk

from desktop_clock import DesktopClock
from pic_conversion import PicConversion


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

        self.root.mainloop()


    def desktop_clock(self):
        DesktopClock(self.root)

    def pic_conversion(self):
        PicConversion(self.root)

if __name__ == "__main__":
    app = MainApplication()
