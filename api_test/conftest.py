import time
import uuid
import pytest
from datetime import datetime, timedelta


@pytest.fixture(scope="session")
def client_id(api):
    """创建测试客户，返回 clientId"""
    payload = {
        "officeId": 1,
        "firstname": "自动化",
        "lastname": "测试客户",
        "legalFormId": 1,
        "active": True,
        "activationDate": "01 January 2023",
        "dateFormat": "dd MMMM yyyy",
        "locale": "en",
        "externalId": f"AUTO-TEST-{int(time.time())}",
    }
    res = api.post("/clients", json=payload)
    assert res.status_code == 200, f"创建客户失败: {res.text}"

    data = res.json()
    cid = data.get("clientId") or data.get("resourceId")
    assert isinstance(cid, int) and cid > 0
    print(f"\n✅ 测试客户已创建 clientId={cid}")
    return cid


@pytest.fixture(scope="session")
def loan_product_id(api):
    """创建贷款产品，返回 productId"""
    suffix = uuid.uuid4().hex[:4]
    payload = {
        "name": f"自动化测试贷款产品_{uuid.uuid4().hex[:6]}",
        "shortName": f"T{suffix[:3]}",
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

    pid = res.json().get("resourceId")
    assert isinstance(pid, int) and pid > 0
    print(f"\n✅ 贷款产品已创建 productId={pid}")
    return pid


@pytest.fixture(scope="session")
def savings_product_id(api):
    """创建储蓄产品，返回 productId"""
    suffix = uuid.uuid4().hex[:4]
    payload = {
        "name": f"自动化测试储蓄产品_{suffix}",
        "shortName": f"S{suffix[:3]}",
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

    pid = res.json().get("resourceId")
    assert isinstance(pid, int) and pid > 0
    print(f"\n✅ 储蓄产品已创建 productId={pid}")
    return pid


@pytest.fixture(scope="session")
def loan_id(api, client_id, loan_product_id):
    """创建 → 审批 → 放款，返回 ACTIVE 状态的 loanId"""
    today = datetime.now()
    submit_date = (today - timedelta(days=5)).strftime("%d %B %Y")
    approve_date = (today - timedelta(days=3)).strftime("%d %B %Y")
    disburse_date = (today - timedelta(days=2)).strftime("%d %B %Y")

    DATE_META = {"dateFormat": "dd MMMM yyyy", "locale": "en"}

    # 1. 提交申请
    res = api.post("/loans", json={
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
        **DATE_META,
    })
    assert res.status_code == 200, f"贷款申请失败: {res.text}"
    lid = res.json()["loanId"]

    # 2. 审批
    res = api.post(f"/loans/{lid}?command=approve", json={
        "approvedOnDate": approve_date,
        "expectedDisbursementDate": disburse_date,
        **DATE_META,
    })
    assert res.status_code == 200, f"贷款审批失败: {res.text}"

    # 3. 放款
    res = api.post(f"/loans/{lid}?command=disburse", json={
        "actualDisbursementDate": disburse_date,
        **DATE_META,
    })
    assert res.status_code == 200, f"放款失败: {res.text}"

    print(f"\n✅ 贷款已放款 loanId={lid}")
    return lid


@pytest.fixture(scope="session")
def savings_account_id(api, client_id, savings_product_id):
    """创建 → 审批 → 激活，返回 ACTIVE 状态的储蓄账户ID"""
    today = datetime.now()
    DATE_META = {"dateFormat": "dd MMMM yyyy", "locale": "en"}

    # 1. 创建储蓄账户
    res = api.post("/savingsaccounts", json={
        "clientId": client_id,
        "productId": savings_product_id,
        "submittedOnDate": today.strftime("%d %B %Y"),
        **DATE_META,
    })
    assert res.status_code == 200, f"创建储蓄账户失败: {res.text}"
    sid = res.json()["savingsId"]

    # 2. 审批
    res = api.post(f"/savingsaccounts/{sid}?command=approve", json={
        "approvedOnDate": today.strftime("%d %B %Y"),
        **DATE_META,
    })
    assert res.status_code == 200, f"审批储蓄账户失败: {res.text}"

    # 3. 激活
    res = api.post(f"/savingsaccounts/{sid}?command=activate", json={
        "activatedOnDate": today.strftime("%d %B %Y"),
        **DATE_META,
    })
    assert res.status_code == 200, f"激活储蓄账户失败: {res.text}"

    print(f"\n✅ 储蓄账户已激活 savingsAccountId={sid}")
    return sid