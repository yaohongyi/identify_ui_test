#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import pytest
import os
from public.api import get_config, get_browser
from public import backend_api

username = get_config('base_info', 'user_name')
password = get_config('base_info', 'user_password')
# 脚本操作鉴定系统时，经常出现打开了鉴定系统不操作元素的情况，经排查是句柄的问题。如果出现不操作元素的情况，请在1和2之间进行切换尝试
handle_index = int(get_config('base_info', 'handle_num'))


@pytest.fixture(scope='module')
def login():
    """
    # 登录鉴定系统并生成浏览器对象
    :return: 浏览器对象browser
    """
    browser = get_browser()
    yield browser
    try:
        browser.quit()
    finally:
        os.system("taskkill /im 国音智能声纹鉴定专家系统.exe /f >nul 2>nul")
    backend_api.del_all_case()
