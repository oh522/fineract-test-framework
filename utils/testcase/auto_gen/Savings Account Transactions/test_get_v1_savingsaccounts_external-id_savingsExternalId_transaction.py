import pytest
from api_test.common.base_api import BaseApi

class TestSavingsAccountTransactionByExternalId:
    
    # 正常用例：使用有效的储蓄账户外部ID和交易外部ID，期望成功获取交易详情
    def test_get_transaction_success(self, api):
        savings_external_id = "valid_savings_external_id_123"
        transaction_external_id = "valid_transaction_external_id_456"
        url = f"/v1/savingsaccounts/external-id/{savings_external_id}/transactions/external-id/{transaction_external_id}"
        resp = api.get(url)
        assert resp.status_code == 200
        assert "id" in resp.json()
        assert "externalId" in resp.json()
        assert "transactionType" in resp.json()
    
    # 参数缺失用例：缺少储蓄账户外部ID
    @pytest.mark.parametrize("savings_external_id, transaction_external_id", [
        (None, "valid_transaction_external_id_456"),
        ("", "valid_transaction_external_id_456"),
    ])
    def test_get_transaction_missing_savings_external_id(self, api, savings_external_id, transaction_external_id):
        if savings_external_id is None:
            url = f"/v1/savingsaccounts/external-id//transactions/external-id/{transaction_external_id}"
        else:
            url = f"/v1/savingsaccounts/external-id/{savings_external_id}/transactions/external-id/{transaction_external_id}"
        resp = api.get(url)
        assert resp.status_code in [400, 403, 404, 422]
    
    # 参数缺失用例：缺少交易外部ID
    @pytest.mark.parametrize("savings_external_id, transaction_external_id", [
        ("valid_savings_external_id_123", None),
        ("valid_savings_external_id_123", ""),
    ])
    def test_get_transaction_missing_transaction_external_id(self, api, savings_external_id, transaction_external_id):
        if transaction_external_id is None:
            url = f"/v1/savingsaccounts/external-id/{savings_external_id}/transactions/external-id/"
        else:
            url = f"/v1/savingsaccounts/external-id/{savings_external_id}/transactions/external-id/{transaction_external_id}"
        resp = api.get(url)
        assert resp.status_code in [400, 403, 404, 422]
    
    # 边界值用例：空字符串参数
    @pytest.mark.parametrize("savings_external_id, transaction_external_id", [
        ("", ""),
        ("", "valid_transaction_external_id_456"),
        ("valid_savings_external_id_123", ""),
    ])
    def test_get_transaction_empty_string_params(self, api, savings_external_id, transaction_external_id):
        url = f"/v1/savingsaccounts/external-id/{savings_external_id}/transactions/external-id/{transaction_external_id}"
        resp = api.get(url)
        assert resp.status_code in [400, 403, 404, 422]
    
    # 边界值用例：极大值参数
    @pytest.mark.parametrize("savings_external_id, transaction_external_id", [
        ("a" * 1000, "b" * 1000),
        ("a" * 1000, "valid_transaction_external_id_456"),
        ("valid_savings_external_id_123", "b" * 1000),
    ])
    def test_get_transaction_extreme_large_params(self, api, savings_external_id, transaction_external_id):
        url = f"/v1/savingsaccounts/external-id/{savings_external_id}/transactions/external-id/{transaction_external_id}"
        resp = api.get(url)
        assert resp.status_code in [400, 403, 404, 422]
    
    # 边界值用例：极小值参数（单个字符）
    @pytest.mark.parametrize("savings_external_id, transaction_external_id", [
        ("a", "b