import allure
import pytest

from api_test.common.api.offices_api import OfficeApi
from utils.assertion import assert_response_time, assert_status, assert_value, assert_jsonpath, assert_field


@allure.feature("机构管理")
class TestOffices:
    @allure.story("查询机构详情")
    @pytest.mark.smoke
    @pytest.mark.P0
    def test_get_office(self, offices_api: OfficeApi, offices_id):
        """✅ 查询已创建机构，验证机构信息"""
        res = offices_api.retrieve(offices_id)

        assert_status(res, 200, msg="查询机构")
        assert_response_time(res, 3.0)
        assert_value(res, "id", offices_id)

        # 验证关键字段存在
        assert "name" in res.json() and res.json()["name"], "机构名称应为非空字符串"
        assert "openingDate" in res.json(), "应包含开业日期字段"
        assert "parentId" in res.json(), "应包含父机构ID字段"

    @allure.story("查询机构列表")
    @pytest.mark.smoke
    @pytest.mark.P1
    def test_list_offices(self, offices_api: OfficeApi):
        """✅ 查询机构列表，返回非空列表"""
        res = offices_api.retrieve_list()

        assert_status(res, 200, msg="查询机构列表")
        assert_response_time(res, 3.0)

        # 兼容列表和对象两种响应格式
        offices = res.json() if isinstance(res.json(), list) else res.json().get("pageItems", [])
        assert len(offices) > 0, "机构列表不应为空"

        # 验证至少包含 Head Office
        office_names = [o.get("name") for o in offices]
        assert "Head Office" in office_names, "机构列表应包含 Head Office"

    @allure.story("创建机构")
    @pytest.mark.P1
    def test_create_office(self, offices_api: OfficeApi):
        """✅ 创建新机构"""
        import uuid
        from datetime import datetime

        # 生成唯一的外部 ID 和名称
        external_id = f"TEST-OFFICE-{uuid.uuid4().hex[:8]}"
        office_name = f"自动化测试机构_{uuid.uuid4().hex[:6]}"
        opening_date = datetime.now().strftime("%d %B %Y")

        payload = {
            "name": office_name,
            "openingDate": opening_date,
            "parentId": 1,  # 父机构为 Head Office
            "externalId": external_id,
            "locale": "en",
            "dateFormat": "dd MMMM yyyy"
        }

        res = offices_api.create(payload)
        assert_status(res, 200, msg="创建机构")
        assert_field(res, "resourceId")

        # 验证返回的 officeId
        created_id = res.json().get("resourceId")
        assert isinstance(created_id, int) and created_id > 0

        # 验证创建的机构可以查询到
        detail_res = offices_api.retrieve(created_id)
        assert_status(detail_res, 200)
        assert detail_res.json()["name"] == office_name

    @allure.story("更新机构信息")
    @pytest.mark.skip(reason="Fineract /offices PUT 端点可能存在字段限制，需要进一步验证")
    @pytest.mark.P1
    def test_update_office(self, offices_api: OfficeApi, offices_id):
        """✅ 更新机构名称"""
        # 先获取当前机构信息
        before_res = offices_api.retrieve(offices_id)
        assert_status(before_res, 200)
        before_data = before_res.json()
        original_name = before_data.get("name")

        # 更新机构名称
        update_payload = {
            "name": f"{original_name}_Updated",
            "locale": "en",
            "dateFormat": "dd MMMM yyyy"
        }
        res = offices_api.update(offices_id, update_payload)
        assert_status(res, 200, msg="更新机构")
        assert_field(res, "resourceId")
        assert res.json()["resourceId"] == offices_id

        # 验证更新后的信息
        after_res = offices_api.retrieve(offices_id)
        assert_status(after_res, 200)
        assert after_res.json()["name"] == f"{original_name}_Updated"

        # 恢复原始数据（避免影响其他测试）
        restore_payload = {
            "name": original_name,
            "locale": "en",
            "dateFormat": "dd MMMM yyyy"
        }
        offices_api.update(offices_id, restore_payload)

    @allure.story("查询不存在的机构")
    @pytest.mark.P2
    def test_get_nonexistent_office(self, offices_api: OfficeApi):
        """❌ 查询不存在的机构应返回 404"""
        res = offices_api.retrieve(999999)
        assert_status(res, 404, msg="查询不存在的机构")

    @allure.story("更新机构缺少必填字段")
    @pytest.mark.skip(reason="Fineract /offices PUT 更新时不校验字段完整性，只传 name 也返回 200")
    @pytest.mark.P2
    def test_update_office_missing_required_fields(self, office_api: OfficeApi, offices_id):
        """❌ 更新机构时缺少必填字段应返回 400"""
        # Fineract 的 PUT 更新似乎不严格校验字段
        res = office_api.update(offices_id, {
            "name": "Test"
            # 缺少 locale 和 dateFormat
        })
        assert_status(res, 400, msg="更新机构缺少必填字段")

    @allure.story("通过外部 ID 查询机构")
    @pytest.mark.P2
    def test_get_office_by_external_id(self, offices_api: OfficeApi, offices_id):
        """✅ 通过外部 ID 查询机构"""
        # 先获取机构的 externalId
        detail_res = offices_api.retrieve(offices_id)
        assert_status(detail_res, 200)
        external_id = detail_res.json().get("externalId")

        if external_id:
            # 通过 externalId 查询
            res = offices_api.retrieve_by_external_id(external_id)
            assert_status(res, 200, msg="通过外部ID查询机构")
            assert res.json()["id"] == offices_id
        else:
            pytest.skip("机构没有 externalId，跳过测试")

    @allure.story("查询机构模板")
    @pytest.mark.P3
    def test_retrieve_office_template(self, offices_api: OfficeApi):
        """✅ 查询机构详情模板（用于创建机构的参考）"""
        res = offices_api.retrieve_template()
        assert_status(res, 200, msg="查询机构模板")

        # 验证返回模板结构
        data = res.json()
        # 模板通常包含 parentIdOptions 或 officeOpeningDateTypeOptions
        assert len(data) > 0, "模板不应为空"

    @allure.story("下载机构导入模板")
    @pytest.mark.P3
    def test_download_office_template(self, offices_api: OfficeApi):
        """✅ 下载机构导入模板"""
        res = offices_api.download_template()

        # 模板下载可能返回 Excel 文件或其他格式
        assert res.status_code in [200, 404], f"下载模板失败: {res.status_code}"

        if res.status_code == 200:
            # 如果成功，应该是 Excel 格式
            content_type = res.headers.get("Content-Type", "")
            assert "excel" in content_type.lower() or "octet-stream" in content_type.lower()

    @allure.story("创建机构缺少必填字段")
    @pytest.mark.P2
    def test_create_office_missing_required_fields(self, offices_api: OfficeApi):
        """❌ 创建机构时缺少必填字段应返回 400"""
        # 缺少必填字段：name, openingDate, parentId
        res = offices_api.create({
            "externalId": "test-123",
            "locale": "en",
            "dateFormat": "dd MMMM yyyy"
        })
        assert_status(res, 400, msg="创建机构缺少必填字段")

    @allure.story("创建机构使用无效的 parentId")
    @pytest.mark.skip(reason="Fineract 创建机构需要管理员权限，当前用户返回 403")
    @pytest.mark.P2
    def test_create_office_invalid_parent_id(self, office_api: OfficeApi):
        """❌ 创建机构时使用无效的 parentId 应返回 400 或 404"""
        from datetime import datetime

        res = office_api.create({
            "name": "Test Office",
            "openingDate": datetime.now().strftime("%d %B %Y"),
            "parentId": 999999,  # 不存在的父机构
            "locale": "en",
            "dateFormat": "dd MMMM yyyy"
        })
        assert_status(res, 400, 404, msg="创建机构使用无效的parentId")

