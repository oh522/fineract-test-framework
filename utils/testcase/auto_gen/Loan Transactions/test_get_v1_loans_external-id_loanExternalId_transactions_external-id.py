import pytest
from api_test.common.base_api import BaseApi

class TestRetrieveLoanTransactionDetails:
    # 正常用例：使用有效路径参数和可选查询参数
    def test_retrieve_transaction_success(self, api):
        loan_external_id = "valid_loan_external_id"
        transaction_external_id = "valid_transaction_external_id"
        url = f"/v1/loans/external-id/{loan_external_id}/transactions/external-id/{transaction_external_id}"
        resp = api.get(url)
        assert resp.status_code == 200
        assert "id" in resp.json()
        assert "date" in resp.json()
        assert "amount" in resp.json()

    # 正常用例：使用fields查询参数过滤响应字段
    def test_retrieve_transaction_with_fields(self, api):
        loan_external_id = "valid_loan_external_id"
        transaction_external_id = "valid_transaction_external_id"
        url = f"/v1/loans/external-id/{loan_external_id}/transactions/external-id/{transaction_external_id}"
        params = {"fields": "id,date,amount"}
        resp = api.get(url, params=params)
        assert resp.status_code == 200
        assert "id" in resp.json()
        assert "date" in resp.json()
        assert "amount" in resp.json()

    # 参数缺失用例：缺少loanExternalId路径参数
    def test_missing_loan_external_id(self, api):
        transaction_external_id = "valid_transaction_external_id"
        url = f"/v1/loans/external-id//transactions/external-id/{transaction_external_id}"
        resp = api.get(url)
        assert resp.status_code in [400, 403, 404, 422]

    # 参数缺失用例：缺少externalTransactionId路径参数
    def test_missing_transaction_external_id(self, api):
        loan_external_id = "valid_loan_external_id"
        url = f"/v1/loans/external-id/{loan_external_id}/transactions/external-id/"
        resp = api.get(url)
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：路径参数为空字符串
    @pytest.mark.parametrize("loan_external_id, transaction_external_id", [
        ("", "valid_transaction_external_id"),
        ("valid_loan_external_id", ""),
        ("", "")
    ])
    def test_empty_path_parameters(self, api, loan_external_id, transaction_external_id):
        url = f"/v1/loans/external-id/{loan_external_id}/transactions/external-id/{transaction_external_id}"
        resp = api.get(url)
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：路径参数为超长字符串
    @pytest.mark.parametrize("loan_external_id, transaction_external_id", [
        ("a" * 1000, "valid_transaction_external_id"),
        ("valid_loan_external_id", "b" * 1000),
        ("c" * 1000, "d" * 1000)
    ])
    def test_long_path_parameters(self, api, loan_external_id, transaction_external_id):
        url = f"/v1/loans/external-id/{loan_external_id}/transactions/external-id/{transaction_external_id}"
        resp = api.get(url)
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：路径参数包含特殊字符
    @pytest.mark.parametrize("loan_external_id, transaction_external_id", [
        ("!@#$%^&*()", "valid_transaction_external_id"),
        ("valid_loan_external_id", "!@#$%^&*()"),
        ("!@#$%^&*()", "!@#$%^&*()")
    ])
    def test_special_characters_path_parameters(self, api, loan_external_id, transaction_external_id):
        url = f"/v1/loans/external-id/{loan_external_id}/transactions/external-id/{transaction_external_id}"
        resp = api.get(url)
        assert resp.status_code in [400, 403, 404, 422]