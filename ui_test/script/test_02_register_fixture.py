from page.page_register import Register
from script import log
from tools import DriverTools
class TestRegister:
    #前置方法

    def test_01_register_success(self, go_register_page):
        go_register_page.register("13866801668", "Aa123456", "8888", "666666")
        #打印日志
        result =go_register_page.get_success_result()
        log.info(f"注册结果：{result}")
        #断言
        assert "注册成功" in result
    def test_02_register_fail_phone_error(self, go_register_page):
        go_register_page.register("1386680166", "Aa123456", "8888", "666666")
        #打印日志
        result =go_register_page.get_fail_result()
        log.info(f"注册结果：{result}")
        #断言
        assert "注册抢88现金" in result
