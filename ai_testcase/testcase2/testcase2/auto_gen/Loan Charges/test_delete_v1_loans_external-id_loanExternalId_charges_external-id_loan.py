import pytest
from api_test.common.base_api import BaseApi

class TestDeleteLoanCharge:
    # 正常用例：使用有效的贷款外部ID和费用外部ID删除费用
    def test_delete_loan_charge_success(self, api):
        loan_external_id = "valid_loan_external_id_123"
        loan_charge_external_id = "valid_charge_external_id_456"
        url = f"/v1/loans/external-id/{loan_external_id}/charges/external-id/{loan_charge_external_id}"
        resp = api.delete(url)
        assert resp.status_code == 200
        assert "resourceId" in resp.json()

    # 参数缺失用例：缺少贷款外部ID
    @pytest.mark.parametrize("loan_external_id, loan_charge_external_id", [
        ("", "valid_charge_external_id_456"),
    ])
    def test_delete_loan_charge_missing_loan_external_id(self, api, loan_external_id, loan_charge_external_id):
        url = f"/v1/loans/external-id/{loan_external_id}/charges/external-id/{loan_charge_external_id}"
        resp = api.delete(url)
        assert resp.status_code in [400, 403, 404, 422]

    # 参数缺失用例：缺少费用外部ID
    @pytest.mark.parametrize("loan_external_id, loan_charge_external_id", [
        ("valid_loan_external_id_123", ""),
    ])
    def test_delete_loan_charge_missing_charge_external_id(self, api, loan_external_id, loan_charge_external_id):
        url = f"/v1/loans/external-id/{loan_external_id}/charges/external-id/{loan_charge_external_id}"
        resp = api.delete(url)
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：贷款外部ID为空字符串
    @pytest.mark.parametrize("loan_external_id, loan_charge_external_id", [
        ("", "valid_charge_external_id_456"),
    ])
    def test_delete_loan_charge_empty_loan_external_id(self, api, loan_external_id, loan_charge_external_id):
        url = f"/v1/loans/external-id/{loan_external_id}/charges/external-id/{loan_charge_external_id}"
        resp = api.delete(url)
        assert resp.status_code in [400, 403, 404, 422]