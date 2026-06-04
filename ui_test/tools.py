import json
import logging
import time
import os
import sys
from pathlib import Path
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from logging import handlers

# 添加 ui_test 目录到 sys.path，确保能导入 ui_test/config.py
current_file = Path(__file__).resolve()
ui_test_dir = str(current_file.parent)
if ui_test_dir not in sys.path:
    sys.path.insert(0, ui_test_dir)

# 使用绝对导入避免与根目录 config 包冲突
from ui_test.config import PATH


class DriverTools:
    """浏览器驱动类"""
    driver = None
    __log = None
    @classmethod
    def get_driver(cls):
        if cls.driver is None:
            cls.driver = webdriver.Edge()
            cls.driver.maximize_window()
            cls.driver.implicitly_wait(10)  # 隐式等待 10 秒
        return cls.driver
    @classmethod
    def quit_driver(cls):
        if cls.driver:
            cls.driver.quit()
            cls.driver = None
def read_json(file_name):
        """
        读取 JSON 文件并转换为格式为 [(),(),...] 的列表
        :param file_name: json 文件名
        :return: 列表
        """
        data = []
        file_path = PATH + "/data/" + file_name
        with open(file_path, mode='r', encoding='utf-8') as f:
            # 读取 JSON 文件并解析为 Python 对象
            tmp = json.load(f)
            for i in tmp:
                a = tuple(i.values())
                data.append(a)
        # 返回列表
        return data
class GetLog:
    __log = None  # 日志器
    @classmethod
    def get_log(cls):
        if cls.__log is None:
            # 获取日志器
            cls.__log = logging.getLogger()
            # 设置入口级别
            cls.__log.setLevel(logging.INFO)
            # 获取处理器
            filename = PATH + "/log/" + "web.log"
            tf = logging.handlers.TimedRotatingFileHandler(filename=filename,
                                                           when="midnight",
                                                           interval=1,
                                                           backupCount=3,
                                                           encoding="utf-8")
            # 获取格式器
            fmt = "%(asctime)s %(levelname)s [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
            fm = logging.Formatter(fmt)
            # 将格式器添加到处理器
            tf.setFormatter(fm)
            # 将处理器添加到日志器
            cls.__log.addHandler(tf)
        # 返回日志器
        return cls.__log
if __name__ == '__main__':
    driver = DriverTools.get_driver()
    driver.get("http://www.baidu.com")
    time.sleep(2)
    DriverTools.quit_driver()


