# 导包
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# 创建浏览器对象
driver = webdriver.Edge()
# 访问网页
driver.get("http://tp123.com/Home/user/login.html/")
driver.refresh()
driver.back()
driver.forward()
# 等待三秒
time.sleep(3)
# 推出浏览器
driver.quit()