#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import time
import pytest
from public import api
from operate.operate_menu import OperateMenu
"""
“修改密码成功”的用例必须最后执行，因为修改成功后会退出系统
"""


@pytest.fixture(scope='class')
def init_test_menu(login):
    # 登录系统并获得浏览器对象
    operate_menu = OperateMenu(login)
    yield operate_menu


class TestMenu:
    @staticmethod
    def test_user_and_group(login, init_test_menu):
        """测试新增用户"""
        operate_menu = init_test_menu
        # 打开用户管理窗口
        operate_menu.open_menu('设置', '用户管理')
        data = api.read_excel('test_user_and_group')
        user_name = data.get('user_name')
        group_name = data.get('group_name')
        # 新增用户组
        operate_menu.add_user_group(group_name)
        add_user_group_test_result = operate_menu.find_user_group(group_name)
        assert add_user_group_test_result
        # 新增用户
        operate_menu.add_user(group_name, user_name)
        # 断言：用户分组下是否存在刚才添加的用户
        add_user_test_result = operate_menu.find_user(group_name, user_name)
        assert add_user_test_result
        # 删除用户
        operate_menu.del_user(group_name, user_name)
        del_user_test_result = operate_menu.find_user(group_name, user_name)
        assert not del_user_test_result
        # 删除用户组
        operate_menu.del_user_group(group_name)
        del_user_group_test_result = operate_menu.find_user_group(group_name)
        assert not del_user_group_test_result
        # 关闭用户管理窗口
        operate_menu.close_user_window()

    @staticmethod
    def test_old_password_wrong(login, init_test_menu):
        """修改密码时旧密码输入错误"""
        operate_menu = init_test_menu
        operate_menu.open_menu('设置', '修改密码')
        data = api.read_excel('test_old_password_wrong')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        operate_menu.change_password(old_password, new_password, confirm_password)
        time.sleep(1)
        prompt_message = api.prompt_message(login).text
        assert prompt_message == data.get('msg')
        time.sleep(1)
        # 关闭修改密码窗口
        operate_menu.close_password_window()

    @staticmethod
    def test_new_password_diff(login, init_test_menu):
        """修改密码时，两次新密码不同"""
        operate_menu = init_test_menu
        operate_menu.open_menu('设置', '修改密码')
        data = api.read_excel('test_new_password_diff')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        operate_menu.change_password(old_password, new_password, confirm_password)
        time.sleep(1)
        prompt_message = api.prompt_message(login).text
        assert prompt_message == data.get('msg')
        time.sleep(1)
        # 关闭修改密码窗口
        operate_menu.close_password_window()

    @staticmethod
    def test_password_change_succeed(login, init_test_menu):
        """修改密码成功"""
        operate_menu = init_test_menu
        operate_menu.open_menu('设置', '修改密码')
        data = api.read_excel('test_password_change_succeed')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        operate_menu.change_password(old_password, new_password, confirm_password)
        time.sleep(1)
        prompt_message = api.get_prompt_message(login)
        assert prompt_message == data.get('msg')


if __name__ == '__main__':
    pytest.main()
