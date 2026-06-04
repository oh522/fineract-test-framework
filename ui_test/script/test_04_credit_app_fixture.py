import time
import pytest
from page.page_credit_app import CreditAppPage
from page.page_login import PageLogin
from script import log
from tools import DriverTools, read_json
class TestCreditApp:

    @pytest.mark.parametrize("expect_money,detail,code",read_json("credit_app.json") )
    def test_01_credit_app(self,expect_money,detail,code,go_credit_app):
        go_credit_app.switch_roll()
        go_credit_app.click_app()
        go_credit_app.credit_app(expect_money,detail, code)
        time.sleep(2)
        result = go_credit_app.get_success_result()
        result_clean = result.replace(",", "")
        expected_formatted = f"{float(expect_money):.2f}"
        #日志
        log.info(f"申请额度结果：{result}")
        assert result_clean == expected_formatted
    # def test_01_credit_app(self):
    #     expect_money = "1003"
    #     self.page_credit_app.switch_roll()
    #     self.page_credit_app.click_app()
    #     self.page_credit_app.credit_app(expect_money, "test", "8888")
    #     # time.sleep(2)
    #     result = self.page_credit_app.get_success_result()
    #     assert expect_money == result

