import time
import pytest


@pytest.fixture(scope="session")
def client_id(api_client, base_url):
    """创建测试客户，返回 clientId"""
    unique_id = f"AUTO-TEST-{int(time.time())}"
    payload = {
        "officeId": 1,
        "firstname": "自动化",
        "lastname": "测试客户",
        "legalFormId": 1,
        "active": True,
        "activationDate": "01 January 2023",
        "dateFormat": "dd MMMM yyyy",
        "locale": "en",
        "externalId": unique_id
    }
    # 使用 api_client.post（内部会自动拼接完整 URL）
    res = api_client.post("/clients", json=payload)
    assert res.status_code == 200, f"创建客户失败: {res.text}"
    cid = res.json().get("clientId") or res.json().get("resourceId")
    print(f"\n✅ 测试客户已创建 clientId={cid}")
    return cid

@pytest.fixture(scope="session")
def loan_product_id(api_session, base_url):
    """创建贷款产品，返回productId"""
    payload = {
        "name": "自动化测试贷款产品",
        "shortName": "ATP1",
        "currencyCode": "USD",
        "digitsAfterDecimal": 2,
        "inMultiplesOf": 0,
        "principal": 10000,
        "numberOfRepayments": 12,
        "repaymentEvery": 1,
        "repaymentFrequencyType": 2,
        "interestRatePerPeriod": 1.5,
        "interestRateFrequencyType": 2,
        "amortizationType": 1,
        "interestType": 0,
        "interestCalculationPeriodType": 1,
        "transactionProcessingStrategyCode": "mifos-standard-strategy",
        "accountingRule": 1,
        "dateFormat": "dd MMMM yyyy",
        "locale": "en"
    }
    res = api_session.post(f"{base_url}/loanproducts", json=payload)
    assert res.status_code == 200, f"创建贷款产品失败: {res.text}"
    product_id = res.json()["resourceId"]
    print(f"\n✅ 贷款产品已创建 productId={product_id}")
    return product_id

@pytest.fixture(scope="session")
def savings_product_id(api_session, base_url):
    """创建储蓄产品，返回productId"""
    payload = {
        "name": "自动化测试储蓄产品",
        "shortName": "ATSP",
        "currencyCode": "USD",
        "digitsAfterDecimal": 2,
        "inMultiplesOf": 0,
        "nominalAnnualInterestRate": 3.5,
        "interestCompoundingPeriodType": 1,
        "interestPostingPeriodType": 4,
        "interestCalculationType": 1,
        "interestCalculationDaysInYearType": 365,
        "accountingRule": 1,
        "locale": "en"
    }
    res = api_session.post(f"{base_url}/savingsproducts", json=payload)
    assert res.status_code == 200, f"创建储蓄产品失败: {res.text}"
    pid = res.json()["resourceId"]
    print(f"\n✅ 储蓄产品已创建 productId={pid}")
    return pid

@pytest.fixture(scope="session")
def loan_id(api_session, base_url, client_id, loan_product_id):
    """创建并审批放款，返回处于ACTIVE状态的loanId"""
    # 提交申请
    apply_payload = {
        "clientId": client_id,
        "productId": loan_product_id,
        "principal": 50000,
        "loanTermFrequency": 12,
        "loanTermFrequencyType": 2,
        "numberOfRepayments": 12,
        "repaymentEvery": 1,
        "repaymentFrequencyType": 2,
        "interestRatePerPeriod": 1.5,
        "amortizationType": 1,
        "interestType": 0,
        "interestCalculationPeriodType": 1,
        "transactionProcessingStrategyCode": "mifos-standard-strategy",
        "expectedDisbursementDate": "10 January 2024",
        "submittedOnDate": "01 January 2024",
        "dateFormat": "dd MMMM yyyy",
        "locale": "en"
    }
    res = api_session.post(f"{base_url}/loans", json=apply_payload)
    assert res.status_code == 200, f"贷款申请失败: {res.text}"
    lid = res.json()["loanId"]

    # 审批
    approve_payload = {
        "approvedOnDate": "05 January 2024",
        "expectedDisbursementDate": "10 January 2024",
        "dateFormat": "dd MMMM yyyy",
        "locale": "en"
    }
    res = api_session.post(
        f"{base_url}/loans/{lid}?command=approve",
        json=approve_payload
    )
    assert res.status_code == 200, f"贷款审批失败: {res.text}"

    # 放款
    disburse_payload = {
        "actualDisbursementDate": "10 January 2024",
        "dateFormat": "dd MMMM yyyy",
        "locale": "en"
    }
    res = api_session.post(
        f"{base_url}/loans/{lid}?command=disburse",
        json=disburse_payload
    )
    assert res.status_code == 200, f"放款失败: {res.text}"
    print(f"\n✅ 贷款已放款 loanId={lid}")
    return lid