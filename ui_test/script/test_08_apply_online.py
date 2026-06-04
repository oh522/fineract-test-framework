from script import log
class TestApplyOnline():
    def test_apply_online(self, go_apply_online):
        go_apply_online.go_apply_online()
        log.info("测试通过")


