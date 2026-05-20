import logging
import os
import pymysql
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)


class DBHelper:
    """
    数据库工具类
    - PyMySQL 连接，DictCursor 返回字典
    - with 语句管理连接，用完自动关闭，避免连接泄露
    - 从配置文件读取，多环境隔离
    """

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parents[1] / "config" / "config.yaml"

        with open(config_path, "r", encoding="utf-8") as f:
            full_cfg = yaml.safe_load(f)

        # 多环境：优先读环境变量
        env = os.environ.get("TEST_ENV", full_cfg.get("env", "test"))
        cfg = full_cfg[env]["db"]

        self._cfg = {
            "host":        cfg["host"],
            "port":        cfg["port"],
            "user":        cfg["user"],
            "password":    cfg["password"],
            "database":    cfg["database"],
            "charset":     "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor,  # 返回 dict，不用索引取值
        }
        self._conn = None

    # ─── 上下文管理（用完自动关闭） ──────────────────────────

    def __enter__(self):
        self._conn = pymysql.connect(**self._cfg)
        logger.info(f"✅ DB 已连接: {self._cfg['host']}/{self._cfg['database']}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            self._conn.close()
            logger.info("🔒 DB 连接已关闭")

    # ─── 查询接口 ──────────────────────────────────────────────

    def query_one(self, sql: str, params: tuple = None) -> dict | None:
        """查询单条，返回 dict 或 None"""
        with self._conn.cursor() as cur:
            cur.execute(sql, params or ())
            row = cur.fetchone()
            logger.debug(f"query_one ← {row}")
            return row

    def query_all(self, sql: str, params: tuple = None) -> list[dict]:
        """查询多条，返回 list[dict]"""
        with self._conn.cursor() as cur:
            cur.execute(sql, params or ())
            rows = cur.fetchall()
            logger.debug(f"query_all ← {len(rows)} 条")
            return rows

    def execute(self, sql: str, params: tuple = None) -> int:
        """写操作（INSERT/UPDATE/DELETE），返回影响行数"""
        with self._conn.cursor() as cur:
            affected = cur.execute(sql, params or ())
            self._conn.commit()
            logger.info(f"execute 影响 {affected} 行")
            return affected

    # ─── 业务级校验方法（对应小林coding典型场景） ────────────

    def assert_client_active(self, client_id: int):
        """校验客户状态为 Active(300)"""
        row = self.query_one(
            "SELECT status_enum FROM m_client WHERE id = %s", (client_id,)
        )
        assert row, f"数据库中不存在 clientId={client_id}"
        assert row["status_enum"] == 300, (
            f"客户 {client_id} 状态期望 300(Active)，实际 {row['status_enum']}"
        )

    def assert_loan_active(self, loan_id: int):
        """校验贷款状态为 Active(300)"""
        row = self.query_one(
            "SELECT loan_status_id FROM m_loan WHERE id = %s", (loan_id,)
        )
        assert row, f"数据库中不存在 loanId={loan_id}"
        assert row["loan_status_id"] == 300, (
            f"贷款 {loan_id} 状态期望 300(Active)，实际 {row['loan_status_id']}"
        )

    def assert_user_exists(self, username: str):
        """校验用户存在且未删除"""
        row = self.query_one(
            "SELECT is_deleted FROM m_appuser WHERE username = %s", (username,)
        )
        assert row, f"数据库中不存在用户 {username}"
        assert row["is_deleted"] == 0, f"用户 {username} 已被删除"