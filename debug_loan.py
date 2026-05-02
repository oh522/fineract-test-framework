# debug_loan.py
from api_test.common.base_api import BaseApi
import json

api = BaseApi()

# ✅ 先登录
resp = api.post("/authentication", json={
    "username": "mifos",
    "password": "password",
    "tenantId": "default"
})
token = resp.json().get("base64EncodedAuthenticationKey")
api._session.headers.update({"Authorization": f"Basic {token}"})
print(f"✅ 登录成功")

# 创建贷款
payload = {
    "clientId": 1,
    "productId": 1,
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
    "submittedOnDate": "01 January 2024",
    "expectedDisbursementDate": "01 January 2024",
    "dateFormat": "dd MMMM yyyy",
    "locale": "en_GB",
    "transactionProcessingStrategyCode": "mifos-standard-strategy"
}

resp = api.post("/loans", json=payload)
print(f"状态码：{resp.status_code}")
print(f"响应：{json.dumps(resp.json(), indent=2, ensure_ascii=False)}")