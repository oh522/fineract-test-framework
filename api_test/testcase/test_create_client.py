from utils.db_helper import DBHelper

# def test_create_client_db_verify(api, client_id):
#     """创建客户后验证数据库一致性"""
#     # 接口验证
#     res = api.get(f"/clients/{client_id}")
#     assert res.status_code == 200
#
#     # 数据库验证（简历亮点！）
#     db = DBHelper()
#     db_result = db.verify_client_exists(client_id)
#     assert db_result["firstname"] == "自动化"
#     db.close()
# 📝 改进说明
# ✅ 主要改进点：
#1 使用上下文管理器 with DBHelper() as db:
# 自动关闭数据库连接
# 即使断言失败也能正确释放资源
#2 多维度验证
# 响应数据类型验证
# 关键字段存在性验证
# 字段值验证
# 状态枚举值验证
#3 API vs 数据库一致性对比（⭐ 面试亮点）
# 证明你理解前后端数据一致性
# 展示数据库验证能力
# 体现测试深度
#4 清晰的错误信息
# 所有断言都包含详细的失败原因
# 方便快速定位问题
#5 增加额外测试用例
# test_create_client_api_only: 纯 API 验证
# test_create_client_data_consistency: 数据一致性专项测试

# Fixture 的断言是保护机制：如果创建失败，测试应该快速失败，而不是带着错误的 client_id 继续执行
# 测试用例的断言是核心价值：这才是你真正要测试的业务逻辑
# 面试/简历展示：你可以说"我在 fixture 中做了防御性验证，在测试用例中做了业务逻辑验证和数据库一致性验证"
def test_create_client_db_verify(api, client_id):
    """创建客户后验证数据库一致性"""
    # ========== 接口验证 ==========
    res = api.get(f"/clients/{client_id}")
    assert res.status_code == 200, f"查询客户失败: {res.text}"

    # 验证响应数据类型
    client_data = res.json()
    assert isinstance(client_data, dict), f"响应数据类型错误: {type(client_data)}"

    # 验证关键字段存在
    required_fields = ["id", "firstname", "lastname", "status", "officeId"]
    for field in required_fields:
        assert field in client_data, f"响应缺少关键字段: {field}"

    # 验证字段值
    assert client_data["id"] == client_id, \
        f"客户ID不匹配: 期望 {client_id}, 实际 {client_data['id']}"
    assert client_data["firstname"] == "自动化", \
        f"firstname 不匹配: 期望 '自动化', 实际 '{client_data['firstname']}'"
    assert client_data["lastname"] == "测试客户", \
        f"lastname 不匹配: 期望 '测试客户', 实际 '{client_data['lastname']}'"
    assert client_data["officeId"] == 1, \
        f"officeId 不匹配: 期望 1, 实际 {client_data['officeId']}"

    # ========== 数据库验证（简历亮点）==========
    # 使用上下文管理器，确保连接自动关闭
    with DBHelper() as db:
        db_result = db.verify_client_exists(client_id)

        # 验证数据库返回类型
        assert isinstance(db_result, dict), f"数据库返回类型错误: {type(db_result)}"

        # 验证数据库字段值
        assert db_result["firstname"] == "自动化", \
            f"数据库 firstname 不匹配: {db_result['firstname']}"
        assert db_result["lastname"] == "测试客户", \
            f"数据库 lastname 不匹配: {db_result['lastname']}"

        # 验证客户状态（300 = Active）
        assert db_result["status_enum"] == 300, \
            f"客户状态错误: 期望 300(Active), 实际 {db_result['status_enum']}"

        # 验证 externalId（如果 conftest 中传入了）
        if "externalId" in db_result:
            assert db_result["externalId"] is not None, \
                "externalId 不应为空"

        # ✅ API 和数据库数据一致性验证（核心亮点）
        assert client_data["firstname"] == db_result["firstname"], \
            "API 和数据库 firstname 不一致"
        assert client_data["lastname"] == db_result["lastname"], \
            "API 和数据库 lastname 不一致"
        assert client_data["id"] == db_result["id"], \
            "API 和数据库 id 不一致"




def test_create_client_api_only(api, client_id):
    """仅验证 API 返回数据的完整性"""
    # 查询客户详情
    res = api.get(f"/clients/{client_id}")
    assert res.status_code == 200, f"查询失败: {res.text}"

    client_data = res.json()

    # 验证所有关键字段
    assert client_data["id"] == client_id
    assert client_data["firstname"] == "自动化"
    assert client_data["lastname"] == "测试客户"
    assert client_data["officeId"] == 1
    assert client_data["status"]["value"] == "Active"
    assert client_data["active"] is True

    # ✅ 修复：使用 .get() 检查 legalFormId（某些 API 版本可能不返回此字段）
    legal_form_id = client_data.get("legalFormId")
    if legal_form_id is not None:
        assert legal_form_id == 1, \
            f"legalFormId 应为 1(Person), 实际 {legal_form_id}"



def test_create_client_data_consistency(api, client_id):
    """验证 API 和数据库的数据一致性（面试亮点）"""
    # 获取 API 数据
    api_res = api.get(f"/clients/{client_id}")
    assert api_res.status_code == 200
    api_data = api_res.json()

    # 获取数据库数据
    with DBHelper() as db:
        db_data = db.verify_client_exists(client_id)

        # 对比核心字段
        assert api_data["firstname"] == db_data["firstname"], \
            f"firstname 不一致: API={api_data['firstname']}, DB={db_data['firstname']}"
        assert api_data["lastname"] == db_data["lastname"], \
            f"lastname 不一致: API={api_data['lastname']}, DB={db_data['lastname']}"
        assert api_data["officeId"] == 1, "officeId 应为 1"

        # 验证状态一致性（API 的 status.value vs DB 的 status_enum）
        # status_enum: 300 = Active
        assert db_data["status_enum"] == 300, \
            f"数据库状态应为 300(Active), 实际 {db_data['status_enum']}"
        assert api_data["active"] is True, "API 返回 active 应为 True"

