from config import *
from page.page_login import PageLogin
from page.page_open_account import OpenAccount
from tools import DriverTools


class TestOpenAccount:
    #前置方法
    def setup_method(self):
        driver = DriverTools.get_driver() # 获取driver对象
        self.page_open_account = OpenAccount(driver) # 创建页面对象
        self.page_open_account.open_url()
        self.page_login = PageLogin(driver) # 创建页面对象
        self.page_login.login("13866801667", "Aa123456")# 登录
    def teardown_method(self):
        DriverTools.quit_driver() # 关闭driver

    def test_01_open_account_success(self):
        self.page_open_account.open_account(NAME, CARD) #开户
        result = self.page_open_account.get_success_result()  # 获取开户结果
        assert "OK" in result     # 断言

