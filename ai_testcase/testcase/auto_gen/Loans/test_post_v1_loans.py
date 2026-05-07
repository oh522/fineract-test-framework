import pytest

class TestLoansPost:
    """Loans POST /v1/loans 测试类"""

    base_payload = {
        "allowFullTermForTranche": False,
        "amortizationType": 1,
        "buyDownFeeCalculationType": "FLAT",
        "buyDownFeeIncomeType": "FEE",
        "buyDownFeeStrategy": "EQUAL_AMORTIZATION",
        "capitalizedIncomeCalculationType": "FLAT",
        "capitalizedIncomeStrategy": "EQUAL_AMORTIZATION",
        "capitalizedIncomeType": {
            "code": "<code>",
            "id": "<id>",
            "value": "<value>"
        },
        "charges": [],
        "clientId": 1,
        "datatables": "List of PostLoansDataTable",
        "dateFormat": "dd MMMM yyyy",
        "daysInYearCustomStrategy": "FULL_LEAP_YEAR",
        "daysInYearType": 360,
        "disbursedAmountPercentageForDownPayment": 0.0,
        "disbursementData": [],
        "enableAutoRepaymentForDownPayment": False,
        "enableBuyDownFee": False,
        "enableDownPayment": False,
        "enableIncomeCapitalization": False,
        "enableInstallmentLevelDelinquency": False,
        "expectedDisbursementDate": "20 September 2011",
        "externalId": "786444UUUYYH7",
        "fixedEmiAmount": 10.0,
        "fixedLength": 1,
        "fixedPrincipalPercentagePerInstallment": 5.5,
        "graceOnArrearsAgeing": 1,
        "graceOnInterestCharged": 1,
        "graceOnInterestPayment": 1,
        "graceOnPrincipalPayment": 1,
        "inArrearsTolerance": 10,
        "interestCalculationPeriodType": 1,
        "interestRateFrequencyType": 3,
        "interestRatePerPeriod": 2,
        "interestRecognitionOnDisbursementDate": False,
        "interestType": 0,
        "loanScheduleProcessingType": "HORIZONTAL",
        "loanTermFrequency": 12,
        "loanTermFrequencyType": 2,
        "loanType": "individual",
        "locale": "en_GB",
        "maxOutstandingLoanBalance": 1,
        "numberOfRepayments": 12,
        "originators": [],
        "principal": 1000.0,
        "productId": 1,
        "repaymentEvery": 1,
        "repaymentFrequencyType": 2,
        "repaymentsStartingFromDate": "01 January 2024",
        "submittedOnDate": "20 September 2011",
        "transactionProcessingStrategyCode": "mifos-standard-strategy"
    }

    # 正常用例：使用完整有效字段，期望成功
    def test_loans_post_success(self, api):
        """正常用例：提交完整的贷款申请，期望返回200"""
        payload = self.base_payload.copy()
        resp = api.post("/loans", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "resourceId" in data, f"响应缺少 resourceId：{data}"

    # 参数缺失用例：逐个缺少必填字段（此处无required_fields，故跳过）
    def test_loans_post_missing_required_fields(self, api):
        """参数缺失用例：无必填字段，跳过"""
        pass

    # 边界值用例：空字符串、极大值、极小值、0、负数等
    @pytest.mark.parametrize("field,value,desc", [
        ("principal", 0, "principal为0"),
        ("principal", -100, "principal为负数"),
        ("principal", 999999999999, "principal为极大值"),
        ("principal", 0.001, "principal为极小正数"),
        ("numberOfRepayments", 0, "numberOfRepayments为0"),
        ("numberOfRepayments", -1, "numberOfRepayments为负数"),
        ("numberOfRepayments", 100000, "numberOfRepayments为极大值"),
        ("interestRatePerPeriod", 0, "interestRatePerPeriod为0"),
        ("interestRatePerPeriod", -1, "interestRatePerPeriod为负数"),
        ("interestRatePerPeriod", 100000, "interestRatePerPeriod为极大值"),
        ("loanTermFrequency", 0, "loanTermFrequency为0"),
        ("loanTermFrequency", -1, "loanTermFrequency为负数"),
        ("loanTermFrequency", 100000, "loanTermFrequency为极大值"),
        ("repaymentEvery", 0, "repaymentEvery为0"),
        ("repaymentEvery", -1, "repaymentEvery为负数"),
        ("repaymentEvery", 100000, "repaymentEvery为极大值"),
        ("graceOnArrearsAgeing", -1, "graceOnArrearsAgeing为负数"),
        ("graceOnInterestCharged", -1, "graceOnInterestCharged为负数"),
        ("graceOnInterestPayment", -1, "graceOnInterestPayment为负数"),
        ("graceOnPrincipalPayment", -1, "graceOnPrincipalPayment为负数"),
        ("inArrearsTolerance", -1, "inArrearsTolerance为负数"),
        ("fixedEmiAmount", -1, "fixedEmiAmount为负数"),
        ("fixedLength", -1, "fixedLength为负数"),
        ("fixedPrincipalPercentagePerInstallment", -1, "fixedPrincipalPercentagePerInstallment为负数"),
        ("maxOutstandingLoanBalance", -1, "maxOutstandingLoanBalance为负数"),
        ("disbursedAmountPercentageForDownPayment", -1, "disbursedAmountPercentageForDownPayment为负数"),
        ("externalId", "", "externalId为空字符串"),
        ("externalId", "a"*1000, "externalId为超长字符串"),
        ("dateFormat", "", "dateFormat为空字符串"),
        ("expectedDisbursementDate", "", "expectedDisbursementDate为空字符串"),
        ("submittedOnDate", "", "submittedOnDate为空字符串"),
        ("repaymentsStartingFromDate", "", "repaymentsStartingFromDate为空字符串"),
        ("locale", "", "locale为空字符串"),
        ("transactionProcessingStrategyCode", "", "transactionProcessingStrategyCode为空字符串"),
        ("loanType", "", "loanType为空字符串"),
        ("loanScheduleProcessingType", "", "loanScheduleProcessingType为空字符串"),
        ("daysInYearCustomStrategy", "", "daysInYearCustomStrategy为空字符串"),
        ("buyDownFeeCalculationType", "", "buyDownFeeCalculationType为空字符串"),
        ("buyDownFeeIncomeType", "", "buyDownFeeIncomeType为空字符串"),
        ("buyDownFeeStrategy", "", "buyDownFeeStrategy为空字符串"),
        ("capitalizedIncomeCalculationType", "", "capitalizedIncomeCalculationType为空字符串"),
        ("capitalizedIncomeStrategy", "", "capitalizedIncomeStrategy为空字符串"),
    ])
    def test_loans_post_boundary(self, api, field, value, desc):
        """边界值用例：测试边界值，期望返回4xx"""
        payload = self.base_payload.copy()
        payload[field] = value
        resp = api.post("/loans", json=payload)
        assert resp.status_code in [400, 403, 404, 422]

    # 异常用例：错误类型、非法枚举值、特殊字符等
    @pytest.mark.parametrize("field,value,desc", [
        ("principal", "abc", "principal为字符串"),
        ("principal", None, "principal为null"),
        ("principal", [100], "principal为列表"),
        ("principal", {"amount": 100}, "principal为字典"),
        ("numberOfRepayments", "abc", "numberOfRepayments为字符串"),
        ("numberOfRepayments", None, "numberOfRepayments为null"),
        ("interestRatePerPeriod", "abc", "interestRatePerPeriod为字符串"),
        ("interestRatePerPeriod", None, "interestRatePerPeriod为null"),
        ("loanTermFrequency", "abc", "loanTermFrequency为字符串"),
        ("loanTermFrequency", None, "loanTermFrequency为null"),
        ("repaymentEvery", "abc", "repaymentEvery为字符串"),
        ("repaymentEvery", None, "repaymentEvery为null"),
        ("amortizationType", 999, "amortizationType为非法枚举值"),
        ("amortizationType", -1, "amortizationType为负数枚举"),
        ("interestType", 999, "interestType为非法枚举值"),
        ("interestType", -1, "interestType为负数枚举"),
        ("interestCalculationPeriodType", 999, "interestCalculationPeriodType为非法枚举值"),
        ("interestCalculationPeriodType", -1, "interestCalculationPeriodType为负数枚举"),
        ("interestRateFrequencyType", 999, "interestRateFrequencyType为非法枚举值"),
        ("interestRateFrequencyType", -1, "interestRateFrequencyType为负数枚举"),
    # ... existing code ...
        ("loanTermFrequency", "abc", "loanTermFrequency为字符串"),
        ("loanTermFrequency", None, "loanTermFrequency为null"),
        ("repaymentEvery", "abc", "repaymentEvery为字符串"),
        ("repaymentEvery", None, "repaymentEvery为null"),
        ("amortizationType", 999, "amortizationType为非法枚举值"),
        ("amortizationType", -1, "amortizationType为负数枚举"),
        ("interestType", 999, "interestType为非法枚举值"),
        ("interestType", -1, "interestType为负数枚举"),
        ("interestCalculationPeriodType", 999, "interestCalculationPeriodType为非法枚举值"),
        ("interestCalculationPeriodType", -1, "interestCalculationPeriodType为负数枚举"),
        ("interestRateFrequencyType", 999, "interestRateFrequencyType为非法枚举值"),
        ("interestRateFrequencyType", -1, "interestRateFrequencyType为负数枚举"),
        ("loanTermFrequencyType", 999, "loanTermFrequencyType为非法枚举值"),
        ("loanTermFrequencyType", -1, "loanTermFrequencyType为负数枚举"),
        ("repaymentFrequencyType", 999, "repaymentFrequencyType为非法枚举值"),
        ("repaymentFrequencyType", -1, "repaymentFrequencyType为负数枚举"),
        ("daysInYearType", 999, "daysInYearType为非法枚举值"),
        ("daysInYearType", -1, "daysInYearType为负数枚举"),
        ("loanType", "invalid", "loanType为非法枚举值"),
        ("loanScheduleProcessingType", "INVALID", "loanScheduleProcessingType为非法枚举值"),
        ("daysInYearCustomStrategy", "INVALID", "daysInYearCustomStrategy为非法枚举值"),
        ("buyDownFeeCalculationType", "INVALID", "buyDownFeeCalculationType为非法枚举值"),
        ("buyDownFeeIncomeType", "INVALID", "buyDownFeeIncomeType为非法枚举值"),
        ("buyDownFeeStrategy", "INVALID", "buyDownFeeStrategy为非法枚举值"),
        ("capitalizedIncomeCalculationType", "INVALID", "capitalizedIncomeCalculationType为非法枚举值"),
        ("capitalizedIncomeStrategy", "INVALID", "capitalizedIncomeStrategy为非法枚举值"),
        ("transactionProcessingStrategyCode", "invalid", "transactionProcessingStrategyCode为非法枚举值"),
        ("allowFullTermForTranche", "true", "allowFullTermForTranche为字符串而非布尔值"),
        ("enableAutoRepaymentForDownPayment", "true", "enableAutoRepaymentForDownPayment为字符串而非布尔值"),
        ("enableBuyDownFee", "true", "enableBuyDownFee为字符串而非布尔值"),
        ("enableDownPayment", "true", "enableDownPayment为字符串而非布尔值"),
        ("enableIncomeCapitalization", "true", "enableIncomeCapitalization为字符串而非布尔值"),
        ("enableInstallmentLevelDelinquency", "true", "enableInstallmentLevelDelinquency为字符串而非布尔值"),
        ("interestRecognitionOnDisbursementDate", "true", "interestRecognitionOnDisbursementDate为字符串而非布尔值"),
        ("clientId", "abc", "clientId为字符串"),
        ("clientId", None, "clientId为null"),
        ("productId", "abc", "productId为字符串"),
        ("productId", None, "productId为null"),
        ("charges", "invalid", "charges为字符串而非数组"),
        ("charges", None, "charges为null"),
        ("disbursementData", "invalid", "disbursementData为字符串而非数组"),
        ("disbursementData", None, "disbursementData为null"),
        ("datatables", "invalid", "datatables为字符串而非数组"),
        ("originators", "invalid", "originators为字符串而非数组"),
        ("capitalizedIncomeType", "invalid", "capitalizedIncomeType为字符串而非对象"),
        ("capitalizedIncomeType", None, "capitalizedIncomeType为null"),
    ])
    def test_loans_post_wrong_type(self, api, field, value, desc):
        """异常用例：测试错误类型字段，期望返回4xx"""
        payload = self.base_payload.copy()
        payload[field] = value
        resp = api.post("/loans", json=payload)
        assert resp.status_code in [400, 403, 404, 422]

    # 特殊字符用例：SQL注入、XSS等
    @pytest.mark.parametrize("field,value,desc", [
        ("externalId", "'; DROP TABLE loans; --", "externalId包含SQL注入"),
        ("externalId", "<script>alert('xss')</script>", "externalId包含XSS脚本"),
        ("externalId", "../../../etc/passwd", "externalId包含路径遍历"),
        ("firstname", "'; DROP TABLE clients; --", "firstname包含SQL注入"),
        ("firstname", "<script>alert('xss')</script>", "firstname包含XSS脚本"),
    ])
    def test_loans_post_special_chars(self, api, field, value, desc):
        """特殊字符用例：测试SQL注入、XSS等特殊字符，期望返回4xx"""
        payload = self.base_payload.copy()
        payload[field] = value
        resp = api.post("/loans", json=payload)
        assert resp.status_code in [400, 403, 404, 422]

    # 日期格式错误用例
    @pytest.mark.parametrize("field,value,desc", [
        ("expectedDisbursementDate", "2026-05-02", "expectedDisbursementDate格式错误（应为dd MMMM yyyy）"),
        ("expectedDisbursementDate", "02/05/2026", "expectedDisbursementDate格式错误（斜杠分隔）"),
        ("expectedDisbursementDate", "invalid", "expectedDisbursementDate非法日期"),
        ("submittedOnDate", "2026-05-02", "submittedOnDate格式错误（应为dd MMMM yyyy）"),
        ("submittedOnDate", "02/05/2026", "submittedOnDate格式错误（斜杠分隔）"),
        ("submittedOnDate", "invalid", "submittedOnDate非法日期"),
        ("repaymentsStartingFromDate", "2026-05-02", "repaymentsStartingFromDate格式错误（应为dd MMMM yyyy）"),
        ("repaymentsStartingFromDate", "02/05/2026", "repaymentsStartingFromDate格式错误（斜杠分隔）"),
        ("repaymentsStartingFromDate", "invalid", "repaymentsStartingFromDate非法日期"),
    ])
    def test_loans_post_invalid_date_format(self, api, field, value, desc):
        """日期格式错误用例：测试错误的日期格式，期望返回4xx"""
        payload = self.base_payload.copy()
        payload[field] = value
        resp = api.post("/loans", json=payload)
        assert resp.status_code in [400, 403, 404, 422]

    # 逻辑错误用例：日期前后矛盾、参数组合不合理等
    @pytest.mark.parametrize("update_fields,desc", [
        ({"submittedOnDate": "01 January 2030", "expectedDisbursementDate": "01 January 2020"}, "提交日期晚于放款日期"),
        ({"repaymentsStartingFromDate": "01 January 2020", "expectedDisbursementDate": "01 January 2030"}, "还款开始日期早于放款日期"),
        ({"numberOfRepayments": 1, "loanTermFrequency": 120}, "还款期数远小于贷款期限"),
        ({"principal": 10, "maxOutstandingLoanBalance": 1000}, "最大未还余额远大于本金"),
    ])
    def test_loans_post_logical_errors(self, api, update_fields, desc):
        """逻辑错误用例：测试参数逻辑矛盾，期望返回4xx"""
        payload = self.base_payload.copy()
        payload.update(update_fields)
        resp = api.post("/loans", json=payload)
        assert resp.status_code in [400, 403, 404, 422]
