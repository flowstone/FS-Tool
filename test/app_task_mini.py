import pystray
from pystray import MenuItem as item
from PIL import Image
import tkinter as tk


class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        image = Image.open("../desktop_clock.ico")  # 替换为自己的图标路径
        menu = (
            item('最小化', lambda: self.minimize_to_tray),
            item('退出', lambda: self.exit_program)
        )
        self.icon = pystray.Icon("name", image, "title", menu)
        self.icon.run()
    def minimize_to_tray(self):
        self.root.iconify()

    def exit_program(self):
        self.icon.stop()
        self.root.destroy()




if __name__ == "__main__":
    app = MainApplication()