#类的三要素
#定义页面类
#定义实例属性
#定义实例方法
from ui_test.config import BASE_URL
from ui_test.base import BasePage
from ui_test.tools import DriverTools
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class PageLogin(BasePage):
    def open_url(self):
        self.driver.get(BASE_URL + "/common/member/login")
    """登录页面"""
    #设置页面实例属性
    def __init__(self, driver):#浏览器会变化使用driver形参
        #获取driver对象
        # self.driver = Tools.get_driver()
        # driver = DriverTools.get_driver()  #获取driver对象
        super().__init__(driver) #继承父类属性
        self.username = (By.ID, "keywords")
        self.password = (By.ID, "password")
        self.login_button = (By.ID, "login-btn")
        # 成功结果元素
        self.success_result = (By.XPATH, "//*[@id='mlayout']/div[1]/div[1]/div/div[2]/li[1]/span/a")
        # self.success_result = (By.CLASS_NAME, "a-link1")
        #失败结果元素
        self.fail_result = (By.CSS_SELECTOR, "#err > span")
    def login(self, username, password):
        """登录方法"""
        self.base_input(self.username, username)
        self.base_input(self.password, password)
        self.base_click(self.login_button)
        # ele1 = self.fd_element(self.username)
        # ele1.clear()
        # ele1.send_keys(username)
        # ele2 = self.fd_element(self.password)
        # ele2.clear()
        # ele2.send_keys(password)
        # self.fd_element(self.login_button).click()

        # ele1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.username))
        # ele1.clear()
        # ele1.send_keys( username)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.password)).send_keys( password)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.login_button)).click()

        # self.driver.find_element(*self.username).send_keys(username)
        # self.driver.find_element(*self.password).send_keys(password)
        # self.driver.find_element(*self.login_button).click()
    # def get_success_result(self):
    #     """获取登录结果"""
    #     time.sleep(2)
    #     return self.fd_element(self.success_result).text
    def get_success_result(self):
        """获取登录结果"""
        return self.fd_element(self.success_result).text

    def get_fail_result(self):
        """获取登录结果"""
        return self.fd_element(self.fail_result).text



if __name__ == '__main__':
    #创建登录页面对象
    page_login1 = PageLogin(DriverTools.get_driver())
    page_login1.open_url()
    #调用登录方法
    page_login1.login("13800001001", "Aa123456")


