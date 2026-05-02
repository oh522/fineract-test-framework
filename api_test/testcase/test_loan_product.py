from datetime import datetime, timedelta

def test_create_loan_success(api, client_id, loan_product_id):
    """测试创建贷款申请"""
    assert loan_product_id is not None, "贷款产品 ID 为空"
    assert client_id is not None, "客户 ID 为空"
    
    # 使用当前日期和未来日期
    today = datetime.now()
    future_date = today + timedelta(days=30)
    
    payload = {
        "clientId": client_id,
        "productId": loan_product_id,
        "principal": 1000,
        "loanTermFrequency": 12,
        "loanTermFrequencyType": 2,
        "numberOfRepayments": 12,
        "repaymentEvery": 1,
        "repaymentFrequencyType": 2,
        "interestRatePerPeriod": 2,
        "amortizationType": 1,
        "interestType": 0,
        "interestCalculationPeriodType": 1,
        "transactionProcessingStrategyCode": "mifos-standard-strategy",
        "expectedDisbursementDate": future_date.strftime("%d %B %Y"),
        "submittedOnDate": today.strftime("%d %B %Y"),
        "dateFormat": "dd MMMM yyyy",
        "locale": "en",
        "loanType": "individual",
        "charges": []
    }
    
    res = api.post("/loans", json=payload)
    assert res.status_code == 200, f"贷款申请失败: {res.text}"