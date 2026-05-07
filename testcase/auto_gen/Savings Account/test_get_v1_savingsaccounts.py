import pytest


class TestSavingsAccountsList:
    """Savings Account list API tests"""

    @pytest.mark.parametrize("query_params", [
        {},
        {"offset": 0, "limit": 10},
        {"externalId": "test-ext-001"},
        {"orderBy": "id", "sortOrder": "ASC"},
        {"offset": 0, "limit": 10, "orderBy": "id", "sortOrder": "DESC"},
    ])
    def test_list_savings_accounts_success(self, api, query_params):
        """正常用例：使用各种有效查询参数组合，期望成功"""
        resp = api.get("/savingsaccounts", params=query_params)
        assert resp.status_code == 200
        data = resp.json()
        assert "totalFilteredRecords" in data
        assert "pageItems" in data

    @pytest.mark.parametrize("missing_param", [
        "offset",
        "limit",
        "externalId",
        "orderBy",
        "sortOrder",
    ])
    def test_list_savings_accounts_missing_optional_param(self, api, missing_param):
        """参数缺失用例：逐个缺少可选查询参数，期望成功（因为所有参数都是可选的）"""
        params = {"offset": 0, "limit": 10, "externalId": "test", "orderBy": "id", "sortOrder": "ASC"}
        params.pop(missing_param, None)
        resp = api.get("/savingsaccounts", params=params)
        assert resp.status_code == 200

    @pytest.mark.parametrize("query_params", [
        {"offset": -1},
        {"offset": 999999999},
        {"limit": -1},
        {"limit": 0},
        {"limit": 999999999},
        {"externalId": ""},
        {"orderBy": ""},
        {"sortOrder": ""},
        {"sortOrder": "INVALID"},
        {"offset": "abc"},
        {"limit": "xyz"},
    ])
    def test_list_savings_accounts_boundary_and_invalid(self, api, query_params):
        """边界值/异常用例：空字符串、极大值、极小值、0、负数、错误类型、非法枚举值等"""
        resp = api.get("/savingsaccounts", params=query_params)
        # 期望返回 400 或 422 等错误状态码
        assert resp.status_code in [400, 422]

    @pytest.mark.parametrize("query_params", [
        {"offset": 0, "limit": 10, "externalId": "!@#$%^&*()"},
        {"offset": 0, "limit": 10, "orderBy": "id", "sortOrder": "asc"},
        {"offset": 0, "limit": 10, "orderBy": "id", "sortOrder": "desc"},
        {"offset": 0, "limit": 10, "externalId": "a" * 256},
    ])
    def test_list_savings_accounts_special_characters(self, api, query_params):
        """异常用例：特殊字符、大小写枚举、超长字符串等"""
        resp = api.get("/savingsaccounts", params=query_params)
        # 特殊字符可能被接受或拒绝，取决于后端实现
        assert resp.status_code in [200, 400, 422]

    def test_list_savings_accounts_no_params(self, api):
        """正常用例：不传任何查询参数，期望成功"""
        resp = api.get("/savingsaccounts")
        assert resp.status_code == 200
        data = resp.json()
        assert "totalFilteredRecords" in data
        assert "pageItems" in data

    @pytest.mark.parametrize("query_params", [
        {"offset": 0, "limit": 10, "externalId": "nonexistent-external-id-999999"},
    ])
    def test_list_savings_accounts_nonexistent_external_id(self, api, query_params):
        """正常用例：使用不存在的 externalId，期望返回空列表"""
        resp = api.get("/savingsaccounts", params=query_params)
        assert resp.status_code == 200
        data = resp.json()
        assert data["totalFilteredRecords"] == 0
        assert data["pageItems"] == []