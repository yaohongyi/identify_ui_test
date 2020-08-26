#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import time
import win32api
import win32gui
import win32con
from public import api
from page_object.menu_page import MenuPage


class OperateMenu:
    def __init__(self, browser):
        self.browser = browser
        self.menu_page = MenuPage(self.browser)

    def logout(self):
        """退出鉴定系统"""
        self.open_menu('文件', '退出系统')
        time.sleep(3)
        # 操作退出弹出框，点击【确定】按钮
        dialog = win32gui.FindWindow('#32770', "国音智能声纹鉴定专家系统")
        win32api.keybd_event(37, 0, 0, 0)
        confirm_button = win32gui.FindWindowEx(dialog, 0, 'Button', None)
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, confirm_button)

    def open_menu(self, level_1_menu_name, level_2_menu_name):
        """
        连续点击一级菜单和二级菜单
        :param level_1_menu_name: 一级菜单名称
        :param level_2_menu_name: 二级菜单名称
        :return: None
        """
        self.menu_page.level_1_menu(level_1_menu_name).click()
        time.sleep(0.5)
        self.menu_page.level_2_menu(level_2_menu_name).click()
        time.sleep(0.5)

    def change_password(self, old_password, new_password, confirm_password):
        """
        修改密码
        :param old_password: 旧密码
        :param new_password: 新密码
        :param confirm_password: 确认新密码
        :return: None
        """
        password_window = api.level_2_window(self.browser)
        self.menu_page.password_input(password_window, 0).send_keys(old_password)
        self.menu_page.password_input(password_window, 1).send_keys(new_password)
        self.menu_page.password_input(password_window, 2).send_keys(confirm_password)
        self.menu_page.password_window_button(password_window, '保存').click()

    def click_confirm_button(self):
        """"""
        prompt_window = api.level_3_window(self.browser)
        api.level_window_button(prompt_window, '确定').click()

    def close_password_window(self):
        """
        关闭修改密码窗口
        :return: None
        """
        password_window = api.level_2_window(self.browser)
        self.menu_page.password_window_button(password_window, '取消').click()

    def add_user_group(self, group_name):
        """
        新增用户组
        :param group_name: 用户组名称
        :return: None
        """
        user_manager_window = api.level_2_window(self.browser)
        self.menu_page.add_user_group_button(user_manager_window).click()
        time.sleep(0.5)
        add_group_window = api.level_3_window(self.browser)
        self.menu_page.user_group_input(add_group_window).send_keys(group_name)
        time.sleep(0.5)
        self.menu_page.confirm_button(add_group_window).click()

    def find_user_group(self, group_name):
        """
        查找用户组
        :param group_name: 用户组名称
        :return: 用户组元素对象
        """
        user_manager_window = api.level_2_window(self.browser)
        result = self.menu_page.find_group_by_name(user_manager_window, group_name)
        return result

    def del_user_group(self, group_name):
        """
        删除用户组
        :param group_name: 用户组名称
        :return: None
        """
        user_manager_window = api.level_2_window(self.browser)
        self.menu_page.find_group_by_name(user_manager_window, group_name).click()
        time.sleep(0.5)
        self.menu_page.group_button(user_manager_window, group_name, 1).click()
        time.sleep(0.5)
        prompt_window = api.level_3_window(self.browser)
        self.menu_page.confirm_button(prompt_window).click()

    def add_user(self, group_name, user_name):
        """
        指定用户组下新增用户
        :param group_name: 用户组名称
        :param user_name: 用户名
        :return: None
        """
        user_manager_window = api.level_2_window(self.browser)
        # 点击选中用户组，在该用户组下新增用户
        self.find_user_group(group_name).click()
        self.menu_page.add_user_button(user_manager_window).click()
        # 打开的新增用户窗口输入信息保存
        add_user_window = api.level_3_window(self.browser)
        self.menu_page.user_name_input(add_user_window).send_keys(user_name)
        self.menu_page.confirm_button(add_user_window).click()

    def find_user(self, group_name, user_name):
        """
        查找指定用户组下面的指定用户
        :param group_name: 用户组名称
        :param user_name: 用户名称
        :return: 用户元素对象
        """
        user_manager_window = api.level_2_window(self.browser)
        self.find_user_group(group_name).click()
        result = self.menu_page.find_user_by_name(user_manager_window, user_name)
        return result

    def del_user(self, group_name, user_name):
        """
        删除指定用户组下面的指定用户
        :param group_name: 用户组名称
        :param user_name: 用户名称
        :return: None
        """
        user_manager_window = api.level_2_window(self.browser)
        self.find_user(group_name, user_name).click()
        self.menu_page.del_user_button(user_manager_window).click()
        level_3_window = api.level_3_window(self.browser)
        api.level_window_button(level_3_window, '确定').click()

    def close_user_window(self):
        """
        关闭用户管理窗口
        :return: None
        """
        user_manager_window = api.level_2_window(self.browser)
        self.menu_page.close_window_button(user_manager_window).click()


if __name__ == '__main__':
    ...
