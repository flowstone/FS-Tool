import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import win32api
import win32con
import win32gui
import threading
import time

class FloatingBall:
    def __init__(self):
        self.floating_ball = tk.Toplevel()

        self.floating_ball.attributes('-alpha', 0.9)  # 设置窗口透明度
        self.floating_ball.attributes('-topmost', True)  # 始终保持在最顶层
        # 设置一个在应用程序中不太会出现的颜色作为背景色
        self.floating_ball.config(bg='#f0f0f0')
        # 将该颜色设置为透明色
        self.floating_ball.attributes('-transparentcolor', '#f0f0f0')
        #self.root.withdraw()  # 隐藏主窗口，先不显示

        # 创建一个椭圆的悬浮图标
        self.icon_image = self.create_icon_with_image()
        self.icon_label = tk.Label(self.floating_ball, image=self.icon_image, foreground='white')



        # 绑定双击图标事件
        self.icon_label.bind("<Double-Button-1>", self.show_main_app)

        # 绑定鼠标按下、移动和释放事件，用于实现图标拖动功能
        self.icon_label.bind("<ButtonPress-1>", self.start_drag)
        self.icon_label.bind("<B1-Motion>", self.drag)
        self.icon_label.bind("<ButtonRelease-1>", self.stop_drag)


        # 去除窗口边框和标题栏
        self.floating_ball.overrideredirect(True)
        # 设置窗口初始位置和大小
        self.floating_ball.geometry("60x60-100+100")
        self.icon_label.pack()

        self.running = True  # 新增标志位，用于控制线程循环


    def create_icon_with_image(self):
        # 加载指定的图片（这里假设图片名为example.jpg，可根据实际情况修改）
        image = Image.open("../resources/pic_conversion.png")
        # 确保图片模式为RGBA（包含透明通道），如果不是则转换
        if image.mode != "RGBA":
            image = image.convert("RGBA")

        # 调整图片大小以适应图标尺寸（可根据需求调整大小参数）
        image = image.resize((60, 60), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    # 显示主界面
    def show_main_app(self, event):
        # 杀死悬浮球
        self.main_window.deiconify()
        self.floating_ball.destroy()



    # 按下悬浮球，获取坐标
    def start_drag(self, event):
        self.drag_x = event.x_root - self.floating_ball.winfo_x()
        self.drag_y = event.y_root - self.floating_ball.winfo_y()

    # 移动悬浮球，获取坐标
    def drag(self, event):
        self.floating_ball.geometry(f"+{event.x_root - self.drag_x}+{event.y_root - self.drag_y}")

    # 松开悬浮球
    def stop_drag(self, event):
        pass


    def set_main_window(self, main_window):
        self.main_window = main_window


    def start(self):
        thread = threading.Thread(target=self.run)
        thread.start()


    def run(self):
        while self.running:
            self.floating_ball.update()  # 定期更新悬浮球窗口状态
            # 可以添加更多的逻辑判断、操作等内容，比如处理其他的事件等
            time.sleep(0.1)  # 适当休眠，避免过度占用CPU资源

    def stop(self):
        self.running = False
        self.floating_ball.destroy()