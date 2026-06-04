import time

from script import log
from tools import DriverTools
from page.page_back_login import BackLogin
from page.page_credit_review import PageCreditReview
class TestCreditReview:
    def setup_method(self):
        driver = DriverTools.get_driver()
        self.back_login = BackLogin(driver)
        self.back_login.open_url()
        self.back_login.input_info("admin","HM_2025_test", "8888")
        self.back_login.click_login_button()
        self.credit_review = PageCreditReview(driver)
        self.credit_review.menu_manager()
        self.credit_review.search_record("13800001001")
        self.credit_review.select_record()
    def teardown_method(self):
        self.credit_review.get_shot("credit_review.png")
        DriverTools.quit_driver()
    def test_credit_review(self):
        self.credit_review.review_commit("审核通过", "8888")
        time.sleep(1)
        self.credit_review.application_record("13800001001")
        result = self.credit_review.get_success_result()
        log.info(f"额度申请记录结果：{result}")
        assert "通过" == result
