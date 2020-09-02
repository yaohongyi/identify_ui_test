#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import os
import pytest
import time
from public import api
from operate.operate_case import OperateCase
from operate.operate_view import OperateView


@pytest.fixture(scope='function')
def init_test_case(login):
    """初始化案件测试"""
    operate_case = OperateCase(login)
    operate_view = OperateView(login)
    operate_case.switch_tab('案件列表')
    yield operate_case, operate_view


class TestCase:
    @staticmethod
    def test_add_public_case(init_test_case):
        """新增共享案件"""
        operate_case, operate_view = init_test_case
        case_name = api.create_case_name()
        operate_case.add_case(case_name, '共享')
        operate_case.switch_tab('案件列表')
        test_result = operate_case.find_case_in_list(case_name)
        assert test_result

    @staticmethod
    def test_add_private_case(init_test_case):
        """新增私有案件"""
        operate_case, operate_view = init_test_case
        case_name = api.create_case_name()
        operate_case.add_case(case_name, '私有')
        operate_case.switch_tab('案件列表')
        test_result = operate_case.find_case_in_list(case_name)
        assert test_result

    @staticmethod
    def test_add_repetition_case(login, init_test_case):
        """新增重复案件"""
        operate_case, operate_view = init_test_case
        data = api.read_excel('test_add_repetition_case')
        case_name = api.create_case_name()
        # 新建案件
        operate_case.add_case(case_name)
        operate_case.switch_tab('案件列表')
        # 新建重复案件
        operate_case.add_case(case_name)
        # 获取提示信息
        prompt_message = api.prompt_message(login).text
        assert prompt_message == data.get('prompt_message')
        # 关闭新增案件窗口
        operate_case.close_add_case_window()

    @staticmethod
    def test_rename_case(init_test_case):
        """案件重命名"""
        operate_case, operate_view = init_test_case
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        operate_case.switch_tab('案件列表')
        operate_case.selected_case_in_list(case_name)
        new_case_name = case_name + '_rename'
        operate_case.rename_case(case_name, new_case_name)
        test_result = operate_case.find_case_in_list(new_case_name)
        assert test_result

    def test_export_case(self, init_test_case):
        """导出案件"""
        operate_case, operate_view = init_test_case
        data = api.read_excel('test_export_case')
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        operate_case.switch_tab('案件列表')
        operate_case.selected_case_in_list(case_name)
        file_path = data.get('file_path')
        window_name = data.get('window_name')
        file_name = file_path + os.path.sep + case_name + ".spk"
        operate_case.export_case(case_name, file_name, window_name)
        time.sleep(5)
        test_result = os.path.exists(file_name)
        assert test_result
        # 还原测试环境，删除导出的案件
        api.remove_spk(file_path)

    @staticmethod
    def test_import_case(init_test_case):
        """案件导入"""
        operate_case, operate_view = init_test_case
        data = api.read_excel('test_import_case')
        file_path = data.get('file_path')
        case_name = file_path.split('\\')[-1][:-4]
        window_name = data.get('window_name')
        operate_case.import_case(file_path, window_name)
        time.sleep(5)
        test_result = operate_case.find_case_in_list(case_name)
        assert test_result

    @staticmethod
    def test_del_case(init_test_case):
        """删除案件(案件移入回收站)"""
        operate_case, operate_view = init_test_case
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        operate_case.switch_tab('案件列表')
        # 选中案件
        operate_case.selected_case_in_list(case_name)
        operate_case.del_case(case_name)
        # 通过在列表查看案件是否被删除
        test_result = operate_case.find_case_in_list(case_name)
        assert test_result is None

    def test_search_case(self, init_test_case):
        """案件搜索"""
        operate_case, operate_view = init_test_case
        # 新建案件
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        # 切换到案件列表
        operate_case.switch_tab('案件列表')
        # 进行搜索
        operate_case.search_case(case_name)
        time.sleep(1)
        case_element_list = operate_case.search_result_in_list(case_name)
        test_result = False
        if len(case_element_list):
            for case_element in case_element_list:
                case_name = case_element.text
                find_result = case_name.find(case_name)
                if find_result == -1:
                    test_result = False
                else:
                    test_result = True
        else:
            test_result = False
        assert test_result
        # 还原环境
        operate_case.clear_search_keyword()

    @staticmethod
    def test_export_case_accept_record(init_test_case):
        """导出案件受理记录"""
        operate_case, operate_view = init_test_case
        data = api.read_excel('test_export_case_accept_record')
        # 新建案件
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        # 新建检材文件夹，并上传音频
        operate_case.add_folder(case_name, '检材')
        time.sleep(0.5)
        operate_case.click_unfold_or_hide(case_name)
        file_path = data.get('material_audio')
        operate_case.add_file('检材', file_path)
        # 新建样本文件夹，并上传音频
        operate_case.add_folder(case_name, '样本')
        time.sleep(0.5)
        file_path = data.get('sample_audio')
        operate_case.add_file('样本', file_path)
        # 切换到案件列表标签页
        operate_case.switch_tab('案件列表')
        # 导出案件受理记录
        export_path = data.get('export_path')
        file_name = export_path + os.path.sep + f"案件《{case_name}》受理记录.docx"
        export_window_name = data.get('export_window_name')
        operate_case.export_case_accept_record(case_name, file_path, export_window_name)
        # 断言
        test_result = os.path.exists(file_name)
        assert test_result
        api.remove_doc(export_path)

    @staticmethod
    def test_allocate_case_to_user(login, init_test_case):
        """将分发案件给单个用户"""
        operate_case, operate_view = init_test_case
        data = api.read_excel('test_allocate_case_to_user')
        group_name = data.get('group_name')
        user_name = data.get('user_name')
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        operate_case.allocate_case_to_user(case_name, group_name, user_name)
        time.sleep(1)
        prompt_message = api.prompt_message(login).text
        time.sleep(1)
        assert prompt_message == data.get('prompt_message')

    @staticmethod
    def test_allocate_case_to_group(login, init_test_case):
        """分发案件给用户组"""
        operate_case, operate_view = init_test_case
        data = api.read_excel('test_allocate_case_to_group')
        group_name = data.get('group_name')
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        operate_case.allocate_case_to_group(case_name, group_name)
        prompt_message = api.prompt_message(login).text
        assert prompt_message == data.get('prompt_message')

    @staticmethod
    def test_case_recycle_search(init_test_case):
        """案件回收站搜索功能"""
        operate_case, operate_view = init_test_case
        data = api.read_excel('test_case_recycle_search')
        # 新建案件
        key_word = data.get('key_word')
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        # 切换到案件列表
        operate_case.switch_tab('案件列表')
        time.sleep(0.5)
        # 删除案件
        operate_case.del_case(case_name)
        time.sleep(1)
        # 进入案件回收站
        operate_case.switch_tab('回收站')
        time.sleep(1)
        # 进行搜索
        operate_case.search_case(key_word)
        time.sleep(1)
        # 对搜索结果进行断言
        case_element_list = operate_case.search_result_in_recycle(case_name)
        test_result = False
        if len(case_element_list):
            for case_element in case_element_list:
                case_name = case_element.text
                find_result = case_name.find(key_word)
                if find_result == -1:
                    test_result = False
                else:
                    test_result = True
        else:
            test_result = False
        assert test_result
        # 环境还原
        operate_case.clear_search_keyword()

    @staticmethod
    def test_case_recycle_restore(init_test_case):
        """案件回收站还原案件功能"""
        operate_case, operate_view = init_test_case
        # 新建案件
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        # 切换到案件列表
        operate_case.switch_tab('案件列表')
        # 删除案件
        operate_case.selected_case_in_list(case_name)
        operate_case.del_case(case_name)
        time.sleep(1)
        # 进入案件回收站
        operate_case.switch_tab('回收站')
        time.sleep(1)
        # 选中案件进行案件还原
        operate_case.selected_case_in_recycle(case_name)
        operate_case.restore_case()
        time.sleep(1)
        # 切换到案件列表
        operate_case.switch_tab(tab_name='案件列表')
        test_result = operate_case.find_case_in_recycle(case_name)
        assert test_result

    @staticmethod
    def test_case_recycle_del(init_test_case):
        """删除案件回收站的案件"""
        operate_case, operate_view = init_test_case
        # 新建案件
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        # 切换到案件列表
        operate_case.switch_tab('案件列表')
        # 删除案件
        operate_case.selected_case_in_list(case_name)
        operate_case.del_case(case_name)
        time.sleep(1)
        # 进入案件回收站
        operate_case.switch_tab('回收站')
        time.sleep(1)
        # 案件彻底删除
        operate_case.selected_case_in_recycle(case_name)
        operate_case.complete_del_case(case_name)
        time.sleep(1)
        # 查看案件是否成功删除
        test_result = operate_case.find_case_in_recycle(case_name)
        assert not test_result

    def test_upload_wav(self, init_test_case):
        operate_case, operate_view = init_test_case
        # 读取excel数据
        data = api.read_excel('test_upload_wav')
        file_path = data.get('file_path')
        assert_result = data.get('assert_result')
        # 新建案件
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        # 上传音频
        operate_case.add_file(case_name, file_path)
        # 验证音频是否存在
        result = operate_case.find_file(case_name, assert_result)
        assert result

    def test_upload_android_amr(self, init_test_case):
        """添加安卓微信音频文件"""
        operate_case, operate_view = init_test_case
        # 读取excel数据
        data = api.read_excel('test_upload_android_amr')
        file_path = data.get('file_path')
        file_type = data.get('file_type')
        assert_result = data.get('assert_result')
        # 新建案件
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        # 上传音频
        operate_case.add_file(case_name, file_path, file_type)
        # 验证音频是否存在
        result = operate_case.find_file(case_name, assert_result)
        assert result

    def test_upload_pcm(self, init_test_case):
        """添加pcm音频文件"""
        operate_case, operate_view = init_test_case
        # 读取excel数据
        data = api.read_excel('test_upload_pcm')
        file_path = data.get('file_path')
        file_type = data.get('file_type')
        assert_result = data.get('assert_result')
        # 新建案件
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        # 上传音频
        operate_case.add_file(case_name, file_path, file_type)
        # 验证音频是否存在
        result = operate_case.find_file(case_name, assert_result)
        assert result

    def test_upload_wavf(self, init_test_case):
        """添加wavf音频文件"""
        operate_case, operate_view = init_test_case
        # 读取excel数据
        data = api.read_excel('test_upload_wavf')
        file_path = data.get('file_path')
        file_type = data.get('file_type')
        assert_result = data.get('assert_result')
        # 新建案件
        case_name = api.create_case_name()
        operate_case.add_case(case_name)
        # 上传音频
        operate_case.add_file(case_name, file_path, file_type)
        # 验证音频是否存在
        result = operate_case.find_file(case_name, assert_result)
        assert result


if __name__ == '__main__':
    ...
