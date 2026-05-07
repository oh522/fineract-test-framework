import pytest
from api_test.common.base_api import BaseApi

class TestSavingsAccountsList:
    # 正常用例：使用所有查询参数，期望成功
    def test_list_savings_accounts_success(self, api):
        params = {
            "externalId": "EXT001",
            "offset": 0,
            "limit": 10,
            "orderBy": "id",
            "sortOrder": "asc"
        }
        resp = api.get("/v1/savingsaccounts", params=params)
        assert resp.status_code == 200
        assert "pageItems" in resp.json()

    # 正常用例：不带任何查询参数，期望成功
    def test_list_savings_accounts_no_params(self, api):
        resp = api.get("/v1/savingsaccounts")
        assert resp.status_code == 200
        assert "pageItems" in resp.json()

    # 正常用例：只带部分查询参数，期望成功
    @pytest.mark.parametrize("params", [
        {"externalId": "EXT002"},
        {"offset": 5, "limit": 20},
        {"orderBy": "id", "sortOrder": "desc"}
    ])
    def test_list_savings_accounts_partial_params(self, api, params):
        resp = api.get("/v1/savingsaccounts", params=params)
        assert resp.status_code == 200
        assert "pageItems" in resp.json()

    # 边界值用例：offset和limit的边界值
    @pytest.mark.parametrize("params, expected_status", [
        ({"offset": 0, "limit": 0}, 200),
        ({"offset": 0, "limit": 1}, 200),
        ({"offset": 0, "limit": 1000}, 200),
        ({"offset": 0, "limit": -1}, 400),
        ({"offset": -1, "limit": 10}, 400),
        ({"offset": 0, "limit": 1001}, 400)
    ])
    def test_list_savings_accounts_boundary_values(self, api, params, expected_status):
        resp = api.get("/v1/savingsaccounts", params=params)
        assert resp.status_code == expected_status

    # 边界值用例：externalId的边界值
    @pytest.mark.parametrize("externalId, expected_status", [
        ("", 200),
        ("a" * 100, 200),
        ("!@#$%^&*()", 200),
        ("EXT-001", 200),
        ("EXT 001", 200)
    ])
    def test_list_savings_accounts_external_id_boundary(self, api, externalId, expected_status):
        params = {"externalId": externalId}
        resp = api.get("/v1/savingsaccounts", params=params)
        assert resp.status_code == expected_status

    # 边界值用例：orderBy和sortOrder的边界值
    @pytest.mark.parametrize("params, expected_status", [
        ({"orderBy": "", "sortOrder": ""}, 200),
        ({"orderBy": "id", "sortOrder": ""}, 200),
        ({"orderBy": "", "sortOrder": "asc"}, 200),
        ({"orderBy": "invalid_field", "sortOrder": "asc"}, 400),
        ({"orderBy": "id", "sortOrder": "invalid_order"}, 400)
    ])
    def test_list_savings_accounts_order_boundary(self, api, params, expected_status):
        resp = api.get("/v1/savingsaccounts", params=params)
        assert resp.status_code == expected_status

    # 异常用例：参数类型错误
    @pytest.mark.parametrize("params, expected_status", [
        ({"offset": "abc", "limit": 10}, 400),
        ({"offset": 0, "limit": "xyz"}, 400),
        ({"offset": 1.5, "limit": 10}, 400),
        ({"offset": 0, "limit": 10.5}, 400)
    ])
    def test_list_savings_accounts_invalid_type(self, api, params, expected_status):
        resp = api.get("/v1/savingsaccounts", params=params)
        assert resp.status_code == expected_status

    # 异常用例：特殊字符和SQL注入尝试
    @pytest.mark.parametrize("params, expected_status", [
        ({"externalId": "'; DROP TABLE savings_accounts; --"}, 200),
        ({"externalId": "<script>alert('xss')</script>"}, 200),
        ({"externalId": "EXT' OR '1'='1"}, 200)
    ])
    def test_list_savings_accounts_special_characters(self, api, params, expected_status):
        resp = api.get("/v1/savingsaccounts", params=params)
        assert resp.status_code == expected_status

    # 异常用例：不存在的资源ID（通过externalId查询）
    def test_list_savings_accounts_nonexistent_external_id(self, api):
        params = {"externalId": "NONEXISTENT_ID_999999"}
        resp = api.get("/v1/savingsaccounts", params=params)
        assert resp.status_code == 200
        assert len(resp.json().get("pageItems", [])) == 0

    # 异常用例：极大值参数
    @pytest.mark.parametrize("params, expected_status", [
        ({"offset": 2147483647, "limit": 10}, 200),
        ({"offset": 0, "limit": 2147483647}, 400),
        ({"offset": 2147483648, "limit": 10}, 400)
    ])
    def test_list_savings_accounts_extreme_values(self, api, params, expected_status):
        resp = api.get("/v1/savingsaccounts", params=params)
        assert resp