import os
import time
import uuid
import pytest
from datetime import datetime, timedelta
from api_test.common.base_api import BaseApi
from api_test.common.api.auth_api import AuthApi
from api_test.common.api.client_api import ClientApi
from api_test.common.api.loan_api import LoanApi
from api_test.common.api.savings_api import SavingsApi


# ══════════════════════════════════════════════════
#  基础客户端 fixture（其他 API 类共享同一个 session）
# ══════════════════════════════════════════════════

@pytest.fixture(scope="session")
def base_api() -> BaseApi:
    """全局唯一 BaseApi 实例，整个 session 只初始化一次"""
    return BaseApi()


# ══════════════════════════════════════════════════
#  API 层 fixture（testcase 层直接注入使用）
# ══════════════════════════════════════════════════

def _clone(api_cls, base: BaseApi):
    """
    复用 base_api 的 session，避免重复初始化
    相当于"同一个人"用不同业务模块的方法
    """
    instance = object.__new__(api_cls)
    instance.__dict__.update(base.__dict__)
    return instance


@pytest.fixture(scope="session")
def auth_api(base_api) -> AuthApi:
    return _clone(AuthApi, base_api)


@pytest.fixture(scope="session")
def client_api(base_api) -> ClientApi:
    return _clone(ClientApi, base_api)


@pytest.fixture(scope="session")
def loan_api(base_api) -> LoanApi:
    return _clone(LoanApi, base_api)


@pytest.fixture(scope="session")
def savings_api(base_api) -> SavingsApi:
    return _clone(SavingsApi, base_api)


# ══════════════════════════════════════════════════
#  业务数据 fixture（使用 API 层，不再直接调用 base_api）
# ══════════════════════════════════════════════════

DATE_META = {"dateFormat": "dd MMMM yyyy", "locale": "en"}


@pytest.fixture(scope="session")
def client_id(client_api):
    """创建测试客户，返回 clientId"""
    worker = os.environ.get("PYTEST_XDIST_WORKER", "master")
    payload = {
        "officeId": 1,
        "firstname": "自动化",
        "lastname": f"测试客户_{worker}",
        "legalFormId": 1,
        "active": True,
        "activationDate": "01 January 2023",
        "externalId": f"AUTO-{worker}-{int(time.time())}",
        **DATE_META,
    }
    res = client_api.create(payload)
    assert res.status_code == 200, f"创建客户失败: {res.text}"

    cid = res.json().get("clientId") or res.json().get("resourceId")
    assert isinstance(cid, int) and cid > 0
    print(f"\n✅ 客户已创建 clientId={cid}")
    yield cid
    print(f"\n🧹 [teardown] 客户 {cid} 测试完成")


@pytest.fixture(scope="session")
def loan_product_id(loan_api):
    """创建贷款产品，返回 productId"""
    suffix = uuid.uuid4().hex[:4]
    payload = {
        "name": f"自动化贷款产品_{uuid.uuid4().hex[:6]}",
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
        "daysInYearType": 360,
        "daysInMonthType": 30,
        "isInterestRecalculationEnabled": False,
        "charges": [],
        **DATE_META,
    }
    res = loan_api.create_product(payload)
    assert res.status_code == 200, f"创建贷款产品失败: {res.text}"

    pid = res.json().get("resourceId")
    assert isinstance(pid, int) and pid > 0
    print(f"\n✅ 贷款产品已创建 productId={pid}")
    yield pid


@pytest.fixture(scope="session")
def savings_product_id(savings_api):
    """创建储蓄产品，返回 productId"""
    suffix = uuid.uuid4().hex[:4]
    payload = {
        "name": f"自动化储蓄产品_{suffix}",
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
    res = savings_api.create_product(payload)
    assert res.status_code == 200, f"创建储蓄产品失败: {res.text}"
    pid = res.json().get("resourceId")
    assert isinstance(pid, int) and pid > 0
    print(f"\n✅ 储蓄产品已创建 productId={pid}")
    yield pid


@pytest.fixture(scope="session")
def loan_id(loan_api, client_id, loan_product_id):
    """创建 → 审批 → 放款，返回 ACTIVE 的 loanId"""
    today = datetime.now()
    submit_date = (today - timedelta(days=5)).strftime("%d %B %Y")
    approve_date = (today - timedelta(days=3)).strftime("%d %B %Y")
    disburse_date = (today - timedelta(days=2)).strftime("%d %B %Y")

    # 1. 申请
    res = loan_api.apply({  # ← 调用 API 层
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
        "submittedOnDate": submit_date,
        "expectedDisbursementDate": disburse_date,
        "loanType": "individual",
        **DATE_META,
    })

    assert res.status_code == 200, f"贷款申请失败: {res.text}"
    lid = res.json()["loanId"]

    # 2. 审批
    res = loan_api.approve(lid, {              # ← 调用 API 层
        "approvedOnDate": approve_date,
        "expectedDisbursementDate": disburse_date,
        **DATE_META,
    })
    assert res.status_code == 200, f"贷款审批失败: {res.text}"

    # 3. 放款
    res = loan_api.disburse(lid, {             # ← 调用 API 层
        "actualDisbursementDate": disburse_date,
        **DATE_META,
    })
    assert res.status_code == 200, f"放款失败: {res.text}"

    print(f"\n✅ 贷款已放款 loanId={lid}")
    yield lid


@pytest.fixture(scope="session")
def savings_account_id(savings_api, client_id, savings_product_id):
    """创建 → 审批 → 激活，返回 ACTIVE 的储蓄账户 ID"""
    today_str = datetime.now().strftime("%d %B %Y")

    res = savings_api.create_account({         # ← 调用 API 层
        "clientId": client_id,
        "productId": savings_product_id,
        "submittedOnDate": today_str,
        **DATE_META,
    })
    assert res.status_code == 200, f"创建储蓄账户失败: {res.text}"
    sid = res.json()["savingsId"]

    savings_api.approve_account(sid, {"approvedOnDate": today_str, **DATE_META})
    savings_api.activate_account(sid, {"activatedOnDate": today_str, **DATE_META})

    print(f"\n✅ 储蓄账户已激活 savingsAccountId={sid}")
    yield sid