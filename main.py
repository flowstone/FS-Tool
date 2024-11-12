import tkinter as tk
from desktop_clock import DesktopClock
from pic_conversion import PicConversion


class MainApplication:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("FS Tool")
        # 设置窗口初始位置和大小
        self.root.geometry("240x500-100+100")

        # 创建两个按钮
        self.desktopClockBtn = tk.Button(self.root, text="透明时间", command=self.desktop_clock)
        self.picConversionBtn = tk.Button(self.root, text="图转大师", command=self.pic_conversion)

        # 布局按钮
        self.desktopClockBtn.pack(pady=10)
        self.picConversionBtn.pack(pady=10)

        self.root.mainloop()


    def desktop_clock(self):
        DesktopClock()

    def pic_conversion(self):
        PicConversion()

if __name__ == "__main__":
    app = MainApplication()
