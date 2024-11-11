import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import os


class ImageFormatConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("图片格式转换应用")

        # 用于存储上传的图片路径
        self.image_path = None

        # 创建上传图片按钮
        self.upload_button = ttk.Button(self.root, text="上传图片", command=self.upload_image)
        self.upload_button.pack(pady=10)

        # 创建用于显示上传图片的标签
        self.image_label = ttk.Label(self.root)
        self.image_label.pack(pady=10)

        # 创建复选框框架
        self.checkbox_frame = ttk.Frame(self.root)
        self.checkbox_frame.pack(pady=10)

        # 定义支持的目标格式
        self.target_formats = ["JPEG", "PNG", "GIF", "BMP", "WEBP", "ICO"]
        self.selected_formats = []

        # 创建复选框
        for format in self.target_formats:
            checkbox = ttk.Checkbutton(self.checkbox_frame, text=format, command=lambda f=format: self.toggle_format(f))
            checkbox.pack(side=tk.LEFT, padx=5)

        # 创建转换按钮
        self.convert_button = ttk.Button(self.root, text="转换", command=self.convert_image, state=tk.DISABLED)
        self.convert_button.pack(pady=10)
        # 指定应用图标
        self.root.iconbitmap('pic_conversion.ico')

        self.root.mainloop()

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("图片文件", "*.jpg;*.png;*.gif;*.bmp;*.webp;;*.ico")])
        if self.image_path:
            print(f"已上传图片: {self.image_path}")
            try:
                image = Image.open(self.image_path)
                image = ImageTk.PhotoImage(image)
                self.image_label.config(image=image)
                self.image_label.image = image  # 保留对图像对象的引用，防止被垃圾回收
            except Exception as e:
                print(f"显示图片时出错: {e}")

    def toggle_format(self, format):
        if format in self.selected_formats:
            self.selected_formats.remove(format)
        else:
            self.selected_formats.append(format)

        # 根据是否有复选框被选中来更新转换按钮的状态
        if len(self.selected_formats) > 0:
            self.convert_button["state"] = tk.NORMAL
        else:
            self.convert_button["state"] = tk.DISABLED

    def convert_image(self):
        if not self.image_path:
            print("请先上传图片!")
            return

        try:
            image = Image.open(self.image_path)

            for target_format in self.selected_formats:
                base_name, ext = os.path.splitext(self.image_path)
                new_image_path = f"{base_name}.{target_format.lower()}"
                if target_format == "JPEG":
                    image = image.convert('RGB')
                elif target_format == "ICO":
                    image = image.convert('RGB') if image.mode != 'RGB' else image
                    image.save(new_image_path, format='ICO')
                    continue
                elif target_format == "WEBP":
                    image = image.convert('RGB') if image.mode!= 'RGB' else image
                image.save(new_image_path)

            print(f"图片已成功转换为所选格式，保存路径分别为: {[f'{base_name}.{f.lower()}' for f in self.selected_formats]}")
        except Exception as e:
            print(f"转换图片时出错: {e}")


if __name__ == "__main__":
    app = ImageFormatConverter()