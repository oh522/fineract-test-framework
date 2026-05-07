import pytest


class TestDownloadClientTemplate:
    """Download client template for bulk import"""

    BASE_PATH = "/clients/downloadtemplate"

    # 正常用例数据
    normal_cases = [
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 1, "staffId": 1, "dateFormat": "dd MMMM yyyy"},
            id="all_params_provided"
        ),
        pytest.param(
            {"legalFormType": "ORGANIZATION", "officeId": 2, "staffId": 3, "dateFormat": "yyyy-MM-dd"},
            id="different_legal_form"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 1, "staffId": 1, "dateFormat": "dd/MM/yyyy"},
            id="different_date_format"
        ),
    ]

    # 参数缺失用例数据
    missing_params_cases = [
        pytest.param(
            {"officeId": 1, "staffId": 1, "dateFormat": "dd MMMM yyyy"},
            id="missing_legalFormType"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "staffId": 1, "dateFormat": "dd MMMM yyyy"},
            id="missing_officeId"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 1, "dateFormat": "dd MMMM yyyy"},
            id="missing_staffId"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 1, "staffId": 1},
            id="missing_dateFormat"
        ),
        pytest.param(
            {},
            id="all_params_missing"
        ),
    ]

    # 边界值用例数据
    boundary_cases = [
        pytest.param(
            {"legalFormType": "", "officeId": 1, "staffId": 1, "dateFormat": "dd MMMM yyyy"},
            id="empty_legalFormType"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 0, "staffId": 1, "dateFormat": "dd MMMM yyyy"},
            id="officeId_zero"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 1, "staffId": 0, "dateFormat": "dd MMMM yyyy"},
            id="staffId_zero"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 999999999, "staffId": 1, "dateFormat": "dd MMMM yyyy"},
            id="officeId_max_value"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 1, "staffId": 999999999, "dateFormat": "dd MMMM yyyy"},
            id="staffId_max_value"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": -1, "staffId": 1, "dateFormat": "dd MMMM yyyy"},
            id="officeId_negative"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 1, "staffId": -1, "dateFormat": "dd MMMM yyyy"},
            id="staffId_negative"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 1, "staffId": 1, "dateFormat": ""},
            id="empty_dateFormat"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 1, "staffId": 1, "dateFormat": "invalid_format"},
            id="invalid_dateFormat"
        ),
    ]

    # 异常用例数据
    error_cases = [
        pytest.param(
            {"legalFormType": 123, "officeId": 1, "staffId": 1, "dateFormat": "dd MMMM yyyy"},
            id="legalFormType_as_integer"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": "abc", "staffId": 1, "dateFormat": "dd MMMM yyyy"},
            id="officeId_as_string"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 1, "staffId": "xyz", "dateFormat": "dd MMMM yyyy"},
            id="staffId_as_string"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 1.5, "staffId": 1, "dateFormat": "dd MMMM yyyy"},
            id="officeId_as_float"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 1, "staffId": 2.5, "dateFormat": "dd MMMM yyyy"},
            id="staffId_as_float"
        ),
        pytest.param(
            {"legalFormType": "INVALID_TYPE", "officeId": 1, "staffId": 1, "dateFormat": "dd MMMM yyyy"},
            id="invalid_legalFormType"
        ),
        pytest.param(
            {"legalFormType": "PERSON", "officeId": 1, "staffId": 1, "dateFormat": 12345},
            id="dateFormat_as_integer"
        ),
    ]

    @pytest.mark.parametrize("params", normal_cases)
    def test_download_template_normal(self, api, params):
        """
        正常用例：使用正确参数下载模板
        验证：状态码200，响应包含Excel文件内容
        """
        resp = api.get(self.BASE_PATH, params=params)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        content_type = resp.headers.get("Content-Type", "")
        assert "application/vnd.ms-excel" in content_type or "application/octet-stream" in content_type, \
            f"Expected Excel content type, got {content_type}"
        assert len(resp.content) > 0, "Response content should not be empty"
        # 验证响应头包含文件下载相关信息
        content_disposition = resp.headers.get("Content-Disposition", "")
        assert "attachment" in content_disposition or "filename" in content_disposition, \
            f"Expected file download headers, got {content_disposition}"

    @pytest.mark.parametrize("params", missing_params_cases)
    def test_download_template_missing_params(self, api, params):
        """
        参数缺失用例：缺少必填参数
        验证：状态码400或422，返回错误信息
        """
        resp = api.get(self.BASE_PATH, params=params)
        assert resp.status_code in [400, 422], f"Expected 400 or 422, got {resp.status_code}"
        response_data = resp.json()
        assert "errors" in response_data or "error" in response_data, \
            f"Expected error information in response: {response_data}"
        # 验证错误信息包含缺失参数提示
        error_msg = str(response_data)
        missing_params = [k for k in ["legalFormType", "officeId", "staffId", "dateFormat"] if k not in params]
        for param in missing_params:
            assert param.lower() in error_msg.lower(), f"Expected error about missing {param}"

    @pytest.mark.parametrize("params", boundary_cases)
    def test_download_template_boundary(self, api, params):
        """
        边界值用例：测试边界值和特殊值
        验证：根据输入返回适当响应（成功或错误）
        """
        resp = api.get(self.BASE_PATH, params=params)
        # 空字符串和无效格式可能返回错误，其他边界值可能成功
        if params.get("legalFormType") == "" or params.get("dateFormat") in ["", "invalid_format"]:
            assert resp.status_code in [400, 422], f"Expected 400 or 422 for empty/invalid values, got {resp.status_code}"
            response_data = resp.json()
            assert "errors" in response_data or "error" in response_data
        elif params.get("officeId") == 0 or params.get("staffId") == 0:
            # 零值可能被视为有效或无效，取决于业务逻辑
            assert resp.status_code in [200, 400, 422], f"Unexpected status code: {resp.status_code}"
        elif params.get("officeId") == -1 or params.get("staffId") == -1:
            # 负值通常无效
            assert resp.status_code in [400, 422], f"Expected 400 or 422 for negative values, got {resp.status_code}"
        else:
            assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"