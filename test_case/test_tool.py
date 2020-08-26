#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import time
import pytest
from public import api
from page_object.tool_page import ToolPage
from operate.operate_tool import OperateTool
from operate.operate_case import OperateCase


@pytest.fixture(scope='module')
def init_test_tool(login):
    # 实例化案件操作类和工具栏操作类
    operate_case = OperateCase(login)
    operate_case.switch_tab('案件列表')
    operate_tool = OperateTool(login)
    tool_page = ToolPage(login)
    yield operate_case, operate_tool, tool_page


class TestTool:
    @staticmethod
    def test_add_inspection_record(init_test_tool):
        operate_case, operate_tool, tool_page = init_test_tool
        """新增检验记录"""
        # 从excel读取数据
        data = api.read_excel('test_add_inspection_record')
        case_name = data.get('case_name')
        # 打开案件
        operate_case.open_case(case_name)
        operate_tool.add_inspection_record(**data)
        save_prompt_message = tool_page.prompt_message().text
        # 保存结果断言
        assert save_prompt_message == data.get('save_prompt_message')
        # 关闭提示信息窗口及二级窗口
        operate_tool.click_confirm_button()
        time.sleep(0.5)
        operate_tool.close_level_2_window()

    @staticmethod
    def test_insert_picture(init_test_tool):
        """给检验记录上传图片"""
        operate_case, operate_tool, tool_page = init_test_tool
        data = api.read_excel('test_insert_picture')
        file_path = data.get('file_path')
        file_name = file_path.split('\\')[-1]
        window_name = data.get('window_name')
        operate_case.switch_tab('案件列表')
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        # 打开检验记录
        inspection_record_window = operate_tool.open_inspection_record()
        operate_tool.switch_inspection_record_tab(inspection_record_window, '送检材料情况')
        # 上传图片
        operate_tool.upload_picture(file_path, window_name)
        # 断言：上传图片是否成功
        upload_prompt_message = tool_page.prompt_message().text
        assert upload_prompt_message == data.get('upload_prompt_message')
        tool_page.prompt_message_button(button_name='确定').click()
        time.sleep(0.5)
        # 将图片插入到检验记录正文
        operate_tool.insert_picture_to_text()
        time.sleep(0.5)
        # 断言：图片是否插入到文本域中
        textarea = tool_page.inspection_record_textarea(inspection_record_window)
        textarea_content = textarea.text
        print(textarea_content)
        assert textarea_content.count(file_name)
        time.sleep(0.5)
        # 点击【保存】按钮
        operate_tool.click_inspection_record_button('保存')
        time.sleep(0.5)
        # 关闭二级窗口
        operate_tool.click_confirm_button()
        time.sleep(0.5)
        operate_tool.close_level_2_window()

    # @staticmethod
    # def test_export_inspection_record(init_test_tool):
    #     """
    #     测试导出检验记录
    #     :return: None
    #     """
    #     # 从excel读取数据
    #     operate_case, operate_tool, tool_page = init_test_tool
    #     data = api.read_excel('test_export_inspection_record')
    #     case_name = data.get('case_name')
    #     file_path = data.get('file_path')
    #     window_name = data.get('window_name')
    #     # 打开案件
    #     operate_case.open_case(case_name)
    #     time.sleep(1)
    #     operate_tool.open_inspection_record()
    #     operate_tool.export_inspection_record(file_path, window_name)
    #     # 对结果进行断言
    #     export_prompt_message = tool_page.prompt_message().text
    #     assert export_prompt_message == data.get('export_prompt_message')
    #     # 还原测试环境，删除导出的文件
    #     api.remove_doc(data.get('file_path'))

    @staticmethod
    def test_add_identify_opinion(init_test_tool):
        """新增鉴定意见"""
        operate_case, operate_tool, tool_page = init_test_tool
        # 读取excel数据
        data = api.read_excel('test_add_identify_opinion')
        case_name = data.get('case_name')
        # 打开案件
        operate_case.open_case(case_name)
        # 打开鉴定意见
        operate_tool.open_identify_opinion()
        # 新增鉴定意见
        operate_tool.add_identify_opinion(**data)
        time.sleep(1)
        # 对结果进行断言
        save_prompt_message = tool_page.prompt_message().text
        assert save_prompt_message == data.get('save_prompt_message')
        # 关闭提示信息窗口及二级窗口
        operate_tool.click_confirm_button()
        operate_tool.close_level_2_window()

    @staticmethod
    def test_export_identify_opinion(init_test_tool):
        """导出鉴定意见"""
        operate_case, operate_tool, tool_page = init_test_tool
        data = api.read_excel('test_export_identify_opinion')
        case_name = data.get('case_name')
        file_path = data.get('file_path')
        window_name = data.get('window_name')
        # 打开案件
        operate_case.open_case(case_name)
        time.sleep(1)
        operate_tool.open_identify_opinion()
        operate_tool.export_identify_opinion(file_path, window_name)
        # 对结果进行断言
        export_prompt_message = tool_page.prompt_message().text
        assert export_prompt_message == data.get('export_prompt_message')
        # 关闭提示信息窗口及二级窗口
        operate_tool.click_confirm_button()
        operate_tool.close_level_2_window()
        # 还原测试环境，删除导出的文件
        api.remove_doc(data.get('file_path'))


if __name__ == '__main__':
    pytest.main()
