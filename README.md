# FS Tool


### 脚本

#### 开始

在项目根目录下运行脚本
``` bash
pip install -r requirements.txt
```

##### 1.打包Tkinter脚本
``` bash
pyinstaller --name "应用名" --onefile --window --icon=clock.ico 程序脚本.py
```

##### 2.打包PyQt脚本
``` bash
pyinstaller --name "流体石头的工具箱" --onefile --window --add-data "F:\Workspace\PycharmProjects\fs-tool\.venv\Lib\site-packages\PyQt5\Qt5\bin;./PyQt5/Qt/bin" --add-data "F:\Workspace\PycharmProjects\fs-tool\.venv\Lib\site-packages\PyQt5\Qt5\plugins;./PyQt5/Qt/plugins" --add-data "resources;resources" --collect-all PyQt5 --icon=resources/app.ico .\app.py
```

###### 说明

``` bash 
F:\Workspace\PycharmProjects\fs-tool\.venv\Lib\site-packages\PyQt5\Qt5\bin;./PyQt5/Qt/bin
源PyQt5的目录:exe包中的目标路径
```

##### 预览
1. 应用图标

![](https://raw.githubusercontent.com/flowstone/fs-tool/release/resources/preview/app-logo.png)

2. 应用界面

![](https://raw.githubusercontent.com/flowstone/fs-tool/release/resources/preview/app-main-window.png)

3. 关闭应用窗口，屏幕右上角会有悬浮球

![](https://raw.githubusercontent.com/flowstone/fs-tool/release/resources/preview/app-mini.png)

4. 任务栏托盘

![](https://raw.githubusercontent.com/flowstone/fs-tool/release/resources/preview/app-menu-bar.png)

5. 欢迎预览

![](https://raw.githubusercontent.com/flowstone/fs-tool/release/resources/preview/start-work.gif)


##### 备注
Chrome浏览器指定版本**131.0.6778.69**