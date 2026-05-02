# ui_test/pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Fineract 登录页面对象"""

    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.ID, "login-username")
        self.password_field = (By.ID, "login-password")
        self.login_button = (By.ID, "login-submit")

    def open(self, url):
        """打开登录页面"""
        self.driver.get(url)

    def login(self, username, password):
        """执行登录操作"""
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.username_field)
        )
        username_input.clear()
        username_input.send_keys(username)

        password_input = self.driver.find_element(*self.password_field)
        password_input.clear()
        password_input.send_keys(password)

        login_btn = self.driver.find_element(*self.login_button)
        login_btn.click()

        # 等待登录完成，跳转到主页
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/#/home")
        )
