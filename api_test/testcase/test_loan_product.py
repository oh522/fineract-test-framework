# test_loan_product.py
import uuid
from datetime import datetime, timedelta


class TestCreateLoan:
    """贷款申请测试"""

    def test_create_loan_success(self, api, client_id, loan_product_id):
        """✅ 正常创建贷款申请"""
        today = datetime.now()
        future = today + timedelta(days=30)

        payload = {
            "clientId": client_id,
            "productId": loan_product_id,
            "principal": 1000,
            "loanTermFrequency": 12,
            "loanTermFrequencyType": 2,
            "numberOfRepayments": 12,
            "repaymentEvery": 1,
            "repaymentFrequencyType": 2,
            "interestRatePerPeriod": 2,
            "amortizationType": 1,
            "interestType": 0,
            "interestCalculationPeriodType": 1,
            "transactionProcessingStrategyCode": "mifos-standard-strategy",
            "expectedDisbursementDate": future.strftime("%d %B %Y"),
            "submittedOnDate": today.strftime("%d %B %Y"),
            "dateFormat": "dd MMMM yyyy",
            "locale": "en",
            "loanType": "individual",
        }

        res = api.post("/loans", json=payload)
        assert res.status_code == 200, f"创建失败: {res.text}"
        
        # ---- 验证返回结果 ----
        data = res.json()
        assert "loanId" in data, "应返回 loanId"
        assert isinstance(data["loanId"], int)

    def test_create_loan_invalid_client(self, api, loan_product_id):
        """❌ 不存在的客户，应失败"""
        payload = {
            "clientId": 9999999,  # 不存在
            "productId": loan_product_id,
            "principal": 1000,
            # ...
        }
        res = api.post("/loans", json=payload)
        assert res.status_code == 404, "无效客户应返回404"

    def test_create_loan_zero_amount(self, api, client_id, loan_product_id):
        """❌ 金额为0，应失败"""
        payload = {
            "clientId": client_id,
            "productId": loan_product_id,
            "principal": 0,  # 零金额
            # ...
        }
        res = api.post("/loans", json=payload)
        assert res.status_code == 400, "零金额应返回400"

    def test_create_loan_exceeds_max(self, api, client_id, loan_product_id):
        """❌ 超过最大贷款额度"""
        payload = {
            "clientId": client_id,
            "productId": loan_product_id,
            "principal": 999999999,  # 超大金额
            # ...
        }
        res = api.post("/loans", json=payload)
        # 根据业务规则，可能是 400 或 403
        assert res.status_code in [400, 403]