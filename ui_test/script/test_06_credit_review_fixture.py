import time

from script import log
from tools import DriverTools
from page.page_back_login import BackLogin
from page.page_credit_review import PageCreditReview
class TestCreditReview:
    def test_credit_review(self, go_credit_review):
        go_credit_review.review_commit("审核通过", "8888")
        time.sleep(1)
        go_credit_review.application_record("13800001001")
        result = go_credit_review.get_success_result()
        log.info(f"额度申请记录结果：{result}")
        assert "通过" == result
