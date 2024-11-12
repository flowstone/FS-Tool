import tkinter as tk
from tkinter import ttk
import time



# 时间应用，透明，在桌面左上角显示
class DesktopClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # 去除窗口边框和标题栏
        self.root.attributes('-alpha', 0.8)  # 设置窗口透明度
        self.root.attributes('-topmost', True)  # 始终保持在最顶层




        # 设置一个在应用程序中不太会出现的颜色作为背景色
        self.root.config(bg='#f0f0f0')
        # 将该颜色设置为透明色
        self.root.attributes('-transparentcolor', '#f0f0f0')

        self.label_time = ttk.Label(self.root, font=("Helvetica", 24),foreground='white')
        self.label_time.pack()

        # 指定应用图标
        self.root.iconbitmap('desktop_clock.ico')

        self.update_time()

        self.root.mainloop()



    def update_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.label_time.config(text=current_time)
        self.root.after(1000, self.update_time)



#if __name__ == "__main__":
#    app = DesktopClock()