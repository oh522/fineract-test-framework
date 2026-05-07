import pytest


class TestApplicationWadl:
    """测试 /application.wadl 接口"""

    # ==================== 正常用例 ====================
    @pytest.mark.parametrize("desc", [
        "正常请求，期望返回200和默认响应结构",
    ])
    def test_normal_request(self, api, desc):
        """正常用例：正确参数，期望成功"""
        resp = api.get("/application.wadl")
        assert resp.status_code == 200, f"状态码应为200，实际为{resp.status_code}"
        json_data = resp.json()
        # 验证响应包含 default 字段
        assert "default" in json_data, "响应应包含 default 字段"
        default = json_data["default"]
        # 验证 content 字段存在
        assert "content" in default, "default 应包含 content 字段"
        content = default["content"]
        # 验证支持的媒体类型
        assert "application/vnd.sun.wadl+xml" in content, "应支持 application/vnd.sun.wadl+xml"
        assert "application/xml" in content, "应支持 application/xml"
        # 验证 description 字段
        assert "description" in default, "default 应包含 description 字段"
        assert default["description"] == "default response", f"description 应为 'default response'，实际为 {default['description']}"

    # ==================== 参数缺失用例 ====================
    @pytest.mark.parametrize("params, desc", [
        ({}, "无参数请求，期望成功（接口无必填参数）"),
        ({"unexpected_param": "value"}, "携带未定义参数，期望忽略并成功"),
    ])
    def test_missing_or_extra_params(self, api, params, desc):
        """参数缺失/额外参数用例：接口无必填参数，应正常处理"""
        resp = api.get("/application.wadl", params=params)
        assert resp.status_code == 200, f"状态码应为200，实际为{resp.status_code}"
        json_data = resp.json()
        assert "default" in json_data, "响应应包含 default 字段"
        default = json_data["default"]
        assert "content" in default, "default 应包含 content 字段"
        content = default["content"]
        assert "application/vnd.sun.wadl+xml" in content, "应支持 application/vnd.sun.wadl+xml"
        assert "application/xml" in content, "应支持 application/xml"
        assert default["description"] == "default response", f"description 应为 'default response'，实际为 {default['description']}"

    # ==================== 边界值用例 ====================
    @pytest.mark.parametrize("params, desc", [
        ({"large_param": "x" * 10000}, "超大参数值（10000字符），期望正常处理"),
        ({"small_param": ""}, "空字符串参数值，期望正常处理"),
        ({"param1": "a", "param2": "b", "param3": "c", "param4": "d", "param5": "e"}, "多个参数（5个），期望正常处理"),
    ])
    def test_boundary_params(self, api, params, desc):
        """边界值用例：极大值、极小值、空字符串等"""
        resp = api.get("/application.wadl", params=params)
        assert resp.status_code == 200, f"状态码应为200，实际为{resp.status_code}"
        json_data = resp.json()
        assert "default" in json_data, "响应应包含 default 字段"
        default = json_data["default"]
        assert "content" in default, "default 应包含 content 字段"
        content = default["content"]
        assert "application/vnd.sun.wadl+xml" in content, "应支持 application/vnd.sun.wadl+xml"
        assert "application/xml" in content, "应支持 application/xml"
        assert default["description"] == "default response", f"description 应为 'default response'，实际为 {default['description']}"

    # ==================== 异常用例 ====================
    @pytest.mark.parametrize("method, desc", [
        ("POST", "使用POST方法请求GET接口，期望405或错误"),
        ("PUT", "使用PUT方法请求GET接口，期望405或错误"),
        ("DELETE", "使用DELETE方法请求GET接口，期望405或错误"),
        ("PATCH", "使用PATCH方法请求GET接口，期望405或错误"),
    ])
    def test_wrong_http_method(self, api, method, desc):
        """异常用例：错误HTTP方法"""
        resp = self.request(method, "/application.wadl")
        # 预期返回405 Method Not Allowed 或 其他错误状态码
        assert resp.status_code in [405, 400, 404], f"状态码应为405/400/404，实际为{resp.status_code}"

    @pytest.mark.parametrize("headers, desc", [
        ({"Accept": "text/plain"}, "不支持的Accept类型，期望406或默认响应"),
        ({"Accept": "application/json"}, "请求JSON格式，期望406或默认响应"),
        ({"Accept": "*/*"}, "通配符Accept，期望正常返回"),
    ])
    def test_unsupported_accept_header(self, api, headers, desc):
        """异常用例：不支持的Accept头"""
        resp = api.get("/application.wadl", headers=headers)
        # 根据实际实现，可能返回406或返回默认响应
        if resp.status_code == 406:
            assert True, "返回406 Not Acceptable"
        elif resp.status_code == 200:
            json_data = resp.json()
            assert "default" in json_data, "响应应包含 default 字段"
            default = json_data["default"]
            assert "content" in default, "default 应包含 content 字段"
            content = default["content"]
            assert "application/vnd.sun.wadl+xml" in content or "application/xml" in content, "应支持至少一种媒体类型"
            assert default["description"] == "default response", f"description 应为 'default response'，实际为 {default['description']}"
        else:
            assert False, f"状态码应为200或406，实际为{resp.status_code}"

    @pytest.mark.parametrize("path, desc", [
        ("/application.wadl/extra", "路径多出额外段，期望404"),
        ("/application.wadl?invalid=1", "携带无效查询参数，期望正常处理"),
        ("/Application.wadl", "大小写不同，期望404或重定向"),
    ])
    def test_invalid_path(self, api, path, desc):
        """异常用例：无效路径"""
        resp = api.get(path)
        # 预期返回404 Not Found
        assert resp.status_code == 404, f"状态码应为404，实际为{resp.status_code}"