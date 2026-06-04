from page.page_back_login import BackLogin
from script import log
from tools import DriverTools


class TestBackLogin:
    def setup_method(self):
        driver = DriverTools.get_driver()
        self.page_back_login = BackLogin(driver)
        self.page_back_login.open_url()
    def teardown_method(self):
        self.page_back_login.get_shot("back_login.png")
        DriverTools.quit_driver()
    def test_back_login(self):
        self.page_back_login.input_info("admin","HM_2026_test", "8888")
        self.page_back_login.click_login_button()
        result = self.page_back_login.get_success_result()
        log.info(f"后台登录结果：{result}")
        assert "欢迎您的光临" in result
