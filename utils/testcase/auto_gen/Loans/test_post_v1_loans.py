import pytest
from api_test.common.base_api import BaseApi

class TestLoanApplication:
    # 正常用例：使用所有必填字段提交贷款申请
    def test_create_loan_success(self, api):
        payload = {
            "clientId": 1,
            "productId": 1,
            "principal": 1000.0,
            "loanTermFrequency": 12,
            "loanTermFrequencyType": 2,
            "numberOfRepayments": 12,
            "repaymentEvery": 1,
            "repaymentFrequencyType": 2,
            "interestRatePerPeriod": 2,
            "interestRateFrequencyType": 3,
            "interestType": 0,
            "interestCalculationPeriodType": 1,
            "amortizationType": 1,
            "submittedOnDate": "20 September 2011",
            "expectedDisbursementDate": "20 September 2011",
            "transactionProcessingStrategyCode": "mifos-standard-strategy",
            "repaymentsStartingFromDate": "01 January 2024",
            "locale": "en_GB",
            "dateFormat": "dd MMMM yyyy",
            "loanType": "individual"
        }
        resp = api.post("/v1/loans", json=payload)
        assert resp.status_code == 200
        assert "loanId" in resp.json() or "resourceId" in resp.json()

    # 正常用例：计算还款计划
    def test_calculate_loan_schedule_success(self, api):
        payload = {
            "clientId": 1,
            "productId": 1,
            "principal": 1000.0,
            "loanTermFrequency": 12,
            "loanTermFrequencyType": 2,
            "numberOfRepayments": 12,
            "repaymentEvery": 1,
            "repaymentFrequencyType": 2,
            "interestRatePerPeriod": 2,
            "interestRateFrequencyType": 3,
            "interestType": 0,
            "interestCalculationPeriodType": 1,
            "amortizationType": 1,
            "submittedOnDate": "20 September 2011",
            "expectedDisbursementDate": "20 September 2011",
            "transactionProcessingStrategyCode": "mifos-standard-strategy",
            "repaymentsStartingFromDate": "01 January 2024",
            "locale": "en_GB",
            "dateFormat": "dd MMMM yyyy",
            "loanType": "individual"
        }
        resp = api.post("/v1/loans?command=calculateSchedule", json=payload)
        assert resp.status_code == 200
        assert "periods" in resp.json()

    # 参数缺失用例：缺少clientId
    def test_create_loan_missing_client_id(self, api):
        payload = {
            "productId": 1,
            "principal": 1000.0,
            "loanTermFrequency": 12,
            "loanTermFrequencyType": 2,
            "numberOfRepayments": 12,
            "repaymentEvery": 1,
            "repaymentFrequencyType": 2,
            "interestRatePerPeriod": 2,
            "interestRateFrequencyType": 3,
            "interestType": 0,
            "interestCalculationPeriodType": 1,
            "amortizationType": 1,
            "submittedOnDate": "20 September 2011",
            "expectedDisbursementDate": "20 September 2011",
            "transactionProcessingStrategyCode": "mifos-standard-strategy",
            "repaymentsStartingFromDate": "01 January 2024",
            "locale": "en_GB",
            "dateFormat": "dd MMMM yyyy",
            "loanType": "individual"
        }
        resp = api.post("/v1/loans", json=payload)
        assert resp.status_code in [400, 403, 404, 422]

    # 参数缺失用例：缺少productId
    def test_create_loan_missing_product_id(self, api):
        payload = {
            "clientId": 1,
            "principal": 1000.0,
            "loanTermFrequency": 12,
            "loanTermFrequencyType": 2,
            "numberOfRepayments": 12,
            "repaymentEvery": 1,
            "repaymentFrequencyType": 2,
            "interestRatePerPeriod": 2,
            "interestRateFrequencyType": 3,
            "interestType": 0,
            "interestCalculationPeriodType": 1,
            "amortizationType": 1,
            "submittedOnDate": "20 September 2011",
            "expectedDisbursementDate": "20 September 2011",
            "transactionProcessingStrategyCode": "mifos-standard-strategy",
            "repaymentsStartingFromDate": "01 January 2024",
            "locale": "en_GB",
            "dateFormat":