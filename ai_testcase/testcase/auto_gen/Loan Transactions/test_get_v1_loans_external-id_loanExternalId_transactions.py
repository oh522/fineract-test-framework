import pytest
from typing import Dict, List, Optional, Any

class TestLoanTransactions:
    """Loan Transactions接口测试类"""
    
    BASE_PATH = "/loans/external-id/{loanExternalId}/transactions"
    
    @pytest.fixture
    def valid_loan_external_id(self) -> str:
        """返回一个有效的贷款外部ID"""
        return "valid-external-id-123"
    
    @pytest.fixture
    def invalid_loan_external_id(self) -> str:
        """返回一个无效的贷款外部ID"""
        return "999999"
    
    # ==================== 正常用例 ====================
    @pytest.mark.parametrize("loan_external_id, query_params", [
        ("valid-external-id-123", {}),
        ("valid-external-id-123", {"page": 0, "size": 10}),
        ("valid-external-id-123", {"page": 1, "size": 20}),
        ("valid-external-id-123", {"sort": "id,asc"}),
        ("valid-external-id-123", {"excludedTypes": ["REPAYMENT"]}),
        ("valid-external-id-123", {"excludedTypes": ["REPAYMENT", "DISBURSEMENT"]}),
        ("valid-external-id-123", {"page": 0, "size": 10, "sort": "date,desc", "excludedTypes": ["REPAYMENT"]}),
    ])
    def test_normal_cases(self, api, loan_external_id: str, query_params: Dict[str, Any]):
        """正常用例：使用有效的贷款外部ID和可选查询参数，期望成功"""
        path = self.BASE_PATH.format(loanExternalId=loan_external_id)
        resp = api.get(path, params=query_params)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        # 验证响应字段存在
        data = resp.json()
        assert "totalFilteredRecords" in data or "content" in data or "pageItems" in data, "Response missing expected fields"
    
    # ==================== 参数缺失用例 ====================
    @pytest.mark.parametrize("loan_external_id, query_params, expected_status", [
        ("", {}, 404),  # 空字符串路径参数
        (None, {}, 404),  # None路径参数
        ("valid-external-id-123", {"page": None}, 400),  # page为None
        ("valid-external-id-123", {"size": None}, 400),  # size为None
        ("valid-external-id-123", {"sort": None}, 400),  # sort为None
        ("valid-external-id-123", {"excludedTypes": None}, 400),  # excludedTypes为None
    ])
    def test_missing_params(self, api, loan_external_id: str, query_params: Dict[str, Any], expected_status: int):
        """参数缺失用例：缺少必填路径参数或查询参数为None"""
        if loan_external_id is None:
            path = self.BASE_PATH.format(loanExternalId="")
        else:
            path = self.BASE_PATH.format(loanExternalId=loan_external_id)
        resp = api.get(path, params=query_params)
        assert resp.status_code in [400, 403, 404, 422, expected_status], f"Expected error status, got {resp.status_code}"
    
    # ==================== 边界值用例 ====================
    @pytest.mark.parametrize("loan_external_id, query_params, description", [
        ("", {}, "空字符串路径参数"),
        ("a" * 1000, {}, "超长路径参数"),
        ("valid-external-id-123", {"page": -1}, "page为负数"),
        ("valid-external-id-123", {"page": 0}, "page为0"),
        ("valid-external-id-123", {"page": 2147483647}, "page为int32最大值"),
        ("valid-external-id-123", {"page": -2147483648}, "page为int32最小值"),
        ("valid-external-id-123", {"size": -1}, "size为负数"),
        ("valid-external-id-123", {"size": 0}, "size为0"),
        ("valid-external-id-123", {"size": 2147483647}, "size为int32最大值"),
        ("valid-external-id-123", {"size": -2147483648}, "size为int32最小值"),
        ("valid-external-id-123", {"sort": ""}, "sort为空字符串"),
        ("valid-external-id-123", {"sort": "a" * 1000}, "sort为超长字符串"),
        ("valid-external-id-123", {"excludedTypes": []}, "excludedTypes为空数组"),
        ("valid-external-id-123", {"excludedTypes": [""]}, "excludedTypes包含空字符串"),
        ("valid-external-id-123", {"excludedTypes": ["a" * 100]}, "excludedTypes包含超长字符串"),
    ])
    def test_boundary_cases(self, api, loan_external_id: str, query_params: Dict[str, Any], description: str):
        """边界值用例：测试各种边界条件"""
        path = self.BASE_PATH.format(loanExternalId=loan_external_id)
        resp = api.get(path, params=query_params)
        # 边界值可能返回200或错误状态码
        assert resp.status_code in [200, 400, 403, 404, 422], f"Unexpected status code {resp.status_code} for {description}"
    
    # ==================== 异常用例 ====================
    @pytest.mark.parametrize("loan_external_id, query_params, description", [
        ("valid-external-id-123", {"page": "abc"}, "page为字符串"),
        ("valid-external-id-123", {"page": 1.5}, "page为浮点数"),
        ("valid-external-id-123", {"page": True}, "page为布尔值"),
        ("valid-external-id-123", {"size": "abc"}, "size为字符串"),
        ("valid-external-id-123", {"size": 1.5}, "size为浮点数"),
        ("valid-external-id-123", {"size": True}, "size为布尔值"),
        ("valid-external-id-123", {"sort": 123}, "sort为整数"),
        ("valid-external-id-123", {"sort": True}, "sort为布尔值"),
        ("valid-external-id-123", {"sort": ["invalid"]}, "sort为数组"),
        ("valid-external-id-123", {"sort": {"key": "value"}}, "sort为对象"),
        ("valid-external-id-123", {"excludedTypes": "INVALID_TYPE"}, "excludedTypes为字符串"),
        ("valid-external-id-123", {"excludedTypes": 123}, "excludedTypes为整数"),
        ("valid-external-id-123", {"excludedTypes": True}, "excludedTypes为布尔值"),
        ("valid-external-id-123", {"excludedTypes": {"key": "value"}}, "excludedTypes为对象"),
        ("valid-external-id-123", {"excludedTypes": ["INVALID_TYPE"]}, "excludedTypes包含无效枚举值"),
        ("valid-external-id-123", {"excludedTypes": ["REPAYMENT", "INVALID_TYPE"]}, "excludedTypes混合有效和无效枚举值"),
        ("valid-external-id-123", {"page": None, "size": None, "sort": None, "excludedTypes": None}, "所有查询参数为None"),
        ("<script>alert('xss')</script>", {}, "路径参数包含XSS攻击字符串"),
        ("valid-external-id-123", {"page": "<script>alert('xss')</script>"}, "page包含XSS攻击字符串"),
        ("valid-external-id-123", {"size": "<script>alert('xss')</script>"}, "size包含XSS攻击字符串"),
        ("valid-external-id-123", {"sort": "<script>alert('xss')</script>"}, "sort包含XSS攻击字符串"),
        ("valid-external-id-123", {"excludedTypes": ["<script>alert('xss')</script>"]}, "excludedTypes包含XSS攻击字符串"),
    ])
    def test_exception_cases(self, api, loan_external_id: str, query_params: Dict[str, Any], description: str):
        """异常用例：测试错误类型、非法枚举值、特殊字符等"""
        path = self.BASE_PATH.format(loanExternalId=loan_external_id)
        resp = api.get(path, params=query_params)
        assert resp.status_code in [400, 403, 404, 422], f"Expected error status for {description}, got {resp.status_code}"
    
    # ==================== 不存在的资源ID用例 ====================
    @pytest.mark.parametrize("