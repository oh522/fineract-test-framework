# 自动生成 | [P3] GET /application.wadl
# 描述：

import pytest
import allure

@allure.feature("WADL文件获取")
@allure.story("WADL接口测试")
class TestGetApplicationWadl:
    
    @pytest.mark.P3
    def test_get_application_wadl_success(self, api):
        """正向用例：验证成功获取WADL文件"""
        response = api.get("/application.wadl")
        assert response.status_code == 200
    
    @pytest.mark.P3
    def test_get_application_wadl_not_found(self, api):
        """反向用例：验证访问不存在的WADL路径返回错误状态码"""
        response = api.get("/application.wadl/nonexistent")
        assert response.status_code in [400, 401, 403, 404]