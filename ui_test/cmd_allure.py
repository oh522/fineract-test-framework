import os

# 生成 allure 报告
run_cmd = "allure generate ./report -o ./new_report --clean"
os.system(run_cmd)

