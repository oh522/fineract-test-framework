from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from ui_test.config import PATH
from ui_test.tools import GetLog


class BasePage(object):

    def __init__(self, driver, timeout=10):
        # 获取浏览器对象
        self.driver = driver  # 相当于：self.driver = DriverTools.get_driver()
        self.default_timeout = timeout  # 默认等待时间

    def fd_element(self, loc):
        """
        元素定位的公共方法
        :param loc: 元素定位方式及属性值
        :return: 定位到的元素
        """
        try:
            # element = WebDriverWait(self.driver, self.default_timeout).until(lambda x: x.find_element(*loc))
            # 推荐写法
            element = WebDriverWait(self.driver, self.default_timeout).until(EC.presence_of_element_located(loc))
            return element
        except Exception as e:
            GetLog.get_log().error(f"元素定位超时，定位信息：{loc}, 错误详情：{e}")
            raise  # 重新抛出异常供上层处理
    def base_input(self, loc, text):
                """
                输入框输入公共方法
                :param loc: 元素定位方式及属性值
                :param text: 输入内容
                :return: 无
                """
                # 定位元素
                ele = self.fd_element(loc)
                # 清空输入框
                ele.clear()
                # 输入内容
                ele.send_keys(text)
    def base_click(self, loc):
        """
        点击元素公共方法
        :param loc: 元素定位方式及属性值
        :return: 无
        """
        self.fd_element(loc).click()

    def get_shot(self, file_name):
        """
        截图
        :param file_name: 截图文件名
        :return: 无
        """
        file_path = os.path.join(PATH, 'img', file_name)
        self.driver.get_screenshot_as_file(file_path)

    def base_switch_handle(self, loc):
        """
        切换多窗口并获取指定元素
        :param loc: 定位的元素信息
        :return: 第一个窗口的页面元素
        """
        # 等待页面加载
        WebDriverWait(self.driver, self.default_timeout).until(lambda x: len(x.window_handles) > 1)
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        # 切换到新窗口进行定位
        element = self.fd_element(loc)
        return element

    def base_switch_frame(self, loc):
        """
        切换 frame
        :param loc: frame 的定位信息
        :return: 无
        """
        frame_ele = self.fd_element(loc)
        self.driver.switch_to.frame(frame_ele)

    def base_default_frame(self):
        """
        切换到默认 frame
        :return: 无
        """
        self.driver.switch_to.default_content()

