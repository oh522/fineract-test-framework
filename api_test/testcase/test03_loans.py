import pytest
from datetime import datetime, timedelta

DATE_META = {"dateFormat": "dd MMMM yyyy", "locale": "en"}


def _base_loan_payload(client_id: int, product_id: int) -> dict:
    """构建最小可用贷款申请 payload"""
    today = datetime.now()
    return {
        "clientId": client_id,
        "productId": product_id,
        "principal": 10000,
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
        "expectedDisbursementDate": (today + timedelta(days=7)).strftime("%d %B %Y"),
        "submittedOnDate": today.strftime("%d %B %Y"),
        "loanType": "individual",
        **DATE_META,
    }


class TestCreateLoan:
    """POST /loans"""

    def test_success(self, api, client_id, loan_product_id):
        """✅ 正常创建贷款申请"""
        res = api.post("/loans", json=_base_loan_payload(client_id, loan_product_id))
        assert res.status_code == 200, f"创建失败: {res.text}"

        data = res.json()
        assert "loanId" in data, "响应缺少 loanId"
        assert isinstance(data["loanId"], int)
        assert "resourceExternalId" in data

    def test_invalid_client(self, api, loan_product_id):
        """❌ 不存在的客户"""
        payload = _base_loan_payload(999999, loan_product_id)
        res = api.post("/loans", json=payload)
        assert res.status_code in [400, 404], f"无效客户应返回错误，实际: {res.status_code}"

    def test_invalid_product(self, api, client_id):
        """❌ 不存在的贷款产品"""
        payload = _base_loan_payload(client_id, 999999)
        res = api.post("/loans", json=payload)
        assert res.status_code in [400, 404]

    @pytest.mark.parametrize("principal, desc", [
        (0,          "零金额"),
        (-1,         "负金额"),
        (999999999,  "超大金额"),
    ])
    def test_invalid_principal(self, api, client_id, loan_product_id, principal, desc):
        """❌ 金额边界值"""
        payload = _base_loan_payload(client_id, loan_product_id)
        payload["principal"] = principal
        res = api.post("/loans", json=payload)
        assert res.status_code in [400, 403], f"{desc} 应返回错误，实际: {res.status_code}"

    @pytest.mark.parametrize("field", [
        "clientId", "productId", "principal",
        "loanTermFrequency", "numberOfRepayments",
    ])
    def test_missing_required_field(self, api, client_id, loan_product_id, field):
        """❌ 缺少必填字段"""
        payload = _base_loan_payload(client_id, loan_product_id)
        del payload[field]
        res = api.post("/loans", json=payload)
        assert res.status_code in [400, 422], f"缺少 {field} 应返回错误"


class TestGetLoan:
    """GET /loans/{loanId}"""

    def test_get_active_loan(self, api, loan_id):
        """✅ 查询已放款的贷款（loan_id 由 conftest 创建→审批→放款）"""
        res = api.get(f"/loans/{loan_id}")
        assert res.status_code == 200, f"查询失败: {res.text}"

        data = res.json()
        assert data["id"] == loan_id
        assert data["status"]["value"] == "Active"

    def test_get_nonexistent(self, api):
        """❌ 查询不存在的贷款"""
        res = api.get("/loans/999999")
        assert res.status_code == 404

    def test_get_with_associations(self, api, loan_id):
        """✅ 查询贷款详情附带关联数据"""
        res = api.get(f"/loans/{loan_id}", params={
            "associations": "repaymentSchedule,transactions"
        })
        assert res.status_code == 200
        data = res.json()
        assert "repaymentSchedule" in data
        assert "transactions" in data