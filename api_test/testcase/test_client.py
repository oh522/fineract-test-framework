from utils.db_helper import DBHelper

def test_create_client_db_verify(api, client_id):
    """创建客户后验证数据库一致性"""
    # 接口验证
    res = api.get(f"/clients/{client_id}")
    assert res.status_code == 200

    # 数据库验证（简历亮点！）
    db = DBHelper()
    db_result = db.verify_client_exists(client_id)
    assert db_result["firstname"] == "自动化"
    db.close()

