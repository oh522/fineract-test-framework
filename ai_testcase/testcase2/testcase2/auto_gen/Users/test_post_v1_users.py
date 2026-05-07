import pytest
from api_test.common.base_api import BaseApi

class TestCreateUser:
    # 正常用例：使用所有字段创建用户，期望成功
    def test_create_user_success(self, api):
        payload = {
            "clients": [2, 3],
            "email": "whatever@mifos.org",
            "firstname": "Test",
            "isLoginRetriesEnabled": True,
            "isPasswordResetAllowed": True,
            "lastname": "User",
            "officeId": 1,
            "password": "password",
            "passwordNeverExpires": True,
            "repeatPassword": "password",
            "roles": [2, 3],
            "sendPasswordToEmail": True,
            "staffId": 1,
            "username": "newuser"
        }
        resp = api.post("/v1/users", json=payload)
        assert resp.status_code == 200
        assert "resourceId" in resp.json()

    # 参数缺失用例：逐个缺少所有字段（因为required_fields为空，所以测试空请求体）
    def test_create_user_missing_all_fields(self, api):
        payload = {}
        resp = api.post("/v1/users", json=payload)
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：测试空字符串、极大值、极小值、0、负数等
    @pytest.mark.parametrize("field, value, expected_status", [
        ("email", "", 400),
        ("email", "a" * 1000, 400),
        ("firstname", "", 400),
        ("firstname", "a" * 1000, 400),
        ("lastname", "", 400),
        ("lastname", "a" * 1000, 400),
        ("username", "", 400),
        ("username", "a" * 1000, 400),
        ("password", "", 400),
        ("password", "a" * 1000, 400),
        ("repeatPassword", "", 400),
        ("repeatPassword", "a" * 1000, 400),
        ("officeId", 0, 400),
        ("officeId", -1, 400),
        ("officeId", 999999, 404),
        ("staffId", 0, 400),
        ("staffId", -1, 400),
        ("staffId", 999999, 404),
        ("clients", [], 400),
        ("clients", [999999], 404),
        ("roles", [], 400),
        ("roles", [999999], 404),
    ])
    def test_create_user_boundary_values(self, api, field, value, expected_status):
        payload = {
            "clients": [2, 3],
            "email": "whatever@mifos.org",
            "firstname": "Test",
            "isLoginRetriesEnabled": True,
            "isPasswordResetAllowed": True,
            "lastname": "User",
            "officeId": 1,
            "password": "password",
            "passwordNeverExpires": True,
            "repeatPassword": "password",
            "roles": [2, 3],
            "sendPasswordToEmail": True,
            "staffId": 1,
            "username": "newuser"
        }
        payload[field] = value
        resp = api.post("/v1/users", json=payload)
        assert resp.status_code == expected_status

    # 异常用例：错误类型、非法枚举值、特殊字符等
    @pytest.mark.parametrize("field, value, expected_status", [
        ("email", 123, 400),
        ("email", "invalid-email", 400),
        ("firstname", 123, 4