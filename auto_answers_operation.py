import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger
from selenium.webdriver.support.select import Select


def perform_operation(zone3, zone4, zone5, name, age, gender, culture, job, company):
    # 这里编写具体要执行的操作内容，以下只是示例打印信息
    logger.info(f"城市: {zone3}")
    logger.info(f"区/县: {zone4}")
    logger.info(f"证件类型: {zone5}")
    logger.info(f"姓名: {name}")
    logger.info(f"年龄: {age}")
    logger.info(f"性别: {gender}")
    logger.info(f"文化程度: {culture}")
    logger.info(f"职业: {job}")
    logger.info(f"公司: {company}")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # 窗口最大化，等同于Java中窗口全屏操作
    web_driver = webdriver.Chrome(options=options) # 如果没配置环境变量，可在这里指定驱动路径，如webdriver.Chrome('path/to/chromedriver')
    web_driver.delete_all_cookies()  # 删除所有Cookie

    """
        自动做题的主函数，包含整个自动化流程操作
        """
    # 设置隐式等待时间为10秒

    web_driver.get("http://www.jscdc.cn/")
    web_driver.find_element(By.LINK_TEXT, "疾控服务").click()
    health_element = web_driver.find_element(By.XPATH, "//*[@class='part03']/div[2]/a[1]")
    href = health_element.get_attribute("href")
    web_driver.get(href)
    # 获取当前窗口句柄
    current_handle = web_driver.current_window_handle
    print("currentHandle:", current_handle)

    # 切换到新打开的窗口（根据实际情况，可能需要更准确的判断逻辑，如果有多个窗口的话）
    for handle in web_driver.window_handles:
        if handle != current_handle:
            web_driver.switch_to.window(handle)
    print(web_driver.title)


    """
    填充个人信息的函数
    """
    zone3_status, zone4_status, zone5_status, age_status, gender_status, culture_status, job_status = False
    # 市  地区
    city = web_driver.find_element(By.ID, "zone3")
    city_options = city.find_elements(By.TAG_NAME, "option")
    for city_option in city_options:
        if city_option.text == zone3:
            city_option.click()
            zone3_status = True
            break
    # 县  地区
    county = web_driver.find_element(By.ID, "zone4")
    county_options = county.find_elements(By.TAG_NAME, "option")
    for county_option in county_options:
        if county_option.text == zone4:
            county_option.click()
            zone4_status = True
            break
    # 乡  地区
    countryside = web_driver.find_element(By.ID, "zone5")
    countryside_options = countryside.find_elements(By.TAG_NAME, "option")
    for countryside_option in countryside_options:
        if countryside_option.text == zone5:
            countryside_option.click()
            zone5_status = True
            break
    # 姓名，这里假设你有获取中文姓名的对应逻辑，示例中暂时使用固定字符串替代
    name = web_driver.find_element(By.ID, "name")
    name.send_keys("示例姓名")
    # 年龄
    age_group = web_driver.find_element(By.ID, "ageGroup")
    age_group_options = age_group.find_elements(By.TAG_NAME, "option")
    for age_group_option in age_group_options:
        if age_group_option.text == age:
            age_group_option.click()
            age_status = True
            break
    # 性别
    sex = web_driver.find_element(By.ID, "sex")
    sex_options = sex.find_elements(By.TAG_NAME, "option")
    for sex_option in sex_options:
        if sex_option.text == gender:
            sex_option.click()
            gender_status = True
            break
    # 教育
    education_status = web_driver.find_element(By.ID, "educationStatus")
    education_status_options = education_status.find_elements(By.TAG_NAME, "option")
    for education_status_option in education_status_options:
        if education_status_option.text == culture:
            education_status_option.click()
            culture_status = True
            break
    # 职业
    metier = web_driver.find_element(By.ID, "metier")
    metier_options = metier.find_elements(By.TAG_NAME, "option")

    for metier_option in metier_options:
        if metier_option.text == job:
            metier_option.click()
            job_status = True
            break

    # 单位
    org_name = web_driver.find_element(By.ID, "orgName")
    org_name.send_keys(company)


    # 点击按钮
    web_driver.find_element(By.ID, "log_img").click()

    print("currentHandle:", web_driver.current_window_handle)

    # 做题部分
    subject = web_driver.find_element(By.ID, "subject")
    lis = subject.find_elements(By.TAG_NAME, "li")
    for ls in lis:
        k_wait = ls.find_element(By.CLASS_NAME, "KWait")
        input = k_wait.find_elements(By.TAG_NAME, "input")
        if len(input) > 4:
            i = random.randint(0, 3)
            input[i].click()
            web_driver.find_element(By.ID, "btnNext").click()
        else:
            i = random.randint(0, 1)
            input[i].click()
        # 交卷按钮
        count = len(lis)
        element = web_driver.find_element(By.ID, "btnAct" + str(count))
        element.find_element(By.TAG_NAME, "input").click()
        time.sleep(1)
        # 接受弹窗确认
        web_driver.switch_to.alert.accept()
        time.sleep(1)

        # 关闭窗口
        web_driver.quit()

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