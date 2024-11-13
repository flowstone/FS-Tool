 #!/bin/bash
pyinstaller --name "FSTool" --onefile --window  --add-data "desktop_clock.ico;."  main.py
echo "---- 完成打包Win应用 ----"