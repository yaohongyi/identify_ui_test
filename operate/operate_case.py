#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
# 案件相关操作的封装
import time
from public import api
from selenium.webdriver.common.action_chains import ActionChains
from page_object.case_page import CasePage
from page_object.view_page import ViewPage


class OperateCase:
    def __init__(self, browser):
        """
        案件相关操作类
        :param browser:浏览器对象
        """
        self.browser = browser
        self.case_page = CasePage(self.browser)
        self.view_page = ViewPage(self.browser)

    def choose_case_classify(self, level_1_classify: str, level_2_classify: str):
        """
        选择案件分类
        :param level_1_classify: 一级分类
        :param level_2_classify: 二级分类
        :return:
        """
        self.case_page.case_classify(level_1_classify).click()
        time.sleep(1)
        if level_2_classify:
            self.case_page.case_classify(level_2_classify).click()

    def add_case(self, case_name: str, case_attribute: str = '私有', level_1_classify: str = '无分类',
                 level_2_classify: str = None):
        """
        新增案件，新增成功后案件会自动打开
        :param case_name: 案件名
        :param case_attribute: 共享、私有
        :param level_1_classify: 一级分类
        :param level_2_classify: 二级分类
        :return: None
        """
        # 点击【新建】按钮
        time.sleep(0.5)
        self.case_page.case_button(button_name='新建案件').click()
        time.sleep(0.5)
        add_case_window = api.level_2_window(self.browser)
        # 输入案件名
        self.case_page.case_name_input_box(add_case_window).send_keys(case_name)
        # 选择案件属性
        self.case_page.case_attribute_radio(add_case_window, case_attribute).click()
        # 选择案件分类
        self.case_page.case_classify_drop_down_box(add_case_window).click()
        time.sleep(0.5)
        self.choose_case_classify(level_1_classify, level_2_classify)
        time.sleep(0.5)
        # 点击【新建】按钮
        self.case_page.window_button(add_case_window, button_name='确定').click()
        time.sleep(0.5)

    def close_add_case_window(self):
        """关闭新增案件窗口"""
        add_case_window = api.level_2_window(self.browser)
        self.case_page.window_button(add_case_window, button_name='取消').click()

    def find_case(self, case_name):
        """
        在列表中查找案件
        :param case_name: 案件名
        :return: 案件查找结果：None或者案件元素对象
        """
        case = self.case_page.find_case(case_name)
        return case

    def selected_case(self, case_name):
        """
        在列表中选中案件
        :param case_name: 案件名称
        :return: None
        """
        self.find_case(case_name).click()
        time.sleep(1)

    def open_case(self, case_name):
        """
        从案件列表找到案件并打开
        :param case_name: 案件名
        :return: None
        """
        target_case = self.case_page.find_case(case_name)
        target_case.click()
        target_case.click()
        time.sleep(1)

    def switch_tab(self, tab_name):
        """
        切换案件标签页：案件列表、历史案件、处理中、回收站
        :param tab_name: 标签页名称
        :return: None
        """
        time.sleep(2)
        self.case_page.case_tab(tab_name).click()
        time.sleep(2)

    def case_context_menu_operate(self, case_name, button_name):
        """
        针对指定案件进行鼠标右键操作
        :param case_name: 案件名称
        :param button_name: 右键菜单按钮
        :return: None
        """
        # 在指定案件上点击鼠标右键
        target_case = self.find_case(case_name)
        ActionChains(self.browser).move_to_element(target_case).context_click(target_case).perform()
        time.sleep(1)
        # 点击右键菜单中的按钮
        self.case_page.case_context_menu(button_name).click()

    def add_folder(self, parent_folder_name, folder_name):
        """
        新增子文件夹
        :param parent_folder_name: 父文件夹
        :param folder_name: 子文件夹名称
        :return:
        """
        parent_folder = self.case_page.folder_name(parent_folder_name)
        self.context_menu_operate(parent_folder, '新建文件夹')
        add_folder_window = api.level_2_window(self.browser)
        self.case_page.folder_name_input(add_folder_window).send_keys(folder_name)
        self.case_page.window_button(add_folder_window, '确认').click()

    def click_material_drop_down_box(self):
        level_2_window = api.level_2_window(self.browser)
        self.case_page.material_drop_down_box(level_2_window).click()

    def click_sample_drop_down_box(self):
        level_2_window = api.level_2_window(self.browser)
        self.case_page.sample_drop_down_box(level_2_window).click()

    def choose_folder(self, folders: list):
        """
        选择弹出窗口上的文件夹
        :param folders: 一级、二级....N级文件夹组成的列表
        :return:
        """
        for folder in folders:
            if folder:
                self.case_page.location_folder(folder).click()
                time.sleep(0.5)

    def rename_case(self, case_name, new_name):
        """
        案件重命名
        :param case_name: 案件名
        :param new_name: 新案件名
        :return: None
        """
        self.case_context_menu_operate(case_name, '修改案件')
        rename_window = api.level_2_window(self.browser)
        case_name_input = self.case_page.case_name_input_box(rename_window)
        case_name_input.clear()
        case_name_input.send_keys(new_name)
        time.sleep(0.5)
        self.case_page.window_button(rename_window, '确定').click()

    def export_case(self, case_name, file_path, window_name):
        """
        导出案件
        :param case_name: 案件名
        :param file_path: 文件路径（不包含名称）
        :param window_name: 导出窗口标题名称
        :return: None
        """
        self.case_context_menu_operate(case_name, '导出案件')
        api.export_file(file_path, window_name)

    def import_case(self, file_path, window_name):
        """
        导入案件
        :param file_path: 案件路径（路径+名称）
        :param window_name: 导入窗口名称
        :return: None
        """
        self.case_page.case_button(button_name='导入案件').click()
        api.import_file(file_path, window_name)

    def export_case_accept_record(self, case_name, file_path, window_name):
        """"""
        self.case_context_menu_operate(case_name, button_name='导出案件受理记录')
        self.click_material_drop_down_box()
        time.sleep(0.5)
        self.choose_folder([case_name, '检材'])
        time.sleep(0.5)
        self.click_sample_drop_down_box()
        time.sleep(0.5)
        self.choose_folder([case_name, '样本'])
        time.sleep(0.5)
        level_2_window = api.level_2_window(self.browser)
        api.level_window_button(level_2_window, '确认').click()
        api.export_file(file_path, window_name)

    def del_case(self, case_name):
        """
        删除案件
        :param case_name:
        :return: None
        """
        case = self.case_page.find_case(case_name)
        self.context_menu_operate(case, button_name='删除案件')
        time.sleep(1)
        prompt_window = api.level_2_window(self.browser)
        self.case_page.window_button(prompt_window, '确定').click()
        time.sleep(1)

    def search_case(self, key_word):
        """
        输入关键字搜索案件
        :param key_word: 关键字
        :return: None
        """
        self.case_page.case_button(button_name='搜索案件').click()
        time.sleep(0.5)
        self.case_page.search_input().send_keys(key_word)

    def clear_search_keyword(self):
        """
        清除搜索输入框关键字，并将搜索输入框收起
        :return:
        """
        self.case_page.search_input().clear()
        time.sleep(0.5)
        self.case_page.case_button(button_name='搜索案件').click()

    def search_result(self) -> list:
        """
        定位案件列表所有案件元素
        :return: 所有案件元素对象
        """
        case_element_list = self.case_page.find_cases()
        return case_element_list

    def allocate_case_to_user(self, case_name, group_name, user_name):
        """
        分发案件给用户
        :param case_name: 案件名
        :param group_name: 用户组名称
        :param user_name: 用户名称
        :return: None
        """
        case = self.case_page.folder_name(case_name)
        self.context_menu_operate(case, '分发案件')
        allocate_window = api.level_2_window(self.browser)
        time.sleep(0.5)
        self.case_page.user_group_unfold_button(allocate_window, group_name).click()
        time.sleep(1)
        self.case_page.user_check_box(allocate_window, user_name).click()
        time.sleep(0.5)
        self.case_page.window_button(allocate_window, button_name='确定').click()

    def allocate_case_to_group(self, case_name, group_name):
        """
        给用户组分发案件
        :param case_name: 案件名称
        :param group_name: 用户组名称
        :return: None
        """
        case = self.case_page.folder_name(case_name)
        self.context_menu_operate(case, '分发案件')
        allocate_window = api.level_2_window(self.browser)
        time.sleep(1)
        self.case_page.user_group_check_box(allocate_window, group_name).click()
        time.sleep(0.5)
        self.case_page.window_button(allocate_window, button_name='确定').click()
        time.sleep(1)

    def context_menu_operate(self, target_element_object, button_name):
        """
        处理中的案件，（案件、文件、文件夹）右键操作
        :param target_element_object: 需要进行右键操作的元素对象
        :param button_name: 右键菜单按钮
        :return: None
        """
        # 在指定对象上点击鼠标右键
        ActionChains(self.browser).move_to_element(target_element_object).context_click(target_element_object).perform()
        time.sleep(1)
        # 点击右键菜单中的按钮
        self.case_page.file_context_menu(button_name).click()

    def add_file(self, folder_name, file_path, file_type='常见格式'):
        """
        给指定文件夹下上传音频文件
        :param folder_name: 目标文件夹名称
        :param file_path:
        :param file_type:
        :return:
        """
        folder = self.case_page.folder_name(folder_name)
        self.context_menu_operate(folder, button_name='添加文件')
        level_2_window = api.level_2_window(self.browser)
        self.case_page.file_format_radio_button(level_2_window, file_type).click()
        self.case_page.window_button(level_2_window, "浏 览").click()
        api.import_file(file_path, '打开')
        time.sleep(1)
        if file_type != 'Wavf':
            self.case_page.window_button(level_2_window, '开始转换').click()
            time.sleep(2)
        self.case_page.window_button(level_2_window, "开始上传").click()
        time.sleep(2)
        self.case_page.window_button(level_2_window, "确 定").click()
        time.sleep(1)

    def find_file(self, folder_name, file_name):
        """
        在文件夹下找文件
        :param folder_name: 文件夹名称
        :param file_name: 文件名称
        :return: 文件元素对象
        """
        self.case_page.unfold_and_hide_button(folder_name).click()
        time.sleep(0.5)
        result = self.case_page.find_file(folder_name, file_name)
        return result

    def restore_case(self):
        """
        案件回收站的案件进行还原
        :return: None
        """
        self.case_page.case_button('还原').click()
        prompt_window = api.level_2_window(self.browser)
        self.case_page.window_button(prompt_window, '确定').click()

    def get_audio_info(self, audio_name, info_name: str):
        """
        获取音频信息
        :param audio_name: 音频文件名
        :param info_name: 信息字段名
        :return: 音频信息
        """
        self.case_page.unfold_and_hide_case_button().click()
        self.case_page.unfold_and_hide_button(folder_name='检材').click()
        time.sleep(0.5)
        audio_file = self.case_page.find_file_by_name(audio_name)
        audio_file.click()
        time.sleep(0.5)
        ActionChains(self.browser).context_click(audio_file).perform()
        self.case_page.file_context_menu('文件详情').click()
        time.sleep(0.5)
        level_2_window = api.level_2_window(self.browser)
        info = self.case_page.audio_info(level_2_window, info_name)
        info_value = info.text
        return info_value

    def click_unfold_or_hide(self, folder_name):
        """
        点击展开或收拢“检材”“样本”“我的图片”列表
        :param folder_name: 文件对象（可选：“检材”“样本”“我的图片”）
        :return: None
        """
        self.case_page.unfold_and_hide_button(folder_name).click()

    def open_audio(self, folder_name, audio_name, window_index: int):
        """
        在指定的语谱图窗口
        :param folder_name: 文件对象（可选：“检材”“样本”“我的图片”）
        :param audio_name: 音频文件名称
        :param window_index: 窗口序号
        :return:
        """
        # 单击激活语谱图窗口
        view_window = self.view_page.view_window(window_index)
        view_window.click()
        time.sleep(0.5)
        # 双击指定文件夹下的音频打开到语谱图中
        self.click_unfold_or_hide(folder_name)
        audio_file = self.case_page.find_file(folder_name, audio_name)
        ActionChains(self.browser).double_click(audio_file).perform()


if __name__ == '__main__':
    import os
    from public.api import get_browser
    driver = get_browser()
    operate_case = OperateCase(driver)
    try:
        operate_case.switch_tab('案件列表')
        operate_case.export_case_accept_record('2020年9月1日', r'C:\Users\yaoch\Desktop', '导出案件受理记录')
        driver.quit()
    finally:
        os.system("taskkill /im 国音智能声纹鉴定专家系统.exe /f >nul 2>nul")
