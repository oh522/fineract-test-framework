import allure
import pytest
from datetime import datetime

from api_test.common.api.loan_api import LoanApi
from utils.assertion import (
    assert_status, assert_field, assert_jsonpath, assert_response_time,
)
from utils.db_helper import DBHelper

DATE_META = {"dateFormat": "dd MMMM yyyy", "locale": "en"}


@allure.feature("贷款管理")
class TestLoans:

    @allure.story("查询贷款详情")
    @pytest.mark.smoke
    @pytest.mark.P0
    def test_get_loan_detail(self, loan_api: LoanApi, loan_id):
        """✅ 已放款贷款状态应为 Active"""
        res = loan_api.get_detail(loan_id)           # ← API 层

        assert_status(res, 200)
        assert_response_time(res, 3.0)
        assert_jsonpath(res, "$.status.value", "Active")

        with DBHelper() as db:
            db.assert_loan_active(loan_id)           # ← DB 校验

    @allure.story("还款计划验证")
    @pytest.mark.P1
    def test_loan_repayment_schedule(self, loan_api: LoanApi, loan_id):
        """✅ 12 期还款计划结构验证"""
        res = loan_api.get_detail(loan_id)
        assert_status(res, 200)

        data = res.json()

        numberOfRepayments = data.get("numberOfRepayments")
        assert numberOfRepayments == 12, (
            f"期望12期，实际 {numberOfRepayments} 期"
        )

        with DBHelper() as db:
            rows = db.query_all(
                "SELECT * FROM m_loan_repayment_schedule WHERE loan_id = %s ORDER BY installment",
                (loan_id,)
            )
            assert len(rows) == 12, (
                f"数据库中期望12期还款计划，实际 {len(rows)} 期"
            )



    @allure.story("还款操作")
    @pytest.mark.P1
    @pytest.mark.flaky(reruns=2, reruns_delay=1)
    def test_loan_repayment(self, loan_api: LoanApi, loan_id):
        """✅ 还款后余额减少"""
        today = datetime.now().strftime("%d %B %Y")

        detail = loan_api.get_detail(loan_id).json()
        summary = detail.get("summary", {})
        before_balance = summary.get("principalOutstanding", 0)
        if isinstance(before_balance, dict):
            before_balance = before_balance.get("amount", 0)

        res = loan_api.repay(loan_id, {
            "transactionDate": today,
            "transactionAmount": 5000,
            "paymentTypeId": 1,
            **DATE_META,
        })
        assert_status(res, 200, msg="还款")
        assert_field(res, "resourceId")

        detail = loan_api.get_detail(loan_id).json()
        summary = detail.get("summary", {})
        after_balance = summary.get("principalOutstanding", 0)
        if isinstance(after_balance, dict):
            after_balance = after_balance.get("amount", 0)

        assert after_balance < before_balance, "还款后余额未减少"

    @allure.story("无效参数申请贷款")
    @pytest.mark.P2
    @pytest.mark.parametrize("desc,override", [
        ("金额为0",  {"principal": 0}),
        ("期数为0",  {"numberOfRepayments": 0}),
        ("缺clientId", {"clientId": None}),
    ], ids=["金额为零", "期数为零", "缺clientId"])
    def test_apply_loan_invalid(
        self, loan_api: LoanApi, client_id, loan_product_id, desc, override
    ):
        """❌ 无效参数应返回 4xx"""
        today = datetime.now().strftime("%d %B %Y")
        payload = {
            "clientId": client_id,
            "productId": loan_product_id,
            "principal": 50000,
            "loanTermFrequency": 12,
            "loanTermFrequencyType": 2,
            "numberOfRepayments": 12,
            "repaymentEvery": 1,
            "repaymentFrequencyType": 2,
            "interestRatePerPeriod": 1.5,
            "amortizationType": 1,
            "interestType": 0,
            "interestCalculationPeriodType": 1,
            "transactionProcessingStrategyCode": "mifos-standard-strategy",
            "submittedOnDate": today,
            "expectedDisbursementDate": today,
            **DATE_META,
        }
        # 应用无效覆盖
        for k, v in override.items():
            if v is None:
                payload.pop(k, None)
            else:
                payload[k] = v

        res = loan_api.apply(payload)                # ← API 层
        assert_status(res, 400, 403, 422, msg=desc)