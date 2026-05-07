import pytest


class TestCreditBureauConfiguration:
    """信贷局配置-贷款产品查询接口测试"""

    BASE_PATH = "/CreditBureauConfiguration/loanProduct"

    def get_loan_product(self, loan_product_id):
        """封装GET请求"""
        url = f"{self.BASE_PATH}/{loan_product_id}"
        return api.get(url)

    # ==================== 正常用例 ====================
    @pytest.mark.parametrize(
        "loan_product_id, expected_status, description",
        [
            (1, 200, "正常-最小有效正整数值1"),
            (100, 200, "正常-常规正整数100"),
            (999999, 200, "正常-较大正整数999999"),
            (2147483647, 200, "正常-接近int32最大值"),
        ],
        ids=[
            "正常用例-最小有效值",
            "正常用例-常规值",
            "正常用例-较大值",
            "正常用例-int32边界值",
        ]
    )
    def test_normal_cases(self, api, loan_product_id, expected_status, description):
        """正常参数请求，期望返回200"""
        resp = self.get_loan_product(loan_product_id)
        assert resp.status_code == expected_status, f"状态码异常: {resp.status_code}, 描述: {description}"
        response_data = resp.json()
        assert response_data is not None, "响应数据为空"
        assert isinstance(response_data, str), f"响应类型异常，期望str，实际{type(response_data)}"

    # ==================== 参数缺失用例 ====================
    @pytest.mark.parametrize(
        "loan_product_id, expected_status, description",
        [
            (None, 404, "缺失-路径参数为None"),
            ("", 404, "缺失-路径参数为空字符串"),
            ("   ", 404, "缺失-路径参数为空白字符串"),
        ],
        ids=[
            "参数缺失-None值",
            "参数缺失-空字符串",
            "参数缺失-空白字符串",
        ]
    )
    def test_missing_parameter_cases(self, api, loan_product_id, expected_status, description):
        """缺少必填路径参数，期望返回404"""
        if loan_product_id is None:
            url = f"{self.BASE_PATH}/"
        else:
            url = f"{self.BASE_PATH}/{loan_product_id}"
        resp = api.get(url)
        assert resp.status_code == expected_status, f"状态码异常: {resp.status_code}, 描述: {description}"

    # ==================== 边界值用例 ====================
    @pytest.mark.parametrize(
        "loan_product_id, expected_status, description",
        [
            (0, 200, "边界-极小值0"),
            (-1, 200, "边界-负整数-1"),
            (-2147483648, 200, "边界-int32最小值"),
            (9223372036854775807, 200, "边界-int64最大值"),
            (-9223372036854775808, 200, "边界-int64最小值"),
        ],
        ids=[
            "边界值-0",
            "边界值-负整数",
            "边界值-int32最小值",
            "边界值-int64最大值",
            "边界值-int64最小值",
        ]
    )
    def test_boundary_cases(self, api, loan_product_id, expected_status, description):
        """边界值测试，包括0、负数、int32/int64边界"""
        resp = self.get_loan_product(loan_product_id)
        assert resp.status_code == expected_status, f"状态码异常: {resp.status_code}, 描述: {description}"
        response_data = resp.json()
        assert response_data is not None, "响应数据为空"

    # ==================== 异常用例 ====================
    @pytest.mark.parametrize(
        "loan_product_id, expected_status, description",
        [
            ("abc", 400, "异常-字符串类型"),
            ("12.34", 400, "异常-浮点数字符串"),
            ("0x1F", 400, "异常-十六进制字符串"),
            ("true", 400, "异常-布尔字符串"),
            ("null", 400, "异常-null字符串"),
            (" ", 400, "异常-空格字符串"),
            ("-", 400, "异常-负号字符串"),
            ("+", 400, "异常-正号字符串"),
            ("1e5", 400, "异常-科学计数法字符串"),
            ("一二三", 400, "异常-中文字符串"),
            ("<script>", 400, "异常-HTML标签字符串"),
            ("1; DROP TABLE", 400, "异常-SQL注入字符串"),
        ],
        ids=[
            "异常-字母字符串",
            "异常-浮点数字符串",
            "异常-十六进制字符串",
            "异常-布尔字符串",
            "异常-null字符串",
            "异常-空格字符串",
            "异常-负号字符串",
            "异常-正号字符串",
            "异常-科学计数法字符串",
            "异常-中文字符串",
            "异常-HTML标签字符串",
            "异常-SQL注入字符串",
        ]
    )
    def test_exception_cases(self, api, loan_product_id, expected_status, description):
        """异常参数类型，期望返回400"""
        resp = self.get_loan_product(loan_product_id)
        assert resp.status_code == expected_status, f"状态码异常: {resp.status_code}, 描述: {description}"
        response_data = resp.json()
        assert response_data is not None, "响应数据为空"

    # ==================== 特殊异常场景 ====================
    @pytest.mark.parametrize(
        "loan_product_id, expected_status, description",
        [
            (999999999999999999999999999999, 400, "异常-超大整数超出int64范围"),
            (-999999999999999999999999999999, 400, "异常-超小负整数超出int64范围"),
            (1.5, 400, "异常-浮点数类型"),
            (True, 400, "异常-布尔类型True"),
            (False, 400, "异常-布尔类型False"),
        ],
        ids=[
            "异常-超大整数",
            "异常-超小负整数",
            "异常-浮点数类型",
            "异常-布尔类型True",
            "异常-布尔类型False",
        ]
    )
    def test_special_exception_cases(self, api, loan_product_id, expected_status, description):
        """特殊异常场景：超出范围数值、错误数据类型"""
        resp = self.get_loan_product(loan_product_id)
        assert resp.status_code == expected_status, f"状态码异常: {resp.status_code}, 描述: {description}"
        response_data = resp.json()
        assert response_data is not None, "响应数据为空"