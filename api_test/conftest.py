import time
import pytest


# @pytest.fixture(scope="session")
# def login_id(api):
#     """创建测试用户，返回 loginId"""
#     payload = {
#                 "password": "password",
#                 "username": "mifos"
# }
#     res = api.post("/authentication", json=payload)
#     assert res.status_code == 200, f"登录失败：{res.text}"
#     return res.json()["base64EncodedAuthenticationKey"]

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
        "externalId": unique_id
    }

    # 发送请求
    res = api.post("/clients", json=payload)

    # ✅ 改进 1：验证状态码
    assert res.status_code == 200, f"创建客户失败: {res.text}"

    # ✅ 改进 2：验证响应结构
    response_data = res.json()
    assert "resourceId" in response_data or "clientId" in response_data, \
        f"响应缺少关键字段: {response_data}"

    # ✅ 改进 3：验证返回数据一致性
    cid = response_data.get("clientId") or response_data.get("resourceId")
    assert cid is not None, "clientId 不能为空"
    assert isinstance(cid, int), f"clientId 类型错误，期望 int，实际 {type(cid)}"

    # ✅ 改进 4：验证 externalId 一致性（如果 API 返回）
    if "externalId" in response_data:
        assert response_data["externalId"] == unique_id, \
            f"externalId 不匹配: 期望 {unique_id}, 实际 {response_data['externalId']}"

    print(f"\n✅ 测试客户已创建 clientId={cid}")
    return cid


@pytest.fixture(scope="session")
def loan_product_id(api):
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

    res = api.post("/loanproducts", json=payload)

    # ✅ 改进：完整的断言链
    assert res.status_code == 200, f"创建贷款产品失败: {res.text}"

    response_data = res.json()
    assert "resourceId" in response_data, f"响应缺少 resourceId: {response_data}"

    product_id = response_data["resourceId"]
    assert isinstance(product_id, int), f"productId 类型错误: {type(product_id)}"
    assert product_id > 0, f"productId 应为正数: {product_id}"

    print(f"\n✅ 贷款产品已创建 productId={product_id}")
    return product_id


@pytest.fixture(scope="session")
def savings_product_id(api):
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

    res = api.post("/savingsproducts", json=payload)

    assert res.status_code == 200, f"创建储蓄产品失败: {res.text}"

    response_data = res.json()
    assert "resourceId" in response_data, f"响应缺少 resourceId: {response_data}"

    pid = response_data["resourceId"]
    assert isinstance(pid, int) and pid > 0, f"productId 无效: {pid}"

    print(f"\n✅ 储蓄产品已创建 productId={pid}")
    return pid


@pytest.fixture(scope="session")
def loan_id(api, client_id, loan_product_id):
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

    res = api.post("/loans", json=apply_payload)
    assert res.status_code == 200, f"贷款申请失败: {res.text}"

    response_data = res.json()
    assert "loanId" in response_data, f"响应缺少 loanId: {response_data}"
    lid = response_data["loanId"]
    assert isinstance(lid, int) and lid > 0, f"loanId 无效: {lid}"

    # 审批
    approve_payload = {
        "approvedOnDate": "05 January 2024",
        "expectedDisbursementDate": "10 January 2024",
        "dateFormat": "dd MMMM yyyy",
        "locale": "en"
    }
    res = api.post(
        f"/loans/{lid}?command=approve",
        json=approve_payload
    )
    assert res.status_code == 200, f"贷款审批失败: {res.text}"

    # ✅ 验证审批后的状态
    approve_response = res.json()
    assert "changes" in approve_response or "status" in approve_response, \
        f"审批响应格式异常: {approve_response}"

    # 放款
    disburse_payload = {
        "actualDisbursementDate": "10 January 2024",
        "dateFormat": "dd MMMM yyyy",
        "locale": "en"
    }
    res = api.post(
        f"/loans/{lid}?command=disburse",
        json=disburse_payload
    )
    assert res.status_code == 200, f"放款失败: {res.text}"

    # ✅ 验证放款后的状态
    disburse_response = res.json()
    assert "changes" in disburse_response or "status" in disburse_response, \
        f"放款响应格式异常: {disburse_response}"

    print(f"\n✅ 贷款已放款 loanId={lid}")
    return lid
