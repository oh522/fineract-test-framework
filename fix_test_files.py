# fix_test_files.py（完整替换）
import os
import re

auto_gen_dir = "testcase/auto_gen"

for root, dirs, files in os.walk(auto_gen_dir):
    for file in files:
        if not file.endswith(".py"):
            continue

        filepath = os.path.join(root, file)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        original = content

        # 1. 去掉 BaseApi 导入
        content = re.sub(r"from api_test\.common\.base_api import BaseApi\n", "", content)

        # 2. class TestXxx(BaseApi): → class TestXxx:
        content = re.sub(r"class (Test\w+)\(BaseApi\):", r"class \1:", content)

        # 3. 修复重复 api 参数
        content = re.sub(r"def (test_\w+)\(self,\s*api,\s*api([^)]*)\):", r"def \1(self, api\2):", content)

        # 4. 给没有 api 参数的 test 方法加上 api
        def add_api_if_missing(m):
            full = m.group(0)
            if "api" in full:
                return full
            full = re.sub(r"\(self\):", "(self, api):", full)
            full = re.sub(r"\(self,\s*", "(self, api, ", full)
            return full
        content = re.sub(r"def test_\w+\(self[^)]*\):", add_api_if_missing, content)

        # 5. self.get/post/put/delete/patch → api.方法
        content = re.sub(r"\bself\.(get|post|put|delete|patch)\(", r"api.\1(", content)

        # 6. ✅ 关键修复：去掉路径里重复的 /v1
        # "/v1/loans" → "/loans"
        content = re.sub(r'(api\.\w+\s*\([^,]*?)"/v1/', r'\1"/', content)
        content = re.sub(r"(api\.\w+\s*\([^,]*?)'/v1/", r"\1'/", content)
        # f-string 路径
        content = re.sub(r'(api\.\w+\s*\([^,]*?)f"/v1/', r'\1f"/', content)
        content = re.sub(r"(api\.\w+\s*\([^,]*?)f'/v1/", r"\1f'/", content)

        # 7. BASE_PATH / endpoint 里的 /v1 也去掉
        content = re.sub(r'(BASE_PATH\s*=\s*)"/v1/', r'\1"/', content)
        content = re.sub(r"(BASE_PATH\s*=\s*)'/v1/", r"\1'/", content)
        content = re.sub(r'(endpoint\s*=\s*)"/v1/', r'\1"/', content)

        # 8. self.base_path / self.endpoint → self.BASE_PATH
        content = re.sub(r"(\s+)base_path\s*=\s*(\"[^\"]+\")", r"\1BASE_PATH = \2", content)
        content = re.sub(r"\bself\.base_path\b", "self.BASE_PATH", content)
        content = re.sub(r"\bself\.endpoint\b", "self.BASE_PATH", content)

        if content != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ 已修复：{filepath}")
        else:
            print(f"⏭️  无需修改：{filepath}")

print("\n🎉 批量修复完成！")