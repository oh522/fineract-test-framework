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
        """鼠标悬停到品质理财"""
        self.base_move_to_element(self.quality_wealth_management)

    def click_personal_loan(self):
        """点击在线申请"""
        self.base_click(self.personal_loan)

    def base_switch_window(self):
        """切换到新窗口"""
        return self.base_switch_handle(self.loc1)

    def input_project_name(self, text="测试项目"):
        """输入项目名称"""
        self.base_input(self.project_name, text)

    def select_city_province(self, text="河北省"):
        """选择省份"""
        self.base_select_list(self.city_province, text)

    def select_city_city(self, text="石家庄"):
        """选择城市"""
        self.base_select_list(self.city_city, text)

    def input_loan_amount(self, text="100"):
        """输入贷款金额"""
        self.base_input(self.loan_amount, text)

    def input_loan_term(self, text="1"):
        """输入贷款期限"""
        self.base_input(self.loan_term, text)

    def input_annualized_return_rate(self, text="5"):
        """输入年化收益率"""
        self.base_input(self.annualized_return_rate, text)

    def input_detailed_description(self, text="测试项目描述"):
        """输入详细描述"""
        self.base_input(self.detailed_description, text)

    def click_submit(self):
        """点击提交按钮"""
        self.base_click(self.submit)

    def get_success_result(self):
        """获取提交成功结果"""
        time.sleep(2)
        try:
            success_text = self.base_get_text(self.success_message)
            return success_text
        except Exception as e:
            self.get_shot("apply_online_error.png")
            raise e

    def go_apply_online(self, project_name="测试项目", province="河北省", city="石家庄",
                        amount="100", period="1", apr="5", description="测试项目描述"):
        """执行完整的在线申请流程，支持参数化"""
        self.move_quality_wealth_management()
        self.click_personal_loan()
        self.base_switch_window()
        self.input_project_name(project_name)
        self.select_city_province(province)
        self.select_city_city(city)
        self.input_loan_amount(amount)
        self.input_loan_term(period)
        self.input_annualized_return_rate(apr)
        self.input_detailed_description(description)
        self.click_submit()
        result = self.get_success_result()
        return result


if __name__ == '__main__':
    driver = DriverTools.get_driver()
    page_login1 = PageLogin(driver)
    page_login1.open_url()
    # 调用登录方法
    page_login1.login("13800001001", "Aa123456")
    time.sleep(2)
    cs = ApplyOnline(driver)
    result = cs.go_apply_online()
    print(f"申请结果: {result}")
    driver.quit()
