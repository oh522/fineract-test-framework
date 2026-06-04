from page.page_register import Register
from script import log
from tools import DriverTools
class TestRegister:
    #前置方法
    def setup_method(self):
        driver = DriverTools.get_driver()
        self.page_register = Register(driver)
        self.page_register.open_url()
    #后置方法
    def teardown_method(self):
        DriverTools.quit_driver()
    def test_01_register_success(self):
        self.page_register.register("13866801667", "Aa123456", "8888", "666666")
        #打印日志
        result =self.page_register.get_success_result()
        log.info(f"注册结果：{result}")
        #断言
        assert "注册成功" in result
    def test_02_register_fail_phone_error(self):
        self.page_register.register("1386680166", "Aa123456", "8888", "666666")
        #打印日志
        result =self.page_register.get_fail_result()
        log.info(f"注册结果：{result}")
        #断言
        assert "注册抢88现金" in result
