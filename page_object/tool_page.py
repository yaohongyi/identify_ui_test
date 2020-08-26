#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import time
from public import api


class ToolPage:
    def __init__(self, browser):
        self.browser = browser

    def tool_button(self, button_name):
        """
        工具栏按钮：【音素】【比对】【宽带】【窄带】【共振峰】【基频】【能量】【过零率】【波形图】【4K】【8K】【设置】【横选】
        【抓手】【居中】【全屏】【放大】【缩小】【100%】【参考线】【标记】【截图】【回收站】【录音】【谱分析】【偏差】
        :param button_name: 按钮名称
        :return: 工具栏按钮元素对象
        """
        value = f"//p[text()='{button_name}']/preceding-sibling::div"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    def tool_button2(self, button_name):
        """
        工具栏按钮：【报告】
        :param button_name: 按钮名称
        :return: 工具栏按钮元素对象
        """
        value = f"//span[text()='{button_name}']/ancestor::p/preceding-sibling::div"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    def mode_drop_down_box(self):
        """
        模式选择下拉框按钮
        :return: 模式选择下拉框按钮
        """
        value = "//div[@class='menu-wrap']/div[@class='menu-ope']/div[contains(@class, 'ant-select')]"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    def audio_input(self):
        """搜索音素输入框"""
        value = "//div[@class='ant-input-search-wrapper']//input[@type='text']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    def find_spectrogram(self):
        """ 查找语谱图类型:宽带语谱图、窄带语谱图、共振峰语谱图、基频语谱图、能量语谱图、过零率语谱图、波形图 """
        time.sleep(5)
        value = "//div[@class='spectrum-item active']//span[@title='语谱图类型']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    def report(self, report_type):
        """
        定位【检验记录】、【鉴定意见】按钮
        :param report_type: 报告类型，只能是【检验记录】或【鉴定意见】
        :return: 【检验记录】或【鉴定意见】按钮元素对象
        """
        if report_type not in ['检验记录', '鉴定意见']:
            element = None
        else:
            value = f"//ul[@class='menu-list']//li[@title='报告']//li[@class and text()='{report_type}']"
            element = api.find_element(self.browser, 'xpath', value)
        return element

    @staticmethod
    def inspection_record_tab(parent, tab_name):
        """
        定位“检验记录”窗口的标签页
        :param parent: 标签页名称
        :param tab_name: 标签页名称
        :return: 标签页元素对象
        """
        value = f".//div[@class='identify_report']//li[contains(text(), '{tab_name}')]"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def inspection_record_input(parent, field_name):
        """
        检验记录窗口，“报告标题”标签页下的所有文本输入框
        :param parent: “检验记录”窗口元素对象
        :param field_name: 字段名
        :return: 字段名对应的输入框元素对象
        """
        value = f".//div[@class='identify_report__content']//" \
            f"label[contains(text(), '{field_name}')]/following-sibling::input"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def inspection_record_title_input(parent):
        """
        定位检验记录第2~7标签页中的标题输入框
        :param parent: “检验记录”窗口元素对象
        :return: 标题输入框元素对象
        """
        value = ".//div[@class='identify_report']//input"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def inspection_record_textarea(parent):
        """
        定位检验记录第2~7标签页中的文本域
        :param parent: “检验记录”窗口元素对象
        :return: 文本域元素对象
        """
        value = ".//div[@class='identify_report']//textarea"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def inspection_record_left_common(parent, common_name):
        """
        定位检验记录中的左侧
        :param parent: 检验记录窗口对象
        :param common_name: 左侧菜单名称
        :return: 左侧菜单元素对象
        """
        value = f".//div[@class='report_sidebar']//div[contains(text(), '{common_name}')]"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def inspection_record_button(parent, button_name):
        """
        检验记录窗口上的按钮：【插入图片】、【预览】、【保存】、【导出】
        :param parent:
        :param button_name:
        :return:
        """
        value = f".//div[@class='identify_report']//i[contains(@title, '{button_name}')]"
        element = api.find_element(parent, 'xpath', value)
        return element

    def insert_picture_window(self):
        """
        定位插入图片窗口
        :return: 插入图片窗口对象
        """
        value = f"//label[text()='插入图片']/ancestor::div/ancestor::div[@class='md-content com-dia']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    @staticmethod
    def upload_picture_button(parent):
        """
        插入图片窗口的【上传图片】按钮
        :param parent: 插入图片窗口
        :return: 【上传图片】按钮元素对象
        """
        value = ".//div[@class='upload_btn']"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def import_picture_button(parent):
        """
        定位插入图片窗口的【确定导入】按钮
        :param parent: 插入图片窗口
        :return:【确定导入】按钮元素对象
        """
        value = ".//div[@class='import_btn']/span[text()='确定导入']"
        element = api.find_element(parent, 'xpath', value)
        return element

    def prompt_message(self):
        """
        定位检验记录操作弹出框提示信息
        :return: 弹出提示框的提示信息文本
        """
        value = "//div[@class='md-content com-dia']//p[@class='dialog-text-wrap']/span"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    def prompt_window(self):
        """
        定位提示窗口
        :return: 提示窗口元素对象
        """
        value = "//label[text()='提示']/parent::div/parent::div[@class='com-dia']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    def prompt_message_button(self, button_name):
        """
        定位弹出提示框上的按钮
        :param button_name: 按钮名称
        :return: 按钮元素对象
        """
        value = f"//div[@class='md-content com-dia']//div[@class='dialog-btn-wrap']/span[text()='{button_name}']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    @staticmethod
    def identify_opinion_tab(parent, tab_name):
        """
        定位“鉴定意见”窗口的标签页
        :param parent: 鉴定意见窗口
        :param tab_name: 标签页名称
        :return: 标签页元素对象
        """
        value = f".//li[contains(text(), '{tab_name}')]"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def identify_opinion_input(parent, field_name):
        """
        根据冒号:前的字段名，定位字段名对应的文本输入框
        :param parent: 鉴定意见窗口
        :param field_name: 字段名
        :return: 字段名对应的文本输入框元素对象
        """
        value = f".//*[contains(text(), '{field_name}')]/following-sibling::input"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def identify_opinion_textarea(parent):
        """
        定位鉴定意见窗口中的文本域
        :param parent: 鉴定意见窗口
        :return: 文本域元素对象
        """
        value = f".//div[@class='rsc-bot']/textarea"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def identify_opinion_button(parent, button_name):
        value = f".//span[@title='{button_name}']"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def close_button(parent):
        """
        窗口右上角【X】关闭按钮
        :param parent: 窗口对象
        :return: 关闭按钮元素对象
        """
        value = ".//i[@class='close-dia']"
        element = api.find_element(parent, 'xpath', value)
        return element


if __name__ == '__main__':
    ...
