import pytest
from api_test.common.base_api import BaseApi


class TestRescheduleLoans:
    # 正常用例：不带任何参数查询所有reschedule请求
    def test_reschedule_loans_success_no_params(self, api):
        resp = api.get("/v1/rescheduleloans")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    # 正常用例：使用command参数