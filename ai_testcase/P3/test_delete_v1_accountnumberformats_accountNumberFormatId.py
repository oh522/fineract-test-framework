# 自动生成 | [P3] DELETE /v1/accountnumberformats/{accountNumberFormatId}
# 描述：Delete an Account number format

import pytest
import allure

@allure.feature("账户号码格式管理")
@allure.story("删除账户号码格式")
class TestAccountNumberFormatsDelete:
    
    @pytest.mark.P3
    def test_delete_account_number_format_positive(self, api):
        """正向用例：测试删除存在的账户号码格式"""
        # 先创建一个账户号码格式用于测试
        create_response = api.post("/v1/accountnumberformats", json={
            "formatName": "Test Format",
            "formatPattern": "XXX-XXX-XXX"
        })
        format_id = create_response.json()["id"]
        
        # 删除刚创建的账户号码格式
        response = api.delete(f"/v1/accountnumberformats/{format_id}")
        assert response.status_code == 200
    
    @pytest.mark.P3
    def test_delete_account_number_format_negative_nonexistent(self, api):
        """反向用例：测试删除不存在的账户号码格式"""
        # 使用一个不存在的ID
        nonexistent_id = 99999999
        response = api.delete(f"/v1/accountnumberformats/{nonexistent_id}")
        assert response.status_code in [400, 401, 403, 404]
