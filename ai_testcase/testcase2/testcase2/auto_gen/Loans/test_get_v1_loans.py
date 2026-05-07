import pytest
from api_test.common.base_api import BaseApi

class TestListLoans:
    # 正常用例：使用所有查询参数，期望成功
    def test_list_loans_with_all_params(self, api):
        params = {
            "externalId": "EXT-LOAN-001",
            "offset": 0,
            "limit": 10,
            "orderBy": "id",
            "sortOrder": "ASC",
            "accountNo": "LN000001",
            "associations": "all",
            "clientId": 1,
            "status": "active"
        }
        resp = api.get("/v1/loans", params=params)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    # 正常用例：仅使用必填参数（无必填参数，使用最小参数集）
    def test_list_loans_minimal_params(self, api):
        resp = api.get("/v1/loans")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    # 参数缺失用例：逐个测试可选参数缺失
    @pytest.mark.parametrize("missing_param", [
        "externalId", "offset", "limit", "orderBy", "sortOrder", 
        "accountNo", "associations", "clientId", "status"
    ])
    def test_list_loans_missing_optional_param(self, api, missing_param):
        params = {
            "externalId": "EXT-LOAN-001",
            "offset": 0,
            "limit": 10,
            "orderBy": "id",
            "sortOrder": "ASC",
            "accountNo": "LN000001",
            "associations": "all",
            "clientId": 1,
            "status": "active"
        }
        params.pop(missing_param, None)
        resp = api.get("/v1/loans", params=params)
        assert resp.status_code == 200

    # 边界值用例：测试整数参数的边界值
    @pytest.mark.parametrize("param_name, param_value", [
        ("offset", 0),
        ("offset", -1),
        ("offset", 2147483647),  # int32最大值
        ("offset", -2147483648), # int32最小值
        ("limit", 0),
        ("limit", -1),
        ("limit", 2147483647),
        ("limit", -2147483648),
        ("clientId", 0),
        ("clientId", -1),
        ("clientId", 9223372036854775807),  # int64最大值
        ("clientId", -9223372036854775808)  # int64最小值
    ])
    def test_list_loans_integer_boundary_values(self, api, param_name, param_value):
        params = {param_name: param_value}
        resp = api.get("/v1/loans", params=params)
        # 根据参数类型和值，可能返回200或400
        assert resp.status_code in [200, 400]

    # 边界值用例：测试字符串参数的边界值
    @pytest.mark.parametrize("param_name, param_value", [
        ("externalId", ""),
        ("externalId", "a" * 1000),  # 长字符串
        ("externalId", "!@#$%^&*()_+{}|:\"<>?"),
        ("accountNo", ""),
        ("accountNo", "a" * 1000),
        ("accountNo", "!@#$%^&*()_+{}|:\"<>?"),
        ("orderBy", ""),
        ("orderBy", "a" * 1000),
        ("orderBy", "!@#$%^&*()_+{}|:\"<>?"),
        ("sortOrder", ""),
        ("sortOrder", "a" * 1000),
        ("sortOrder", "!@#$%^&*()_+{}|:\"<>?"),
        ("status", ""),
        ("status", "a" * 1000),
        ("status", "!@#$%^&*()_+{}|:\"<>?"),
        ("associations", ""),
        ("associations", "a" * 1000),
        ("associations", "!@#$%^&*()_+{}|:\"<>?")
    ])
    def test_list_loans_string_boundary_values(self, api, param_name, param_value):
        params = {param_name: param_value}
        resp = api.get("/v1/loans", params=params)
        assert resp.status_code in [200, 400]

    # 异常用例：测试错误类型参数
    @pytest.mark.parametrize("param_name, param_value", [
        ("offset", "abc"),
        ("offset", "12.5"),
        ("offset", ""),
        ("limit", "abc"),
        ("limit