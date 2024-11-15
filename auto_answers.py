import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,QPixmap, QIcon
import auto_answers_operation
from path_util import PathUtil

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("自动答题")
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)  # 设置主垂直布局的间距为10像素，可根据实际调整

        # 设置通用字体
        font = QFont()
        font.setPointSize(12)

        self.setWindowIcon(QIcon(PathUtil.get_resource_path("resources/app.ico")))

        # 图片标签，单独占一行
        image_label = QLabel(self)
        pixmap = QPixmap(PathUtil.get_resource_path("resources/auto_answers_title.png"))  # 替换为实际的图片路径
        # 对图片进行缩放，这里示例将宽度缩放为300像素，高度按比例缩放，保持图片比例不变
        scaled_pixmap = pixmap.scaled(217, 217, Qt.KeepAspectRatio)
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(image_label, alignment=Qt.AlignCenter)

        # 第一行（城市、乡镇、证）
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(10)  # 设置第一行水平布局间距为10像素

        # 城市下拉框和标签
        zone3_label = QLabel("城市")
        zone3_label.setFont(font)
        self.zone3_combo = QComboBox()
        self.zone3_combo.addItems(["淮安市"])
        #self.zone3_codes = {"淮安市": "3208000000"}

        self.zone3_combo.setFont(font)
        self.zone3_combo.setFixedWidth(120)
        self.zone3_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                min-width: 60px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 0px;
                border-left-color: transparent;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
        """)
        row1_layout.addWidget(zone3_label)
        row1_layout.addWidget(self.zone3_combo, 1)  # 设置拉伸因子为1，合理分配空间

        # 乡镇下拉框和标签
        zone4_label = QLabel("区/县")
        zone4_label.setFont(font)
        self.zone4_combo = QComboBox()
        self.zone4_combo.addItems(["涟水县"])
        #self.zone4_codes = {"涟水县": "3208260000"}

        self.zone4_combo.setFont(font)
        self.zone4_combo.setFixedWidth(120)
        self.zone4_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                min-width: 60px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 0px;
                border-left-color: transparent;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
        """)
        row1_layout.addWidget(zone4_label)
        row1_layout.addWidget(self.zone4_combo, 1)

        # 乡镇
        zone5_label = QLabel("乡镇")
        zone5_label.setFont(font)
        self.zone5_combo = QComboBox()
        self.zone5_combo.addItems(["石湖镇", "五港镇"])
        #self.zone5_codes = {"石湖镇": "3208262600","五港镇": "3208262300"}

        self.zone5_combo.setFont(font)
        self.zone5_combo.setFixedWidth(120)
        self.zone5_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                min-width: 60px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 0px;
                border-left-color: transparent;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
        """)
        row1_layout.addWidget(zone5_label)
        row1_layout.addWidget(self.zone5_combo, 1)

        main_layout.addLayout(row1_layout)

        # 第二行（姓名、年龄、性别）
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(10)

        # 姓名输入框和标签
        name_label = QLabel("姓名")
        name_label.setFont(font)
        self.name_edit = QLineEdit()
        self.name_edit.setFont(font)
        self.name_edit.setFixedWidth(120)
        row2_layout.addWidget(name_label)
        row2_layout.addWidget(self.name_edit, 1)

        # 年龄下拉框和标签
        age_label = QLabel("年龄")
        age_label.setFont(font)
        self.age_combo = QComboBox()
        self.age_combo.addItems([ "30～35岁以下", "35～40岁以下", "40～45岁以下", "45～50岁以下", "50～55岁以下"])
       # self.age_codes = {"30～35岁以下": "05","35～40岁以下": "06","40～45岁以下": "07","45～50岁以下": "08","50～55岁以下": "09"}

        self.age_combo.setFont(font)
        self.age_combo.setFixedWidth(120)
        self.age_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                min-width: 60px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 0px;
                border-left-color: transparent;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
        """)
        row2_layout.addWidget(age_label)
        row2_layout.addWidget(self.age_combo, 1)

        # 性别下拉框和标签
        gender_label = QLabel("性别")
        gender_label.setFont(font)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["男", "女"])
        #self.gender_codes = {"男": "1","女": "2"}

        self.gender_combo.setFont(font)
        self.gender_combo.setFixedWidth(120)
        self.gender_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                min-width: 60px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 0px;
                border-left-color: transparent;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
        """)
        row2_layout.addWidget(gender_label)
        row2_layout.addWidget(self.gender_combo, 1)

        main_layout.addLayout(row2_layout)

        # 第三行（文化、职业、公司）
        row3_layout = QHBoxLayout()
        row3_layout.setSpacing(10)

        # 文化下拉框和标签
        culture_label = QLabel("文化程度")
        culture_label.setFont(font)
        self.culture_combo = QComboBox()
        self.culture_combo.addItems(["小学", "中学", "高中/职高/中专", "大专/本科","硕士及以上"])
        #self.culture_codes = {"小学": "1","中学": "2","高中/职高/中专": "3","大专/本科": "4","硕士及以上": "5"}

        self.culture_combo.setFont(font)
        self.culture_combo.setFixedWidth(120)
        self.culture_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                min-width: 60px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 0px;
                border-left-color: transparent;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
        """)
        row3_layout.addWidget(culture_label)
        row3_layout.addWidget(self.culture_combo, 1)

        # 职业下拉框和标签
        job_label = QLabel("职业")
        job_label.setFont(font)
        self.job_combo = QComboBox()
        self.job_combo.addItems(["饮食服务", "商业服务", "医务人员", "工人","民工","农民","家务待业"])
        #self.job_codes = {"饮食服务": "04","商业服务": "05","医务人员": "06","工人": "07","民工": "08","农民": "09","家务待业": "13"}

        self.job_combo.setFont(font)
        self.job_combo.setFixedWidth(120)
        self.job_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                min-width: 60px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 0px;
                border-left-color: transparent;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
        """)
        row3_layout.addWidget(job_label)
        row3_layout.addWidget(self.job_combo, 1)

        # 公司输入框和标签
        company_label = QLabel("公司")
        company_label.setFont(font)
        self.company_edit = QLineEdit()
        self.company_edit.setFont(font)
        self.company_edit.setFixedWidth(120)
        row3_layout.addWidget(company_label)
        row3_layout.addWidget(self.company_edit, 1)

        main_layout.addLayout(row3_layout)

        # 第四行（次数下拉框）
        row4_layout = QHBoxLayout()
        row4_layout.setSpacing(10)

        times_label = QLabel("次数")  # 添加次数标签，使界面更清晰
        times_label.setFont(font)
        self.times_combo = QComboBox()
        self.times_combo.addItems(["1", "2", "3", "4", "5"])
        self.times_combo.setFont(font)
        self.times_combo.setFixedWidth(120)
        self.times_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                min-width: 60px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 0px;
                border-left-color: transparent;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
        """)
        row4_layout.addWidget(times_label)
        row4_layout.addWidget(self.times_combo, 1)

        main_layout.addLayout(row4_layout)

        # 第五行（提交按钮）
        submit_button = QPushButton("提交")
        submit_button.setFont(font)
        submit_button.setFixedSize(100, 30)
        # 为按钮添加样式，鼠标悬停时背景变色，按下时文字变色等效果示例（可根据喜好调整）
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                color: #ccc;
            }
        """)
        main_layout.addWidget(submit_button, alignment=Qt.AlignCenter)

        # 设置窗口整体样式，例如背景颜色（可按需修改）
        self.setStyleSheet("QWidget { background-color: #f9f9f9; }")

        # 连接次数下拉框的信号与槽函数，当选择改变时执行相应操作
        submit_button.clicked.connect(self.start_answers)
        self.setLayout(main_layout)

    def start_answers(self):
        if self.is_all_selected():
            zone3_value = self.zone3_combo.currentText()

            zone4_value = self.zone4_combo.currentText()

            zone5_value = self.zone5_combo.currentText()

            name_value = self.name_edit.text()

            age_value = self.age_combo.currentText()

            gender_value = self.gender_combo.currentText()

            culture_value = self.culture_combo.currentText()

            job_value = self.job_combo.currentText()

            company_value = self.company_edit.text()
            selected_number = int(self.times_combo.currentText())
            for _ in range(selected_number):
                auto_answers_operation.perform_operation(zone3_value, zone4_value, zone5_value, name_value, age_value, gender_value,
                                         culture_value, job_value, company_value)

    def is_all_selected(self):
        return (
                self.zone3_combo.currentIndex() != -1 and
                self.zone4_combo.currentIndex() != -1 and
                self.zone5_combo.currentIndex() != -1 and
                self.age_combo.currentIndex() != -1 and
                self.gender_combo.currentIndex() != -1 and
                self.culture_combo.currentIndex() != -1 and
                self.job_combo.currentIndex() != -1
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())