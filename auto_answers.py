import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,QPixmap, QIcon

from path_util import PathUtil
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 这里定义一些常见的姓氏和名字的列表，可以根据实际情况扩展
last_names = ["赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", "褚", "卫", "蒋", "沈", "韩", "杨"]
first_names = ["强", "伟", "芳", "娜", "秀英", "敏", "静", "丽", "军", "磊", "超", "鹏", "慧", "勇", "杰"]

class AutoAnswersApp(QWidget):
    def __init__(self):
        super().__init__()

        COMBO_BOX_STYLE = """
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
        """
        self.zone3_status = False
        self.zone4_status = False
        self.zone5_status = False
        self.age_status = False
        self.gender_status = False
        self.culture_status = False
        self.job_status = False
        self.while_flag = True

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
        self.zone3_combo.setStyleSheet(COMBO_BOX_STYLE)
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
        self.zone4_combo.setStyleSheet(COMBO_BOX_STYLE)
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
        self.zone5_combo.setStyleSheet(COMBO_BOX_STYLE)
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
        self.age_combo.setStyleSheet(COMBO_BOX_STYLE)
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
        self.gender_combo.setStyleSheet(COMBO_BOX_STYLE)
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
        self.culture_combo.setStyleSheet(COMBO_BOX_STYLE)
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
        self.job_combo.setStyleSheet(COMBO_BOX_STYLE)
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
        self.times_combo.setStyleSheet(COMBO_BOX_STYLE)
        row4_layout.addWidget(times_label)
        row4_layout.addWidget(self.times_combo, 1)

        main_layout.addLayout(row4_layout)

        # 第五行（提交按钮）
        submit_button = QPushButton("提交")
        submit_button.setFont(font)
        submit_button.setFixedSize(100, 30)
        # 为按钮添加样式，鼠标悬停时背景变色，按下时文字变色等效果示例（可根据喜好调整）
        submit_button.setStyleSheet(COMBO_BOX_STYLE)
        main_layout.addWidget(submit_button, alignment=Qt.AlignCenter)

        # 设置窗口整体样式，例如背景颜色（可按需修改）
        self.setStyleSheet("QWidget { background-color: #f9f9f9; }")

        # 连接次数下拉框的信号与槽函数，当选择改变时执行相应操作
        submit_button.clicked.connect(self.start_answers)
        self.setLayout(main_layout)

        self.zone3_value = self.zone3_combo.currentText()
        self.zone4_value = self.zone4_combo.currentText()
        self.zone5_value = self.zone5_combo.currentText()
        self.name_value = self.generate_name()
        self.age_value = self.age_combo.currentText()
        self.gender_value = self.gender_combo.currentText()
        self.culture_value = self.culture_combo.currentText()
        self.job_value = self.job_combo.currentText()
        self.company_value = self.company_edit.text()
        self.selected_number = int(self.times_combo.currentText())

        logger.info("-----------------")
        # 这里编写具体要执行的操作内容，以下只是示例打印信息
        logger.info(f"城市: {self.zone3_value}")
        logger.info(f"区/县: {self.zone4_value}")
        logger.info(f"证件类型: {self.zone5_value}")
        logger.info(f"姓名: {self.name_value}")
        logger.info(f"年龄: {self.age_value}")
        logger.info(f"性别: {self.gender_value}")
        logger.info(f"文化程度: {self.culture_value}")
        logger.info(f"职业: {self.job_value}")
        logger.info(f"公司: {self.company_value}")

    @staticmethod
    def generate_name():
        last_name = random.choice(last_names)
        first_name = random.choice(first_names)
        full_name = last_name + first_name
        return full_name

    def start_answers(self):
        logger.info("---- 开始进行自动答案 ----")
        for index in range(self.selected_number):
            logger.info(f"---- 自动答案第<{self.selected_number}>次 ----")
            self.start()

    def start(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")  # 窗口最大化，等同于Java中窗口全屏操作
        self.web_driver = webdriver.Chrome(
            options=options)  # 如果没配置环境变量，可在这里指定驱动路径，如webdriver.Chrome('path/to/chromedriver')
        # self.web_driver.delete_all_cookies()  # 删除所有Cookie
        # 设置隐式等待时间为10秒
        self.web_driver.implicitly_wait(10)  # 设置隐式等待时间为10秒
        self.web_driver.get("http://www.jscdc.cn/")
        self.web_driver.find_element(By.LINK_TEXT, "疾控服务").click()
        health_element = self.web_driver.find_element(By.XPATH, "//*[@class='part03']/div[2]/a[1]")
        href = health_element.get_attribute("href")
        self.web_driver.get(href)


        # 获取当前窗口句柄
        current_handle = self.web_driver.current_window_handle
        logger.info(f"currentHandle:{current_handle}")

        # 切换到新打开的窗口（根据实际情况，可能需要更准确的判断逻辑，如果有多个窗口的话）
        for handle in self.web_driver.window_handles:
            if handle != current_handle:
                self.web_driver.switch_to.window(handle)
        self.set_auto_option()




    def set_auto_option(self):
        # 市  地区
        city = self.web_driver.find_element(By.ID, "zone3")
        city_options = city.find_elements(By.TAG_NAME, "option")
        for city_option in city_options:
            if city_option.text == self.zone3_value:
                city_option.click()
                logger.info(f"---- 设置<市>:{city_option.text} ----")
                self.zone3_status = True
                break

        # 县  地区
        county = self.web_driver.find_element(By.ID, "zone4")
        county_options = county.find_elements(By.TAG_NAME, "option")
        for county_option in county_options:
            if county_option.text == self.zone4_value:
                county_option.click()
                logger.info(f"---- 设置<县>:{county_option.text} ----")
                self.zone4_status = True
                break

        # 乡  地区
        countryside = self.web_driver.find_element(By.ID, "zone5")
        countryside_options = countryside.find_elements(By.TAG_NAME, "option")
        for countryside_option in countryside_options:
            if countryside_option.text == self.zone5_value:
                countryside_option.click()
                logger.info(f"---- 设置<乡>:{countryside_option.text} ----")
                self.zone5_status = True
                break

        # 姓名，这里假设你有获取中文姓名的对应逻辑，示例中暂时使用固定字符串替代
        name = self.web_driver.find_element(By.ID, "name")
        name.send_keys(self.name_value)
        # 年龄
        age_group = self.web_driver.find_element(By.ID, "ageGroup")
        age_group_options = age_group.find_elements(By.TAG_NAME, "option")
        for age_group_option in age_group_options:
            if age_group_option.text == self.age_value:
                age_group_option.click()
                logger.info(f"---- 设置<年龄>:{age_group_option.text} ----")
                self.age_status = True
                break

        # 性别
        sex = self.web_driver.find_element(By.ID, "sex")
        sex_options = sex.find_elements(By.TAG_NAME, "option")
        for sex_option in sex_options:
            if sex_option.text == self.gender_value:
                sex_option.click()
                logger.info(f"---- 设置<性别>:{sex_option.text} ----")
                self.gender_status = True
                break

        # 教育
        education_status = self.web_driver.find_element(By.ID, "educationStatus")
        education_status_options = education_status.find_elements(By.TAG_NAME, "option")
        for education_status_option in education_status_options:
            if education_status_option.text == self.culture_value:
                education_status_option.click()
                logger.info(f"---- 设置<教育>:{education_status_option.text} ----")
                self.culture_status = True
                break

        # 职业
        metier = self.web_driver.find_element(By.ID, "metier")
        metier_options = metier.find_elements(By.TAG_NAME, "option")

        for metier_option in metier_options:
            if metier_option.text == self.job_value:
                metier_option.click()
                self.job_status = True
                logger.info(f"---- 设置<职业>:{metier_option.text} ----")
                break

        # 单位
        logger.info("---- 设置<单位> ----")
        org_name = self.web_driver.find_element(By.ID, "orgName")
        org_name.send_keys(self.company_value)


        logger.info("---- 开始死循环判断 ----")
        max_retries = 10  # 定义最大重试次数，可以根据实际情况调整
        retry_count = 0
        while self.while_flag and retry_count < max_retries:
            try:
                if self.is_all_selected():
                    self.while_flag = False
                    logger.info("---- 全部已选择，开始提交 ----")
                    self.submit_auto_answers()
                    break
                else:
                    logger.info("---- 缺失部分下拉选择，刷新页面 ----")
                    self.web_driver.refresh()
                    self.set_auto_option()

            except Exception as e:
                logger.error(f"在循环操作中出现异常: {e}")
                break
            retry_count += 1

        if retry_count == max_retries:
            logger.error("达到最大重试次数，仍未满足提交条件，自动答题流程结束。")

    def submit_auto_answers(self):

        wait = WebDriverWait(self.web_driver, 10)
        log_img_button = wait.until(EC.element_to_be_clickable((By.ID, "log_img")))
        log_img_button.click()
        logger.info("---- 点击了<开始学习测评> ----")

        # 点击按钮
        self.web_driver.find_element(By.ID, "log_img").click()

        logger.info("currentHandle:", self.web_driver.current_window_handle)

        # 做题部分
        subject = self.web_driver.find_element(By.ID, "subject")
        lis = subject.find_elements(By.TAG_NAME, "li")
        for ls in lis:
            k_wait = ls.find_element(By.CLASS_NAME, "KWait")
            input_radio = k_wait.find_elements(By.TAG_NAME, "input")
            if len(input_radio) > 4:
                i = random.randint(0, 3)
                input_radio[i].click()
                self.web_driver.find_element(By.ID, "btnNext").click()
            else:
                i = random.randint(0, 1)
                input_radio[i].click()
            # 交卷按钮
            count = len(lis)
            element = self.web_driver.find_element(By.ID, "btnAct" + str(count))
            element.find_element(By.TAG_NAME, "input").click()
            time.sleep(1)
            # 接受弹窗确认
            self.web_driver.switch_to.alert.accept()
            time.sleep(1)

            # 关闭窗口
            self.web_driver.quit()
    # 判断Select是不是全部选中
    def is_all_selected(self):
        # 这里编写具体要执行的操作内容，以下只是示例打印信息
        logger.info(f"城市: {self.zone3_status}")
        logger.info(f"区/县: {self.zone4_status}")
        logger.info(f"证件类型: {self.zone5_status}")
        logger.info(f"年龄: {self.age_status}")
        logger.info(f"性别: {self.gender_status}")
        logger.info(f"文化程度: {self.culture_status}")
        logger.info(f"职业: {self.job_status}")
        return (
                self.zone3_status and
                self.zone4_status and
                self.zone5_status and
                self.age_status and
                self.gender_status and
                self.culture_status and
                self.job_status
        )
