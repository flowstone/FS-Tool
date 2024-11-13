rem 设置当前目录为脚本所在目录（避免因运行时工作目录不同导致的问题）
@echo off


rem 使用pyinstaller进行打包，参数解释如下：
rem --name "FSTool" 指定打包后的可执行文件名为FSTool
rem --onefile 表示打包成单个可执行文件
rem --window  这里应该是你想写--windowed吧，表示生成无控制台窗口的GUI应用程序（如果写错了请修正哦）
rem --add-data "desktop_clock.ico;." 表示将desktop_clock.ico文件添加到打包内容中，并使其与生成的可执行文件处于同一目录
rem main.py 是要打包的主程序文件

   pyinstaller --name "FSTool" --onefile --windowed --add-data "desktop_clock.ico;."  main.py

rem package complete
echo package complete。
pause