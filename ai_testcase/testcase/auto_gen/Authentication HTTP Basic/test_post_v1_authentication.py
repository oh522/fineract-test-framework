import pytest


class TestAuthentication:
    """Authentication HTTP Basic 接口测试类"""

    BASE_PATH = "/authentication"

    # 正常用例：使用必填字段，期望成功
    @pytest.mark.parametrize("username, password", [
        ("mifos", "password"),
        ("admin", "password"),
    ])
    def test_authentication_success(self, api, username, password):
        payload = {
            "username": username,
            "password": password
        }
        resp = api.post(self.BASE_PATH, json=payload)
        assert resp.status_code == 200
        assert "username" in resp.json()
        assert "userId" in resp.json()
        assert "base64EncodedAuthenticationKey" in resp.json()

    # 参数缺失用例：逐个缺少必填字段
    @pytest.mark.parametrize("payload", [
        {"username": "mifos"},  # 缺少 password
        {"password": "password"},  # 缺少 username
        {},  # 缺少所有必填字段
    ])
    def test_authentication_missing_required_fields(self, api, payload):
        resp = api.post(self.BASE_PATH, json=payload)
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：空字符串、极大值、极小值、0、负数等
    @pytest.mark.parametrize("username, password", [
        ("", "password"),  # 空字符串 username
        ("mifos", ""),  # 空字符串 password
        ("a" * 1000, "password"),  # 极大值 username
        ("mifos", "b" * 1000),  # 极大值 password
        ("a", "password"),  # 极小值 username
        ("mifos", "b"),  # 极小值 password
        ("0", "password"),  # 0 作为 username
        ("mifos", "0"),  # 0 作为 password
        ("-1", "password"),  # 负数作为 username
        ("mifos", "-1"),  # 负数作为 password
    ])
    def test_authentication_boundary_values(self, api, username, password):
        payload = {
            "username": username,
            "password": password
        }
        resp = api.post(self.BASE_PATH, json=payload)
        assert resp.status_code in [400, 403, 404, 422]

    # 异常用例：错误类型、非法枚举值、特殊字符等
    @pytest.mark.parametrize("username, password", [
        (123, "password"),  # username 为整数
        ("mifos", 456),  # password 为整数
        (None, "password"),  # username 为 None
        ("mifos", None),  # password 为 None
        (True, "password"),  # username 为布尔值
        ("mifos", False),  # password 为布尔值
        ("<script>alert('xss')</script>", "password"),  # username 含特殊字符
        ("mifos", "<script>alert('xss')</script>"),  # password 含特殊字符
        ("mifos@#$%^&*()", "password"),  # username 含特殊字符
        ("mifos", "password@#$%^&*()"),  # password 含特殊字符
    ])
    def test_authentication_invalid_types_and_values(self, api, username, password):
        payload = {
            "username": username,
            "password": password
        }
        resp = api.post(self.BASE_PATH, json=payload)
        assert resp.status_code in [400, 403, 404, 422, 401, 500]