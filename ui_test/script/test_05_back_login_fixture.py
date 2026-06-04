from page.page_back_login import BackLogin
from script import log
from tools import DriverTools
class TestBackLogin:

     def test_back_login(self, go_back_login):
        go_back_login.input_info("admin","HM_2025_test", "8888")
        go_back_login.click_login_button()
        result = go_back_login.get_success_result()
        log.info(f"后台登录结果：{result}")
        assert "欢迎您的光临" in result
