# 自动生成 | [P3] GET /v1/accountnumberformats
# 描述：List Account number formats

port pytest
import allure

@allure.feature("账户号码格式管理")
@allure.story("查询账户号码格式列表")
class TestAccountNumberFormatsList:
    
    @pytest.mark.P3
    def test_get_account_number_formats_success(self, api):
        """正向用例：成功获取账户号码格式列表"""
        response = api.get("/v1/accountnumberformats")
        assert response.status_code == 200

    @pytest.mark.P3
    def test_get_account_number_formats_with_invalid_endpoint(self, api):
        """反向用例：使用无效路径访问账户号码格式列表接口"""
        response = api.get("/v1/invalidaccountnumberformats")
        assert response