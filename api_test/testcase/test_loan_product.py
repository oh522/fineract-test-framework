from datetime import datetime, timedelta
import pytest
from common.base_api import BaseApi


class TestCreateLoan:
    """贷款申请测试"""

    def test_create_loan_success(self, api, client_id, loan_product_id):
        """✅ 正常创建贷款申请"""
        today = datetime.now()
        future = today + timedelta(days=30)

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
            "expectedDisbursementDate": future.strftime("%d %B %Y"),
            "submittedOnDate": today.strftime("%d %B %Y"),
            "dateFormat": "dd MMMM yyyy",
            "locale": "en",
            "loanType": "individual",
        }

        res = api.post("/loans", json=payload)
        assert res.status_code == 200, f"创建失败: {res.text}"

        # ---- 验证返回结果 ----
        data = res.json()
        assert "loanId" in data, "应返回 loanId"
        assert isinstance(data["loanId"], int)

    def test_create_loan_invalid_client(self, api, loan_product_id):
        """❌ 不存在的客户，应失败"""
        payload = {
            "clientId": 9999999,  # 不存在
            "productId": loan_product_id,
            "principal": 1000,
            # ...
        }
        res = api.post("/loans", json=payload)
        assert res.status_code == 404, "无效客户应返回404"

    def test_create_loan_zero_amount(self, api, client_id, loan_product_id):
        """❌ 金额为0，应失败"""
        payload = {
            "clientId": client_id,
            "productId": loan_product_id,
            "principal": 0,  # 零金额
            # ...
        }
        res = api.post("/loans", json=payload)
        assert res.status_code == 400, "零金额应返回400"

    def test_create_loan_exceeds_max(self, api, client_id, loan_product_id):
        """❌ 超过最大贷款额度"""
        payload = {
            "clientId": client_id,
            "productId": loan_product_id,
            "principal": 999999999,  # 超大金额
            # ...
        }
        res = api.post("/loans", json=payload)
        # 根据业务规则，可能是 400 或 403
        assert res.status_code in [400, 403]



class TestLoanApplication():
    """贷款申请测试用例"""

    def test_create_loan_with_json_file(self, api, client_id, loan_product_id):
        """✅ 测试从 JSON 文件加载数据创建贷款"""
        payload = api.load_json_data("loan_payload.json", key="test_create_loan_success")

        payload["clientId"] = client_id
        payload["productId"] = loan_product_id

        response = api.post("/loans", json=payload)
        assert response.status_code == 200, f"创建贷款失败: {response.text}"

        data = response.json()
        assert "loanId" in data
        print(f"✓ 从 JSON 文件创建贷款成功，ID: {data['loanId']}")

    def test_create_loan_with_override(self, api, client_id, loan_product_id):
        """✅ 测试创建贷款时覆盖部分字段"""
        payload = api.load_json_data(
            "loan_payload.json",
            key="base",
            principal=5000,
            loanTermFrequency=6
        )

        payload["clientId"] = client_id
        payload["productId"] = loan_product_id

        assert payload["principal"] == 5000
        assert payload["loanTermFrequency"] == 6

        response = api.post("/loans", json=payload)
        assert response.status_code == 200
        print("✓ 字段覆盖并创建成功")

    def test_create_loan_invalid_client(self, api, loan_product_id):
        """❌ 测试无效客户ID创建贷款"""
        payload = api.load_json_data("loan_payload.json", key="test_create_loan_invalid_client")
        payload["productId"] = loan_product_id

        response = api.post("/loans", json=payload)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code in [400, 403, 404], \
            f"期望错误响应，但得到: {response.status_code}"
        print("✓ 无效客户ID正确返回错误")

    def test_create_loan_zero_amount(self, api, client_id, loan_product_id):
        """ 测试零金额贷款"""
        payload = api.load_json_data("loan_payload.json", key="test_create_loan_zero_amount")
        payload["clientId"] = client_id
        payload["productId"] = loan_product_id

        response = api.post("/loans", json=payload)

        print(f"Status Code: {response.status_code}")

        assert response.status_code in [400, 403], \
            f"期望验证错误，但得到: {response.status_code}"
        print("✓ 零金额贷款正确返回验证错误")

    def test_create_loan_exceeds_max(self, api, client_id, loan_product_id):
        """❌ 测试超额贷款"""
        payload = api.load_json_data("loan_payload.json", key="test_create_loan_exceeds_max")
        payload["clientId"] = client_id
        payload["productId"] = loan_product_id

        response = api.post("/loans", json=payload)

        print(f"Status Code: {response.status_code}")

        assert response.status_code in [400, 403], \
            f"期望错误响应，但得到: {response.status_code}"
        print("✓ 超额贷款正确返回错误")

    def test_create_loan_success(self, api, client_id, loan_product_id):
        """测试成功创建贷款申请"""
        # 从JSON文件加载数据
        payload = api.load_json_data("loan_payload.json", key="test_create_loan_success")
        payload["clientId"] = client_id
        payload["productId"] = loan_product_id
        response = api.post("/loans", json=payload)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 200, f"创建贷款失败: {response.text}"
        data = response.json()
        assert "loanId" in data, "响应中缺少loanId"
        assert "resourceExternalId" in data
        print(f"✓ 贷款创建成功，ID: {data['loanId']}")

    def test_create_loan_success_v2(self, api, client_id, loan_product_id):
        """测试成功创建贷款申请（使用load_and_send）"""
        # 直接加载并发送
        response = api.load_and_send("/loans", key="test_create_loan_success")

        assert response.status_code == 200
        data = response.json()
        assert "loanId" in data
        print(f"✓ 贷款创建成功，ID: {data['loanId']}")

    def test_create_loan_with_override1(self, api, client_id, loan_product_id):
        """测试创建贷款时覆盖部分字段"""
        # 加载基础数据并覆盖principal
        payload = api.load_json_data(
            "loan_payload.json",
            key="base",
            principal=5000,  # 覆盖为5000
            loanTermFrequency=6  # 覆盖为6期
        )

        assert payload["principal"] == 5000
        assert payload["loanTermFrequency"] == 6
        print("✓ 字段覆盖成功")

    def test_create_loan_invalid_client1(self, api):
        """测试无效客户ID创建贷款"""
        payload = api.load_json_data("loan_payload.json", key="test_create_loan_invalid_client")

        response = api.post("/loans", json=payload)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        # 无效客户应该返回错误
        assert response.status_code in [404], f"期望错误响应，但得到: {response.status_code}"
        print("✓ 无效客户ID正确返回错误")

    def test_create_loan_zero_amount1(self, api):
        """测试零金额贷款"""
        payload = api.load_json_data("loan_payload.json", key="test_create_loan_zero_amount")

        response = api.post("/loans", json=payload)

        print(f"Status Code: {response.status_code}")

        # 零金额应该返回验证错误
        assert response.status_code in [400, 403], f"期望验证错误，但得到: {response.status_code}"
        print("✓ 零金额贷款正确返回验证错误")

    def test_create_loan_exceeds_max1(self, api):
        """测试超额贷款"""
        payload = api.load_json_data("loan_payload.json", key="test_create_loan_exceeds_max")

        response = api.post("/loans", json=payload)

        print(f"Status Code: {response.status_code}")

        # 超额应该返回错误
        assert response.status_code in [400, 403], f"期望错误响应，但得到: {response.status_code}"
        print("✓ 超额贷款正确返回错误")


class TestLoanRetrieval(BaseApi):
    """贷款查询测试用例"""

    def test_get_loan_details(self, api, loan_id):
        """测试查询贷款详情"""
        # 先创建一个贷款
        payload = api.load_json_data("loan_payload.json", key="base")
        create_resp = api.post("/loans", json=payload)

        if create_resp.status_code == 200:

            loan_id = create_resp.json()["loanId"]
            # 查询贷款详情
            get_resp = api.get(f"/loans/{loan_id}")
            assert get_resp.status_code == 200

            data = get_resp.json()
            assert data["id"] == loan_id
            print(f"✓ 成功查询贷款详情，ID: {loan_id}")
        else:
            pytest.skip("无法创建贷款，跳过查询测试")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-s"])
