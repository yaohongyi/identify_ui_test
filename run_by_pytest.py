#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import os
import shutil

# 删除测试报告目录
try:
    shutil.rmtree('./report')
except FileNotFoundError:
    ...

# 运行测试用例并生成测试结果数据
create_report_command = 'pytest ./test_case/test_view.py -k test_add_tag'
# create_report_command = 'pytest -q --alluredir report'  # 执行所有模块
os.system(create_report_command)

# 将测试结果数据转换为HTML报告
# generate_report_html = 'allure generate report/ -o report/html --clean'
# os.system(generate_report_html)
