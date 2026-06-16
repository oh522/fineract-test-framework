# 自动生成 | [P3] DELETE /v1/clients/{clientId}/familymembers/{familyMemberId}
# 描述：Delete a client family member

port pytest
import allure

@allure.feature("客户家庭成员")
@allure.story("删除家庭成员")
class TestClientFamilyMemberDelete:
    
    @pytest.mark.P3
    def test_delete_family_member_success(self, api):
        """正向用例：删除客户家庭成员成功"""
        # 假设存在有效的clientId和familyMemberId
        client_id = 1
        family_member_id = 1
        response = api.delete(f"/v1/clients/{client_id}/familymembers/{family_member_id}")
        assert response.status_code == 200
    
    @pytest.mark.P3
    @pytest.mark.parametrize("client_id, family_member_id, expected_status", [
        ("invalid", 1, 400),  # 无效的clientId
        (1, "invalid", 400),  # 无效的familyMemberId
        (999999, 999999, 404),  # 不存在的clientId和familyMemberId
        ("", 1, 400),  # 空clientId
        (1, "", 400),  # 空familyMemberId
    ])
    def test_delete_family_member_invalid(self, api, client_id, family_member_id, expected_status):
        """反向用例：删除客户家庭成员失败的各种场景"""
        response = api.delete(f"/v1/clients/{client_id}/familymembers/{family_member_id}")
        assert response.status_code == expected_status
```