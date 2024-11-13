from tkinter import Tk, Button, Label
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk


class ImageUploadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片上传预览（tkinter）")
        self.root.geometry("400x300")
        self.root.configure(bg='#F0F0F0')

        title_label = Label(self.root, text="图片上传工具", font=("Helvetica", 16), bg='#F0F0F0')
        title_label.pack(pady=10)

        upload_button = Button(self.root, text="上传", command=self.on_upload, font=("Helvetica", 12), bg='#0080FF', fg='white')
        upload_button.pack(pady=10)
        self.image_label = Label(self.root)
        self.image_label.pack()

    def on_upload(self):
        file_path = askopenfilename(filetypes=[("图片文件", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo, bg='#F0F0F0')
            self.image_label.image = photo


if __name__ == "__main__":
    root = Tk()
    app = ImageUploadApp(root)
    root.mainloop()