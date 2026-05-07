import pytest


class TestCreditBureauConfigurationMappings:
    """征信机构配置映射接口测试"""

    BASE_PATH = "/CreditBureauConfiguration/mappings"

    @pytest.mark.parametrize(
        "organisation_credit_bureau_id, request_body, expected_status, expected_desc",
        [
            # 正常用例1：使用有效ID和合法JSON字符串
            (1001, '{"key": "value"}', 200, "正常请求-有效ID和合法JSON"),
            # 正常用例2：使用最小有效ID和空JSON对象
            (1, '{}', 200, "正常请求-最小有效ID和空JSON"),
            # 正常用例3：使用较大ID和复杂JSON结构
            (999999, '{"name": "test", "enabled": true, "count": 100}', 200, "正常请求-较大ID和复杂JSON"),
        ],
        ids=["valid_id_and_json", "min_id_and_empty_json", "large_id_and_complex_json"]
    )
    def test_normal_cases(self, api, organisation_credit_bureau_id, request_body, expected_status, expected_desc):
        """正常用例：正确参数，期望成功"""
        path = f"{self.BASE_PATH}/{organisation_credit_bureau_id}"
        resp = api.post(path, json=request_body)
        assert resp.status_code == expected_status, f"{expected_desc} - 状态码不符合预期"
        response_data = resp.json()
        assert response_data is not None, f"{expected_desc} - 响应数据不应为空"
        assert isinstance(response_data, str), f"{expected_desc} - 响应应为字符串类型"

    @pytest.mark.parametrize(
        "organisation_credit_bureau_id, request_body, expected_status, expected_desc",
        [
            # 参数缺失用例1：ID为None
            (None, '{"key": "value"}', 400, "缺失必填路径参数-ID为None"),
            # 参数缺失用例2：ID为空字符串（路径参数不允许空字符串）
            ("", '{"key": "value"}', 400, "缺失必填路径参数-ID为空字符串"),
            # 参数缺失用例3：请求体为空
            (1001, None, 400, "缺失必填请求体-请求体为None"),
            # 参数缺失用例4：请求体为空字符串
            (1001, "", 400, "缺失必填请求体-请求体为空字符串"),
        ],
        ids=["missing_id_none", "missing_id_empty", "missing_body_none", "missing_body_empty"]
    )
    def test_missing_parameter_cases(self, api, organisation_credit_bureau_id, request_body, expected_status, expected_desc):
        """参数缺失用例：缺少必填字段"""
        path = f"{self.BASE_PATH}/{organisation_credit_bureau_id}" if organisation_credit_bureau_id is not None else self.BASE_PATH
        resp = api.post(path, json=request_body)
        assert resp.status_code == expected_status, f"{expected_desc} - 状态码不符合预期"

    @pytest.mark.parametrize(
        "organisation_credit_bureau_id, request_body, expected_status, expected_desc",
        [
            # 边界值用例1：ID为0（极小值）
            (0, '{"key": "value"}', 400, "边界值-ID为0"),
            # 边界值用例2：ID为负数
            (-1, '{"key": "value"}', 400, "边界值-ID为负数"),
            # 边界值用例3：ID为极大值（超过int64范围）
            (9223372036854775808, '{"key": "value"}', 400, "边界值-ID超过int64最大值"),
            # 边界值用例4：ID为极小负值（超过int64范围）
            (-9223372036854775809, '{"key": "value"}', 400, "边界值-ID小于int64最小值"),
            # 边界值用例5：请求体为超长字符串
            (1001, '{"data": "' + "a" * 10000 + '"}', 400, "边界值-请求体超长字符串"),
            # 边界值用例6：请求体为特殊字符
            (1001, '{"special": "!@#$%^&*()_+{}|:<>?"}', 200, "边界值-请求体含特殊字符"),
        ],
        ids=["id_zero", "id_negative", "id_exceed_max", "id_below_min", "body_too_long", "body_special_chars"]
    )
    def test_boundary_value_cases(self, api, organisation_credit_bureau_id, request_body, expected_status, expected_desc):
        """边界值用例：极大值、极小值、空字符串等"""
        path = f"{self.BASE_PATH}/{organisation_credit_bureau_id}"
        resp = api.post(path, json=request_body)
        assert resp.status_code == expected_status, f"{expected_desc} - 状态码不符合预期"

    @pytest.mark.parametrize(
        "organisation_credit_bureau_id, request_body, expected_status, expected_desc",
        [
            # 异常用例1：ID为字符串类型
            ("abc", '{"key": "value"}', 400, "异常-ID为字符串类型"),
            # 异常用例2：ID为浮点数
            (1.5, '{"key": "value"}', 400, "异常-ID为浮点数"),
            # 异常用例3：ID为布尔值
            (True, '{"key": "value"}', 400, "异常-ID为布尔值"),
            # 异常用例4：ID为列表
            ([1, 2, 3], '{"key": "value"}', 400, "异常-ID为列表"),
            # 异常用例5：ID为字典
            ({"id": 1001}, '{"key": "value"}', 400, "异常-ID为字典"),
            # 异常用例6：请求体为数字（非字符串）
            (1001, 12345, 400, "异常-请求体为数字"),
            # 异常用例7：请求体为列表
            (1001, [1, 2, 3], 400, "异常-请求体为列表"),
            # 异常用例8：请求体为布尔值
            (1001, True, 400, "异常-请求体为布尔值"),
            # 异常用例9：请求体为无效JSON格式
            (1001, "not a json", 400, "异常-请求体为无效JSON格式"),
            # 异常用例10：请求体为None（显式传递）
            (1001, None, 400, "异常-请求体为None"),
        ],
        ids=["id_string", "id_float", "id_boolean", "id_list", "id_dict",
             "body_number", "body_list", "body_boolean", "body_invalid_json", "body_none"]
    )
    def test_exception_cases(self, api, organisation_credit_bureau_id, request_body, expected_status, expected_desc):
        """异常用例：错误类型、非法值"""
        path = f"{self.BASE_PATH}/{organisation_credit_bureau_id}"
        resp = api.post(path, json=request_body)
        assert resp.status_code == expected_status, f"{expected_desc} - 状态码不符合预期"
        # 对于异常情况，验证响应中包含错误信息
        if resp.status_code >= 400:
            response_data = resp.json()
            assert "error" in response_data or "message" in response_data, \
                f"{expected_desc} - 错误响应应包含error或message字段"