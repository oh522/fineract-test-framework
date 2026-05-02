
from api_test.common.base_api import BaseApi
import json

api = BaseApi()

payload = {
    "productId": 1,
    "clientId": 1,
    "loanType": "individual",
    "principal": 1000.0,
    "loanTermFrequency": 12,
    "loanTermFrequencyType": 2,
    "numberOfRepayments": 12,
    "repaymentEvery": 1,
    "repaymentFrequencyType": 2,
    "interestRatePerPeriod": 2,
    "interestType": 0,
    "interestCalculationPeriodType": 1,
    "amortizationType": 1,
    "submittedOnDate": "20 September 2011",
    "expectedDisbursementDate": "20 September 2011",
    "dateFormat": "dd MMMM yyyy",
    "locale": "en_GB",
    "transactionProcessingStrategyCode": "mifos-standard-strategy"
}

resp = api.post("/loans", json=payload)
print(f"状态码：{resp.status_code}")
print(f"响应：{json.dumps(resp.json(), indent=2, ensure_ascii=False)}")