"""
Locust 性能测试
复用接口自动化的 API 封装，不需要重写请求逻辑
运行：locust -f locustfile.py --host=https://localhost:8443
"""
import base64
from locust import HttpUser, task, between, events


class FineractUser(HttpUser):
    """
    模拟真实用户行为：登录 → 查客户 → 查贷款
    wait_time：每个任务之间等待 1~3 秒（模拟真实用户思考时间）
    """
    wait_time = between(1, 3)

    # 通过 weight 控制各任务执行频率比例
    # weight=3 表示执行频率是 weight=1 的3倍

    def on_start(self):
        """用户启动时初始化认证 Header（对应接口自动化的 BaseApi.__init__）"""
        token = base64.b64encode(b"mifos:password").decode()
        self.client.headers.update({
            "Authorization": f"Basic {token}",
            "Fineract-Platform-TenantId": "default",
            "Content-Type": "application/json",
        })
        self.client.verify = False
        self.loan_id = None

    # ─── 高频任务 ──────────────────────────────────────────────

    @task(3)
    def get_clients(self):
        """查询客户列表（高频，weight=3）"""
        with self.client.get(
            "/fineract-provider/api/v1/clients",
            params={"limit": 10, "offset": 0},
            name="/clients [LIST]",     # name 参数用于 Locust 报告分组
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"查询客户失败: {resp.status_code}")

    @task(3)
    def get_loan_detail(self):
        """查询贷款详情（高频）"""
        with self.client.get(
            "/fineract-provider/api/v1/loans/1",
            name="/loans/{id} [GET]",
            catch_response=True,
        ) as resp:
            if resp.status_code in (200, 404):
                resp.success()
            else:
                resp.failure(f"查询贷款失败: {resp.status_code}")

    @task(1)
    def login(self):
        """登录接口（低频，weight=1）"""
        with self.client.post(
            "/fineract-provider/api/v1/authentication",
            json={"username": "mifos", "password": "password"},
            name="/authentication [POST]",
            catch_response=True,
        ) as resp:
            if resp.status_code == 200 and "base64EncodedAuthenticationKey" in resp.text:
                resp.success()
            else:
                resp.failure(f"登录失败: {resp.status_code}")

    @task(1)
    def get_savings_account(self):
        """查询储蓄账户（低频）"""
        with self.client.get(
            "/fineract-provider/api/v1/savingsaccounts/1",
            name="/savingsaccounts/{id} [GET]",
            catch_response=True,
        ) as resp:
            if resp.status_code in (200, 404):
                resp.success()
            else:
                resp.failure(f"查询储蓄账户失败: {resp.status_code}")


# ─── 自定义指标监控 ───────────────────────────────────────────

@events.request.add_listener
def on_request(request_type, name, response_time, response_length,
               exception, context, **kwargs):
    """记录响应时间超过3秒的请求，用于定位性能瓶颈"""
    if response_time > 3000:  # 毫秒
        print(f"⚠️  慢请求: {request_type} {name} 耗时 {response_time:.0f}ms")