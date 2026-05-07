import pytest


class TestCreditBureauConfiguration:
    """信贷局配置管理 - 更新配置接口测试"""

    BASE_PATH = "/CreditBureauConfiguration/configuration/{configurationId}"

    # ==================== 正常用例 ====================
    @pytest.mark.parametrize(
        "configuration_id, request_body, expected_status, expected_msg",
        [
            # 正常更新：有效ID + 合法JSON字符串
            (1, '{"name": "test", "enabled": true}', 200, None),
            # 正常更新：ID为边界值1
            (1, '{"name": "min_id"}', 200, None),
            # 正常更新：ID为较大值
            (999999, '{"name": "large_id"}', 200, None),
        ],
        ids=[
            "正常用例-有效ID和合法JSON体",
            "正常用例-最小ID边界",
            "正常用例-较大ID边界",
        ]
    )
    def test_normal_update(self, api, configuration_id, request_body, expected_status, expected_msg):
        """
        正常用例：使用正确的参数更新配置
        预期：状态码200，返回响应体不为空
        """
        url = self.BASE_PATH.format(configurationId=configuration_id)
        resp = api.put(url, data=request_body)
        assert resp.status_code == expected_status, f"状态码异常，期望{expected_status}，实际{resp.status_code}"
        response_data = resp.json()
        assert response_data is not None, "响应体为空"
        # 如果响应有特定字段可进一步断言，此处仅验证返回字符串类型
        assert isinstance(response_data, str), f"响应体类型异常，期望str，实际{type(response_data)}"

    # ==================== 参数缺失用例 ====================
    @pytest.mark.parametrize(
        "configuration_id, request_body, expected_status",
        [
            # 缺少路径参数：ID为None（实际无法构造，但测试框架层面模拟）
            (None, '{"name": "test"}', 404),
            # 请求体为空字符串
            (1, "", 400),
            # 请求体为None（不传body）
            (1, None, 400),
        ],
        ids=[
            "参数缺失-路径参数ID为None",
            "参数缺失-请求体为空字符串",
            "参数缺失-请求体为None",
        ]
    )
    def test_missing_parameters(self, api, configuration_id, request_body, expected_status):
        """
        参数缺失用例：缺少必填参数
        预期：状态码4xx
        """
        if configuration_id is None:
            # 模拟路径参数缺失，使用不存在的ID或空路径
            url = self.BASE_PATH.format(configurationId="")
        else:
            url = self.BASE_PATH.format(configurationId=configuration_id)
        resp = api.put(url, data=request_body)
        assert resp.status_code == expected_status, f"状态码异常，期望{expected_status}，实际{resp.status_code}"

    # ==================== 边界值用例 ====================
    @pytest.mark.parametrize(
        "configuration_id, request_body, expected_status",
        [
            # ID为0（极小值）
            (0, '{"name": "zero_id"}', 400),
            # ID为负数
            (-1, '{"name": "negative_id"}', 400),
            # ID为极大值（超过int64范围）
            (9223372036854775808, '{"name": "overflow_id"}', 400),
            # 请求体为超长字符串（10MB）
            (1, "x" * 10 * 1024 * 1024, 413),
            # 请求体为特殊字符
            (1, '{"name": "\u0000\u0001\u0002"}', 400),
        ],
        ids=[
            "边界值-ID为0",
            "边界值-ID为负数",
            "边界值-ID超过int64范围",
            "边界值-请求体超长",
            "边界值-请求体含特殊字符",
        ]
    )
    def test_boundary_values(self, api, configuration_id, request_body, expected_status):
        """
        边界值用例：测试参数边界情况
        预期：状态码4xx或413
        """
        url = self.BASE_PATH.format(configurationId=configuration_id)
        resp = api.put(url, data=request_body)
        assert resp.status_code == expected_status, f"状态码异常，期望{expected_status}，实际{resp.status_code}"

    # ==================== 异常用例 ====================
    @pytest.mark.parametrize(
        "configuration_id, request_body, expected_status",
        [
            # ID为字符串类型
            ("abc", '{"name": "test"}', 400),
            # ID为浮点数
            (1.5, '{"name": "test"}', 400),
            # 请求体不是合法JSON
            (1, "not a json string", 400),
            # 请求体为数字
            (1, 12345, 400),
            # 请求体为布尔值
            (1, True, 400),
            # 请求体为列表
            (1, [1, 2, 3], 400),
        ],
        ids=[
            "异常用例-ID为字符串",
            "异常用例-ID为浮点数",
            "异常用例-请求体非JSON格式",
            "异常用例-请求体为数字",
            "异常用例-请求体为布尔值",
            "异常用例-请求体为列表",
        ]
    )
    def test_invalid_inputs(self, api, configuration_id, request_body, expected_status):
        """
        异常用例：传入错误类型或非法值
        预期：状态码4xx
        """
        url = self.BASE_PATH.format(configurationId=configuration_id)
        resp = api.put(url, data=request_body)
        assert resp.status_code == expected_status, f"状态码异常，期望{expected_status}，实际{resp.status_code}"