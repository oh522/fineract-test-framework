import pytest
from config import *
from page.page_login import PageLogin
from page.page_open_account import OpenAccount
from tools import DriverTools
class TestOpenAccount:
    def test_01_open_account_success(self, a_login, a_open_account):
        a_open_account.open_account(NAME, CARD)# 开户
        result = a_open_account.get_success_result()  # 获取开户结果
        assert "OK" in result     # 断言

