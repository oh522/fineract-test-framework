import pytest
from api_test.common.base_api import BaseApi

class TestRetrieveLoanTransactions:
    # 正常用例：使用有效的贷款外部ID，期望成功获取交易记录
    def test_retrieve_transactions_success(self, api):
        loan_external_id = "loan_external_id_1"
        resp = api.get(f"/v1/loans/external-id/{loan_external_id}/transactions")
        assert resp.status_code == 200
        assert "pageItems" in resp.json()

    # 正常用例：使用有效贷款外部ID和查询参数，期望成功获取交易记录
    @pytest.mark.parametrize("params", [
        {"excludedTypes": ["DISBURSEMENT", "REPAYMENT"]},
        {"page": 0, "size": 10},
        {"sort": "id,desc"},
        {"excludedTypes": ["DISBURSEMENT"], "page": 1, "size": 5, "sort": "date,asc"}
    ])
    def test_retrieve_transactions_with_params_success(self, api, params):
        loan_external_id = "loan_external_id_1"
        resp = api.get(f"/v1/loans/external-id/{loan_external_id}/transactions", params=params)
        assert resp.status_code == 200
        assert "pageItems" in resp.json()

    # 参数缺失用例：缺少必填的路径参数loanExternalId
    def test_retrieve_transactions_missing_path_param(self, api):
        resp = api.get("/v1/loans/external-id//transactions")
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：使用不存在的贷款外部ID
    def test_retrieve_transactions_nonexistent_loan(self, api):
        loan_external_id = "999999"
        resp = api.get(f"/v1/loans/external-id/{loan_external_id}/transactions")
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：查询参数page为0
    def test_retrieve_transactions_page_zero(self, api):
        loan_external_id = "loan_external_id_1"
        params = {"page": 0}
        resp = api.get(f"/v1/loans/external-id/{loan_external_id}/transactions", params=params)
        assert resp.status_code == 200

    # 边界值用例：查询参数page为负数
    def test_retrieve_transactions_page_negative(self, api):
        loan_external_id = "loan_external_id_1"
        params = {"page": -1}
        resp = api.get(f"/v1/loans/external-id/{loan_external_id}/transactions", params=params)
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：查询参数size为0
    def test_retrieve_transactions_size_zero(self, api):
        loan_external_id = "loan_external_id_1"
        params = {"size": 0}
        resp = api.get(f"/v1/loans/external-id/{loan_external_id}/transactions", params=params)
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：查询参数size为极大值
    def test_retrieve_transactions_size_large(self, api):
        loan_external_id = "loan_external_id_1"
        params = {"size": 1000000}
        resp = api.get(f"/v1/loans/external-id/{loan_external_id}/transactions", params=params)
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：查询参数sort为空字符串
    def test_retrieve_transactions_sort_empty(self, api):
        loan_external_id = "loan_external_id_1"
        params = {"sort": ""}
        resp = api.get(f"/v1/loans/external-id/{loan_external_id}/transactions", params=params)
        assert resp.status_code in [400, 403, 404, 422]

    # 异常用例：查询参数excludedTypes包含无效的交易类型
    def test_retrieve_transactions_invalid_excluded_types(self, api):
        loan_external_id = "loan_external_id_1"
        params = {"excludedTypes": ["INVALID_TYPE", "ANOTHER_INVALID"]}
        resp = api.get(f"/v1/loans/external-id/{loan_external_id}/transactions", params=params)
        assert resp.status_code in [400, 403, 404, 422]

    # 异常用例：查询参数page为字符串
    def test_retrieve_transactions_page_string(self, api):
        loan_external_id = "loan_external_id_1"
        params = {"page": "abc"}
        resp = api.get(f"/v1/loans/external-id/{loan_external_id}/transactions", params=params)
        assert resp.status_code in [400, 403, 404, 422]

    # 异常用例：查询参数size为字符串
    def test_retrieve_transactions_size_string(self, api):
        loan_external_id = "loan_external_id_1"
        params = {"size": "xyz"}
        resp = api.get(f"/v1/loans/external-id/{loan_external_id}/transactions", params=params)
        assert resp.status_code in [400, 403, 404, 422]

    # 异常用例：查询参数sort包含特殊字符
    def test_re