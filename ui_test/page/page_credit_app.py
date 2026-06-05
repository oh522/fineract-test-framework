import time
from base.base import BasePage
from selenium.webdriver.common.by import By
from page.page_login import PageLogin
class CreditAppPage(BasePage):
    def open_url(self):
        from ui_test.config import BASE_URL
        self.driver.get(BASE_URL + "/common/member/login")
        # ... existing code ...
    def __init__(self, driver):
        super().__init__(driver)
        self.switch = (By.XPATH, "//em[text()='借款账户']")
        self.application = (By.LINK_TEXT, "申请额度")
        self.money = (By.ID, "amount_account")
        self.detail = (By.NAME, "remark")
        self.code = (By.ID, "verifycode")
        self.submit = (By.CSS_SELECTOR, ".btn-submit.btn-md")
        self.success_result = (By.CSS_SELECTOR, "#amount_list > tr:nth-child(1) > td:nth-child(3)")
    def switch_roll(self):
        #隐式等待
        self.driver.implicitly_wait(10)
        self.base_click(self.switch)
    def click_app(self):
        self.base_click(self.application)
    def credit_app(self, money, detail, code):
        self.base_input(self.money, money)
        self.base_input(self.detail, detail)
        self.base_input(self.code, code)
        self.base_click(self.submit)
    def get_success_result(self):
        """获取登录结果"""
        # js = "window.scrollTo(0,2000)"
        # self.driver.execute_script(js)
        # time.sleep(2)
        return self.fd_element(self.success_result).text
if __name__ == '__main__':
    from tools import DriverTools
    driver = DriverTools.get_driver()
    page = CreditAppPage(driver)
    page.open_url()
    #登录
    PageLogin(driver).login("13800001001", "Aa123456")
    page.switch_roll()
    page.click_app()
    page.credit_app("1000", "test", "8888")




