import pytest
from api_test.common.base_api import BaseApi

class TestLoansDownloadTemplate:
    # 正常用例：使用所有可选参数，期望成功
    def test_download_template_success_with_all_params(self, api):
        params = {
            "officeId": 1,
            "staffId": 1,
            "dateFormat": "dd MMMM yyyy"
        }
        resp = api.get("/v1/loans/downloadtemplate", params=params)
        assert resp.status_code == 200
        assert resp.headers.get("Content-Type") is not None

    # 正常用例：不使用任何参数，期望成功
    def test_download_template_success_without_params(self, api):
        resp = api.get("/v1/loans/downloadtemplate")
        assert resp.status_code == 200
        assert resp.headers.get("Content-Type") is not None

    # 参数缺失用例：逐个测试缺少单个参数的情况
    @pytest.mark.parametrize("missing_param", [
        {"officeId": 1, "staffId": 1},
        {"officeId": 1, "dateFormat": "dd MMMM yyyy"},
        {"staffId": 1, "dateFormat": "dd MMMM yyyy"}
    ])
    def test_download_template_missing_params(self, api, missing_param):
        resp = api.get("/v1/loans/downloadtemplate", params=missing_param)
        assert resp.status_code == 200

    # 边界值用例：测试整数参数的边界值
    @pytest.mark.parametrize("office_id, staff_id", [
        (0, 0),
        (1, 1),
        (999999, 999999),
        (-1, -1),
        (2147483647, 2147483647),
        (-2147483648, -2147483648)
    ])
    def test_download_template_integer_boundary(self, api, office_id, staff_id):
        params = {
            "officeId": office_id,
            "staffId": staff_id,
            "dateFormat": "dd MMMM yyyy"
        }
        resp = api.get("/v1/loans/downloadtemplate", params=params)
        assert resp.status_code in [200, 400, 404]

    # 边界值用例：测试字符串参数的边界值
    @pytest.mark.parametrize("date_format", [
        "",
        " ",
        "dd MMMM yyyy",
        "yyyy-MM-dd",
        "dd/MM/yyyy",
        "a" * 1000,
        "特殊字符!@#$%^&*()",
        "中文日期格式",
        "null",
        "undefined"
    ])
    def test_download_template_string_boundary(self, api, date_format):
        params = {
            "officeId": 1,
            "staffId": 1,
            "dateFormat": date_format
        }
        resp = api.get("/v1/loans/downloadtemplate", params=params)
        assert resp.status_code in [200, 400, 422]

    # 异常用例：测试错误类型参数
    @pytest.mark.parametrize("invalid_params", [
        {"officeId": "abc", "staffId": 1, "dateFormat": "dd MMMM yyyy"},
        {"officeId": 1, "staffId": "xyz", "dateFormat": "dd MMMM yyyy"},
        {"officeId": 1.5, "staffId": 1, "dateFormat": "dd MMMM yyyy"},
        {"officeId": 1, "staffId": 1.5, "dateFormat": "dd MMMM yyyy"},
        {"officeId": None, "staffId": 1, "dateFormat": "dd MMMM yyyy"},
        {"officeId": 1, "staffId": None, "dateFormat": "dd MMMM yyyy"},
        {"officeId": True, "staffId": 1, "dateFormat": "dd MMMM yyyy"},
        {"officeId": 1, "staffId": False, "dateFormat": "dd MMMM yyyy"}
    ])
    def test_download_template_invalid_type(self, api, invalid_params):
        resp = api.get("/v1/loans/downloadtemplate", params=invalid_params)
        assert resp.status_code in [400, 422]

    # 异常用例：测试不存在的资源ID
    def test_download_template_nonexistent_resource(self, api):
        params = {
            "officeId": 999999,
            "staffId": 999999,
            "dateFormat": "dd MMMM yyyy"
        }
        resp = api.get("/v1/loans/downloadtemplate", params=params)
        assert resp.status_code in [400, 404]

    # 异常用例：测试特殊字符和SQL注入
    @pytest.mark.parametrize("special_params", [
        {"officeId": "1; DROP TABLE loans;--", "staffId": 1, "dateFormat": "dd MMMM yyyy"},
        {"officeId": 1, "staffId": "1 OR 1=1", "dateFormat": "dd MMMM yyyy"},
        {"officeId": 1, "staffId": 1, "dateFormat": "dd MMMM yyyy' OR '1'='1"},
        {"officeId": "<script>alert('xss')</script>", "staffId": 1, "dateFormat": "dd MMMM yyyy"}
    ])
    def test_download_template_special_characters(self, api, special_params):
        resp = api.get("/v1/loans/downloadtemplate", params=special_params)
        assert resp.status_code in [400, 422]