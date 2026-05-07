import pytest


class TestCreditBureauConfiguration:
    """征信机构配置接口测试类"""

    # 基础路径模板
    BASE_PATH = "/CreditBureauConfiguration/configuration/{credit_bureau_id}"

    def _send_request(self, credit_bureau_id, request_body=None):
        """发送请求的辅助方法"""
        path = self.BASE_PATH.format(credit_bureau_id=credit_bureau_id)
        return api.post(path, json=request_body)

    # ==================== 正常用例 ====================
    @pytest.mark.parametrize(
        "credit_bureau_id, request_body, description",
        [
            (1, {"name": "test_config"}, "正常整数ID，有效JSON字符串"),
            (100, {"enabled": True, "timeout": 30}, "正常整数ID，复杂JSON对象"),
            (999999, "simple_string", "正常整数ID，纯字符串请求体"),
        ],
        ids=["normal_int_id", "normal_complex_json", "normal_string_body"]
    )
    def test_normal_cases(self, api, credit_bureau_id, request_body, description):
        """正常用例：正确参数，期望成功"""
        resp = self._send_request(credit_bureau_id, request_body)
        assert resp.status_code == 200, f"预期状态码200，实际{resp.status_code}，场景：{description}"
        response_data = resp.json()
        assert response_data is not None, f"响应体不应为空，场景：{description}"
        # 根据实际业务逻辑调整断言
        assert isinstance(response_data, str), f"响应应为字符串类型，场景：{description}"

    # ==================== 参数缺失用例 ====================
    @pytest.mark.parametrize(
        "credit_bureau_id, request_body, description",
        [
            (None, {"name": "test"}, "缺少必填路径参数creditBureauId"),
            ("", {"name": "test"}, "路径参数为空字符串"),
            (1, None, "请求体为None"),
            (1, "", "请求体为空字符串"),
        ],
        ids=["missing_path_param", "empty_path_param", "none_body", "empty_string_body"]
    )
    def test_missing_params_cases(self, api, credit_bureau_id, request_body, description):
        """参数缺失用例：缺少必填字段"""
        if credit_bureau_id is None:
            # 模拟缺少路径参数的情况，直接使用不完整的路径
            path = "/v1/CreditBureauConfiguration/configuration/"
            resp = api.post(path, json=request_body)
        else:
            resp = self._send_request(credit_bureau_id, request_body)
        # 预期返回400或404，根据实际API设计调整
        assert resp.status_code in [400, 404], f"预期状态码400或404，实际{resp.status_code}，场景：{description}"
        response_data = resp.json()
        assert response_data is not None, f"响应体不应为空，场景：{description}"

    # ==================== 边界值用例 ====================
    @pytest.mark.parametrize(
        "credit_bureau_id, request_body, description",
        [
            (0, {"name": "test"}, "极小值：ID为0"),
            (1, {"name": "a" * 10000}, "极大值：请求体字符串长度10000"),
            (9223372036854775807, {"name": "test"}, "极大值：ID为int64最大值"),
            (-9223372036854775808, {"name": "test"}, "极小值：ID为int64最小值"),
            (1, {"name": ""}, "空字符串字段值"),
            (1, {}, "空JSON对象"),
        ],
        ids=["min_id_zero", "max_body_length", "max_int64_id", "min_int64_id", "empty_field_value", "empty_json_object"]
    )
    def test_boundary_cases(self, api, credit_bureau_id, request_body, description):
        """边界值用例：极大值、极小值、空字符串等"""
        resp = self._send_request(credit_bureau_id, request_body)
        # 边界值可能成功也可能失败，根据实际API设计调整断言
        if description in ["max_body_length", "empty_field_value", "empty_json_object"]:
            # 这些情况可能成功
            assert resp.status_code in [200, 400], f"预期状态码200或400，实际{resp.status_code}，场景：{description}"
        else:
            # ID边界值可能成功或失败
            assert resp.status_code in [200, 400, 404], f"预期状态码200/400/404，实际{resp.status_code}，场景：{description}"
        response_data = resp.json()
        assert response_data is not None, f"响应体不应为空，场景：{description}"

    # ==================== 异常用例 ====================
    @pytest.mark.parametrize(
        "credit_bureau_id, request_body, description",
        [
            (-1, {"name": "test"}, "负数ID"),
            (1.5, {"name": "test"}, "浮点数ID（非整数）"),
            ("abc", {"name": "test"}, "字符串ID（非数字）"),
            (1, 12345, "请求体为整数（非字符串/对象）"),
            (1, [1, 2, 3], "请求体为数组"),
            (1, True, "请求体为布尔值"),
            (1, None, "请求体为null"),
        ],
        ids=["negative_id", "float_id", "string_id", "int_body", "array_body", "bool_body", "null_body"]
    )
    def test_exception_cases(self, api, credit_bureau_id, request_body, description):
        """异常用例：错误类型、非法值"""
        resp = self._send_request(credit_bureau_id, request_body)
        # 异常情况预期返回4xx错误
        assert resp.status_code in [400, 404, 415, 422], f"预期状态码4xx，实际{resp.status_code}，场景：{description}"
        response_data = resp.json()
        assert response_data is not None, f"响应体不应为空，场景：{description}"
        # 验证错误响应中包含错误信息
        if isinstance(response_data, dict):
            assert "error" in response_data or "message" in response_data or "code" in response_data, \
                f"错误响应应包含错误信息字段，场景：{description}"