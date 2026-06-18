# 自动生成 | [P3] GET /application.wadl/{path}
# 描述：

import pytest
import allure

@allure.feature("应用配置")
@allure.story("WADL文档访问")
class TestApplicationWadlPath:
    
    @pytest.mark.P3
    def test_get_wadl_document_with_valid_path(self, api):
        """正向用例：测试使用有效路径访问WADL文档"""
        response = api.get("/application.wadl/test")
        assert response.status_code == 200
    
    @pytest.mark.P3
    def test_get_wadl_document_with_invalid_path(self, api):
        """反向用例：测试使用无效路径访问WADL文档"""
        response = api.get("/application.wadl/invalid_path_123456")
        assert response.status_code in [400, 401, 403, 404]