import pytest
from page.page_login import PageLogin
from script import log
from tools import DriverTools, read_json
class TestLogin:
    @pytest.mark.parametrize("phone,password,expect",read_json("login_data.json"))
    def test_01_login(self,phone,password, expect,a_login):

        a_login.login(phone, password)#登录
        #打印日志
        if expect == phone:
            result = a_login.get_success_result()
        else:
            result = a_login.get_fail_result()
        # print(result)
        log.info(f"登录结果：{result}")
        #断言
        assert expect in result



