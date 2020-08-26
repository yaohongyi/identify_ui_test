#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
from public import api
from page_object.right_page import RightPage
from operate.operate_tool import OperateTool


class OperateRight:
    def __init__(self, browser):
        self.browser = browser
        self.right_page = RightPage(self.browser)

    def switch_tab(self, tab_name):
        """
        切换右侧窗口标签页
        :param tab_name: 标签页名称
        :return: None
        """
        right_window = self.right_page.right_window()
        self.right_page.right_window_tab(right_window, tab_name).click()

    def add_measurement_record(self, button_index):
        """
        新增图谱测量记录
        :param button_index: 0-灰色，1-黄色，2-粉色，3-绿色，4-兰色，5-紫色
        :return: None
        """
        right_window = self.right_page.right_window()
        self.right_page.append_record_button(right_window, button_index).click()


if __name__ == '__main__':
    driver = api.login()
    # 打开案件
    from operate.operate_case import OperateCase
    operate_case = OperateCase(driver)
    operate_case.open_case('都君AutoTest')
    # 打开图谱测量
    from operate.operate_tool import OperateTool
    operate_tool = OperateTool(driver)
    operate_tool.click_tool_button('图谱测量')
    # 新增测量记录
    operate_right = OperateRight(driver)
    operate_right.add_measurement_record(0)
    operate_right.add_measurement_record(1)
