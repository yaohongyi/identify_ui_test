#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
# 定位案件列表相关元素：列表数据、案件标签页、案件操作按钮等
from public import api


class CasePage:
    def __init__(self, browser):
        self.browser = browser

    def case_button(self, button_name):
        """
        通过按钮名定位案件操作栏按钮:【新建案件】【导入案件】【同步】【搜索案件】【重置案件列表】
        :param button_name: 按钮名称
        :return: 按钮元素对象
        """
        value = f"//div[contains(@style, 'display: flex')]//div[@class='case_tool']/" \
            f"*[contains(@title, '{button_name}')]"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    @staticmethod
    def case_name_input_box(parent):
        """
        案件窗口：“案件名称”输入框
        :param parent: 案件窗口
        :return: “案件名称”输入框
        """
        element = api.find_element(parent, 'xpath', ".//input[@type='text']")
        return element

    @staticmethod
    def case_attribute_radio(parent, case_attribute: str = '共享'):
        """
        案件属性单选按钮
        :param parent: 新增案件窗口
        :param case_attribute: 共享、私有
        :return:
        """
        value = f".//label[text()='案件属性']/following-sibling::div//span[text()='{case_attribute}']/" \
            f"preceding-sibling::span"
        element = api.find_element(parent, value=value)
        return element

    @staticmethod
    def case_classify_drop_down_box(parent):
        """
        案件分类下拉按钮
        :param parent:
        :return:
        """
        value = f".//label[text()='案件分类']/following-sibling::span/i"
        element = api.find_element(parent, value=value)
        return element

    def case_classify(self, classify_name: str = '无分类'):
        """
        案件分类选项
        :param classify_name:
        :return:
        """
        value = f"//ul[@class='ant-cascader-menu']/li[text()='{classify_name}']"
        element = api.find_element(self.browser, value=value)
        return element

    @staticmethod
    def window_button(parent, button_name='确定'):
        """
        查找二级窗口（也叫“一级弹窗”）上的按钮，例如：【确定】【取消】【确定上传】【浏览】等
        :param parent: 弹窗窗体元素
        :param button_name: 窗体上的按钮名称
        :return: 弹窗上的按钮元素
        """
        value = f".//span[text()='{button_name}']"
        element = api.find_element(parent, 'xpath', value)
        return element

    def find_case(self, case_name):
        """
        查找单个案件
        :param case_name: 案件名称
        :return: 案件元素对象
        """
        value = f"//div[@class='case_list']//div[contains(@class, 'menu_item')]//span[text()='{case_name}']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    def find_cases(self):
        """
        查找出列表所有案件
        :return: 所有案件元素对象组成的列表
        """
        value = "//div[contains(@style, 'display: flex;')]//div[@class='folder_wrap']/span"
        element = api.find_elements(self.browser, 'xpath', value)
        return element

    def case_context_menu(self, button_name):
        """
        (案件、文件夹、文件)右键菜单按钮
        :param button_name: 右键菜单按钮名称
        :return: 右键菜单按钮元素对象
        """
        value = f"//div[@class='contextmenu']/div/span[text()='{button_name}']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    @staticmethod
    def folder_name_input(parent):
        """
        文件夹名称输入框
        :param parent:
        :return:
        """
        value = ".//input[@type='text']"
        element = api.find_element(parent, value=value)
        return element

    def folder_name(self, folder_name):
        """
        处理中的案件，根据文件夹名称定位文件夹（案件名也属于文件夹）
        :param folder_name:
        :return:
        """
        value = f"//div[@class='ant-spin-container']/div[@class='case_tool']/following-sibling::div/" \
            f"ul[@class='rc-tree']//a[@title='{folder_name}']"
        element = api.find_element(self.browser, value=value)
        return element

    def file_name(self, folder_name, file_name):
        """
        处理中的案件，定位指定文件夹下的文件
        :param folder_name:
        :param file_name:
        :return:
        """
        value = f"//div[@class='ant-spin-container']/div[@class='case_tool']/following-sibling::div/" \
            f"ul[@class='rc-tree']//a[@title='{folder_name}']/following-sibling::ul//div[text()='{file_name}']"
        element = api.find_element(self.browser, value=value)
        return element

    @staticmethod
    def user_group_check_box(parent, group_name):
        """
        通过用户分组名称定位用户分组选择框
        :param parent: 用户管理窗口
        :param group_name: 用户分组名称
        :return: 用户分组选择框元素对象
        """
        value = f".//li[@class]/a[@title='{group_name}']/preceding-sibling::span" \
            f"[contains(@class, 'ant-tree-checkbox')]/span"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def user_group_unfold_button(parent, group_name):
        """
        通过用户分组名称定位用户分组展开、收拢按钮
        :param parent: 用户管理窗口
        :param group_name: 用户分组名称
        :return: 用户分组展开、收拢按钮元素对象
        """
        value = f".//a[@title='{group_name}']/preceding-sibling::span[contains(@class, 'ant-tree-switcher')]"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def user_check_box(parent, user_name):
        """
        通过用户分组名称定位用户分组展开、收拢按钮
        :param parent: 用户管理窗口
        :param user_name: 用户名称
        :return: 用户名称前的复选框元素对象
        """
        value = f".//a[@title='{user_name}']/preceding-sibling::span[@class='ant-tree-checkbox']"
        element = api.find_element(parent, 'xpath', value)
        return element

    def case_tab(self, tab_name):
        """
        通过名称定位案件tab标签页：案件列表、处理中案件、回收站
        :param tab_name: 标签页名称
        :return: 标签页元素对象
        """
        value = f"//div[@class='case_tab']//span[text()='{tab_name}']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    def search_input(self):
        """
        定位案件搜索输入框
        :return: None
        """
        value = "//div[@class='input-box']/input[@type='text']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    def sampling_message(self, sampling):
        """
        定位提示窗口的采样率信息 8K 16K 32K
        :param sampling: 采样率
        :return: 采样率单选按钮
        """
        value = f"//div[@class='ant-radio-group']//span[text()='{sampling}']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    @staticmethod
    def file_format_radio_button(parent, button_name='常见格式'):
        """
        上传检材/样本窗口，文件格式选择单选按钮
        :param parent: 上传检材/样本窗口
        :param button_name: 单选按钮名称
        :return: 文件格式单选按钮元素对象
        """
        value = f".//span[contains(text(), '{button_name}')]/preceding-sibling::span[contains(@class, 'ant-radio')]"
        element = api.find_element(parent, 'xpath', value)
        return element

    def find_file(self, folder_name, file_name):
        """
        查找指定文件夹（案件也算文件夹）下的文件
        :param folder_name: 文件夹名称
        :param file_name: 文件名
        :return:
        """
        value = f"//div[@class='ant-spin-container']/div[@class='case_tool']/following-sibling::div/" \
            f"ul[@class='rc-tree']//a[@title='{folder_name}']/following-sibling::ul//div[text()='{file_name}']"
        element = api.find_element(self.browser, value=value)
        return element

    def unfold_and_hide_case_button(self):
        """
        案件【展开】【隐藏】按钮
        :return:
        """
        value = "//div[@class='menu_wrap']//span[@class='caret-right']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    def unfold_and_hide_button(self, folder_name):
        """
        文件夹展开、隐藏按钮
        :param folder_name:
        :return:
        """
        value = f"//div[@class='ant-spin-container']/div[@class='case_tool']/following-sibling::div/" \
            f"ul[@class='rc-tree']//a[@title='{folder_name}']/" \
            f"preceding-sibling::span[contains(@class, 'rc-tree-switcher')]"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    def file_context_menu(self, menu_name):
        """
        案件文件列表右键菜单（音频右键菜单、图片右键菜单）
        :param menu_name: 菜单名
        :return: 菜单元素
        """
        value = f"//div[@class='menu-item']/span[text()='{menu_name}']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    @staticmethod
    def audio_info(parent, field_name):
        """
        获取音频相关信息
        :param parent: 音频信息窗口
        :param field_name: 音频信息字段名
        :return: 音频信息元素对象
        """
        info_name = field_name.upper()
        value = f".//div[@class='file-details']//p/span[contains(text(), '{info_name}')]/following-sibling::span"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def material_drop_down_box(parent):
        """
        导出案件受理记录窗口，检材音频下拉框按钮
        :param parent:
        :return:
        """
        value = ".//label[text()='检材音频：']/following-sibling::span/i"
        element = api.find_element(parent, value=value)
        return element

    @staticmethod
    def sample_drop_down_box(parent):
        """
        导出案件受理记录窗口，样本音频下拉框按钮
        :param parent:
        :return:
        """
        value = ".//label[text()='样本音频：']/following-sibling::span/i"
        element = api.find_element(parent, value=value)
        return element

    @staticmethod
    def window_check_folder(parent, folder_name):
        """"""
        value = f".//div[contains(@class, 'ant-cascader-menus')]//ul/li[text()='{folder_name}']"
        element = api.find_element(parent, value=value)
        return element


if __name__ == '__main__':
    ...
