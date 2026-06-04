from selenium.webdriver.common.by import By
from ui_test.base import BasePage
from ui_test.config import BACK_URL
class BackLogin(BasePage):
    """后台登录页面类"""
    def __init__(self, driver):#浏览器会变化使用driver形参
        super().__init__(driver)#继承父类属性
        self.username = (By.ID, "username")
        self.password = (By.ID, "password")
        self.valicode = (By.ID, "valicode")
        self.login_button = (By.CLASS_NAME, "login-button")

        # self.success_result = (By.XPATH, '//*[@id="breadcrumbs"]/div')
        self.success_result = (By.CLASS_NAME, 'wel')
        self.fail_result = (By.ID, 'errorMessage')
    def open_url(self):#打开页面
        self.driver.get(BACK_URL)
    def input_info(self, username, password, valicode):#输入账号密码验证码的 方法
        self.base_input(self.username, username)
        self.base_input(self.password, password)
        self.base_input(self.valicode, valicode)
    def click_login_button(self):    #点击登录按钮的 方法
        self.base_click(self.login_button)
    def get_success_result(self):
        return self.fd_element(self.success_result).text
    def get_fail_result(self):
        return self.fd_element(self.fail_result)

