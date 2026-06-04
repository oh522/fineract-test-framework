import pytest
from page.page_login import PageLogin
from script import log
from tools import DriverTools, read_json
class TestLogin:
    #前置方法
    def setup_method(self):
        driver = DriverTools.get_driver()#获取driver对象
        self.page_login = PageLogin(driver)#创建页面对象
        self.page_login.open_url()#打开页面
    #后置方法
    def teardown_method(self):
        DriverTools.quit_driver()
    @pytest.mark.parametrize("phone,password,expect",read_json("login_data.json"))
    def test_01_login(self,phone,password, expect):
        self.page_login.login(phone, password)#登录
        #打印日志
        if expect == phone:
            result =self.page_login.get_success_result()
        else:
            result =self.page_login.get_fail_result()
        # print(result)
        log.info(f"登录结果：{result}")
        #断言
        assert expect in result



