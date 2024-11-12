import tkinter as tk
from tkinter import ttk
import pystray
from PIL import Image, ImageDraw
import threading
import sys
import os

class FloatingBall:
    def __init__(self):
        self.ball = None
        self.x = 0
        self.y = 0
        self.dragging = False

        self.root = tk.Tk()
        self.root.title("示例应用")

        # 设置窗口大小等其他属性
        self.root.geometry("400x300")

        #self.root.bind("<Unmap>", self.on_minimize)

        self.root.protocol("WM_DELETE_WINDOW", lambda: self.root.iconify())

        self.root.mainloop()

    def create_ball(self):
        # 创建悬浮球窗口（这里简单用一个小的 `tkinter` 窗口模拟）
        self.ball = tk.Toplevel()
        self.ball.overrideredirect(True)
        self.ball.attributes('-alpha', 0.8)
        self.ball.geometry("30x30")
        label = tk.Label(self.ball, text="球", bg="blue")
        label.pack()

        # 绑定鼠标事件实现拖动等功能
        self.ball.bind("<ButtonPress-1>", self.on_ball_press)
        self.ball.bind("<B1-Motion>", self.on_ball_drag)
        self.ball.bind("<ButtonRelease-1>", self.on_ball_release)
        self.ball.bind("<Double-Button-1>", self.on_ball_double_click)

    def on_ball_press(self, event):
        self.dragging = True
        self.x = event.x
        self.y = event.y

    def on_ball_drag(self, event):
        if self.dragging:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.ball.winfo_x() + deltax
            y = self.ball.winfo_y() + deltay
            self.ball.geometry(f"+{x}+{y}")

    def on_ball_release(self, event):
        self.dragging = False

    def on_ball_double_click(self, event):
        self.root.deiconify()

    def create_system_tray_icon(self):
        # 创建用于托盘图标的图像
        image = Image.new('RGB', (64, 64), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, 64, 64), fill=(0, 0, 255))

        # 创建托盘图标对象
        icon = pystray.Icon("示例应用托盘", image, "示例应用")

        # 定义托盘图标菜单选项及对应的函数
        menu = (pystray.MenuItem('显示窗口', self.show_window),
                pystray.MenuItem('退出', self.exit_app))
        icon.menu = menu

        # 运行托盘图标
        icon.run()

    def show_window(self):
        self.root.deiconify()

    def exit_app(self):
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
        floating_ball = FloatingBall()
        tray_thread = threading.Thread(target=floating_ball.create_system_tray_icon)
        floating_ball_thread = threading.Thread(target=floating_ball.create_ball)

        tray_thread.start()
        floating_ball_thread.start()

