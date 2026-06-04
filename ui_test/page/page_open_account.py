from ui_test.base import BasePage
from ui_test.config import BASE_URL
class OpenAccount(BasePage):
    #地址
    def open_url(self):
        self.driver.get(BASE_URL + "/common/member/login")
    """开户页面类"""
    def __init__(self, driver):
        super().__init__(driver)
        from selenium.webdriver.common.by import By
        self.Subscribe_Now = (By.LINK_TEXT, "立即开通")
        self.name = (By.NAME, "realname")
        self.id_card = (By.NAME, "card_id")
        self.submit = (By.CLASS_NAME, "btn")
        self.submit2 = (By.CSS_SELECTOR, '.btn.ng-scope')
        self.success_result = (By.CSS_SELECTOR, 'body')

    def open_account(self, name, id_card):
        self.base_click(self.Subscribe_Now)
        self.base_input(self.name, name)
        self.base_input(self.id_card, id_card)
        self.base_click(self.submit)
        self.base_click(self.submit2)
    def get_success_result(self):
        """获取开户结果"""
        #切换到新窗口
        ele = self.base_switch_handle(self.success_result)
        return ele.text


