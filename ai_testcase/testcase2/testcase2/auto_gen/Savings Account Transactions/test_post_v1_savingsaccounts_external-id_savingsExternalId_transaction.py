import pytest
from api_test.common.base_api import BaseApi

class TestSavingsAccountTransactions:
    # 正常用例：使用所有字段，期望成功
    def test_undo_transaction_success(self, api):
        savings_external_id = "valid_savings_external_id"
        transaction_external_id = "valid_transaction_external_id"
        payload = {
            "externalId": "5dd80a7c-ccba-4446-b378-01eb6f53e871",
            "isBulk": "true"
        }
        resp = api.post(
            f"/v1/savingsaccounts/external-id/{savings_external_id}/transactions/external-id/{transaction_external_id}",
            json=payload,
            params={"command": "undo"}
        )
        assert resp.status_code == 200
        assert "resourceId" in resp.json()

    # 正常用例：不带查询参数command
    def test_undo_transaction_without_command(self, api):
        savings_external_id = "valid_savings_external_id"
        transaction_external_id = "valid_transaction_external_id"
        payload = {
            "externalId": "5dd80a7c-ccba-4446-b378-01eb6f53e871",
            "isBulk": "true"
        }
        resp = api.post(
            f"/v1/savingsaccounts/external-id/{savings_external_id}/transactions/external-id/{transaction_external_id}",
            json=payload
        )
        assert resp.status_code == 200

    # 边界值用例：路径参数为空字符串
    @pytest.mark.parametrize("savings_external_id, transaction_external_id", [
        ("", "valid_transaction_external_id"),
        ("valid_savings_external_id", ""),
        ("", "")
    ])
    def test_undo_transaction_empty_path_params(self, api, savings_external_id, transaction_external_id):
        payload = {
            "externalId": "5dd80a7c-ccba-4446-b378-01eb6f53e871",
            "isBulk": "true"
        }
        resp = api.post(
            f"/v1/savingsaccounts/external-id/{savings_external_id}/transactions/external-id/{transaction_external_id}",
            json=payload,
            params={"command": "undo"}
        )
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：路径参数为不存在的资源ID
    def test_undo_transaction_nonexistent_path_params(self, api):
        savings_external_id = "999999"
        transaction_external_id = "999999"
        payload = {
            "externalId": "5dd80a7c-ccba-4446-b378-01eb6f53e871",
            "isBulk": "true"
        }
        resp = api.post(
            f"/v1/savingsaccounts/external-id/{savings_external_id}/transactions/external-id/{transaction_external_id}",
            json=payload,
            params={"command": "undo"}
        )
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：请求体字段边界值测试
    @pytest.mark.parametrize("payload", [
        {"externalId": "", "isBulk": "true"},
        {"externalId": "a" * 256, "isBulk": "true"},
        {"externalId": "5dd80a7c-ccba-4446-b378-01eb6f53e871", "isBulk": ""},
        {"externalId": "5dd80a7c-ccba-4446-b378-01eb6f53e871", "isBulk": "invalid"},
        {"externalId": "5dd80a7c-ccba-4446-b3