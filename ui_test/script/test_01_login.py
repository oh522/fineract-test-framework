from page.page_login import PageLogin
from script import log
from tools import DriverTools
class TestLogin:
    #前置方法
    def setup_method(self):
        driver = DriverTools.get_driver()#获取driver对象
        self.page_login = PageLogin(driver)#创建页面对象
        self.page_login.open_url()#打开页面
    #后置方法
    def teardown_method(self):
        DriverTools.quit_driver()
    def test_01_login_success(self):
        #准备数据
        # driver = DriverTools.get_driver()#获取driver对象
        # page_login = PageLogin(driver)#创建页面对象
        # # 调用方法
        # page_login.open_url()#打开页面
        self.page_login.login("13800001001", "Aa123456")#登录
        #打印日志
        result =self.page_login.get_success_result()
        # print(result)
        log.info(f"登录结果：{result}")
        #断言
        assert "13800001001" == result
        #退出
        # DriverTools.quit_driver()
    def test_02_login_fail_pwd_error(self):
        #准备数据
        # driver = DriverTools.get_driver()#获取driver对象
        # page_login = PageLogin(driver)#创建页面对象
        # # 调用方法
        # page_login.open_url()#打开页面
        self.page_login.login("13800001001", "Aa1234567")#登录
        #打印日志
        result =self.page_login.get_fail_result()
        # print(result)
        log.info(f"登录结果：{result}")
        #断言
        assert "密码错误" in result
        #退出
        # DriverTools.quit_driver()


