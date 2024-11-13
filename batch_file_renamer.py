import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image


class FileRenamerApp:
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("文件名批量修改工具")

        # 创建菜单栏
        menubar = tk.Menu(self.root)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        self.root.config(menu=menubar)

        # 选择文件夹相关部件
        self.folder_path_label = tk.Label(self.root, text="选择文件夹：")
        self.folder_path_label.pack()
        self.folder_path_entry = tk.Entry(self.root, width=50)
        self.folder_path_entry.pack()
        self.browse_button = tk.Button(self.root, text="浏览", command=self.browse_folder)
        self.browse_button.pack()

        # 文件名前缀输入部件
        self.prefix_label = tk.Label(self.root, text="文件名前缀：")
        self.prefix_label.pack()
        self.prefix_entry = tk.Entry(self.root)
        self.prefix_entry.pack()

        # 文件名后缀输入部件
        self.suffix_label = tk.Label(self.root, text="文件名后缀：")
        self.suffix_label.pack()
        self.suffix_entry = tk.Entry(self.root)
        self.suffix_entry.pack()

        # 查找字符输入部件
        self.char_to_find_label = tk.Label(self.root, text="查找字符：")
        self.char_to_find_label.pack()
        self.char_to_find_entry = tk.Entry(self.root)
        self.char_to_find_entry.pack()

        # 替换字符输入部件
        self.replace_char_label = tk.Label(self.root, text="替换字符：")
        self.replace_char_label.pack()
        self.replace_char_entry = tk.Entry(self.root)
        self.replace_char_entry.pack()

        # 作者和Github信息文本
        self.author_label = tk.Label(self.root, text="Author：xueyao.me@gmail.com", font=("楷体", 11), fg='blue')
        self.author_label.pack()
        self.github_label = tk.Label(self.root, text="Github：https://github.com/flowstone/Tooool", font=("楷体", 11),
                                     fg='blue')
        self.github_label.pack()

        # 操作按钮
        self.start_button = tk.Button(self.root, text="开始修改", command=self.start_operation)
        self.start_button.pack(side=tk.LEFT)
        self.exit_button = tk.Button(self.root, text="退出", command=self.root.destroy)
        self.exit_button.pack(side=tk.RIGHT)

        self.root.mainloop()

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.folder_path_entry.delete(0, tk.END)
        self.folder_path_entry.insert(0, folder_path)

    def show_about(self):
        messagebox.showinfo("关于", "只限于修改文件夹下文件！")

    def start_operation(self):
        folder_path = self.folder_path_entry.get()
        prefix = self.prefix_entry.get()
        suffix = self.suffix_entry.get()
        char_to_find = self.char_to_find_entry.get()
        replace_char = self.replace_char_entry.get()
        if folder_path:
            self.rename_files(folder_path, prefix, suffix, char_to_find, replace_char)
            messagebox.showinfo("提示", "批量文件名修改完成！")
        else:
            messagebox.showwarning("警告", "请选择要修改的文件夹！")

    # 修改文件名
    def rename_files(self, folder_path, prefix, suffix, char_to_find, replace_char):
        # 遍历文件夹下的文件名
        for filename in os.listdir(folder_path):
            old_path = os.path.join(folder_path, filename)
            # 判断是否是文件
            if os.path.isfile(old_path):
                new_filename = f"{prefix}{filename}{suffix}"
                # 判断是否需要进行文件替换操作
                if char_to_find and replace_char:
                    # 替换字符
                    new_filename = new_filename.replace(char_to_find, replace_char)
                new_path = os.path.join(folder_path, new_filename)
                os.rename(old_path, new_path)




