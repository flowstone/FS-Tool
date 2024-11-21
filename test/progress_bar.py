import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QProgressBar


class FileRenameApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 文件夹路径输入框
        self.folderPathEdit = QLineEdit(self)
        layout.addWidget(self.folderPathEdit)

        # 选择文件夹按钮
        self.folderButton = QPushButton('选择文件夹', self)
        self.folderButton.clicked.connect(self.selectFolder)
        layout.addWidget(self.folderButton)

        # 文件名修改输入框
        self.newNameEdit = QLineEdit(self)
        layout.addWidget(self.newNameEdit)

        # 开始按钮
        self.startButton = QPushButton('开始', self)
        self.startButton.clicked.connect(self.startRenaming)
        layout.addWidget(self.startButton)
        self.startButton.setEnabled(False)

        # 进度条（初始隐藏）
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 100)
        # 为进度条设置样式表进行美化
        self.progressBar.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid #ccc;
                border-radius: 5px;
                text-align: center;
                font-size: 12px;
                color: white;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                border-radius: 5px;
                background-color: #007BFF;
            }
            """
        )
        self.progressBar.hide()
        layout.addWidget(self.progressBar)

        self.setLayout(layout)
        self.setWindowTitle('文件重命名工具')
        self.show()

    def selectFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if folderPath:
            # 将选择的文件夹路径回显到输入框
            self.folderPathEdit.setText(folderPath)
            self.startButton.setEnabled(True)

    def startRenaming(self):
        new_name = self.newNameEdit.text()
        folder_path = self.folderPathEdit.text()
        # 统计文件夹下的文件总数
        file_count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
        # 显示进度条
        self.progressBar.show()
        for i, file in enumerate(os.listdir(folder_path)):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                file_extension = os.path.splitext(file)[1]
                new_file_path = os.path.join(folder_path, new_name + str(i) + file_extension)
                os.rename(file_path, new_file_path)
                # 更新进度条
                progress = int((i + 1) / file_count * 100)
                self.progressBar.setValue(progress)
                time.sleep(0.1)  # 模拟重命名耗时操作


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileRenameApp()
    sys.exit(app.exec_())