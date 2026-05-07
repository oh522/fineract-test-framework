import pytest


class TestCreditBureauConfigurationLoanProduct:
    """信贷局配置-贷款产品查询接口测试"""

    # 正常用例
    @pytest.mark.parametrize("params, expected_status, expected_msg", [
        # 无参数请求，期望成功返回字符串
        ({}, 200, None),
        # 带空字典参数，期望成功
        ({"dummy": ""}, 200, None),
    ])
    def test_normal_loan_product(self, api, params, expected_status, expected_msg):
        """正常用例：正确参数，期望成功返回字符串"""
        resp = api.get("/CreditBureauConfiguration/loanProduct", params=params)
        assert resp.status_code == expected_status
        # 响应类型为字符串，验证返回内容非空
        assert isinstance(resp.text, str)
        assert len(resp.text) > 0

    # 参数缺失用例（接口无必填参数，但测试空参数场景）
    @pytest.mark.parametrize("params, expected_status", [
        # 无参数（默认空）
        (None, 200),
        # 参数为None
        (None, 200),
    ])
    def test_missing_params_loan_product(self, api, params, expected_status):
        """参数缺失用例：无参数或None，期望仍能正常返回"""
        resp = api.get("/CreditBureauConfiguration/loanProduct", params=params)
        assert resp.status_code == expected_status
        assert isinstance(resp.text, str)

    # 边界值用例
    @pytest.mark.parametrize("params, expected_status", [
        # 空字符串参数
        ({"key": ""}, 200),
        # 极大值参数（长字符串）
        ({"key": "a" * 10000}, 200),
        # 极小值参数（单个字符）
        ({"key": "a"}, 200),
        # 特殊字符参数
        ({"key": "!@#$%^&*()_+"}, 200),
        # 数字参数
        ({"key": 12345678901234567890}, 200),
        # 布尔参数
        ({"key": True}, 200),
        # 列表参数
        ({"key": [1, 2, 3]}, 200),
        # 字典参数
        ({"key": {"nested": "value"}}, 200),
    ])
    def test_boundary_loan_product(self, api, params, expected_status):
        """边界值用例：各种极端参数值，期望正常返回"""
        resp = api.get("/CreditBureauConfiguration/loanProduct", params=params)
        assert resp.status_code == expected_status
        assert isinstance(resp.text, str)

    # 异常用例
    @pytest.mark.parametrize("params, expected_status", [
        # 非法参数类型（二进制）
        ({"key": b"binary"}, 200),
        # 超大参数（超过URL长度限制，但GET请求可能截断）
        ({"key": "a" * 100000}, 200),
        # 多层嵌套参数
        ({"key": {"level1": {"level2": {"level3": "deep"}}}}, 200),
        # 空列表参数
        ({"key": []}, 200),
        # 空字典参数
        ({"key": {}}, 200),
        # 负数参数
        ({"key": -1}, 200),
        # 浮点数参数
        ({"key": 3.141592653589793}, 200),
        # 特殊Unicode字符
        ({"key": "\u0000\u001f\u007f"}, 200),
        # 超长键名
        ({"a" * 1000: "value"}, 200),
        # 多个参数
        ({"key1": "value1", "key2": "value2", "key3": "value3"}, 200),
    ])
    def test_exception_loan_product(self, api, params, expected_status):
        """异常用例：非法参数值，期望服务端能正确处理"""
        resp = api.get("/CreditBureauConfiguration/loanProduct", params=params)
        assert resp.status_code == expected_status
        # 验证响应为字符串类型
        assert isinstance(resp.text, str)
        # 验证响应内容不为空
        assert len(resp.text) > 0

    # 额外：验证响应格式
    def test_response_format_loan_product(self, api):
        """验证响应格式：确保返回的是字符串"""
        resp = api.get("/CreditBureauConfiguration/loanProduct")
        assert resp.status_code == 200
        # 根据schema定义，响应类型为string
        assert isinstance(resp.text, str)
        # 验证响应头Content-Type
        assert "application/json" in resp.headers.get("Content-Type", "")

    # 额外：并发请求测试
    @pytest.mark.parametrize("num_requests", [1, 5, 10])
    def test_concurrent_loan_product(self, api, num_requests):
        """并发请求测试：多次调用接口，验证稳定性"""
        for _ in range(num_requests):
            resp = api.get("/CreditBureauConfiguration/loanProduct")
            assert resp.status_code == 200
            assert isinstance(resp.text, str)
            assert len(resp.text) > 0