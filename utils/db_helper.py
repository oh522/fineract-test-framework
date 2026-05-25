import os
from pathlib import Path
import pymysql
import yaml
import logging
logger = logging.getLogger(__name__)


class DBHelper:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parents[1] / "config" / "config.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            full_cfg = yaml.safe_load(f)
        env = os.environ.get("TEST_ENV", full_cfg.get("env", "test"))
        cfg = full_cfg[env]["db"]
        self._cfg = {
            "host": cfg["host"],
            "port": int(cfg["port"]),
            "user": cfg["user"],
            "password": cfg["password"],
            "database": cfg["database"],
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor,
        }
        self.conn = None

    def __enter__(self):
        self._conn = pymysql.connect(**self._cfg)
        logger.info(f"DB 已连接： {self._cfg['host']}/{self._cfg['database']}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self._conn.close()
            logger.info(f"DB 已断开： {self._cfg['host']}/{self._cfg['database']}")

    def query_one(self, sql:str, params: tuple = None) -> dict | None:
        with self._conn.cursor() as cur:
            cur.execute(sql, params or ())
            row = cur.fetchone()
            logger.debug(f"query_one ← {row}")
            return row

    def query_all(self, sql: str, params: tuple = None) -> list[dict]:
        with self._conn.cursor() as cur:
            cur.execute(sql, params or ())
            rows = cur.fetchall()
            logger.debug(f"query_all ← {len(rows)} 条")
            return rows

    def execute(self, sql: str, params: tuple = None) -> int:
        with self._conn.cursor() as  cur:
            affected = cur.execute(sql, params or ())
            self._conn.commit()
            logger.info(f"execute 影响 {affected} 行")
            return affected

    def assert_client_active(self, client_id: int):
        row = self.query_one("SELECT * FROM m_client WHERE id = %s", (client_id,))
        assert row, f"客户 {client_id} 不存在"
        assert row["status_enum"] == 300, (
            f"客户 {client_id} 状态期望 300(Active)，实际 {row['status_enum']}"
        )

    def assert_loan_active(self, loan_id: int):
        row = self.query_one("SELECT * FROM m_loan WHERE id = %s", (loan_id,))
        assert row, f"贷款 {loan_id} 不存在"
        actual_status = row.get("loan_status_id")
        assert actual_status == 300, (
            f"贷款 {loan_id} 状态期望 300(Active)，实际 {actual_status}"
        )




    def assert_user_exists(self, username: str):
        row = self.query_one("SELECT * FROM m_appuser WHERE username = %s", (username,))
        assert row, f"数据库中不存在用户 {username}"
        assert row["is_deleted"] == 0, f"用户 {username} 已被删除"