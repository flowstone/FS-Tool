import PySimpleGUI as sg
from PIL import Image


def main():
    sg.theme('LightBlue')

    layout = [[sg.Text('图片上传预览（PySimpleGUI）', font=('Helvetica', 16))],
              [sg.Button("上传", button_color=('white', 'blue'), font=('Helvetica', 12)),
               sg.Image(key='-IMAGE-', background_color='lightgray')]]
    window = sg.Window("图片上传预览", layout, size=(400, 300))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "上传":
            file_path = sg.popup_get_file("选择图片", file_types=(("图片文件", "*.png;*.jpg;*.jpeg"),))
            if file_path:
                image = Image.open(file_path)
                image.thumbnail((300, 300))
                bio = sg.BytesIO()
                image.save(bio, format='PNG')
                window['-IMAGE-'].update(data=bio.getvalue(), background_color='lightgray')
    window.close()



if __name__ == "__main__":
    main()