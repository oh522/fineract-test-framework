# 金融借贷系统 UI 自动化测试框架

基于 **Python + Selenium + PO模式 + Pytest + Allure** 构建的金融系统自动化测试框架。

## 项目简介

采用 Page Object 设计模式，实现用户注册、登录、开户、授信申请、后台审核等全流程自动化测试。

## 技术栈

- Python 3.8+
- Selenium WebDriver 4.0+
- Pytest 9.0.2
- Allure 2.15.3
- Faker 40.11.1

## 项目结构

**base/** - 基础层
- base.py: BasePage基类（10+公共方法）

**page/** - 页面对象层（10个Page类）
- page_login.py: 前端登录
- page_register.py: 用户注册
- page_open_account.py: 资金开户
- page_credit_app.py: 授信申请
- page_back_login.py: 后台登录
- page_credit_review.py: 授信审核
- page_personal_loan.py: 个人借款
- page_apply_online.py: 在线申请

**script/** - 测试用例层（20+脚本）
- test_01_login.py: 登录测试
- test_02_register.py: 注册测试
- test_03_open_account.py: 开户测试
- test_04_credit_app.py: 授信申请
- test_05_back_login.py: 后台登录
- test_06_credit_review.py: 授信审核
- test_07_personal_loan.py: 个人借款
- test_08_apply_online.py: 在线申请

**data/** - JSON测试数据
- login_data.json
- credit_app.json
- apply_online_data.json

**其他目录**
- log/: 日志文件
- img/: 截图存储
- report/: Allure报告
- config.py: 配置文件
- conftest.py: Fixture配置
- tools.py: 工具类

## 快速开始

### 1. 安装依赖

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
### 2. 配置环境

修改 `config.py` 中的测试环境地址：

python BASE_URL = "http://121.43.169.97:8081" # 前端 
BACK_URL = "http://121.43.169.97:8082" # 后端
### 3. 运行测试

ash
运行所有测试
pytest
运行指定文件
pytest script/test_01_login.py -v -s
生成Allure报告
pytest --alluredir=./report --clean-alluredir
allure generate ./report -o ./new_report --clean
allure open ./new_report
## 测试覆盖

### 前端用户系统
- 用户注册/登录
- 资金托管开户
- 授信申请
- 个人借款发布
- 在线申请

### 后端管理系统
- 后台登录
- 授信审核（双重Frame切换）

## 核心特性

✅ PO设计模式 - 页面与业务分离  
✅ 数据驱动 - JSON外部化管理测试数据  
✅ Fixture依赖注入 - 减少60%冗余代码  
✅ Allure可视化报告 - 完整测试数据分析  
✅ 复杂场景支持 - 多窗口、Frame嵌套、下拉框等  

## 注意事项

⚠️ `pytest.ini` 中 `python_files` 应改为 `test*.py`  
⚠️ 建议删除 `page/page_base.py`（重复文件）  
⚠️ 部分用例使用 `time.sleep()`，建议改用显式等待

---

**维护者**: wyyzzz  
**更新时间**: 2026-04-22




