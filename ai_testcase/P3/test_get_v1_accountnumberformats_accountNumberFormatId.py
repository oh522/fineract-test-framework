# 自动生成 | [P3] GET /v1/accountnumberformats/{accountNumberFormatId}
# 描述：Retrieve an Account number format

port pytest
import allure

@allure.feature("账户管理")
@allure.story("账户号码格式")
class TestAccountnumberformatsAccountNumberFormatId:
    
    @pytest.mark.P3
    def test_retrieve_account_number_format_positive(self, api):
        """正向用例：测试获取存在的账户号码格式"""
        response = api.get("/v1/accountnumberformats/1")
        assert response.status_code == 200
    
    @pytest.mark.P3
    def test_retrieve_account_number_format_negative(self, api):
        """反向用例：测试获取不存在的账户号码格式"""
        response = api.get("/v1/accountnumberformats/999999999")
        assert response.status_code in [400, 401, 403, 404]
```