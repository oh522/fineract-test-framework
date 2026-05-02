import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

BASE_URL = "http://localhost:4200"


@pytest.fixture(scope="session")
def browser():
    """启动浏览器，整个测试会话共用"""
    options = webdriver.EdgeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-notifications")
    # options.add_argument("--headless")  # 无头模式取消注释

    driver = webdriver.Edge(
        service=Service(EdgeChromiumDriverManager().install()),
        options=options
    )
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def logged_in_browser(browser):
    """已登录状态的浏览器，其他UI用例直接用这个"""
    from ui_test.pages.login_page import LoginPage

    login = LoginPage(browser)
    login.open(BASE_URL + "/#/login")
    login.login("mifos", "password")
    yield browser


@pytest.fixture(scope="function")
def fresh_browser(browser):
    """每个用例执行前清理cookies，保证独立性"""
    browser.delete_all_cookies()
    yield browser