import pytest

class TestLoanTransactions:
    base_url = "/v1/loans/external-id/{loanExternalId}/transactions"

    # 正常用例：使用所有字段，期望成功
    @pytest.mark.parametrize("loan_external_id, query_params, body", [
        (
            "valid-external-id-123",
            {"command": "repayment"},
            {
                "accountNumber": "acc123",
                "bankNumber": "ban123",
                "chargeOffReasonId": 1,
                "checkNumber": "che123",
                "classificationId": 1,
                "dateFormat": "dd MMMM yyyy",
                "dueDate": "28 June 2022",
                "externalId": "3e7791ce-aa10-11ec-b909-0242ac120002",
                "frequencyNumber": 1,
                "frequencyType": "frequencyType",
                "interestRefundCalculation": False,
                "loanChargeId": 3,
                "locale": "en_GB",
                "note": "An optional note about why your adjusting or changing the transaction.",
                "numberOfInstallments": 1,
                "paymentTypeId": 3,
                "reAgeInterestHandling": "DEFAULT",
                "reAmortizationInterestHandling": "DEFAULT",
                "reasonCodeValueId": 1,
                "receiptNumber": "rec123",
                "reversalExternalId": "3f7791cf-bb10-11ec-b909-0242ac120012",
                "routingCode": "rou123",
                "startDate": "startDate",
                "transactionAmount": 50000.0,
                "transactionDate": "28 June 2022",
                "writeoffReasonId": 1
            }
        )
    ])
    def test_normal_case(self, api, loan_external_id, query_params, body):
        url = self.base_url.format(loanExternalId=loan_external_id)
        resp = api.post(url, params=query_params, json=body)
        assert resp.status_code == 200
        assert "resourceId" in resp.json() or "transactionId" in resp.json()

    # 参数缺失用例：逐个缺少必填字段（当前无必填字段，故使用常见关键字段模拟）
    @pytest.mark.parametrize("loan_external_id, query_params, body, missing_field", [
        (
            "valid-external-id-123",
            {"command": "repayment"},
            {
                "accountNumber": "acc123",
                "bankNumber": "ban123",
                "chargeOffReasonId": 1,
                "checkNumber": "che123",
                "classificationId": 1,
                "dateFormat": "dd MMMM yyyy",
                "dueDate": "28 June 2022",
                "externalId": "3e7791ce-aa10-11ec-b909-0242ac120002",
                "frequencyNumber": 1,
                "frequencyType": "frequencyType",
                "interestRefundCalculation": False,
                "loanChargeId": 3,
                "locale": "en_GB",
                "note": "An optional note about why your adjusting or changing the transaction.",
                "numberOfInstallments": 1,
                "paymentTypeId": 3,
                "reAgeInterestHandling": "DEFAULT",
                "reAmortizationInterestHandling": "DEFAULT",
                "reasonCodeValueId": 1,
                "receiptNumber": "rec123",
                "reversalExternalId": "3f7791cf-bb10-11ec-b909-0242ac120012",
                "routingCode": "rou123",
                "startDate": "startDate",
                "transactionAmount": 50000.0,
                "transactionDate": "28 June 2022",
                "writeoffReasonId": 1
            },
            "transactionAmount"
        ),
        (
            "valid-external-id-123",
            {"command": "repayment"},
            {
                "accountNumber": "acc123",
                "bankNumber": "ban123",
                "chargeOffReasonId": 1,
                "checkNumber": "che123",
                "classificationId": 1,
                "dateFormat": "dd MMMM yyyy",
                "dueDate": "28 June 2022",
                "externalId": "3e7791ce-aa10-11ec-b909-0242ac120002",
                "frequencyNumber": 1,
                "frequencyType": "frequencyType",
                "interestRefundCalculation": False,
                "loanChargeId": 3,
                "locale": "en_GB",
                "note": "An optional note about why your adjusting or changing the transaction.",
                "numberOfInstallments": 1,
                "paymentTypeId": 3,
                "reAgeInterestHandling": "DEFAULT",
                "reAmortizationInterestHandling": "DEFAULT",
                "reasonCodeValueId": 1,
                "receiptNumber": "rec123",
                "reversalExternalId": "3f7791cf-bb10-11ec-b909-0242ac120012",
                "routingCode": "rou123",
                "startDate": "startDate",
                "transactionDate": "28 June 2022",
                "writeoffReasonId": 1
            },
            "transactionDate"
        ),
        (
            "valid-external-id-123",
            {"command": "repayment"},
            {
                "accountNumber": "acc123",
                "bankNumber": "ban123",
                "chargeOffReasonId": 1,
                "checkNumber": "che123",
                "classificationId": 1,
                "dateFormat": "dd MMMM yyyy",
                "dueDate": "28 June 2022",
                "externalId": "3e7791ce-aa10-11ec-b909-0242ac120002",
                "frequencyNumber": 1,
                "frequencyType": "frequencyType",
                "interestRefundCalculation": False,
                "loanChargeId": 3,
                "locale": "en_GB",
                "note": "An optional note about why your adjusting or changing the transaction.",
                "numberOfInstallments": 1,
                "paymentTypeId": 3,
                "reAgeInterestHandling": "DEFAULT",
                "reAmortizationInterestHandling": "DEFAULT",
                "reasonCodeValueId": 1,
                "receiptNumber": "rec123",
                "reversalExternalId": "3f7791cf-bb10-11ec-b909-0242ac120012",
                "routingCode": "rou123",
                "startDate": "startDate",
                "transactionAmount": 50000.0,
                "writeoffReasonId": 1
            },
            "dueDate"
        )
    ])
    def test_missing_required_field(self, api, loan_external_id, query_params, body, missing_field):
        url = self.base_url.format(loanExternalId=loan_external_id)
        resp = api.post(url, params=query_params, json=body)
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：空字符串、极大值、极小值、0、负数等
    @pytest.mark.parametrize("loan_external_id, query_params, body, boundary_desc", [
        (
            "",
            {"command": "repayment"},
            {
                "accountNumber": "acc123",
                "bankNumber": "ban123",
                "chargeOffReasonId": 1,
                "checkNumber": "che123",
                "classificationId": 1,
                "dateFormat": "dd MMMM yyyy",
                "dueDate": "28 June 2022",
                "externalId": "3e7791ce-aa10-11ec-b909-0242ac120002",
                "frequencyNumber": 1,
                "frequencyType": "frequencyType",
                "interestRefundCalculation": False,
                "loanChargeId": 3,
                "locale": "en_GB",
                "note": "An optional note about why your adjusting or changing the transaction.",
                "numberOfInstallments": 1,
                "paymentTypeId": 3,
                "reAgeInterestHandling": "DEFAULT",
                "reAmortizationInterestHandling": "DEFAULT",
                "reasonCodeValueId": 1,
                "receiptNumber": "rec123",
                "reversalExternalId": "3f7791cf-bb10-11ec-b909-0242ac120012",
                "routingCode": "rou123",
                "startDate": "startDate",
                "transactionAmount": 50000.0,
                "transactionDate": "28 June 2022",
                "writeoffReasonId": 1
            },
            "empty_loan_external_id"
        ),
        (
            "valid-external-id-123",
            {"command": "repayment"},
            {
                "accountNumber": "acc123",
                "bankNumber": "ban123