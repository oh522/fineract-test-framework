import pymysql
import pymysql.cursors
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional


class DBHelper:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parents[1] / "config" / "config.yaml"
        with open(config_path, encoding="utf-8") as f:
            cfg = yaml.safe_load(f)["db"]

        self.conn = pymysql.connect(
            host=cfg["host"],
            port=cfg.get("port", 3306),
            user=cfg["user"],
            password=cfg["password"],
            database=cfg["database"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
    def verify_client_exists(self, client_id: int) -> Dict[str, Any]:
        """验证客户在数据库中存在"""
        result = self.query_one(
            "SELECT id, firstname, lastname, status_enum FROM m_client WHERE id = %s",
            (client_id,)
        )
        if result is None:
            raise AssertionError(f"客户 {client_id} 在数据库中不存在")
        return result

    def query(self, sql: str, params: tuple = None) -> List[Dict[str, Any]]:
        """执行查询，返回所有结果"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"数据库查询失败: {str(e)}")

    def query_one(self, sql: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        """执行查询，返回第一条结果"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()
        except Exception as e:
            raise Exception(f"数据库查询失败: {str(e)}")

    def execute(self, sql: str, params: tuple = None) -> int:
        """执行更新/插入/删除操作"""
        try:
            with self.conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, params)
                return affected_rows
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"数据库执行失败: {str(e)}")



    def verify_loan_status(self, loan_id: int, expected_status: int) -> Dict[str, Any]:
        """
        验证贷款状态
        status: 100=待提交, 200=待审批, 300=已审批, 700=已激活
        """
        result = self.query_one(
            "SELECT id, loan_status_id FROM m_loan WHERE id = %s",
            (loan_id,)
        )
        if result is None:
            raise AssertionError(f"贷款 {loan_id} 不存在")

        actual_status = result["loan_status_id"]
        if actual_status != expected_status:
            raise AssertionError(
                f"贷款状态错误: 期望{expected_status}, 实际{actual_status}"
            )
        return result

    def verify_savings_balance(self, savings_id: int, expected_balance: float) -> float:
        """验证储蓄账户余额"""
        result = self.query_one(
            "SELECT id, account_balance_derived FROM m_savings_account WHERE id = %s",
            (savings_id,)
        )
        if result is None:
            raise AssertionError(f"储蓄账户 {savings_id} 不存在")

        actual = float(result["account_balance_derived"])
        if abs(actual - expected_balance) > 0.01:
            raise AssertionError(
                f"余额错误: 期望{expected_balance}, 实际{actual}"
            )
        return actual

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """支持上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时自动关闭连接"""
        self.close()
