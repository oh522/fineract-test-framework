import pytest
from api_test.common.base_api import BaseApi


@pytest.fixture(scope="session")
def api():
    """
    全局 API 客户端，整个测试会话只创建一次。
    BaseApi.__init__ 已处理好 Basic Auth，无需额外登录。
    """
    return BaseApi()