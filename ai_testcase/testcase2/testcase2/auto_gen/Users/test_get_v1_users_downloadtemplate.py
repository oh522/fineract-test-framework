import pytest
from api_test.common.base_api import BaseApi

class TestDownloadTemplate:
    # 正常用例：使用所有可选参数，期望成功
    def test_download_template_success(self, api):
        params = {
            "officeId": 1,
            "staffId": 1,
            "dateFormat": "yyyy-MM-dd"
        }
        resp = api.get("/v1/users/downloadtemplate", params=params)
        assert resp.status_code == 200
        assert resp.headers.get("Content-Type") is not None

    # 参数缺失用例：不提供任何查询参数
    def test_download_template_no_params(self, api):
        resp = api.get("/v1/users/downloadtemplate")
        assert resp.status_code in [200, 400, 403, 404, 422]

    # 边界值用例：测试整数参数的边界值
    @pytest.mark.parametrize("office_id, staff_id", [
        (0, 0),
        (-1, -1),
        (2**63 - 1, 2**63 - 1),
        (-2**63, -2**63),
        (1, None),
        (None, 1)
    ])
    def test_download_template_boundary_integers(self, api, office_id, staff_id):
        params = {}
        if office_id is not None:
            params["officeId"] = office_id
        if staff_id is not None:
            params["staffId"] = staff_id
        resp = api.get("/v1/users/downloadtemplate", params=params)
        assert resp.status_code in [200, 400, 403, 404, 422]

    # 边界值用例：测试字符串参数的边界值
    @pytest.mark.parametrize("date_format", [
        "",
        " ",
        "a" * 1000,
        "yyyy/MM/dd",
        "dd-MM-yyyy",
        "invalid_format",
        "2024-01-01"
    ])
    def test_download_template_boundary_strings(self, api, date_format):
        params = {"dateFormat": date_format}
        resp = api.get("/v1/users/downloadtemplate", params=params)
        assert resp.status_code in [200, 400, 403, 404, 422]

    # 异常用例：使用错误的参数类型
    @pytest.mark.parametrize("params", [
        {"officeId": "abc"},
        {"staffId": "xyz"},
        {"dateFormat": 12345},
        {"officeId": 1.5},
        {"staffId": 2.7}
    ])
    def test_download_template_invalid_types(self, api, params):
        resp = api.get("/v1/users/downloadtemplate", params=params)
        assert resp.status_code in [400,