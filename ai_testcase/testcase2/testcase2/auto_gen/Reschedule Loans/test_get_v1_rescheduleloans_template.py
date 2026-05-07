import pytest
from api_test.common.base_api import BaseApi

class TestRescheduleLoansTemplate:
    # 正常用例：获取所有重新安排贷款原因，期望成功
    def test_get_reschedule_loan_reasons_success(self, api: BaseApi):
        resp = api.get("/v1/rescheduleloans/template")
        assert resp.status_code == 200
        # 验证响应字段存在（根据Fineract API规范，通常返回列表）
        assert isinstance(resp.json(), list)

    # 边界值用例：测试请求头中的Accept类型
    @pytest.mark.parametrize("accept_header, expected_status", [
        ("application/json", 200),
        ("text/plain", 406),  # 不支持的媒体类型