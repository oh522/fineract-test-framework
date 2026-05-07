import pytest


class TestCreditBureauConfiguration:
    """
    信用局配置查询接口测试
    接口路径: GET /v1/CreditBureauConfiguration/config/{organisationCreditBureauId}
    """

    # ==================== 正常用例 ====================
    @pytest.mark.parametrize("organisation_credit_bureau_id", [
        1,          # 最小有效正整数
        100,        # 普通有效值
        999999,     # 较大有效值
    ])
    def test_normal_valid_id(self, api, organisation_credit_bureau_id):
        """
        正常用例: 使用有效的 organisationCreditBureauId 查询配置
        预期: 返回200，响应为字符串
        """
        resp = api.get(f"/CreditBureauConfiguration/config/{organisation_credit_bureau_id}")
        assert resp.status_code == 200, f"期望状态码200，实际{resp.status_code}"
        response_data = resp.json()
        assert isinstance(response_data, str), f"期望响应为字符串，实际类型{type(response_data)}"
        assert len(response_data) > 0, "响应字符串不应为空"

    # ==================== 参数缺失用例 ====================
    @pytest.mark.parametrize("organisation_credit_bureau_id", [
        None,       # 参数为None
        "",         # 空字符串
        "   ",      # 空白字符串
    ])
    def test_missing_or_empty_id(self, api, organisation_credit_bureau_id):
        """
        参数缺失用例: organisationCreditBureauId 缺失或为空
        预期: 返回400或404，提示参数错误
        """
        if organisation_credit_bureau_id is None:
            # 模拟不传参数的情况，直接请求路径末尾不带参数
            resp = api.get("/CreditBureauConfiguration/config/")
        else:
            resp = api.get(f"/CreditBureauConfiguration/config/{organisation_credit_bureau_id}")
        assert resp.status_code in [400, 404], f"期望状态码400或404，实际{resp.status_code}"
        error_data = resp.json()
        assert "error" in error_data or "message" in error_data, "响应应包含错误信息"

    # ==================== 边界值用例 ====================
    @pytest.mark.parametrize("organisation_credit_bureau_id, expected_status", [
        (0, 400),               # 极小值0，通常无效
        (-1, 400),              # 负值，无效
        (9223372036854775807, 200),  # 极大值（int64最大值），可能有效
        (-9223372036854775808, 400), # 极小负值（int64最小值），无效
    ])
    def test_boundary_values(self, api, organisation_credit_bureau_id, expected_status):
        """
        边界值用例: 测试边界值（极大、极小、0、负数）
        预期: 根据业务逻辑返回对应状态码
        """
        resp = api.get(f"/CreditBureauConfiguration/config/{organisation_credit_bureau_id}")
        assert resp.status_code == expected_status, f"期望状态码{expected_status}，实际{resp.status_code}"
        if expected_status == 200:
            response_data = resp.json()
            assert isinstance(response_data, str), "响应应为字符串"
        else:
            error_data = resp.json()
            assert "error" in error_data or "message" in error_data, "响应应包含错误信息"

    # ==================== 异常用例 ====================
    @pytest.mark.parametrize("organisation_credit_bureau_id, expected_status", [
        ("abc", 400),               # 字符串类型，非整数
        (1.5, 400),                 # 浮点数类型
        (True, 400),                # 布尔类型
        ([1, 2, 3], 400),           # 列表类型
        ({"key": "value"}, 400),    # 字典类型
    ])
    def test_invalid_types(self, api, organisation_credit_bureau_id, expected_status):
        """
        异常用例: 传入错误类型的 organisationCreditBureauId
        预期: 返回400，提示参数类型错误
        """
        resp = api.get(f"/CreditBureauConfiguration/config/{organisation_credit_bureau_id}")
        assert resp.status_code == expected_status, f"期望状态码{expected_status}，实际{resp.status_code}"
        error_data = resp.json()
        assert "error" in error_data or "message" in error_data, "响应应包含错误信息"

    # ==================== 额外异常用例：非法值 ====================
    @pytest.mark.parametrize("organisation_credit_bureau_id, expected_status", [
        (999999999999999999999999999999, 400),  # 超出int64范围的超大整数
        (-999999999999999999999999999999, 400), # 超出int64范围的超小负整数
    ])
    def test_out_of_range_values(self, api, organisation_credit_bureau_id, expected_status):
        """
        异常用例: 传入超出int64范围的 organisationCreditBureauId
        预期: 返回400，提示参数超出范围
        """
        resp = api.get(f"/CreditBureauConfiguration/config/{organisation_credit_bureau_id}")
        assert resp.status_code == expected_status, f"期望状态码{expected_status}，实际{resp.status_code}"
        error_data = resp.json()
        assert "error" in error_data or "message" in error_data, "响应应包含错误信息"