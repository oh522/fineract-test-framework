# Fineract 自动化测试框架

基于 Python + pytest 的 Fineract（Apache Fineract / Mifos X）开源金融平台自动化测试框架，支持 **API 接口测试**、**UI 自动化测试** 和 **数据库验证**。

---

## 📋 目录

- [功能特性](#-功能特性)
- [技术栈](#-技术栈)
- [项目结构](#-项目结构)
- [快速开始](#-快速开始)
- [配置说明](#-配置说明)
- [测试用例编写](#-测试用例编写)
- [运行测试](#-运行测试)
- [测试报告](#-测试报告)
- [最佳实践](#-最佳实践)

---

## ✨ 功能特性

- **API 接口测试**：基于 `requests` 库，封装统一的 API 请求基类
- **UI 自动化测试**：基于 Selenium + Edge 浏览器，支持 Page Object 模式
- **数据库验证**：支持 MySQL/MariaDB 数据库连接与数据校验
- **全局认证**：自动处理 Basic Auth 和 Token 管理
- **数据驱动测试**：支持 pytest 参数化测试
- **Allure 报告**：生成美观的测试报告，支持 CI/CD 集成
- **AI 用例生成**：内置 AI 辅助测试用例生成工具

---

## 🛠 技术栈

| 技术/工具 | 版本 | 用途 |
|----------|------|------|
| Python | 3.8+ | 核心开发语言 |
| pytest | >=8.0 | 测试框架 |
| requests | >=2.31.0 | HTTP API 请求 |
| PyYAML | >=6.0 | 配置文件解析 |
| PyMySQL | >=1.1.0 | 数据库连接 |
| selenium | >=4.15.0 | UI 自动化测试 |
| allure-pytest | >=2.13.0 | 测试报告生成 |
| Edge Browser | Chromium | UI 测试浏览器 |

---

## 📁 项目结构

- **fineract-test-framework/**
  - **api_test/** - API 测试模块
    - `common/`
      - `base_api.py` - API 请求基类
    - `data/`
      - `test_data.json` - 测试数据
    - `testcase/` - 测试用例
      - `test_client.py` - 客户相关测试
      - `reports/` - API 测试报告
  
  - **ui_test/** - UI 测试模块
    - `pages/` - 页面对象
      - `login_page.py` - 登录页面
    - `screenshots/` - 截图保存
    - `testcases/` - UI 测试用例
  
  - **testcase/auto_gen/** - 自动生成的测试用例
    - `Client/` - 客户接口测试
    - `Loans/` - 贷款接口测试
    - `Savings Account/` - 储蓄账户测试
  
  - **config/**
    - `config.yaml` - 全局配置文件
  
  - **utils/**
    - `db_helper.py` - 数据库辅助类
    - `ai_case_gen.py` - AI 用例生成器
  
  - `conftest.py` - 全局 pytest 配置
  - `pytest.ini` - pytest 配置
  - `requirements.txt` - 依赖包
  - `README.md` - 项目文档

# ... existing code ...
