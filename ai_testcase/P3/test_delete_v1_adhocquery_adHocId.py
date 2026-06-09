# 自动生成 | [P3] DELETE /v1/adhocquery/{adHocId}
# 描述：
import pytest

import allure

@allure.feature("广告查询")
@allure.story("删除广告查询")
class TestDeleteAdhocQuery:
    
    @pytest.mark.P3
    def test_delete_adhocquery_positive(self, api):
        """正向用例：测试正常删除广告查询记录"""
        adHocId = "12345"
        response = api.delete(f"/v1/adhocquery/{adHocId}")
        assert response.status_code == 200
    
    @pytest.mark.P3
    def test_delete_adhocquery_negative(self, api):
        """反向用例：测试删除不存在的广告查询记录"""
        adHocId = "nonexistent_id_99999"
        response = api.delete(f"/v1/adhocquery/{adHocId}")
        assert response.status_code in [400, 401, 403, 404]
