import pytest


class TestCreditBureauConfigurationMappings:
    """Credit Bureau Configuration Mappings 接口测试"""

    # 基础路径
    BASE_PATH = "/CreditBureauConfiguration/mappings"

    # ==================== 正常用例 ====================
    @pytest.mark.parametrize(
        "test_data, expected",
        [
            # 正常请求，无参数
            (
                {},
                {"status_code": 200, "response_type": str}
            ),
        ],
        ids=["正常请求-无参数"]
    )
    def test_normal_cases(self, api, test_data, expected):
        """
        测试目的：验证正常请求能正确返回
        测试场景：发送 GET 请求，无参数
        预期结果：状态码 200，响应为字符串类型
        """
        resp = api.get(self.BASE_PATH, params=test_data)
        assert resp.status_code == expected["status_code"], f"状态码错误，期望 {expected['status_code']}，实际 {resp.status_code}"
        response_data = resp.json()
        assert isinstance(response_data, expected["response_type"]), f"响应类型错误，期望 {expected['response_type']}，实际 {type(response_data)}"

    # ==================== 参数缺失用例 ====================
    @pytest.mark.parametrize(
        "test_data, expected",
        [
            # 虽然接口无必填参数，但测试空字典
            (
                {},
                {"status_code": 200, "response_type": str}
            ),
            # 传递 None 作为参数
            (
                None,
                {"status_code": 200, "response_type": str}
            ),
        ],
        ids=["空参数字典", "None参数"]
    )
    def test_missing_params_cases(self, api, test_data, expected):
        """
        测试目的：验证参数缺失时的处理
        测试场景：传递空字典或 None 作为参数
        预期结果：状态码 200，响应为字符串类型
        """
        if test_data is None:
            resp = api.get(self.BASE_PATH)
        else:
            resp = api.get(self.BASE_PATH, params=test_data)
        assert resp.status_code == expected["status_code"], f"状态码错误，期望 {expected['status_code']}，实际 {resp.status_code}"
        response_data = resp.json()
        assert isinstance(response_data, expected["response_type"]), f"响应类型错误，期望 {expected['response_type']}，实际 {type(response_data)}"

    # ==================== 边界值用例 ====================
    @pytest.mark.parametrize(
        "test_data, expected",
        [
            # 空字符串参数
            (
                {"": ""},
                {"status_code": 200, "response_type": str}
            ),
            # 极大值参数（模拟长字符串）
            (
                {"key": "a" * 10000},
                {"status_code": 200, "response_type": str}
            ),
            # 极小值参数（空字符串值）
            (
                {"key": ""},
                {"status_code": 200, "response_type": str}
            ),
            # 特殊字符参数
            (
                {"key": "!@#$%^&*()_+-=[]{}|;':\",./<>?`~"},
                {"status_code": 200, "response_type": str}
            ),
            # Unicode 字符参数
            (
                {"key": "你好世界🌍"},
                {"status_code": 200, "response_type": str}
            ),
        ],
        ids=["空字符串key-value", "极大值参数", "极小值参数", "特殊字符参数", "Unicode参数"]
    )
    def test_boundary_cases(self, api, test_data, expected):
        """
        测试目的：验证边界值参数的处理
        测试场景：传递空字符串、极大值、极小值、特殊字符、Unicode 等边界参数
        预期结果：状态码 200，响应为字符串类型
        """
        resp = api.get(self.BASE_PATH, params=test_data)
        assert resp.status_code == expected["status_code"], f"状态码错误，期望 {expected['status_code']}，实际 {resp.status_code}"
        response_data = resp.json()
        assert isinstance(response_data, expected["response_type"]), f"响应类型错误，期望 {expected['response_type']}，实际 {type(response_data)}"

    # ==================== 异常用例 ====================
    @pytest.mark.parametrize(
        "test_data, expected",
        [
            # 整数类型参数
            (
                {"key": 12345},
                {"status_code": 200, "response_type": str}
            ),
            # 浮点数类型参数
            (
                {"key": 3.14159},
                {"status_code": 200, "response_type": str}
            ),
            # 布尔类型参数
            (
                {"key": True},
                {"status_code": 200, "response_type": str}
            ),
            # 列表类型参数
            (
                {"key": [1, 2, 3]},
                {"status_code": 200, "response_type": str}
            ),
            # 字典类型参数
            (
                {"key": {"nested": "value"}},
                {"status_code": 200, "response_type": str}
            ),
            # 空列表参数
            (
                {"key": []},
                {"status_code": 200, "response_type": str}
            ),
            # 空字典参数
            (
                {"key": {}},
                {"status_code": 200, "response_type": str}
            ),
            # None 值参数
            (
                {"key": None},
                {"status_code": 200, "response_type": str}
            ),
            # 负数参数
            (
                {"key": -100},
                {"status_code": 200, "response_type": str}
            ),
            # 超大整数参数
            (
                {"key": 10**18},
                {"status_code": 200, "response_type": str}
            ),
        ],
        ids=[
            "整数类型参数",
            "浮点数类型参数",
            "布尔类型参数",
            "列表类型参数",
            "字典类型参数",
            "空列表参数",
            "空字典参数",
            "None值参数",
            "负数参数",
            "超大整数参数"
        ]
    )
    def test_exception_cases(self, api, test_data, expected):
        """
        测试目的：验证异常参数的处理
        测试场景：传递错误类型、非法值等异常参数
        预期结果：状态码 200，响应为字符串类型
        """
        resp = api.get(self.BASE_PATH, params=test_data)
        assert resp.status_code == expected["status_code"], f"状态码错误，期望 {expected['status_code']}，实际 {resp.status_code}"
        response_data = resp.json()
        assert isinstance(response_data, expected["response_type"]), f"响应类型错误，期望 {expected['response_type']}，实际 {type(response_data)}"