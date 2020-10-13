#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import configparser
import logging
import os
import time
import win32gui
import win32con
import xlrd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def get_config_file_path():
    """
    获取config.ini文件的绝对路径
    :return:
    """
    current_sep = os.path.sep
    public_folder_path = os.getcwd()
    public_folder_path_list = public_folder_path.split(current_sep)
    project_index = public_folder_path_list.index('identify_ui_test')
    project_path = current_sep.join(public_folder_path_list[:project_index+1])
    config_file_path = project_path + current_sep + 'config' + current_sep + 'config.ini'
    return config_file_path


# 从配置文件读取数据
def get_config(section, key):
    cf = configparser.ConfigParser()
    config_file = get_config_file_path()
    cf.read(config_file, encoding='utf-8-sig')
    value = cf.get(section, key)
    return value


# 从excel读取数据:row_now为序号中的数字，不是excel的行号
def read_excel(case_title, sheet_name='鉴定系统UI自动化', excel_path='./test_case.xlsx') -> dict:
    excel = xlrd.open_workbook(excel_path)
    sheet = excel.sheet_by_name(sheet_name)
    case_title_list = sheet.col_values(0)
    index_num = case_title_list.index(case_title)
    cell_value = sheet.cell_value(index_num, 2).split('\n')
    data = {}
    for i in cell_value:
        key_value = i.split('=')
        key, value = key_value[0], key_value[1]
        data[key] = value
    return data


# 传入对象、方法、值定位一个元素
def find_element(parent, method='xpath', value=''):
    element = None
    try:
        if method == 'xpath':
            element = WebDriverWait(parent, 8).until(ec.presence_of_element_located((By.XPATH, value)))
        elif method == 'css':
            element = WebDriverWait(parent, 8).until(ec.presence_of_element_located((By.CSS_SELECTOR, value)))
        else:
            element = None
    except (NoSuchElementException, TimeoutException):
        element = None
    finally:
        return element


# 传入对象、方法、值定位多个元素
def find_elements(parent, method='xpath', value=''):
    element = None
    try:
        if method == 'xpath':
            element = WebDriverWait(parent, 8).until(ec.presence_of_all_elements_located((By.XPATH, value)))
        elif method == 'css':
            element = WebDriverWait(parent, 8).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, value)))
        else:
            element = None
    except NoSuchElementException:
        element = None
    finally:
        return element


username = get_config('base_info', 'user_name')
password = get_config('base_info', 'user_password')
# 脚本操作鉴定系统时，经常出现打开了鉴定系统不操作元素的情况，经排查是句柄的问题。如果出现不操作元素的情况，请在1和2之间进行切换尝试
handle_index = int(get_config('base_info', 'handle_num'))


def get_browser():
    """
    # 登录鉴定系统并生成浏览器对象
    :return: 浏览器对象browser
    """
    chrome_driver = get_config('base_info', 'chrome_driver')
    chrome_options = webdriver.ChromeOptions()
    exe_path = get_config('base_info', 'exe_path')
    chrome_options.binary_location = exe_path
    browser = webdriver.Chrome(chrome_driver, options=chrome_options)
    # 用户名输入框
    user_input = find_element(browser, 'xpath', "//input[@id='username']")
    user_input.clear()
    user_input.send_keys(username)
    # 密码输入框
    pass_input = find_element(browser, 'xpath', "//input[@id='password']")
    pass_input.clear()
    pass_input.send_keys(password)
    submit_button = browser.find_element_by_id("submit-btn")
    submit_button.click()
    time.sleep(1)
    # 切换句柄
    handles = browser.window_handles
    browser.switch_to.window(handles[handle_index])
    return browser


# 定位二级弹出框
def level_2_window(parent):
    time.sleep(0.5)
    value = ".//div[@style='display: block;']/div/div[@class='md-content com-dia']"
    element = find_elements(parent, 'xpath', value)
    return element[0]


# 定位三级弹出框
def level_3_window(parent):
    time.sleep(0.5)
    value = ".//div[@style='display: block;']/div/div[@class='md-content com-dia']"
    elements = find_elements(parent, 'xpath', value)
    return elements[1]


def level_window_button(parent, button_name):
    """
    根据按钮名称定位二级和三级弹出框上的按钮
    :param parent: 二级、三级弹出框对象
    :param button_name: 按钮名称
    :return: 按钮元素对象
    """
    value = f".//span[text()='{button_name}']"
    element = find_element(parent, 'xpath', value)
    return element


def level_window_message(parent):
    """
    定位二级和三级弹出框上的提示信息
    :param parent: 二级、三级弹出框对象
    :return: 提示信息元素对象
    """
    value = ".//p[@class='dialog-text-wrap']/span"
    element = find_element(parent, 'xpath', value)
    return element


def close_window_button(parent):
    """"""
    value = ".//i[@class='close-dia']"
    element = find_element(parent, 'xpath', value)
    return element


def create_case_name():
    # 从config.ini读取案件名前缀
    case_name_prefix = get_config('base_info', 'case_name_prefix')
    # 生成时间戳
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    case_name = case_name_prefix + timestamp
    return case_name


# 导入
def import_file(file_path, window_name='导入案件'):
    time.sleep(3)
    dialog = win32gui.FindWindow('#32770', window_name)
    combo_box_ex32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
    combo_box = win32gui.FindWindowEx(combo_box_ex32, 0, 'ComboBox', None)
    edit = win32gui.FindWindowEx(combo_box, 0, 'Edit', None)
    button = win32gui.FindWindowEx(dialog, 0, 'Button', None)
    win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, file_path)
    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)


# 导出
def export_file(file_path, window_name='导出案件'):
    time.sleep(2)
    dialog = win32gui.FindWindow('#32770', window_name)
    direct_uihwnd = win32gui.FindWindowEx(dialog, 0, 'DirectUIHWND', None)
    combo_box = win32gui.FindWindowEx(direct_uihwnd, 0, 'ComboBox', None)
    edit = win32gui.FindWindowEx(combo_box, 0, 'Edit', None)
    button = win32gui.FindWindowEx(dialog, 0, 'Button', None)
    win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, file_path)
    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)


def prompt_message(browser):
    """
    定位3秒自动隐藏的提示信息
    :param browser: 浏览器对象
    :return: 提示信息对象
    """
    value = "//div[@class='ant-message']//i/following-sibling::span"
    element = find_element(browser, 'xpath', value)
    return element


def window_prompt_message(parent):
    """
    获取三级弹出框中的提示信息
    :param parent: 三级弹出框
    :return: 弹出框上的提示信息
    """
    value = ".//p[@class='dialog-text-wrap']/span"
    element = find_element(parent, 'xpath', value)
    return element


def get_prompt_message(parent)-> str:
    """
    获得弹出框提示信息
    :return: 弹出框提示信息
    """
    prompt_window = level_3_window(parent)
    message = window_prompt_message(prompt_window).text
    return message


def remove_doc(doc_path):
    """
    还原测试环境，删除指定文件夹下的doc/docx文件
    :param doc_path: 目标文件所在文件夹路径
    :return: None
    """
    file_list = os.listdir(doc_path)
    for file in file_list:
        if file.endswith('docx') or file.endswith('doc'):
            try:
                os.remove(doc_path + '\\' + file)
            except (FileNotFoundError, PermissionError) as reason:
                logging.warning(reason)


def remove_spk(file_name):
    """
    还原测试环境，删除导出的案件（这里判断文件名称大于15个字符的就是导出的案件）
    :param file_name:
    :return:
    """
    try:
        os.remove(file_name)
    except (FileNotFoundError, PermissionError) as reason:
        logging.warning(reason)


if __name__ == '__main__':
    # get_config_file_path()
    username = get_config('base_info', 'user_name')
    print(username)
