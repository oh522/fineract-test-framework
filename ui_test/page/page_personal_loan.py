import time
from selenium.webdriver.common.by import By
from ui_test.base import BasePage
from ui_test.config import BASE_URL
from ui_test.page.page_login import PageLogin
from ui_test.tools import DriverTools

class PersonalLoan(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.quality_wealth_management = (By.XPATH, '//*[contains(text(), "品质理财")]')
        self.personal_loan = (By.XPATH, '//*[contains(text(), "个人借款")]')
        self.credit_listing = (By.XPATH, '//*[contains(text(), "立即借款")][1]')
        self.day_listing = (By.XPATH, '//*[contains(text(), "立即借款")][2]')
        self.guaranteed_listing = (By.XPATH, '//*[contains(text(), "立即借款")][3]')
        self.loan_title = (By.NAME, 'name')
        self.loan_purpose_loc = (By.NAME, "use")
        self.loan_amount = (By.NAME, 'amount')
        self.annual_interest_rate = (By.NAME, 'apr')
        self.loan_term_unit_month = (By.XPATH, '//*[@id="borrowPublish"]/div[7]/span/label[1]/input')
        self.loan_term_unit_day = (By.XPATH, '//*[@id="borrowPublish"]/div[7]/span/label[2]/input')
        self.repayment_method = (By.NAME, 'repay_type')
        self.loan_term = (By.NAME, 'period')
        self.fundraising_period = (By.NAME, 'validate')
        self.min_investment_amount = (By.ID, 'tender_amount_min')
        self.max_investment_amount = (By.ID, 'tender_amount_max')
        self.loan_description = (By.ID, 'borrow_contents')
        self.verification_code = (By.NAME, 'valicode')
        self.submit = (By.ID, 'borrowForm')
        self.loc1 = (By.XPATH, '//*[contains(text(), "我要借款-借款标介绍")]')
        self.loc2 = (By.XPATH, '//*[contains(text(), "下午好，")]')

    # def select_loan_purpose(self,):
    #     """
    #     选择借款用途
    #     :param purpose_text: 下拉选项的可见文本，如 "其他"、"买车"、"买房"
    #     """
    #     # 直接调用父类 BasePage 的 base_select_list 方法
    #     self.base_select_list(self.loan_purpose_loc, "其他")
    # def base_scroll_by_pixel(self, x=0, y=1500):
    #     """
    #     按像素滚动页面
    #     :param x: 水平滚动距离（右为正，左为负）
    #     :param y: 垂直滚动距离（下为正，上为负）
    #     """
    #     self.driver.execute_script(f"window.scrollBy({x}, {y});")
    def move_quality_wealth_management(self):
        self.base_move_to_element(self.quality_wealth_management)
    def click_personal_loan(self):
        self.base_click(self.personal_loan)

    def base_switch_window(self):#切换窗口
        return self.base_switch_handle(self.loc1)

    def click_credit_listing(self):
        self.base_click(self.credit_listing)

    def base_scroll_by_pixel(self, x=0, y=1500):
        self.driver.execute_script(f"window.scrollBy({x}, {y});")

    def input_loan_title(self):
        self.base_input(self.loan_title, "测试借款标题")

    def select_loan_purpose_loc(self):
        self.base_select_list(self.loan_purpose_loc, "其他")
    def input_loan_amount(self):
        self.base_input(self.loan_amount, "1000")
    def input_annual_interest_rate(self):
        self.base_input(self.annual_interest_rate, "5")
    def click_loan_term_unit_month(self):
        self.base_click(self.loan_term_unit_month)
    def select_repayment_method(self):
        self.base_select_list(self.repayment_method, "等额本息")
    def select_loan_term(self):
        self.base_select_list(self.loan_term, "3个月")
    def select_fundraising_period(self):
        self.base_select_list(self.fundraising_period, "1天")
    def select_min_investment_amount(self):
        self.base_select_list(self.min_investment_amount, "50元")
    def select_max_investment_amount(self):
        self.base_select_list(self.max_investment_amount, "1000元")
    def input_loan_description(self):
        self.base_input(self.loan_description, "测试借款描述")
    def input_verification_code(self):
        self.base_input(self.verification_code, "8888")
    def click_submit(self):
        self.base_click(self.submit)

    def go_personal_loan(self):
        self.move_quality_wealth_management()
        self.click_personal_loan()
        self.base_switch_window()
        self.click_credit_listing()
        self.base_scroll_by_pixel()
        self.input_loan_title()
        self.select_loan_purpose_loc()
        self.input_loan_amount()
        self.input_annual_interest_rate()
        self.click_loan_term_unit_month()
        self.select_repayment_method()
        self.select_loan_term()
        self.select_fundraising_period()
        self.select_min_investment_amount()
        self.select_max_investment_amount()
        self.input_loan_description()
        self.input_verification_code()
        self.click_submit()
    def get_success_result(self):
        return self.base_get_text(self.loc2)

if __name__ == '__main__':
    driver = DriverTools.get_driver()
    page_login1 = PageLogin(driver)
    page_login1.open_url()
    #调用登录方法
    page_login1.login("13800001001", "Aa123456")
    time.sleep(2)
    cs = PersonalLoan(driver)
    cs.go_personal_loan()
    driver.quit()


