import pytest


class TestLoansDownloadTemplate:
    """贷款下载模板接口测试"""

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """每个测试方法前初始化"""
        self.BASE_PATH = "/loans/downloadtemplate"

    # ==================== 正常用例 ====================
    def test_download_template_success_without_params(self, api):
        """正常用例：不传任何查询参数，期望成功"""
        resp = api.get(self.BASE_PATH)
        assert resp.status_code == 200
        # 验证响应为文件流或JSON，根据实际返回调整
        assert resp.headers.get("Content-Type") is not None

    def test_download_template_success_with_office_id(self, api):
        """正常用例：仅传officeId，期望成功"""
        params = {"officeId": 1}
        resp = api.get(self.BASE_PATH, params=params)
        assert resp.status_code == 200

    def test_download_template_success_with_all_params(self, api):
        """正常用例：传所有可选参数，期望成功"""
        params = {
            "officeId": 1,
            "staffId": 1,
            "dateFormat": "dd MMMM yyyy"
        }
        resp = api.get(self.BASE_PATH, params=params)
        assert resp.status_code == 200

    # ==================== 参数缺失用例 ====================
    # 本接口无必填参数，故无缺失用例

    # ==================== 边界值用例 ====================
    @pytest.mark.parametrize("office_id", [
        0,          # 极小值
        1,          # 正常值
        999999,     # 极大值（不存在）
        -1,         # 负数
    ])
    def test_download_template_boundary_office_id(self, api, office_id):
        """边界值用例：officeId边界值测试"""
        params = {"officeId": office_id}
        resp = api.get(self.BASE_PATH, params=params)
        # 边界值可能返回200或400，根据实际业务调整
        assert resp.status_code in [200, 400, 404]

    @pytest.mark.parametrize("staff_id", [
        0,
        1,
        999999,
        -1,
    ])
    def test_download_template_boundary_staff_id(self, api, staff_id):
        """边界值用例：staffId边界值测试"""
        params = {"staffId": staff_id}
        resp = api.get(self.BASE_PATH, params=params)
        assert resp.status_code in [200, 400, 404]

    @pytest.mark.parametrize("date_format", [
        "",           # 空字符串
        "dd MMMM yyyy",  # 正常格式
        "yyyy-MM-dd",    # 另一种格式
        "invalid_format", # 非法格式
    ])
    def test_download_template_boundary_date_format(self, api, date_format):
        """边界值用例：dateFormat边界值测试"""
        params = {"dateFormat": date_format}
        resp = api.get(self.BASE_PATH, params=params)
        assert resp.status_code in [200, 400, 422]

    # ==================== 异常用例 ====================
    @pytest.mark.parametrize("office_id", [
        "abc",       # 字符串类型
        1.5,         # 浮点数
        None,        # None
        [1, 2],      # 列表
        {"key": 1},  # 字典
    ])
    def test_download_template_invalid_office_id(self, api, office_id):
        """异常用例：officeId错误类型"""
        params = {"officeId": office_id}
        resp = api.get(self.BASE_PATH, params=params)
        assert resp.status_code in [400, 422]

    @pytest.mark.parametrize("staff_id", [
        "abc",
        1.5,
        None,
        [1, 2],
        {"key": 1},
    ])
    def test_download_template_invalid_staff_id(self, api, staff_id):
        """异常用例：staffId错误类型"""
        params = {"staffId": staff_id}
        resp = api.get(self.BASE_PATH, params=params)
        assert resp.status_code in [400, 422]

    @pytest.mark.parametrize("date_format", [
        123,         # 整数
        1.5,         # 浮点数
        None,        # None
        [1, 2],      # 列表
        {"key": 1},  # 字典
    ])
    def test_download_template_invalid_date_format(self, api, date_format):
        """异常用例：dateFormat错误类型"""
        params = {"dateFormat": date_format}
        resp = api.get(self.BASE_PATH, params=params)
        assert resp.status_code in [400, 422]

    def test_download_template_with_extra_params(self, api):
        """异常用例：传入未定义的参数"""
        params = {"unknownParam": "value"}
        resp = api.get(self.BASE_PATH, params=params)
        assert resp.status_code in [200, 400]