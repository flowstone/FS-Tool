from symtable import Class
import tkinter as tk

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        button = tk.Button(self.root, text="最小化窗口", command=self.minimize_window)
        button.pack()

        self.root.mainloop()

    def minimize_window(self):
        print("测试")
        self.root.iconify()



if __name__ == "__main__":
    app = MainApplication()