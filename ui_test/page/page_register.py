import time
from base import BasePage
from tools import DriverTools
class Register(BasePage):
    #网址
    def open_url(self):
        from config import BASE_URL
        self.driver.get(BASE_URL + "/common/member/reg")
    """注册页面类"""
    def __init__(self,driver):
        super().__init__(driver)
        from selenium.webdriver.common.by import By
        self.phone_number = (By.ID, "phone")
        self.password = (By.ID, "password")
        self.verification_code = (By.ID, "verifycode")
        self.SMS_Verification_Code = (By.ID, "phone_code")
        self.Send_Code = (By.ID, "get_phone_code")
        self.lg_btn = (By.XPATH, '//*[@id="reg_form"]/div[2]/div[6]/input')
        self.success_result = (By.XPATH, '//*[@id="step3"]/div/div')
        self.fail_result = (By.CLASS_NAME, 'reg-title')

    def register(self, phone_number, password, verification_code, SMS_Verification_Code):
        self.base_input(self.phone_number, phone_number)
        self.base_input(self.password, password)
        self.base_input(self.verification_code, verification_code)
        self.base_click(self.Send_Code)
        time.sleep(2)
        self.base_input(self.SMS_Verification_Code, SMS_Verification_Code)
        self.base_click(self.lg_btn)
    def get_success_result(self):
        """获取登录结果"""
        time.sleep(2)
        return self.fd_element(self.success_result).text
    def get_fail_result(self):
        """获取登录结果"""
        return self.fd_element(self.fail_result).text
if __name__ == '__main__':
    #创建登录页面对象
    page_register = Register(DriverTools.get_driver())
    page_register.open_url()
    #调用登录方法
    page_register.register("13800001812", "Aa123456", "8888", "666666")
    print(page_register.get_success_result())
    time.sleep(2)