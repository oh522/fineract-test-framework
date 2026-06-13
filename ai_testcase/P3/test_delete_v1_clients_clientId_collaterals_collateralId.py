# 自动生成 | [P3] DELETE /v1/clients/{clientId}/collaterals/{collateralId}
# 描述：Delete Client Collateral

port pytest
import allure

@allure.feature("客户抵押物管理")
@allure.story("删除客户抵押物")
class TestClientCollateralManagement:
    
    @pytest.mark.P3
    def test_delete_client_collateral_success(self, api):
        """正向用例：成功删除存在的客户抵押物"""
        response = api.delete("/v1/clients/1/collaterals/1")
        assert response.status_code == 200
    
    @pytest.mark.P3
    @pytest.mark.parametrize("client_id,collateral_id", [
        ("invalid", 1),
        (1, "invalid"),
        ("", 1),
        (1, ""),
        (999999, 1),
        (1, 999999),
        ("abc", "xyz"),
    ])
    def test_delete_client_collateral_error(self, api, client_id, collateral_id):
        """反向用例：删除无效客户抵押物应返回错误"""
        response = api.delete(f"/v1/clients/{client_id}/collaterals/{collateral_id}")
        assert response.status_code in [400, 404, 500]
```