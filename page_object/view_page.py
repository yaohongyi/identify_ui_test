#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
# 鉴定系统各种视图窗口的操作
import time
from public import api


class ViewPage:
    def __init__(self, browser):
        self.browser = browser

    def view_window(self, window_index=0):
        """
        视图操作窗口(语谱图+右侧列表栏：音素列表、标记列表...)
        :param window_index: 窗口序号，第一个语谱图为0，以此类推
        :return: 视图操作窗口对象
        """
        value = "//div[contains(@class, 'spectrum-item')]"
        elements = api.find_elements(self.browser, 'xpath', value)
        return elements[window_index]

    @staticmethod
    def audio_window(parent):
        """"""
        value = ""
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def mouse_move(parent, point_in_time):
        value = f"//div[@class='mouse-text' and contains(text(), '{point_in_time}ms')]"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def phoneme_window_tab(parent, tab_name: str):
        """
        通过标签页名称定位指定窗口对应的标签页：标记、音素、快捷设置、历史记录等
        :param tab_name: 标签页名称
        :param parent: 视图操作窗口
        :return: 指定窗口的标签页元素对象
        """
        value = f".//div[@class='Phoneme']//label/span[contains(text(), '{tab_name}')]"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def phoneme_tag_button(parent)-> list:
        """
        定位音素列表的【➕】添加按钮
        :param parent: 视图操作窗口
        :return: 标记按钮元素列表
        """
        value = ".//i[@class='spk-pc icon-tubiao_biaoji']"
        elements = api.find_elements(parent, 'xpath', value)
        return elements

    @staticmethod
    def tag_operate_button(parent, button_name):
        """
        定位标记列表【标记设置】【导出标记】【批量删除】按钮
        :param parent:
        :param button_name:
        :return:
        """
        value = f".//div[@class='markTool_bar']/i[@title='{button_name}']"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def tag_check_box(parent):
        value = ".//input[@type='checkbox']"
        elements = api.find_elements(parent, 'xpath', value)
        return elements

    @staticmethod
    def phoneme_filter_button(parent)-> list:
        """
        定位音素过滤按钮
        :param parent: 视图操作窗口
        :return: 过滤按钮元素列表
        """
        value = ".//i[@class='spk-pc icon-icon_filt_normal-']"
        elements = api.find_elements(parent, 'xpath', value)
        return elements

    @staticmethod
    def phoneme_list_title(parent, title_name):
        """
        音素视图中的列表字段名
        :param parent: 视图操作窗口
        :param title_name: 列表字段名
        :return: 列表字段元素对象
        """
        value = f".//div[@class='list_title']/span[contains(text(), '{title_name}')]"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def cancel_filter_button(parent):
        """
        定位【取消过滤】按钮
        :param parent: 视图操作窗口
        :return: 【取消过滤】按钮元素对象
        """
        value = ".//i[@class='spk-pc icon-icon_backout_normal-']"
        element = api.find_element(parent, 'xpath', value)
        return element

    def add_window_button(self):
        """
        语谱图中的【新增窗口】按钮
        :return: 【新增窗口】按钮元素对象
        """
        value = "//div[@class='add-spectrum']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    @staticmethod
    def spectrum_window_top_element(parent, element_name):
        """
        每个语谱图窗口顶部的元素对象：文件名、音素检索进度、语谱图类型、【关闭】、【双窗口】等
        :param parent: 视图操作窗口
        :param element_name: 元素名称title
        :return: 视图窗口顶部的元素对象
        """
        value = f".//div[@class='si-title']/span[@title='{element_name}']"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def audio_name(parent):
        """
        获得视图窗口打开的音频文件名称
        :param parent: 视图窗口
        :return: 音频文件名称元素对象
        """
        value = ".//span[contains(text(), '文件')]/following-sibling::span[@title]"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def add_file_button(parent, button_index=0):
        """
        【新建文件】按钮
        :param parent: 视图操作窗口
        :param button_index: 按钮序号（因为可能存在多个新建语谱图窗口）
        :return: 【新建文件】按钮元素对象
        """
        value = ".//a[text()='新建文件']"
        elements = api.find_elements(parent, 'xpath', value)
        return elements[button_index]

    @staticmethod
    def sampling_rate_radio_button(parent, sampling_rate='8K'):
        """
        根据采样率，定位新建音频文件窗口的采样率单选按钮
        :param parent: 新建音频文件窗口
        :param sampling_rate: 采样率
        :return: 采样率单选按钮元素对象
        """
        value = f".//span[text()='{sampling_rate}']/preceding-sibling::span/span"
        element = api.find_element(parent, 'xpath', value)
        return element


if __name__ == '__main__':
    driver = api.login()
    # 打开案件
    from operate.operate_case import OperateCase
    operate_case = OperateCase(driver)
    operate_case.open_case('都君AutoTest')
    time.sleep(1)
    # 操作视图
    view_page = ViewPage(driver)
    view_page.view_window(0)
    api.browser_quit(driver)
