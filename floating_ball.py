import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import win32api
import win32con
import win32gui

class MainMini:
    def __init__(self, parent):
        self.parent = parent
        self.mini_window = tk.Toplevel(self.parent)

        self.mini_window.attributes('-alpha', 0.9)  # 设置窗口透明度
        self.mini_window.attributes('-topmost', True)  # 始终保持在最顶层
        # 设置一个在应用程序中不太会出现的颜色作为背景色
        self.mini_window.config(bg='#f0f0f0')
        # 将该颜色设置为透明色
        self.mini_window.attributes('-transparentcolor', '#f0f0f0')
        #self.root.withdraw()  # 隐藏主窗口，先不显示

        # 创建一个椭圆的悬浮图标
        self.icon_image = self.create_icon_with_image()
        self.icon_label = tk.Label(self.mini_window, image=self.icon_image, foreground='white')



        # 绑定双击图标事件
        self.icon_label.bind("<Double-Button-1>", self.show_app)

        # 绑定鼠标按下、移动和释放事件，用于实现图标拖动功能
        self.icon_label.bind("<ButtonPress-1>", self.start_drag)
        self.icon_label.bind("<B1-Motion>", self.drag)
        self.icon_label.bind("<ButtonRelease-1>", self.stop_drag)


        # 去除窗口边框和标题栏
        self.mini_window.overrideredirect(True)
        # 设置窗口初始位置和大小
        self.mini_window.geometry("60x60-100+100")
        self.icon_label.pack()

        self.mini_window.mainloop()


    def create_icon_with_image(self):
        # 加载指定的图片（这里假设图片名为example.jpg，可根据实际情况修改）
        image = Image.open("pic_conversion.png")
        # 确保图片模式为RGBA（包含透明通道），如果不是则转换
        if image.mode != "RGBA":
            image = image.convert("RGBA")

        # 调整图片大小以适应图标尺寸（可根据需求调整大小参数）
        image = image.resize((60, 60), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)


    def show_app(self, event):
        # 显示整个应用程序，恢复窗口边框和标题栏
        self.mini_window.deiconify()
        self.mini_window.overrideredirect(False)

        # 获取屏幕宽度和高度
        screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        # 计算窗口在屏幕中心的位置
        x_pos = (screen_width - 200) // 2
        y_pos = (screen_height - 200) // 2

        self.mini_window.geometry(f"600x400+{x_pos}+{y_pos}")
        self.mini_window.title("我的应用程序")
        label = tk.Label(self.mini_window, text="这是整个应用程序内容")

        label.pack()

    def hide_app(self, event):
        # 隐藏应用程序内容，恢复到悬浮图标状态
        for widget in self.mini_window.winfo_children():
            widget.destroy()
        self.mini_window.geometry("30x30")
        self.icon_label = tk.Label(self.mini_window, image=self.icon_image)
        self.icon_label.pack()



    def start_drag(self, event):
        self.drag_x = event.x_root - self.mini_window.winfo_x()
        self.drag_y = event.y_root - self.mini_window.winfo_y()

    def drag(self, event):
        self.mini_window.geometry(f"+{event.x_root - self.drag_x}+{event.y_root - self.drag_y}")

    def stop_drag(self, event):
        pass
