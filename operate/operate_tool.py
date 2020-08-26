#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import time
from selenium.webdriver import ActionChains
from public import api
from page_object.tool_page import ToolPage
from page_object.case_page import CasePage


class OperateTool:
    def __init__(self, browser):
        self.browser = browser
        self.tool_page = ToolPage(self.browser)
        self.case_page = CasePage(self.browser)

    def click_tool_button(self, button_name):
        """
        点击工具栏按钮
        :return: None
        """
        if button_name in ('播放', '报告'):
            self.tool_page.tool_button2(button_name).click()
        else:
            self.tool_page.tool_button(button_name).click()

    def open_inspection_record(self):
        """
        打开检验记录窗口
        :return: 检验记录窗口对象
        """
        # 点击报告按钮
        self.click_tool_button('报告')
        # 点击打开检验记录
        self.tool_page.report(report_type='检验记录').click()
        # 定位“检验记录”窗口
        inspection_record_window = api.level_2_window(self.browser)
        return inspection_record_window

    def click_inspection_record_button(self, button_name):
        """点击检验记录窗口的【插入图片】【预览】【保存】【导出】按钮"""
        inspection_record_window = api.level_2_window(self.browser)
        self.tool_page.inspection_record_button(inspection_record_window, button_name).click()

    def add_inspection_record(self, **data):
        """ 添加检验记录 """
        # 打开检验记录窗口
        inspection_record_window = self.open_inspection_record()
        time.sleep(1)
        # 对“报告标题”标签页进行输入
        title = self.tool_page.inspection_record_input(inspection_record_window, field_name='标题')
        title.clear()
        title.send_keys(data.get('title'))
        join_no = self.tool_page.inspection_record_input(inspection_record_window, field_name='参加编号')
        join_no.clear()
        join_no.send_keys(data.get('join_no'))
        page_header = self.tool_page.inspection_record_input(inspection_record_window, field_name='页眉')
        page_header.clear()
        page_header.send_keys(data.get('page_header'))
        page_footer = self.tool_page.inspection_record_input(inspection_record_window, field_name='页脚')
        page_footer.clear()
        page_footer.send_keys(data.get('page_footer'))
        time.sleep(1)
        # 对“送检材料情况”标签页进行输入
        self.tool_page.inspection_record_tab(inspection_record_window, tab_name='送检材料情况').click()
        time.sleep(1)
        title_1 = self.tool_page.inspection_record_title_input(inspection_record_window)
        title_1.clear()
        title_1.send_keys(data.get('title_1'))
        textarea_1 = self.tool_page.inspection_record_textarea(inspection_record_window)
        textarea_1.clear()
        textarea_1.send_keys(data.get('textarea_1'))
        # 对“检材、样本的采集”标签页进行输入
        self.tool_page.inspection_record_tab(inspection_record_window, tab_name='检材、样本的采集').click()
        time.sleep(1)
        title_2 = self.tool_page.inspection_record_title_input(inspection_record_window)
        title_2.clear()
        title_2.send_keys(data.get('title_2'))
        textarea_2 = self.tool_page.inspection_record_textarea(inspection_record_window)
        textarea_2.clear()
        textarea_2.send_keys(data.get('textarea_2'))
        # 对“总体情况”标签页进行输入
        self.tool_page.inspection_record_tab(inspection_record_window, tab_name='总体情况').click()
        time.sleep(1)
        title_3 = self.tool_page.inspection_record_title_input(inspection_record_window)
        title_3.clear()
        title_3.send_keys(data.get('title_3'))
        textarea_3 = self.tool_page.inspection_record_textarea(inspection_record_window)
        textarea_3.clear()
        textarea_3.send_keys(data.get('textarea_3'))
        # 对“检验分析”标签页进行输入
        self.tool_page.inspection_record_tab(inspection_record_window, tab_name='检验分析').click()
        time.sleep(1)
        title_4 = self.tool_page.inspection_record_title_input(inspection_record_window)
        title_4.clear()
        title_4.send_keys(data.get('title_4'))
        textarea_4 = self.tool_page.inspection_record_textarea(inspection_record_window)
        textarea_4.clear()
        textarea_4.send_keys(data.get('textarea_4'))
        time.sleep(1)
        # 输入听辨分析内容
        self.tool_page.inspection_record_left_common(inspection_record_window, '听辩分析').click()
        title_4_1 = self.tool_page.inspection_record_title_input(inspection_record_window)
        title_4_1.clear()
        title_4_1.send_keys(data.get('title_4_1'))
        textarea_4_1 = self.tool_page.inspection_record_textarea(inspection_record_window)
        textarea_4_1.clear()
        textarea_4_1.send_keys(data.get('textarea_4_1'))
        time.sleep(1)
        # 输入分析及校验内容
        self.tool_page.inspection_record_left_common(inspection_record_window, '分析及检验').click()
        title_4_2 = self.tool_page.inspection_record_title_input(inspection_record_window)
        title_4_2.clear()
        title_4_2.send_keys(data.get('title_4_2'))
        textarea_4_2 = self.tool_page.inspection_record_textarea(inspection_record_window)
        textarea_4_2.clear()
        textarea_4_2.send_keys(data.get('textarea_4_2'))
        time.sleep(1)
        # 输入比对检验结果
        self.tool_page.inspection_record_left_common(inspection_record_window, '比对检验结果').click()
        title_4_2_1 = self.tool_page.inspection_record_title_input(inspection_record_window)
        title_4_2_1.clear()
        title_4_2_1.send_keys(data.get('title_4_2_1'))
        textarea_4_2_1 = self.tool_page.inspection_record_textarea(inspection_record_window)
        textarea_4_2_1.clear()
        textarea_4_2_1.send_keys(data.get('textarea_4_2_1'))
        time.sleep(1)
        # 对“综合评断”标签页进行输入
        self.tool_page.inspection_record_tab(inspection_record_window, tab_name='综合评断').click()
        time.sleep(1)
        title_5 = self.tool_page.inspection_record_title_input(inspection_record_window)
        title_5.clear()
        title_5.send_keys(data.get('title_5'))
        textarea_5 = self.tool_page.inspection_record_textarea(inspection_record_window)
        textarea_5.clear()
        textarea_5.send_keys(data.get('textarea_5'))
        # 对“鉴定结论”标签页进行输入
        self.tool_page.inspection_record_tab(inspection_record_window, tab_name='鉴定结论').click()
        time.sleep(1)
        title_6 = self.tool_page.inspection_record_title_input(inspection_record_window)
        title_6.clear()
        title_6.send_keys(data.get('title_6'))
        textarea_6 = self.tool_page.inspection_record_textarea(inspection_record_window)
        textarea_6.clear()
        textarea_6.send_keys(data.get('textarea_6'))
        time.sleep(1)
        self.click_inspection_record_button('保存')

    def upload_picture(self, file_path, insert_window_name):
        self.click_inspection_record_button("插入图片")
        insert_picture_window = self.tool_page.insert_picture_window()
        self.tool_page.upload_picture_button(insert_picture_window).click()
        api.import_file(file_path, insert_window_name)
        time.sleep(3)

    def del_picture(self, picture_name):
        self.case_page.unfold_and_hide_button(folder_name='我的图片').click()
        time.sleep(0.5)
        picture_file = self.case_page.find_file_by_name(picture_name)
        picture_file.click()
        time.sleep(0.5)
        ActionChains(self.browser).context_click(picture_file).perform()
        self.case_page.file_context_menu('删除').click()
        time.sleep(0.5)
        prompt_window = api.level_2_window(self.browser)
        self.case_page.window_button(prompt_window, '确定').click()

    def export_inspection_record(self, file_path, window_name):
        """
        导出检验记录
        :param file_path: 文件保存路径及名称
        :param window_name: 导出窗口名
        :return: None
        """
        # 定位检验记录窗口
        inspection_record_window = api.level_2_window(self.browser)
        self.tool_page.inspection_record_button(inspection_record_window, '导出').click()
        self.click_inspection_record_button("导出")
        api.export_file(file_path, window_name)
        time.sleep(5)

    def open_identify_opinion(self):
        """
        打开【鉴定意见】
        :return: None
        """
        # 点击报告按钮
        self.click_tool_button('报告')
        # 点击打开检验记录
        self.tool_page.report(report_type='鉴定意见').click()

    def switch_inspection_record_tab(self, window, tab_name):
        """切换检验记录标签页"""
        self.tool_page.inspection_record_tab(window, tab_name).click()

    def add_identify_opinion(self, **data):
        # 定位鉴定意见窗口
        identify_opinion_window = api.level_2_window(self.browser)
        # 输入标题
        title = self.tool_page.identify_opinion_input(identify_opinion_window, '标题')
        title.clear()
        title.send_keys(data.get('title'))
        # 输入页眉
        page_header = self.tool_page.identify_opinion_input(identify_opinion_window, '页眉')
        page_header.clear()
        page_header.send_keys(data.get('page_header'))
        # 输入页脚
        page_footer = self.tool_page.identify_opinion_input(identify_opinion_window, '页脚')
        page_footer.clear()
        page_footer.send_keys(data.get('page_footer'))
        time.sleep(1)
        # 切换到案件简介标签页进行输入
        self.tool_page.identify_opinion_tab(identify_opinion_window, '案件简介').click()
        title_1 = self.tool_page.identify_opinion_input(identify_opinion_window, '一')
        title_1.clear()
        title_1.send_keys(data.get('title_1'))
        textarea_1 = self.tool_page.identify_opinion_textarea(identify_opinion_window)
        textarea_1.clear()
        textarea_1.send_keys(data.get('textarea_1'))
        time.sleep(1)
        # 切换到比对结果进行输入
        self.tool_page.identify_opinion_tab(identify_opinion_window, '比对结果').click()
        title_3 = self.tool_page.identify_opinion_input(identify_opinion_window, '三')
        title_3.clear()
        title_3.send_keys(data.get('title_3'))
        textarea_3 = self.tool_page.identify_opinion_textarea(identify_opinion_window)
        textarea_3.clear()
        textarea_3.send_keys(data.get('textarea_3'))
        identifier = self.tool_page.identify_opinion_input(identify_opinion_window, '鉴定人')
        identifier.clear()
        identifier.send_keys(data.get('identifier'))
        identify_data = self.tool_page.identify_opinion_input(identify_opinion_window, '鉴定日期')
        identify_data.clear()
        identify_data.send_keys(data.get('identify_data'))
        time.sleep(1)
        self.tool_page.identify_opinion_button(identify_opinion_window, '保存').click()
        time.sleep(1)

    def export_identify_opinion(self, file_path, window_name):
        """
        导出鉴定意见
        :param file_path: 文件路径及文件名
        :param window_name: 导出窗口标题
        :return: None
        """
        # 定位鉴定意见窗口
        identify_opinion_window = api.level_2_window(self.browser)
        self.tool_page.identify_opinion_button(identify_opinion_window, '导出').click()
        api.export_file(file_path, window_name)
        time.sleep(5)

    def insert_picture_to_text(self):
        """
        将图片插入到检验记录正文
        :return: None
        """
        picture_window = self.tool_page.insert_picture_window()
        self.tool_page.import_picture_button(picture_window).click()

    def click_confirm_button(self):
        # 点击提示窗口【确定】按钮
        self.tool_page.prompt_message_button('确定').click()

    def close_level_2_window(self):
        """"""
        level_2_window = api.level_2_window(self.browser)
        api.close_window_button(level_2_window).click()

    def close_level_3_window(self):
        """"""
        level_3_window = api.level_3_window(self.browser)
        api.close_window_button(level_3_window).click()


if __name__ == '__main__':
    ...
