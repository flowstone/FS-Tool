import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image


class CreateFolderApp:
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("批量移动文件")

        # 说明文本
        self.info_label = tk.Label(self.root, text="说明：根据输入的分割字符，取前部分创建文件夹，符合相关的文件都移动到对应文件夹中",
                                   font=("楷体", 10), fg='white')
        self.info_label.pack()

        # 选择文件夹相关部件
        self.folder_path_label = tk.Label(self.root, text="选择文件夹：")
        self.folder_path_label.pack()
        self.folder_path_entry = tk.Entry(self.root, width=50)
        self.folder_path_entry.pack()
        self.browse_button = tk.Button(self.root, text="浏览", command=self.browse_folder)
        self.browse_button.pack()

        # 分割字符输入部件
        self.slice_label = tk.Label(self.root, text="指定分割字符：")
        self.slice_label.pack()
        self.slice_entry = tk.Entry(self.root)
        self.slice_entry.pack()

        # 作者和Github信息文本
        self.author_label = tk.Label(self.root, text="Author：xueyao.me@gmail.com", font=("楷体", 10), fg='blue')
        self.author_label.pack()
        self.github_label = tk.Label(self.root, text="Github：https://github.com/flowstone/Tooool", font=("楷体", 10),
                                     fg='blue')
        self.github_label.pack()

        # 操作按钮
        self.start_button = tk.Button(self.root, text="开始", command=self.start_operation)
        self.start_button.pack(side=tk.LEFT)
        self.exit_button = tk.Button(self.root, text="退出", command=self.root.destroy)
        self.exit_button.pack(side=tk.RIGHT)
        self.root.mainloop()

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.folder_path_entry.delete(0, tk.END)
        self.folder_path_entry.insert(0, folder_path)

    def start_operation(self):
        folder_path = self.folder_path_entry.get()
        slice_char = self.slice_entry.get()
        if folder_path:
            self.create_folder_move_files(folder_path, slice_char)
            messagebox.showinfo("提示", "移动文件完成！")
        else:
            messagebox.showwarning("警告", "请选择要操作的文件夹！")

    # 创建文件夹，并移动到指定目录下
    def create_folder_move_files(self, folder_path, slice_char):
        # 遍历文件夹下的文件名
        for filename in os.listdir(folder_path):
            source_path = os.path.join(folder_path, filename)
            # 判断是否是文件
            if os.path.isfile(source_path):
                # 找到分割的位置，如'-'
                index = filename.find(slice_char)
                if index!= -1:
                    # 提取分割字符前面的部分作为文件夹名
                    folder_name = filename[:index]
                    # 如果文件夹不存在，则创建
                    target_folder = os.path.join(folder_path, folder_name)
                    if not os.path.exists(target_folder):
                        os.mkdir(target_folder)
                    # 将文件移动到对应的文件夹
                    destination_path = os.path.join(target_folder, filename)
                    shutil.move(source_path, destination_path)


