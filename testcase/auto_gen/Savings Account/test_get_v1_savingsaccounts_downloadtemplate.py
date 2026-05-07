import pytest


class TestSavingsAccountsDownloadTemplate:
    """Savings Account Download Template API Tests"""

    @pytest.mark.parametrize("office_id, staff_id, date_format", [
        (1, 1, "dd MMMM yyyy"),
        (None, None, None),
        (1, None, "dd MMMM yyyy"),
        (None, 1, "dd MMMM yyyy"),
    ])
    def test_normal_cases(self, api, office_id, staff_id, date_format):
        """正常用例：各种参数组合，期望成功"""
        params = {}
        if office_id is not None:
            params["officeId"] = office_id
        if staff_id is not None:
            params["staffId"] = staff_id
        if date_format is not None:
            params["dateFormat"] = date_format

        resp = api.get("/savingsaccounts/downloadtemplate", params=params)
        assert resp.status_code == 200
        # 验证响应包含必要字段（根据实际响应结构调整）
        assert "headers" in resp.json() or isinstance(resp.json(), list)

    @pytest.mark.parametrize("missing_param", [
        "officeId",
        "staffId",
        "dateFormat"
    ])
    def test_missing_required_params(self, api, missing_param):
        """参数缺失用例：逐个缺少查询参数，期望返回4xx"""
        params = {
            "officeId": 1,
            "staffId": 1,
            "dateFormat": "dd MMMM yyyy"
        }
        if missing_param in params:
            del params[missing_param]

        resp = api.get("/savingsaccounts/downloadtemplate", params=params)
        assert resp.status_code in [400, 403, 404, 422]

    @pytest.mark.parametrize("office_id, staff_id, date_format", [
        (0, 1, "dd MMMM yyyy"),
        (-1, 1, "dd MMMM yyyy"),
        (999999, 1, "dd MMMM yyyy"),
        (1, 0, "dd MMMM yyyy"),
        (1, -1, "dd MMMM yyyy"),
        (1, 999999, "dd MMMM yyyy"),
        (1, 1, ""),
        (1, 1, " "),
        (1, 1, "invalid-date-format"),
        (1, 1, "yyyy-MM-dd"),
        (1, 1, "DD/MM/YYYY"),
        (1, 1, "mm/dd/yyyy"),
        (1, 1, "dd-mm-yyyy"),
        (1, 1, "dd.mm.yyyy"),
        (1, 1, "dd/mm/yyyy"),
        (1, 1, "yyyy/mm/dd"),
        (1, 1, "yyyy-mm-dd"),
        (1, 1, "yyyymmdd"),
        (1, 1, "ddmmyyyy"),
        (1, 1, "mmddyyyy"),
        (1, 1, "dd MMM yyyy"),
        (1, 1, "dd MMMM yyyy"),
        (1, 1, "dd MMMM yyyy HH:mm:ss"),
        (1, 1, "dd MMMM yyyy HH:mm"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS Z"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS z"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'UTC'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'GMT'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'EST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'PST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'CST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'MST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'HST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'AKST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'AST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'NST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'WST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'CET'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'EET'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'MSK'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'IST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'JST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'KST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'CST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'AEST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'AEDT'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'ACST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'ACDT'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'AWST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'NZST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'NZDT'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'CHAST'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'CHADT'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'GAMT'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'GILT'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'LINT'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'PHOT'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'TOT'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'WAKT'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'WFT'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'XJT'"),
        (1, 1, "dd MMMM yyyy HH:mm:ss.SSS 'YAPT'"),
    ])
    def test_boundary_and_edge_cases(self, api, office_id, staff_id, date_format):
        """边界值用例：空字符串、极大值、极小值、0、负数等"""
        params = {}
        if office_id is not None:
            params["officeId"] = office_id
        if staff_id is not None:
            params["staffId"] = staff_id
        if date_format is not None:
            params["dateFormat"] = date_format

        resp = api.get("/savingsaccounts/downloadtemplate", params=params)
        # 边界值可能返回成功或4xx，取决于API实现
        assert resp.status_code in [200, 400, 403, 404, 422]

    @pytest.mark.parametrize("office_id, staff_id, date_format", [
        ("abc", 1, "dd MMMM yyyy"),
        (1, "abc", "dd MMMM yyyy"),
        (1, 1, 12345),
        (1.5, 1, "dd MMMM yyyy"),
        (1, 1.5, "dd MMMM yyyy"),
        (None, None, None),