#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
"""
右侧视图窗口元素，窗口包含：图谱测试量、测量比对、3D展示、操作日志、偏差分析、声纹比对、偏差分析结果
"""
from public import api


class RightPage:
    def __init__(self, browser):
        self.browser = browser

    def right_window(self):
        """
        定位右侧视图窗口，窗口包含：图谱测试量、测量比对、3D展示、操作日志、偏差分析、声纹比对、偏差分析结果
        :return: 右侧视图窗口元素对象
        """
        value = "//div[@class='right-wrap']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    def atlas_color(self, color):
        """定位图谱测量下的 选择颜色添加记录 包含color1 color2 color3 color4 color5"""
        value = f"//div[@class='lpc-icon']//span[@class='{color}']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    def atlas_button(self, button_name):
        """定位图谱测量下右边4个按钮 包含 测试比对 图谱测试设置 复制全部 全部删除"""
        value = f"//div[@class='lpc-icon']//i[@title='{button_name}']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    @staticmethod
    def right_window_tab(parent, tab_name):
        """
        定位右侧窗口的标签页
        :param parent: 窗口父元素
        :param tab_name: 标签页名称
        :return: 标签页元素对象
        """
        value = f".//div[@class='win-tab']//span[contains(text(), '{tab_name}')]"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def append_record_button(parent, button_index: int):
        """
        图谱测量窗口的【添加记录】按钮
        :param parent: 图谱测量窗口
        :param button_index: 按钮序号
        :return: 【添加记录】按钮元素对象
        """
        value = f".//div[@class='lpc-icon']//span[@title='添加记录']"
        elements = api.find_elements(parent, 'xpath', value)
        return elements[button_index]

    @staticmethod
    def recycle_button(parent, button_name):
        """"""
        value = f".//i[@title='{button_name}']"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def recycle_check_box(parent, button_name):
        """"""
        ...


