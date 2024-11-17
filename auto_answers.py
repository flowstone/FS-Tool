import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication,QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QMenu, QSizePolicy,QMessageBox,QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,QPixmap, QIcon
import os

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time
from common_util import CommonUtil
import hashlib
from fs_constants import FsConstants
from sqlite_util import SQLiteTool
from auto_answers_list import AutoAnswersList

# 这里定义一些常见的姓氏和名字的列表，可以根据实际情况扩展
last_names = ["赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", "褚", "卫", "蒋", "沈", "韩", "杨"]
first_names = ["强", "伟", "芳", "娜", "秀英", "敏", "静", "丽", "军", "磊", "超", "鹏", "慧", "勇", "杰"]

class AutoAnswersApp(QMainWindow):
    def __init__(self):
        super().__init__()

        COMBO_BOX_STYLE = """
            QComboBox {
                #background-color: white;
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
        self.while_second_flag = True

        self.today = CommonUtil.get_today()
        self.error = 0
        self.success = 0
        self.sqlite = SQLiteTool(CommonUtil.get_db_full_path())

        self.setWindowTitle(FsConstants.AUTO_ANSWERS_WINDOW_TITLE)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)  # 设置主垂直布局的间距为10像素，可根据实际调整

        # 设置通用字体
        font = QFont()
        font.setPointSize(12)

        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        self.help_menu = self.addToolBar(FsConstants.TOOLBAR_HELP_TITLE)
        # 创建"打开"菜单项
        readme_action = QAction(FsConstants.TOOLBAR_README_TITLE, self)
        readme_action.triggered.connect(self.show_instructions)
        # 将菜单项添加到文件菜单
        self.help_menu.addAction(readme_action)
        main_layout.addWidget(self.help_menu)
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # 图片标签，单独占一行
        image_label = QLabel(self)
        pixmap = QPixmap(CommonUtil.get_resource_path(FsConstants.AUTO_ANSWERS_TITLE_IMAGE))  # 替换为实际的图片路径
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
        self.name_edit.setPlaceholderText("程序生成")
        self.name_edit.setReadOnly(True)
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
        self.times_combo.addItems(["1", "3", "5", "7", "50", "100", "200", "600"])
        self.times_combo.setFont(font)
        self.times_combo.setFixedWidth(120)
        self.times_combo.setStyleSheet(COMBO_BOX_STYLE)
        row4_layout.addWidget(times_label)
        row4_layout.addWidget(self.times_combo, 1)


        # 姓名输入框和标签
        passwd_label = QLabel("*访问密码")
        passwd_label.setFont(font)
        passwd_label.setStyleSheet("color:red;")
        self.passwd_edit = QLineEdit()
        self.passwd_edit.setPlaceholderText("指定手机号")
        self.passwd_edit.setFont(font)
        self.passwd_edit.setFixedWidth(120)
        row4_layout.addWidget(passwd_label)
        row4_layout.addWidget(self.passwd_edit, 1)
        main_layout.addLayout(row4_layout)

        # 第五行（提交按钮）
        row5_layout = QHBoxLayout()

        submit_button = QPushButton("提交")
        submit_button.setFont(font)
        submit_button.setFixedSize(100, 30)
        # 为按钮添加样式，鼠标悬停时背景变色，按下时文字变色等效果示例（可根据喜好调整）
        submit_button.setStyleSheet(COMBO_BOX_STYLE)
        submit_button.clicked.connect(self.start_answers)
        row5_layout.addWidget(submit_button)

        # 第五行（日志按钮）
        log_btn = QPushButton("日志")
        log_btn.setFont(font)
        log_btn.setFixedSize(100, 30)
        # 为按钮添加样式，鼠标悬停时背景变色，按下时文字变色等效果示例（可根据喜好调整）
        log_btn.setStyleSheet(COMBO_BOX_STYLE)
        row5_layout.addWidget(log_btn)

        main_layout.addLayout(row5_layout)

        log_btn.clicked.connect(self.look_logs)

        # 设置窗口整体样式，例如背景颜色（可按需修改）
        #self.setStyleSheet("QWidget { background-color: #f9f9f9; }")
        self.setLayout(main_layout)

    def look_logs(self):
        self.auto_answers_list = AutoAnswersList()
        self.auto_answers_list.show()

    def show_instructions(self):
        readme_text = FsConstants.AUTO_ANSWER_TOOLBAR_README_TEXT
        QMessageBox.information(self, FsConstants.TOOLBAR_README_TITLE, readme_text)

    @staticmethod
    def generate_name():
        last_name = random.choice(last_names)
        first_name = random.choice(first_names)
        full_name = last_name + first_name
        return full_name

    def start_answers(self):
        # 判断是否输入密码
        if self.passwd_edit.text() == "":
            QMessageBox.warning(self, "警告", "请输入访问密码！")
            return

        password = self.passwd_edit.text().encode('utf-8')
        md5_hash = hashlib.md5()
        md5_hash.update(password)
        encrypted_result = md5_hash.hexdigest()
        logger.info(f"MD加密后的内容：{encrypted_result}")
        # 加密后的密码  adf0558822da93b55f6fc48790ff3137
        if encrypted_result != FsConstants.AUTO_ANSWERS_PASSWORD_MD5:
            QMessageBox.warning(self, "警告", "密码错误！")
            return
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

        logger.info("---- 新增当天的答题记录 [START]----")
        try:
            data_one = self.sqlite.read_one(FsConstants.AUTO_ANSWERS_TABLE_NAME,"error,success",f"today = '{self.today}'")
            if data_one:
                self.error = data_one[0]
                self.success = data_one[1]
            else:
                create_data = {'today': self.today,'create_time': CommonUtil.get_current_time()}
                self.sqlite.create(FsConstants.AUTO_ANSWERS_TABLE_NAME,create_data)
        except Exception as e:
            logger.error(f"操作数据库遇到异常：{e}")
        logger.info("---- 新增当天的答题记录 [END]----")

        logger.info("---- 开始进行自动答题 ----")
        for index in range(self.selected_number):
            logger.info(f"---- 自动答题第<{index+1}>次 ----")
            self.while_flag = True
            self.start()
        self.sqlite.close()
        logger.info("---- 结束自动答题 ----")

    def start(self):

        logger.info("---- 开始配置chrome ----")
        # 获取当前脚本所在目录，用于构建驱动路径（可根据实际情况调整，如果驱动路径是固定的已知路径，可直接写具体路径）
        current_dir = os.path.dirname(os.path.abspath(__file__))
        driver_name = FsConstants.AUTO_ANSWERS_WIN_DRIVER_NAME
        if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
            driver_name = FsConstants.AUTO_ANSWERS_OTHER_DRIVER_NAME
        driver_path = os.path.join(current_dir, FsConstants.AUTO_ANSWERS_DRIVER_PATH,
                                   driver_name)  # Windows系统下驱动文件名是chromedriver.exe，Mac系统下一般是chromedriver（无后缀），这里以Windows为例，根据实际情况替换
        service = webdriver.ChromeService(executable_path=driver_path)

        options = webdriver.ChromeOptions()
        # 窗口最大化，等同于Java中窗口全屏操作
        options.add_argument("--start-maximized")
        #self.web_driver = webdriver.Firefox(options=options,service=FirefoxService(GeckoDriverManager().install()))
        #self.web_driver = webdriver.Edge(options=options, service=EdgeService(EdgeChromiumDriverManager().install()))
        #self.web_driver = webdriver.Chrome(options=options,service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))
        self.web_driver = webdriver.Chrome(service = service, options=options,)

        # self.web_driver.delete_all_cookies()  # 删除所有Cookie
        # 设置隐式等待时间为10秒
        self.web_driver.implicitly_wait(2)  # 设置隐式等待时间为10秒
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
        self.fill_person_info()

        self.set_auto_option()



    def check_is_refresh(self):
        logger.info("---- 判断页面下拉框是否加载完全 ----")
        # 市  地区
        city = self.web_driver.find_element(By.ID, "zone3")
        city_options = city.find_elements(By.TAG_NAME, "option")
        self.zone3_status = len(city_options) > 0
        logger.info(f"下拉框加载状态-zone3_status:{self.zone3_status}")

        # 县  地区
        county = self.web_driver.find_element(By.ID, "zone4")
        county_options = county.find_elements(By.TAG_NAME, "option")
        self.zone4_status = len(county_options) > 0
        logger.info(f"下拉框加载状态-zone4_status:{self.zone4_status}")

        # 乡  地区
        countryside = self.web_driver.find_element(By.ID, "zone5")
        countryside_options = countryside.find_elements(By.TAG_NAME, "option")
        self.zone5_status = len(countryside_options) > 0
        logger.info(f"下拉框加载状态-zone5_status:{self.zone5_status}")

        # 年龄
        age_group = self.web_driver.find_element(By.ID, "ageGroup")
        age_group_options = age_group.find_elements(By.TAG_NAME, "option")
        self.age_status = len(age_group_options) > 0
        logger.info(f"下拉框加载状态-age_status:{self.age_status}")


        # 性别
        sex = self.web_driver.find_element(By.ID, "sex")
        sex_options = sex.find_elements(By.TAG_NAME, "option")
        self.gender_status = len(sex_options) > 0
        logger.info(f"下拉框加载状态-gender_status:{self.gender_status}")



        # 教育
        education_status = self.web_driver.find_element(By.ID, "educationStatus")
        education_status_options = education_status.find_elements(By.TAG_NAME, "option")
        self.culture_status = len(education_status_options) > 0
        logger.info(f"下拉框加载状态-culture_status:{self.culture_status}")




        # 职业
        metier = self.web_driver.find_element(By.ID, "metier")
        metier_options = metier.find_elements(By.TAG_NAME, "option")
        self.job_status = len(metier_options) > 0
        logger.info(f"job_status:{self.job_status}")

    def set_auto_option(self):
        logger.info("---- 全部加载完全，开始设置下拉框 ----")
        # 市  地区
        city = self.web_driver.find_element(By.ID, "zone3")
        city_options = city.find_elements(By.TAG_NAME, "option")
        for city_option in city_options:
            if city_option.text == self.zone3_value:
                city_option.click()
                logger.info(f"设置<市>:{city_option.text} ")
                break

        # 县  地区
        county = self.web_driver.find_element(By.ID, "zone4")
        county_options = county.find_elements(By.TAG_NAME, "option")
        self.zone4_status = len(county_options) > 0
        for county_option in county_options:
            if county_option.text == self.zone4_value:
                county_option.click()
                logger.info(f"设置<县>:{county_option.text}")
                break

        # 乡  地区
        countryside = self.web_driver.find_element(By.ID, "zone5")
        countryside_options = countryside.find_elements(By.TAG_NAME, "option")
        for countryside_option in countryside_options:
            if countryside_option.text == self.zone5_value:
                countryside_option.click()
                logger.info(f"设置<乡>:{countryside_option.text}")
                break

        # 姓名，这里假设你有获取中文姓名的对应逻辑，示例中暂时使用固定字符串替代
        name = self.web_driver.find_element(By.ID, "name")
        name.send_keys(self.name_value)
        logger.info(f"设置<姓名>:{self.name_value}")

        # 年龄
        age_group = self.web_driver.find_element(By.ID, "ageGroup")
        age_group_options = age_group.find_elements(By.TAG_NAME, "option")
        for age_group_option in age_group_options:
            if age_group_option.text == self.age_value:
                age_group_option.click()
                logger.info(f"设置<年龄>:{age_group_option.text}")
                break

        # 性别
        sex = self.web_driver.find_element(By.ID, "sex")
        sex_options = sex.find_elements(By.TAG_NAME, "option")
        for sex_option in sex_options:
            if sex_option.text == self.gender_value:
                sex_option.click()
                logger.info(f"设置<性别>:{sex_option.text}")
                break

        # 教育
        education_status = self.web_driver.find_element(By.ID, "educationStatus")
        education_status_options = education_status.find_elements(By.TAG_NAME, "option")
        for education_status_option in education_status_options:
            if education_status_option.text == self.culture_value:
                education_status_option.click()
                logger.info(f"设置<教育>:{education_status_option.text}")
                break

        # 职业
        metier = self.web_driver.find_element(By.ID, "metier")
        metier_options = metier.find_elements(By.TAG_NAME, "option")

        for metier_option in metier_options:
            if metier_option.text == self.job_value:
                metier_option.click()
                logger.info(f"设置<职业>:{metier_option.text}")
                break

        # 单位
        org_name = self.web_driver.find_element(By.ID, "orgName")
        org_name.send_keys(self.company_value)
        logger.info(f"设置<单位>:{self.company_value}")

        self.submit_auto_answers()





    def fill_person_info(self):
        logger.info("---- 开始填充个人数据 ----")
        max_retries = 10  # 定义最大重试次数，可以根据实际情况调整
        retry_count = 0
        while self.while_flag and retry_count < max_retries:
            try:
                self.check_is_refresh()
                if not self.is_all_selected():
                    logger.info("---- 缺失部分下拉选择，刷新页面 ----")
                    self.web_driver.refresh()
                    time.sleep(2)
                else:
                    logger.info("---- 全部加载下拉框完成 ----")
                    self.while_flag = False
            except Exception as e:
                logger.error(f"在循环操作中出现异常: {e}")
                break
            retry_count += 1
            if retry_count > max_retries:
                logger.error("达到最大重试次数，仍未满足提交条件，自动答题流程结束。")



    def submit_auto_answers(self):

        logger.info("---- 点击了<开始学习测评> ----")
        try:
            # 点击按钮
            self.web_driver.find_element(By.ID, "log_img").click()

            logger.info("currentHandle:", self.web_driver.current_window_handle)
            self.web_driver.switch_to.window(self.web_driver.current_window_handle)

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
            logger.info("---- 交卷成功 ----")
            time.sleep(1)
            # 接受弹窗确认
            self.web_driver.switch_to.alert.accept()
            time.sleep(1)
            self.success += 1
        except Exception as e:
            logger.error(f"在开始评测中出现异常: {e}")
            self.error += 1

        # 关闭窗口
        self.web_driver.quit()
        try:

            logger.info("---- 插入答题次数到数据库 ----")
            logger.info(f"---- 当前error={self.error}, success={self.success} ----")
            update_dict = {'error': self.error, 'success': self.success, 'update_time': CommonUtil.get_current_time()}
            self.sqlite.update(FsConstants.AUTO_ANSWERS_TABLE_NAME, update_dict,
                                      f"today = '{self.today}'")
        except Exception as e:
            logger.warning(f"更新自动答题记录表失败，{e}")

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
