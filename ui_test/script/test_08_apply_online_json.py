import pytest
from script import log
from tools import read_json
from page.page_apply_online_json import ApplyOnline
class TestApplyOnlineJson():
    """在线申请 - JSON数据驱动测试"""

    @pytest.mark.parametrize("project_name,province,city,amount,period,apr,description",
                             read_json("apply_online_data.json"))
    def test_apply_online_with_json(self, project_name, province, city, amount, period, apr, description,
                                    go_apply_online_json: ApplyOnline):
        """使用JSON数据进行在线申请测试"""
        log.info(f"开始测试 - 项目: {project_name}, 金额: {amount}")
        # 执行在线申请流程，传入JSON数据
        result = go_apply_online_json.go_apply_online(
            project_name=project_name,
            province=province,
            city=city,
            amount=amount,
            period=period,
            apr=apr,
            description=description
        )
        log.info(f"申请结果: {result}")
        assert "成功" in result, f"申请失败，结果: {result}"



