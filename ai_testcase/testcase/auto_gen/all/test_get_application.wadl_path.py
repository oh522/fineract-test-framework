import pytest


class TestApplicationWadl:
    """测试 /application.wadl/{path} 接口"""

    # 正常用例数据
    normal_cases = [
        ("正常路径", "index.html", 200),
        ("路径包含数字", "page123", 200),
        ("路径包含特殊字符", "user_profile", 200),
        ("路径为单字符", "a", 200),
        ("路径为长字符串", "a" * 100, 200),
    ]

    # 参数缺失用例数据
    missing_cases = [
        ("路径参数为空字符串", "", 404),
        ("路径参数为None", None, 400),
    ]

    # 边界值用例数据
    boundary_cases = [
        ("路径为极小值(1字符)", "x", 200),
        ("路径为极大值(1000字符)", "x" * 1000, 200),
        ("路径为空白字符串", "   ", 200),
        ("路径为特殊字符组合", "!@#$%^&*()", 200),
        ("路径包含Unicode字符", "测试路径", 200),
    ]

    # 异常用例数据
    exception_cases = [
        ("路径为数字类型", 12345, 400),
        ("路径为布尔类型", True, 400),
        ("路径为列表类型", ["path1", "path2"], 400),
        ("路径为字典类型", {"key": "value"}, 400),
        ("路径包含非法字符", "../etc/passwd", 400),
        ("路径过长(超过限制)", "x" * 10000, 400),
    ]

    @pytest.mark.parametrize("desc, path, expected_status", normal_cases)
    def test_normal_cases(self, api, desc, path, expected_status):
        """
        正常用例测试
        测试目的：验证使用正确的路径参数时，接口能正常返回响应
        """
        resp = api.get(f"/application.wadl/{path}")
        assert resp.status_code == expected_status, f"期望状态码 {expected_status}，实际状态码 {resp.status_code}"
        # 验证响应内容为XML格式
        assert "application/xml" in resp.headers.get("Content-Type", ""), "响应Content-Type应为application/xml"
        # 验证响应体不为空
        assert resp.text is not None and len(resp.text) > 0, "响应体不应为空"

    @pytest.mark.parametrize("desc, path, expected_status", missing_cases)
    def test_missing_cases(self, api, desc, path, expected_status):
        """
        参数缺失用例测试
        测试目的：验证缺少必填路径参数时，接口返回适当的错误信息
        """
        if path is None:
            # 当path为None时，不传path参数
            resp = api.get("/application.wadl/")
        else:
            resp = api.get(f"/application.wadl/{path}")
        assert resp.status_code == expected_status, f"期望状态码 {expected_status}，实际状态码 {resp.status_code}"
        # 验证错误响应包含错误信息
        if resp.status_code != 200:
            assert "error" in resp.text.lower() or "message" in resp.text.lower(), "错误响应应包含错误信息"

    @pytest.mark.parametrize("desc, path, expected_status", boundary_cases)
    def test_boundary_cases(self, api, desc, path, expected_status):
        """
        边界值用例测试
        测试目的：验证路径参数在边界值情况下，接口的健壮性
        """
        resp = api.get(f"/application.wadl/{path}")
        assert resp.status_code == expected_status, f"期望状态码 {expected_status}，实际状态码 {resp.status_code}"
        # 验证响应内容类型
        if resp.status_code == 200:
            assert "application/xml" in resp.headers.get("Content-Type", ""), "成功响应Content-Type应为application/xml"
            assert resp.text is not None and len(resp.text) > 0, "成功响应体不应为空"

    @pytest.mark.parametrize("desc, path, expected_status", exception_cases)
    def test_exception_cases(self, api, desc, path, expected_status):
        """
        异常用例测试
        测试目的：验证传入非法或错误类型的路径参数时，接口能正确处理并返回错误
        """
        # 对于非字符串类型参数，尝试转换为字符串或直接传入
        if isinstance(path, (int, bool)):
            resp = api.get(f"/application.wadl/{path}")
        elif isinstance(path, (list, dict)):
            # 对于列表和字典类型，尝试直接传入（可能触发序列化错误）
            try:
                resp = api.get(f"/application.wadl/{path}")
            except (TypeError, ValueError):
                # 如果请求构造失败，验证接口返回400
                pytest.skip("请求构造失败，跳过此用例")
                return
        else:
            resp = api.get(f"/application.wadl/{path}")
        assert resp.status_code == expected_status, f"期望状态码 {expected_status}，实际状态码 {resp.status_code}"
        # 验证错误响应
        if resp.status_code != 200:
            assert "error" in resp.text.lower() or "message" in resp.text.lower(), "错误响应应包含错误信息"
            # 验证错误响应格式
            assert resp.headers.get("Content-Type", "").startswith("application/xml") or \
                   resp.headers.get("Content-Type", "").startswith("text/plain"), "错误响应应为XML或纯文本格式"