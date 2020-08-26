#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import time
import re
from public import api
from page_object.view_page import ViewPage


class OperateView:
    def __init__(self, browser):
        self.browser = browser
        self.view_page = ViewPage(self.browser)

    def switch_window(self, window_index=0):
        """
        切换语谱图窗口
        :param window_index: 语谱图窗口号，从0开始
        :return: None
        """
        self.view_page.view_window(window_index).click()

    def switch_tab(self, tab_name, window_index=0):
        """
        切换音素操作窗口的标签页
        :param tab_name: 标签页名称
        :param window_index: 语谱图窗口号，从0开始
        :return: None
        """
        view_window = self.view_page.view_window(window_index)
        self.view_page.phoneme_window_tab(view_window, tab_name).click()

    def add_tag(self, window_index=0):
        """
        给音素添加标记
        :param window_index: 语谱图窗口序号，从0开始
        :return: None
        """
        view_window = self.view_page.view_window(window_index)
        tag_button_list = self.view_page.phoneme_tag_button(view_window)
        tag_button_list[0].click()

    def del_all_tag(self, window_index=0):
        """
        全选标记进行删除
        :param window_index: 语谱图窗口序号，从0开始
        :return: None
        """
        view_window = self.view_page.view_window(window_index)
        # 点击【全选】按钮
        self.view_page.tag_check_box(view_window)[0].click()
        self.view_page.tag_operate_button(view_window, '批量删除').click()
        time.sleep(0.5)
        warning_window = api.level_2_window(self.browser)
        api.level_window_button(warning_window, '确定').click()
        time.sleep(0.5)

    def get_tag_and_phoneme_num(self, tab_name, window_index=0):
        """
        获取括号里面的数字，可用作获取：标记数量、元素数量等
        :param tab_name: 标签页名称（标记、音素）
        :param window_index: 语谱图窗口序号
        :return: 标记或者音素个数
        """
        view_window = self.view_page.view_window(window_index)
        tab = self.view_page.phoneme_window_tab(view_window, tab_name)
        tab_text = tab.text
        result = re.search('（(.*)）', tab_text)
        num = int(result.group(1))
        return num

    def filter_phoneme(self, window_index=0):
        """
        过滤音素
        :param window_index: 语谱图窗口序号，从0开始
        :return: None
        """
        view_window = self.view_page.view_window(window_index)
        filter_button_list = self.view_page.phoneme_filter_button(view_window)
        filter_button_list[0].click()

    def get_filter_num(self, window_index=0):
        """
        获得过滤的音素数量
        :param window_index: 语谱图窗口序号，从0开始
        :return: 过滤的音素数量
        """
        view_window = self.view_page.view_window(window_index)
        filter_title = self.view_page.phoneme_list_title(view_window, '过滤')
        filter_text = filter_title.text
        result = re.search(r"\((.*)\)", filter_text)
        filter_num = int(result.group(1))
        return filter_num

    def cancel_filter_phoneme(self, window_index=0):
        """
        取消过滤音素
        :param window_index: 语谱图窗口序号，从0开始
        :return: None
        """
        view_window = self.view_page.view_window(window_index)
        self.view_page.cancel_filter_button(view_window).click()

    def add_spectrum_window(self):
        """
        新增视图窗口
        :return: None
        """
        self.view_page.add_window_button().click()

    def close_spectrum_window(self, window_index: int):
        """
        关闭视图窗口
        :param window_index: 视图窗口序号
        :return: None
        """
        view_window = self.view_page.view_window(window_index)
        self.view_page.spectrum_window_top_element(view_window, element_name='关闭').click()

    def add_file(self, window_index: int, sampling_rate='16K'):
        """
        新建文件
        :param window_index: 视图窗口序号
        :param sampling_rate: 采样率（只能是8K/16K/32K）
        :return: None
        """
        view_window = self.view_page.view_window(window_index)
        # 点击【新建文件】按钮
        self.view_page.add_file_button(view_window, button_index=0).click()
        choose_sampling_rate_window = api.level_2_window(self.browser)
        # 选择采样率
        self.view_page.sampling_rate_radio_button(choose_sampling_rate_window, sampling_rate).click()
        time.sleep(0.5)
        api.level_window_button(choose_sampling_rate_window, button_name='确定').click()

    def get_sampling_rate(self, window_index: int):
        """
        获得语谱图的采样率信息
        :param window_index: 视图窗口序号
        :return: 语谱图的采样率信息
        """
        view_window = self.view_page.view_window(window_index)
        sampling_rate = self.view_page.spectrum_window_top_element(view_window, '采样率').text
        return sampling_rate

    def get_audio_name(self, window_index: int):
        """
        获得视图窗口中的音频名称
        :param window_index: 视图窗口序号
        :return: 音频名称
        """
        view_window = self.view_page.view_window(window_index)
        audio_name = self.view_page.audio_name(view_window).text
        return audio_name


if __name__ == '__main__':
    driver = api.login()
    # 打开案件
    from operate.operate_case import OperateCase
    operate_case = OperateCase(driver)
    operate_case.open_case('都君AutoTest')
    time.sleep(1)
    # 创建语谱图操作对象
    operate_view = OperateView(driver)
    operate_view.del_all_tag()
    api.browser_quit(driver)
