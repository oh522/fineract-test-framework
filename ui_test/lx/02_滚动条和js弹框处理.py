# 导包
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# 创建浏览器对象
driver = webdriver.Edge()
# 访问网页
driver.get("http://tp123.com/Home/user/login.html/")
#滚动条滚动
js = "window.scrollTo(0,400)"
driver.execute_script(js)
# 点击alert按钮(点击后出现弹框)
driver.find_element(by=By.XPATH, value='//*[text()="alert"]').click()
alert = driver.switch_to.alert#切换到alert
alert.accept()#点击确定
alert.dismiss()#点击取消
# 等待三秒
time.sleep(3)
# 推出浏览器
driver.quit()