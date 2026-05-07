import pytest


class TestListClients:
    """List Clients 接口测试类"""

    BASE_PATH = "/clients"

    # 正常用例：使用部分可选参数，期望成功
    @pytest.mark.parametrize("params", [
        {"offset": 0, "limit": 10},
        {"officeId": 1, "status": "Active"},
        {"firstName": "John", "lastName": "Doe"},
        {"externalId": "ext-001"},
        {"displayName": "Test Client"},
        {"underHierarchy": "1"},
        {"orderBy": "id", "sortOrder": "ASC"},
        {"orphansOnly": False},
        {"legalForm": 1},
        {},
    ])
    def test_list_clients_success(self, api, params):
        """正常用例：使用各种可选参数组合，期望返回200"""
        resp = api.get(self.BASE_PATH, params=params)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list) or "pageItems" in data or "totalFilteredRecords" in data

    # 参数缺失用例：逐个缺少可选参数（本接口无必填参数，故测试空参数）
    def test_list_clients_no_params(self, api):
        """参数缺失用例：不传任何参数，期望成功"""
        resp = api.get(self.BASE_PATH)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list) or "pageItems" in data or "totalFilteredRecords" in data

    # 边界值用例：空字符串、极大值、极小值、0、负数等
    @pytest.mark.parametrize("params", [
        {"offset": -1},
        {"offset": 0},
        {"offset": 2147483647},
        {"offset": -2147483648},
        {"limit": -1},
        {"limit": 0},
        {"limit": 2147483647},
        {"limit": -2147483648},
        {"officeId": 0},
        {"officeId": -1},
        {"officeId": 9223372036854775807},
        {"officeId": -9223372036854775808},
        {"externalId": ""},
        {"displayName": ""},
        {"firstName": ""},
        {"lastName": ""},
        {"status": ""},
        {"underHierarchy": ""},
        {"orderBy": ""},
        {"sortOrder": ""},
        {"orphansOnly": True},
        {"orphansOnly": False},
        {"legalForm": 0},
        {"legalForm": -1},
        {"legalForm": 2147483647},
        {"legalForm": -2147483648},
    ])
    def test_list_clients_boundary(self, api, params):
        """边界值用例：测试边界值，期望成功或返回400/422"""
        resp = api.get(self.BASE_PATH, params=params)
        assert resp.status_code in [200, 400, 422]

    # 异常用例：错误类型、非法枚举值、特殊字符等
    @pytest.mark.parametrize("params", [
        {"officeId": "abc"},
        {"externalId": 123},
        {"displayName": 456},
        {"firstName": 789},
        {"lastName": 0.5},
        {"status": 1},
        {"underHierarchy": 2.5},
        {"offset": "abc"},
        {"limit": "xyz"},
        {"orderBy": 123},
        {"sortOrder": 456},
        {"orphansOnly": "yes"},
        {"legalForm": "invalid"},
        {"officeId": None},
        {"externalId": None},
        {"displayName": None},
        {"firstName": None},
        {"lastName": None},
        {"status": None},
        {"underHierarchy": None},
        {"offset": None},
        {"limit": None},
        {"orderBy": None},
        {"sortOrder": None},
        {"orphansOnly": None},
        {"legalForm": None},
        {"externalId": "<script>alert('xss')</script>"},
        {"displayName": "test@#$%^&*()"},
        {"firstName": "John\nDoe"},
        {"lastName": "O'Brien"},
        {"status": "InvalidStatus"},
        {"sortOrder": "invalid"},
        {"legalForm": 999},
    ])
    def test_list_clients_exception(self, api, params):
        """异常用例：错误类型、非法枚举值、特殊字符等，期望返回400/422"""
        resp = api.get(self.BASE_PATH, params=params)
        assert resp.status_code in [400, 422]