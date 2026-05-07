import pytest


class TestLoanTransactionRetrieve:
    """Retrieve a Transaction Details by external IDs"""

    BASE_PATH = "/loans/external-id/{loanExternalId}/transactions/external-id/{externalTransactionId}"

    # 正常用例：使用有效的 loanExternalId 和 externalTransactionId，期望成功
    @pytest.mark.parametrize(
        "loan_external_id, external_transaction_id, fields",
        [
            ("LOAN-EXT-001", "TXN-EXT-001", None),
            ("LOAN-EXT-002", "TXN-EXT-002", "id,date,amount"),
        ],
    )
    def test_retrieve_transaction_success(self, api, loan_external_id, external_transaction_id, fields):
        path = self.BASE_PATH.format(
            loanExternalId=loan_external_id,
            externalTransactionId=external_transaction_id,
        )
        params = {}
        if fields:
            params["fields"] = fields
        resp = api.get(path, params=params)
        assert resp.status_code == 200
        assert "id" in resp.json() or "transactionId" in resp.json()

    # 参数缺失用例：缺少 loanExternalId（路径参数缺失）
    def test_retrieve_transaction_missing_loan_external_id(self, api):
        path = self.BASE_PATH.format(
            loanExternalId="",
            externalTransactionId="TXN-EXT-001",
        )
        resp = api.get(path)
        assert resp.status_code in [400, 403, 404, 422]

    # 参数缺失用例：缺少 externalTransactionId（路径参数缺失）
    def test_retrieve_transaction_missing_external_transaction_id(self, api):
        path = self.BASE_PATH.format(
            loanExternalId="LOAN-EXT-001",
            externalTransactionId="",
        )
        resp = api.get(path)
        assert resp.status_code in [400, 403, 404, 422]

    # 参数缺失用例：缺少两个路径参数
    def test_retrieve_transaction_missing_both_ids(self, api):
        path = self.BASE_PATH.format(
            loanExternalId="",
            externalTransactionId="",
        )
        resp = api.get(path)
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：loanExternalId 为极长字符串
    @pytest.mark.parametrize(
        "loan_external_id, external_transaction_id",
        [
            ("a" * 1000, "TXN-EXT-001"),
            ("", "TXN-EXT-001"),
            ("LOAN-EXT-001", "a" * 1000),
            ("LOAN-EXT-001", ""),
        ],
    )
    def test_retrieve_transaction_boundary_values(self, api, loan_external_id, external_transaction_id):
        path = self.BASE_PATH.format(
            loanExternalId=loan_external_id,
            externalTransactionId=external_transaction_id,
        )
        resp = api.get(path)
        assert resp.status_code in [200, 400, 403, 404, 422]

    # 异常用例：loanExternalId 为不存在的 ID
    def test_retrieve_transaction_nonexistent_loan_external_id(self, api):
        path = self.BASE_PATH.format(
            loanExternalId="999999",
            externalTransactionId="TXN-EXT-001",
        )
        resp = api.get(path)
        assert resp.status_code in [400, 403, 404, 422]

    # 异常用例：externalTransactionId 为不存在的 ID
    def test_retrieve_transaction_nonexistent_external_transaction_id(self, api):
        path = self.BASE_PATH.format(
            loanExternalId="LOAN-EXT-001",
            externalTransactionId="999999",
        )
        resp = api.get(path)
        assert resp.status_code in [400, 403, 404, 422]

    # 异常用例：loanExternalId 包含特殊字符
    @pytest.mark.parametrize(
        "loan_external_id, external_transaction_id",
        [
            ("<script>", "TXN-EXT-001"),
            ("LOAN-EXT-001", "<script>"),
            ("../..", "TXN-EXT-001"),
            ("LOAN-EXT-001", "../.."),
        ],
    )
    def test_retrieve_transaction_special_characters(self, api, loan_external_id, external_transaction_id):
        path = self.BASE_PATH.format(
            loanExternalId=loan_external_id,
            externalTransactionId=external_transaction_id,
        )
        resp = api.get(path)
        assert resp.status_code in [400, 403, 404, 422]

    # 异常用例：fields 参数为无效值
    @pytest.mark.parametrize(
        "fields",
        [
            "invalid_field",
            "id, nonexistent_field",
            "",
        ],
    )
    def test_retrieve_transaction_invalid_fields(self, api, fields):
        path = self.BASE_PATH.format(
            loanExternalId="LOAN-EXT-001",
            externalTransactionId="TXN-EXT-001",
        )
        params = {"fields": fields}
        resp = api.get(path, params=params)
        assert resp.status_code in [200, 400, 403, 404, 422]