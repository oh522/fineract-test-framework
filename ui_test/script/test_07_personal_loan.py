import pytest
from script import log
version = "1.0.0"
# @pytest.mark.skip(reason="跳过测试")
# @pytest.mark.skipif(version == "1.0.0", reason="跳过测试")
# @pytest.mark.flaky(reruns=2, reruns_delay=3)#失败重试
# @pytest.mark.smoke#在控制台中执行时，只执行smoke标记的用例（输入 pytest -s -m smoke）
class TestPersonalLoan:
    def test_personal_loan_01(self, go_personal_loan):
        go_personal_loan.go_personal_loan()
        result = go_personal_loan.get_success_result()
        log.info(f"申请结果:{result}")
        assert "下午好，a" in result

    def test_personal_loan_02(self, go_personal_loan):
        go_personal_loan.go_personal_loan()
        result = go_personal_loan.get_success_result()
        log.info(f"申请结果:{result}")
        assert "下午好，" in result


0