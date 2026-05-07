import pytest


class TestGetClientByExternalId:
    """测试通过外部ID获取客户信息接口"""

    # 基础URL路径
    BASE_PATH = "/clients/external-id/{externalId}"

    # ==================== 正常用例 ====================

    @pytest.mark.parametrize("external_id, staff_only", [
        ("EXT-12345", False),
        ("EXT-67890", True),
        ("ext_abc_xyz", False),
        ("1234567890", True),
    ], ids=["正常外部ID-不限制员工", "正常外部ID-限制员工", "带下划线外部ID", "纯数字外部ID"])
    def test_get_client_by_external_id_success(self, api, external_id, staff_only):
        """
        测试正常获取客户信息
        验证：状态码200，响应包含客户ID等必要字段
        """
        path = self.BASE_PATH.format(externalId=external_id)
        params = {"staffInSelectedOfficeOnly": staff_only} if staff_only else {}
        resp = api.get(path, params=params)

        assert resp.status_code == 200, f"期望状态码200，实际{resp.status_code}"
        resp_data = resp.json()
        assert "clientId" in resp_data, "响应缺少clientId字段"
        assert resp_data["clientId"] is not None, "clientId不应为null"
        assert "externalId" in resp_data, "响应缺少externalId字段"
        assert resp_data["externalId"] == external_id, f"externalId不匹配，期望{external_id}，实际{resp_data.get('externalId')}"

    # ==================== 参数缺失用例 ====================

    @pytest.mark.parametrize("external_id", [
        None,
        "",
    ], ids=["externalId为None", "externalId为空字符串"])
    def test_get_client_by_external_id_missing_param(self, api, external_id):
        """
        测试缺少必填参数externalId
        验证：状态码400或404，返回错误信息
        """
        if external_id is None:
            path = self.BASE_PATH.format(externalId="")
        else:
            path = self.BASE_PATH.format(externalId=external_id)

        resp = api.get(path)

        assert resp.status_code in [400, 404], f"期望状态码400或404，实际{resp.status_code}"
        resp_data = resp.json()
        assert "error" in resp_data or "message" in resp_data, "响应应包含错误信息"

    # ==================== 边界值用例 ====================

    @pytest.mark.parametrize("external_id, expected_status", [
        ("a" * 255, 200),  # 最大长度字符串
        ("a" * 256, 400),  # 超长字符串
        ("a" * 1, 200),    # 最小长度字符串
        ("a" * 0, 400),    # 空字符串（边界）
        ("a" * 1000, 400), # 极大长度
    ], ids=["255字符边界", "256字符超长", "1字符最小", "0字符空", "1000字符极大"])
    def test_get_client_by_external_id_boundary(self, api, external_id, expected_status):
        """
        测试externalId边界值
        验证：不同长度字符串的响应状态码
        """
        path = self.BASE_PATH.format(externalId=external_id)
        resp = api.get(path)

        assert resp.status_code == expected_status, f"期望状态码{expected_status}，实际{resp.status_code}"

    # ==================== 异常用例 ====================

    @pytest.mark.parametrize("external_id, staff_only, expected_status, expected_error", [
        ("EXT-12345", "not_boolean", 400, "invalid"),  # 布尔参数传字符串
        ("EXT-12345", 123, 400, "invalid"),            # 布尔参数传数字
        ("EXT-12345", None, 200, None),                # 布尔参数为None（应视为不传）
        ("<script>alert(1)</script>", False, 404, "not found"),  # XSS注入
        ("../../../etc/passwd", False, 404, "not found"),        # 路径遍历
        ("EXT-12345@#$%^&*()", False, 404, "not found"),        # 特殊字符
    ], ids=["布尔参数传字符串", "布尔参数传数字", "布尔参数为None", "XSS注入", "路径遍历", "特殊字符"])
    def test_get_client_by_external_id_abnormal(self, api, external_id, staff_only, expected_status, expected_error):
        """
        测试异常参数情况
        验证：错误参数导致的状态码和错误信息
        """
        path = self.BASE_PATH.format(externalId=external_id)
        params = {}
        if staff_only is not None:
            params["staffInSelectedOfficeOnly"] = staff_only

        resp = api.get(path, params=params)

        assert resp.status_code == expected_status, f"期望状态码{expected_status}，实际{resp.status_code}"
        if expected_error:
            resp_data = resp.json()
            error_msg = resp_data.get("error", resp_data.get("message", "")).lower()
            assert expected_error in error_msg, f"错误信息应包含'{expected_error}'，实际'{error_msg}'"

    # ==================== 额外异常用例 ====================

    @pytest.mark.parametrize("external_id", [
        " " * 10,           # 纯空格
        "\t\n\r",           # 空白字符
        "null",             # 字符串"null"
        "undefined",        # 字符串"undefined"
        "None",             # 字符串"None"
    ], ids=["纯空格", "空白字符", "字符串null", "字符串undefined", "字符串None"])
    def test_get_client_by_external_id_special_strings(self, api, external_id):
        """
        测试特殊字符串作为externalId
        验证：返回404或400，不返回200
        """
        path = self.BASE_PATH.format(externalId=external_id)
        resp = api.get(path)

        assert resp.status_code in [400, 404], f"期望状态码400或404，实际{resp.status_code}"
        resp_data = resp.json()
        assert "error" in resp_data or "message" in resp_data, "响应应包含错误信息"