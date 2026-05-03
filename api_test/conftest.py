import time
import uuid
import pytest
from datetime import datetime, timedelta

from conftest import api


@pytest.fixture(scope="session")
def client_id(api):
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
        "externalId": unique_id,
    }
    res = api.post("/clients", json=payload)
    assert res.status_code == 200, f"创建客户失败: {res.text}"

    data = res.json()
    cid = data.get("clientId") or data.get("resourceId")
    assert isinstance(cid, int) and cid > 0, f"clientId 无效: {cid}"
    print(f"\n✅ 测试客户已创建 clientId={cid}")
    print(f"\n✅ 测试客户已创建 clientId={cid}, externalId={unique_id}")
    return cid

@pytest.fixture(scope="session")
def loan_product_id(api):
    """创建贷款产品，返回 productId"""
    unique_suffix = uuid.uuid4().hex[:4]
    unique_name = f"自动化测试贷款产品_{uuid.uuid4().hex[:6]}"

    payload = {
        "name": unique_name,
        "shortName": f"T{unique_suffix[:3]}",
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
        "locale": "en",
        "daysInYearType": 360,
        "daysInMonthType": 30,
        "isInterestRecalculationEnabled": False,
        "charges": [],
    }

    res = api.post("/loanproducts", json=payload)
    assert res.status_code == 200, f"创建贷款产品失败: {res.text}"

    data = res.json()
    pid = data.get("resourceId")
    assert isinstance(pid, int) and pid > 0, f"产品ID无效: {pid}"

    print(f"\n✅ 贷款产品已创建 productId={pid}")
    return pid


@pytest.fixture(scope="session")
def savings_product_id(api):
    """创建储蓄产品，返回 productId"""
    unique_suffix = uuid.uuid4().hex[:4]

    payload = {
        "name": f"自动化测试储蓄产品_{unique_suffix}",
        "shortName": f"S{unique_suffix[:3]}",
        "currencyCode": "USD",
        "digitsAfterDecimal": 2,
        "inMultiplesOf": 0,
        "nominalAnnualInterestRate": 3.5,
        "interestCompoundingPeriodType": 1,
        "interestPostingPeriodType": 4,
        "interestCalculationType": 1,
        "interestCalculationDaysInYearType": 365,
        "accountingRule": 1,
        "locale": "en",
    }

    res = api.post("/savingsproducts", json=payload)
    assert res.status_code == 200, f"创建储蓄产品失败: {res.text}"

    data = res.json()
    pid = data.get("resourceId")
    assert isinstance(pid, int) and pid > 0, f"产品ID无效: {pid}"

    print(f"\n✅ 储蓄产品已创建 productId={pid}")
    return pid


@pytest.fixture(scope="session")
def loan_id(api, client_id, loan_product_id):
    """创建 → 审批 → 放款，返回 ACTIVE 状态的 loanId"""
    today = datetime.now()
    submit_date = (today - timedelta(days=5)).strftime("%d %B %Y")
    approve_date = (today - timedelta(days=3)).strftime("%d %B %Y")
    disburse_date = (today - timedelta(days=2)).strftime("%d %B %Y")

    # 1️⃣ 提交申请
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
        "expectedDisbursementDate": disburse_date,
        "submittedOnDate": submit_date,
        "dateFormat": "dd MMMM yyyy",
        "locale": "en",
    }
    res = api.post("/loans", json=apply_payload)
    assert res.status_code == 200, f"贷款申请失败: {res.text}"
    lid = res.json()["loanId"]
    assert isinstance(lid, int) and lid > 0, f"loanId 无效: {lid}"

    # 2️⃣ 审批
    approve_payload = {
        "approvedOnDate": approve_date,
        "expectedDisbursementDate": disburse_date,
        "dateFormat": "dd MMMM yyyy",
        "locale": "en",
    }
    res = api.post(f"/loans/{lid}?command=approve", json=approve_payload)
    assert res.status_code == 200, f"贷款审批失败: {res.text}"

    # 3️⃣ 放款
    disburse_payload = {
        "actualDisbursementDate": disburse_date,
        "dateFormat": "dd MMMM yyyy",
        "locale": "en",
    }
    res = api.post(f"/loans/{lid}?command=disburse", json=disburse_payload)
    assert res.status_code == 200, f"放款失败: {res.text}"

    print(f"\n✅ 贷款已放款 loanId={lid}")
    return lid