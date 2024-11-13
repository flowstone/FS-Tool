# FS Tool

### 工具列表
* 时间应用


### 脚本
##### 1.打包Tkinter脚本
``` bash
pyinstaller --name "应用名" --onefile --window --icon=clock.ico 程序脚本.py
```

##### 2.打包PyQt脚本
``` bash
pyinstaller --onefile --add-data "F:\Workspace\PycharmProjects\fs-tool\.venv\Lib\site-packages\PyQt5\Qt5\bin;./PyQt5/Qt/bin" --add-data "F:\Workspace\PycharmProjects\fs-tool\.venv\Lib\site-packages\PyQt5\Qt5\plugins;./PyQt5/Qt/plugins" --collect-all PyQt5 .\app_mini.py
```

###### 说明

``` bash 
F:\Workspace\PycharmProjects\fs-tool\.venv\Lib\site-packages\PyQt5\Qt5\bin;./PyQt5/Qt/bin
源PyQt5的目录:exe包中的目标路径
```



