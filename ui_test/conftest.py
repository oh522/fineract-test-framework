import pytest
from selenium import webdriver
from page.page_apply_online import ApplyOnline
from page.page_apply_online_json import ApplyOnline as ApplyOnlineJson
from page.page_back_login import BackLogin
from page.page_credit_app import CreditAppPage
from page.page_credit_review import PageCreditReview
from page.page_login import PageLogin
from page.page_open_account import OpenAccount
from page.page_personal_loan import PersonalLoan
from page.page_register import Register
@pytest.fixture()
def browser():
    driver = webdriver.Edge()
    driver.maximize_window()
    driver.implicitly_wait(10)  # 隐式等待 10 秒
    yield driver
    driver.quit()
@pytest.fixture()#test01
def a_login(browser):
    page_login = PageLogin(browser)
    page_login.open_url()
    return page_login
@pytest.fixture()#test03
def a_open_account(browser, a_login):
    # page_open_account = OpenAccount(browser)  # 创建页面对象
    # page_login = PageLogin(browser)
    # page_login.open_url()
    # page_login.login("13866801667", "Aa123456")
    # return page_open_account
    a_login.login("13866801668", "Aa123456")
    page_open_account = OpenAccount(browser)
    return page_open_account
@pytest.fixture()#test02
def go_register_page(browser):
    go_register = Register(browser)
    go_register.open_url()
    return go_register
# ... existing code ...
@pytest.fixture()#test04
def go_credit_app(browser):
    """返回已登录状态下的授信申请页面对象"""
    go_login = PageLogin(browser)
    go_login.open_url()
    go_login.login("13866801667", "Aa123456")
    credit_app = CreditAppPage(browser)
    return credit_app
#多用户登录测试#
# ... existing code ...
# @pytest.fixture(params=read_json("login_data.json"))
# def login_credentials(request):
#     """提供多组登录数据的 fixture"""
#     return request.param
#
# @pytest.fixture()#test04
# def go_credit_app(browser, login_credentials):
#     """返回已登录状态下的授信申请页面对象，支持多组登录数据"""
#     username, password = login_credentials
#     go_login = PageLogin(browser)
#     go_login.open_url()
#     go_login.login(username, password)
#     credit_app = CreditAppPage(browser)
#     return credit_app#duo#
@pytest.fixture()#test05
def go_back_login(browser):
    back_login = BackLogin(browser)
    back_login.open_url()
    back_login.get_shot("back_login.png")
    return back_login
@pytest.fixture()#test06
def go_credit_review(browser):
    """返回已登录状态下的授信审核页面对象"""
    go_back_login = BackLogin(browser)
    go_back_login.open_url()
    go_back_login.input_info("admin", "HM_2025_test", "8888")
    go_back_login.click_login_button()
    credit_review = PageCreditReview(browser)
    credit_review.menu_manager()
    credit_review.search_record("13800001001")
    credit_review.select_record()
    credit_review.get_shot("credit_review.png")
    return credit_review
@pytest.fixture()#test07
def go_personal_loan(browser, a_login):
    """返回已登录状态下的个人借款页面对象"""
    a_login.login("13800001001", "Aa123456")
    personal_loan = PersonalLoan(browser)
    return personal_loan
@pytest.fixture()#test08
def go_apply_online(browser):
    """返回已登录状态下的在线申请页面对象"""
    a_login = PageLogin(browser)
    a_login.open_url()
    a_login.login("13800001001", "Aa123456")
    apply_online = ApplyOnline(browser)
    return apply_online

@pytest.fixture()#test08_json
def go_apply_online_json(browser):
    """返回已登录状态下的在线申请页面对象（JSON数据驱动版本）"""
    a_login = PageLogin(browser)
    a_login.open_url()
    a_login.login("13800001001", "Aa123456")
    apply_online_json = ApplyOnlineJson(browser)
    return apply_online_json








