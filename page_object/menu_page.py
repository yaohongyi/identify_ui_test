#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王

from public import api


class MenuPage:
    def __init__(self, browser):
        self.browser = browser

    # 一级菜单按钮：文件、编辑、波谱图、播放控制、视图等
    def level_1_menu(self, menu_name):
        value = f"//div[@class='custom-menu']//span[@class='cm-item-sp' and text()='{menu_name}']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    # 二级菜单按钮
    def level_2_menu(self, menu_name):
        value = f"//div[@class='cmw-menu']//li[@class='cm-item-li']/span[text()='{menu_name}']"
        element = api.find_element(self.browser, 'xpath', value)
        return element

    # 定位密码输入框：2-旧密码，3-第一个新密码，4-第二个新密码
    @staticmethod
    def password_input(parent, input_box_index: int):
        value = "//input[@type='password']"
        elements = api.find_elements(parent, 'xpath', value)
        return elements[input_box_index]

    @staticmethod
    def password_window_button(parent, button_name='保存'):
        """
        定位密码修改窗口的【保存】【取消】按钮
        :param parent: 修改密码窗口
        :param button_name: 按钮名称
        :return: 按钮元素对象
        """
        button_name_list = list(button_name)
        button_name = button_name_list[0] + " " + button_name_list[1]
        value = f".//button[@type='button']/span[text()='{button_name}']"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def prompt_message(parent):
        """
        获取三级弹出框中的提示信息
        :param parent: 三级弹出框
        :return: 弹出框上的提示信息
        """
        value = ".//p[@class='dialog-text-wrap']/span"
        element = api.find_element(parent, 'xpath', value)
        return element

    # 【添加分组】按钮
    @staticmethod
    def add_user_group_button(parent):
        value = "i.spk-pc.icon-tubiao_tianjiazu-"
        element = api.find_element(parent, 'css', value)
        return element

    # 分组输入框
    @staticmethod
    def user_group_input(parent):
        value = "input[type=text]"
        element = api.find_element(parent, 'css', value)
        return element

    # 确认操作提示框的【确定】按钮
    @staticmethod
    def confirm_button(parent):
        value = "div.dialog-btn-wrap>span.dialog-btn"
        element = api.find_element(parent, 'css', value)
        return element

    # 根据分组名称定位分组列表记录
    @staticmethod
    def find_group_by_name(parent, group_name):
        value = f".//div[@class='manage_wrap']//span[@class='group_name' and text()='{group_name}']"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def group_button(parent, group_name, button_index: int):
        """
        用户组操作按钮：0-编辑，1-删除
        :param parent:
        :param group_name:
        :param button_index:
        :return:
        """
        value = f"//span[text()='{group_name}']/following-sibling::span/i"
        elements = api.find_elements(parent, 'xpath', value)
        return elements[button_index]

    # 【添加用户】按钮
    @staticmethod
    def add_user_button(parent):
        value = "i.spk-pc.icon-tubiao_tianjiayonghu-"
        element = api.find_element(parent, 'css', value)
        return element

    # 用户名输入框
    @staticmethod
    def user_name_input(parent):
        value = ".//input[@type='text' and @placeholder='点击输入用户名称']"
        element = api.find_element(parent, 'xpath', value)
        return element

    # 通过用户名找到用户
    @staticmethod
    def find_user_by_name(parent, user_name):
        value = f".//span[@class='user_name' and text()='{user_name}']"
        element = api.find_element(parent, 'xpath', value)
        return element

    # 【删除用户】按钮
    @staticmethod
    def del_user_button(parent):
        value = ".//span[@class='user_edit']/i[@title='删除用户']"
        element = api.find_element(parent, 'xpath', value)
        return element

    @staticmethod
    def close_window_button(parent):
        """
        用户管理窗口上的【X】关闭按钮
        :param parent:
        :return:
        """
        value = ".//i[@class='close-dia']"
        element = api.find_element(parent, 'xpath', value)
        return element


if __name__ == '__main__':
    pass
