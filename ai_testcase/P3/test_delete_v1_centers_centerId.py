# 自动生成 | [P3] DELETE /v1/centers/{centerId}
# 描述：Delete a Center

port pytest
import allure

@allure.feature("中心管理")
@allure.story("删除中心")
class TestDeleteCenter:
    
    @pytest.mark.P3
    def test_delete_center_success(self, api):
        """正向用例：成功删除指定ID的中心"""
        # 假设已存在ID为1的中心
        center_id = 1
        response = api.delete(f"/v1/centers/{center_id}")
        assert response.status_code == 200
    
    @pytest.mark.P3
    @pytest.mark.parametrize("invalid_center_id, expected_status", [
        ("", 400),
        ("abc", 400),
        ("999999", 404),
        ("-1", 400)
    ])
    def test_delete_center_invalid(self, api, invalid_center_id, expected_status):
        """反向用例：使用无效中心ID删除应返回错误"""
        response = api.delete(f"/v1/centers/{invalid_center_id}")
        assert response.status_code == expected_status
```