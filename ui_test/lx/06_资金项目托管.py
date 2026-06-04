# 导包
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 创建浏览器对象
driver = webdriver.Edge()
# 访问网页
driver.get("http://121.43.169.97:8081/")
driver.maximize_window()
#有奖注册
driver.find_element(by=By.LINK_TEXT, value='有奖注册').click()
#手机号码
driver.find_element(by=By.ID, value='phone').send_keys("13562457707")
#登录密码
driver.find_element(by=By.ID, value='password').send_keys("12345wq")
#验证码
driver.find_element(by=By.ID, value='verifycode').send_keys("8888")
#获取验证码
driver.find_element(by=By.ID, value='get_phone_code').click()
time.sleep(2)
driver.find_element(by=By.ID, value='phone_code').send_keys("666666")
#提交
driver.find_element(by=By.CLASS_NAME, value='lg-btn').click()
time.sleep(2)
#验证注册成功
# result = driver.find_element(by=By.CSS_SELECTOR, value='div.reg-step-last > h1').text
result = driver.find_element(by=By.CLASS_NAME, value='reg-step-last').text
assert "注册成功" in result

#开通资金托管//*[@id="step3"]/div/div/div/div/a/text()
driver.find_element(by=By.XPATH, value='//a[text()="开通资金托管"]').click()
#真实姓名
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "realname"))).send_keys("张三")
#身份证号
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "card_id"))).send_keys("123456789012345661")
#确认提交
driver.find_element(by=By.CLASS_NAME, value='btn').click()
#开通资金托管
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn.ng-scope'))).click()
#验证开通成功
time.sleep(2)
handles = driver.window_handles
driver.switch_to.window(handles[1])
result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body'))).text
assert "User" in result
print( result)


##
# 等待三秒
time.sleep(2)
# 推出浏览器
driver.quit()