# debug_loan.py
from api_test.common.base_api import BaseApi
import json

api = BaseApi()

payload = {
    "name": "自动化测试贷款产品",
    "shortName": "ATP",
    "currencyCode": "USD",
    "digitsAfterDecimal": 2,
    "inMultiplesOf": 0,
    "principal": 1000.0,
    "minPrincipal": 100.0,
    "maxPrincipal": 100000.0,
    "numberOfRepayments": 12,
    "repaymentEvery": 1,
    "repaymentFrequencyType": 2,
    "interestRatePerPeriod": 2,
    "interestRateFrequencyType": 3,
    "interestType": 0,
    "interestCalculationPeriodType": 1,
    "amortizationType": 1,
    "transactionProcessingStrategyCode": "mifos-standard-strategy",
    "dateFormat": "dd MMMM yyyy",
    "locale": "en_GB",
    "accountingRule": 1,
    # ✅ 补上缺少的3个必填字段
    "daysInYearType": 365,              # 每年天数：1/360/364/365
    "daysInMonthType": 1,               # 每月天数：1/30
    "isInterestRecalculationEnabled": False  # 是否重新计算利息
}

resp = api.post("/loanproducts", json=payload)
print(f"状态码：{resp.status_code}")
print(f"响应：{json.dumps(resp.json(), indent=2, ensure_ascii=False)}")