# 导包
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 创建浏览器对象
driver = webdriver.Edge()
# 访问网页
driver.get("http://tp123.com/Home/Index/index.html")
#滑动滚动条
driver.execute_script("window.scrollTo(0,5000)")
#点击友情链接
driver.find_element(by=By.LINK_TEXT, value='四川省科学养生促进会').click()
#获取当前窗口的句柄
handles = driver.window_handles#
print( handles)
# 切换窗口
driver.switch_to.window(handles[1])
#在新窗口进行点击操作
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, '挣脱“数据枷锁”，守护健康本真')))
driver.find_element(by=By.LINK_TEXT, value='挣脱“数据枷锁”，守护健康本真').click()
#操作完的截图
driver.get_screenshot_as_file('screenshot.png')
# 等待三秒
time.sleep(3)
# 推出浏览器
driver.quit()