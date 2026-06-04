import time
from selenium.webdriver.common.by import By
from base.base import BasePage
from page.page_login import PageLogin
from tools import DriverTools


class ApplyOnline(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.quality_wealth_management = (By.XPATH, '//*[contains(text(), "品质理财")]')
        self.personal_loan = (By.XPATH, '//*[contains(text(), "在线申请")]')
        self.loc1 = (By.XPATH, '//*[contains(text(), "在线申请")]')
        self.project_name = (By.NAME, 'name')
        self.city_province = (By.NAME, 'province')
        self.city_city = (By.NAME, 'city')
        self.loan_amount = (By.NAME, 'amount')
        self.loan_term = (By.NAME, 'period')
        self.annualized_return_rate = (By.NAME, 'apr')
        self.detailed_description = (By.NAME, 'contents')
        self.submit = (By.CLASS_NAME, 'lg-btn')
        self.success_message = (By.XPATH, '//*[contains(text(), "成功") or contains(text(), "提交成功")]')
    def move_quality_wealth_management(self):
        self.base_move_to_element(self.quality_wealth_management)
    def click_personal_loan(self):
        self.base_click(self.personal_loan)
    def base_switch_window(self):
        return self.base_switch_handle(self.loc1)
    def input_project_name(self):
        self.base_input(self.project_name, "测试项目")
    def select_city_province(self):
        self.base_select_list(self.city_province, "河北省")
    def select_city_city(self):
        self.base_select_list(self.city_city, "石家庄")
    def input_loan_amount(self):
        self.base_input(self.loan_amount, "100")
    def input_loan_term(self):
        self.base_input(self.loan_term, "1")
    def input_annualized_return_rate(self):
        self.base_input(self.annualized_return_rate, "5")
    def input_detailed_description(self):
        self.base_input(self.detailed_description, "测试项目描述")
    def click_submit(self):
        self.base_click(self.submit)
    def get_success_result(self):
        time.sleep(2)
        try:
            success_text = self.base_get_text(self.success_message)
            return success_text
        except Exception as e:
            self.get_shot("apply_online_error.png")
            raise e
    def go_apply_online(self):
        self.move_quality_wealth_management()
        self.click_personal_loan()
        self.base_switch_window()
        self.input_project_name()
        self.select_city_province()
        self.select_city_city()
        self.input_loan_amount()
        self.input_loan_term()
        self.input_annualized_return_rate()
        self.input_detailed_description()
        self.click_submit()
        result = self.get_success_result()
        return result


if __name__ == '__main__':
    driver = DriverTools.get_driver()
    page_login1 = PageLogin(driver)
    page_login1.open_url()
    #调用登录方法
    page_login1.login("13800001001", "Aa123456")
    time.sleep(2)
    cs = ApplyOnline(driver)
    result = cs.go_apply_online()
    print(f"申请结果: {result}")
    driver.quit()


# class ApplyOnline(BasePage):
#     def __init__(self, driver):
#         super().__init__(driver)
#         self.quality_wealth_management = (By.XPATH, '//*[contains(text(), "品质理财")]')
#         self.personal_loan = (By.XPATH, '//*[contains(text(), "在线申请")]')
#         self.loc1 = (By.XPATH, '//*[contains(text(), "在线申请")]')
#         self.project_name = (By.NAME, 'name')
#         self.city_province = (By.NAME, 'province')
#         self.city_city = (By.NAME, 'city')
#         self.loan_amount = (By.NAME, 'amount')
#         self.loan_term = (By.NAME, 'period')
#         self.annualized_return_rate = (By.NAME, 'apr')
#         self.detailed_description = (By.NAME, 'contents')
#         self.submit = (By.CLASS_NAME, 'lg-btn')
#         self.loc2 = (By.XPATH, '//*[contains(text(), "下午好，")]')
#     def move_quality_wealth_management(self):
#         self.base_move_to_element(self.quality_wealth_management)
#     def click_personal_loan(self):
#         self.base_click(self.personal_loan)
#     def base_switch_window(self):
#         return self.base_switch_handle(self.loc1)
#     def input_project_name(self):
#         self.base_input(self.project_name, "测试项目")
#     def select_city_province(self):
#         self.base_select_list(self.city_province, "河北省")
#     def select_city_city(self):
#         self.base_select_list(self.city_city, "石家庄")
#     def input_loan_amount(self):
#         self.base_input(self.loan_amount, "100")
#     def input_loan_term(self):
#         self.base_input(self.loan_term, "1")
#     def input_annualized_return_rate(self):
#         self.base_input(self.annualized_return_rate, "5")
#     def input_detailed_description(self):
#         self.base_input(self.detailed_description, "测试项目描述")
#     def click_submit(self):
#         self.base_click(self.submit)
#     def get_success_result(self):
#         return self.base_get_text(self.loc2)
#     def go_apply_online(self):
#         self.move_quality_wealth_management()
#         self.click_personal_loan()
#         self.base_switch_window()
#         self.input_project_name()
#         self.select_city_province()
#         self.select_city_city()
#         self.input_loan_amount()
#         self.input_loan_term()
#         self.input_annualized_return_rate()
#         self.input_detailed_description()
#         self.click_submit()
#         self.get_success_result()
#
#
# if __name__ == '__main__':
#     driver = DriverTools.get_driver()
#     page_login1 = PageLogin(driver)
#     page_login1.open_url()
#     #调用登录方法
#     page_login1.login("13800001001", "Aa123456")
#     time.sleep(2)
#     cs = ApplyOnline(driver)
#     cs.go_apply_online()
#     driver.quit()