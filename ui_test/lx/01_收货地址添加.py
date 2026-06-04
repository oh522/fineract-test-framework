import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


# 创建浏览器对象
driver = webdriver.Edge()
# 访问网页
driver.get("http://tp123.com/Home/user/login.html/")
# 窗口最大化
driver.maximize_window()
# 输入用户名
els = driver.find_element(by=By.ID, value="username")
els.send_keys("13800138006")
# 输入密码
driver.find_element(by=By.ID, value="password").send_keys("123456")
# 输入验证码
code_input = driver.find_element(by=By.NAME, value="verify_code")
# 弹出输入框，让你手动看页面输入验证码
verify_code = input("请输入页面上的验证码，输入后按回车：")
code_input.send_keys(verify_code)
# 点击登录
# (WebDriverWait(driver, 10).
#  until(EC.visibility_of_element_located((By.CLASS_NAME, "J-login-submit"))).click())#等待元素可见
driver.find_element(by=By.CLASS_NAME, value="J-login-submit").click()
# 等待三秒
# time.sleep(3)
(WebDriverWait(driver, 10).
 until(EC.visibility_of_element_located((By.XPATH, '//*[text()="王然啊啊啊啊啊啊"]'))))
result = driver.find_element(by=By.XPATH, value='//*[text()="王然啊啊啊啊啊啊"]').text
assert result == "王然啊啊啊啊啊啊"
#进入账户设置
ele1 = (WebDriverWait(driver, 10).
        until(EC.element_to_be_clickable((By.XPATH, "//span[text()='账户设置']"))))#等待元素可点击
action = ActionChains(driver)#创建鼠标操作对象
action.move_to_element(ele1).perform()#鼠标悬停
#点击收获地址
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[2][text()="收货地址"]'))).click()
# driver.find_element(by=By.XPATH, value='//a[2][text()="收货地址"]').click()要加隐式等待
#新增收货地址
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="增加新地址"]'))).click()
# driver.find_element(by=By.XPATH, value='//span[text()="增加新地址"]').click()要加隐式等待
#收货人
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'consignee'))).send_keys("王然")
#手机或固定电话
driver.find_element(by=By.NAME, value='mobile').send_keys("13562457894")
#收货地址
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "province"))
)
select1 = Select(driver.find_element(by=By.ID, value="province"))
select1.select_by_value("1")
(WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "city"))))
select2 = Select(driver.find_element(by=By.ID, value="city"))
select2.select_by_value("2")
(WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "district"))))
select3 = Select(driver.find_element(by=By.ID, value="district"))
select3.select_by_value("3")
#详细地址
driver.find_element(by=By.NAME, value='address').send_keys("中山南路")
#保存//*[@id="address_submit"]
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="address_submit"]'))
).click()

time.sleep(2)
# 推出浏览器.red.userinfo
driver.quit()