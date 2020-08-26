#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import time
import pytest
from public import api
from operate.operate_case import OperateCase
from operate.operate_view import OperateView


@pytest.fixture(scope='class')
def init_test_view(login):
    # 登录系统并获得浏览器对象
    operate_case = OperateCase(login)
    operate_case.switch_tab('案件列表')
    operate_view = OperateView(login)
    yield operate_case, operate_view


class TestView:
    @staticmethod
    def test_add_tag(init_test_view):
        """给音素添加标记"""
        operate_case, operate_view = init_test_view
        data = api.read_excel('test_add_tag')
        # 根据案件名找到指定案件并打开案件
        case_name = data.get('case_name')
        operate_case.open_case(case_name)
        # 定义操作哪个语谱图窗口
        window_index = int(data.get('window_index'))
        # 获取当前标记个数
        current_tag_num = operate_view.get_tag_and_phoneme_num('标记', window_index)
        # 切换到音素标签页
        operate_view.switch_tab('音素', window_index)
        time.sleep(1)
        operate_view.add_tag(window_index)
        time.sleep(1)
        # 再次获取标记个数
        finally_tag_num = operate_view.get_tag_and_phoneme_num('标记', window_index)
        # 断言标记个数是否+1
        assert finally_tag_num == current_tag_num+1
        # 还原环境，删除标记
        operate_view.switch_tab('标记', window_index)
        operate_view.del_all_tag(window_index)

    @staticmethod
    def test_del_tag(init_test_view):
        """删除标记"""
        operate_case, operate_view = init_test_view
        data = api.read_excel('test_del_tag')
        # 根据案件名找到指定案件并打开案件
        case_name = data.get('case_name')
        operate_case.open_case(case_name)
        # 定义操作哪个语谱图窗口
        window_index = int(data.get('window_index'))
        # 在音素列表中添加一个标记
        operate_view.switch_tab('音素', window_index)
        time.sleep(0.5)
        operate_view.add_tag(window_index)
        time.sleep(0.5)
        # 获取当前标记个数
        current_tag_num = operate_view.get_tag_and_phoneme_num('标记', window_index)
        operate_view.switch_tab('标记', window_index)
        time.sleep(0.5)
        operate_view.del_all_tag(window_index)
        time.sleep(0.5)
        finally_tag_num = operate_view.get_tag_and_phoneme_num('标记', window_index)
        # 断言删除后的标记个数
        assert finally_tag_num == current_tag_num-1

    @staticmethod
    def test_filter_phoneme(init_test_view):
        """增加过滤音素"""
        operate_case, operate_view = init_test_view
        data = api.read_excel('test_filter_phoneme')
        # 根据案件名找到指定案件并打开案件
        case_name = data.get('case_name')
        operate_case.open_case(case_name)
        # 定义操作哪个语谱图窗口
        window_index = int(data.get('window_index'))
        # 切换到音素标签页
        operate_view.switch_tab('音素', 0)
        time.sleep(1)
        # 获取当前音素过滤数量
        current_filter_num = operate_view.get_filter_num(window_index)
        # 过滤一个音素
        operate_view.filter_phoneme(window_index)
        time.sleep(1)
        finally_filter_num = operate_view.get_filter_num(window_index)
        # 断言过滤数量是否+1
        assert current_filter_num+1 == finally_filter_num

    @staticmethod
    def test_cancel_filter_phoneme(init_test_view):
        """减少过滤音素"""
        operate_case, operate_view = init_test_view
        data = api.read_excel('test_cancel_filter_phoneme')
        # 根据案件名找到指定案件并打开案件
        case_name = data.get('case_name')
        operate_case.open_case(case_name)
        # 定义操作哪个语谱图窗口
        window_index = int(data.get('window_index'))
        # 切换到音素标签页
        operate_view.switch_tab('音素', window_index)
        time.sleep(1)
        # 获取当前音素过滤数量
        current_filter_num = operate_view.get_filter_num(window_index)
        # 取消过滤一个音素
        operate_view.cancel_filter_phoneme()
        time.sleep(1)
        finally_filter_num = operate_view.get_filter_num()
        assert current_filter_num-1 == finally_filter_num

    @staticmethod
    def test_add_8k_sampling_rate_file(init_test_view):
        """新增8K采样率音频文件"""
        operate_case, operate_view = init_test_view
        data = api.read_excel('test_add_8k_sampling_rate_file')
        # 新建案件
        case_name = api.create_case_name()
        operate_case.switch_tab('案件列表')
        operate_case.add_case(case_name)
        time.sleep(1)
        # 新建8K音频
        sampling_rate = data.get('sampling_rate')
        operate_view.add_file(0, sampling_rate)
        time.sleep(1)
        # 断言
        sampling_rate = operate_view.get_sampling_rate(0)
        assert sampling_rate == '8kHz'

    @staticmethod
    def test_add_16k_sampling_rate_file(init_test_view):
        """新增16K采样率音频文件"""
        operate_case, operate_view = init_test_view
        data = api.read_excel('test_add_16k_sampling_rate_file')
        # 新建案件
        case_name = api.create_case_name()
        operate_case.switch_tab('案件列表')
        operate_case.add_case(case_name)
        time.sleep(1)
        # 新建16K音频
        sampling_rate = data.get('sampling_rate')
        operate_view.add_file(0, sampling_rate)
        time.sleep(1)
        # 断言
        sampling_rate = operate_view.get_sampling_rate(0)
        assert sampling_rate == '16kHz'

    @staticmethod
    def test_add_32k_sampling_rate_file(init_test_view):
        """新增32K采样率音频文件"""
        operate_case, operate_view = init_test_view
        data = api.read_excel('test_add_32k_sampling_rate_file')
        # 新建案件
        case_name = api.create_case_name()
        operate_case.switch_tab('案件列表')
        operate_case.add_case(case_name)
        time.sleep(1)
        # 新建16K音频
        sampling_rate = data.get('sampling_rate')
        operate_view.add_file(0, sampling_rate)
        time.sleep(1)
        # 断言
        sampling_rate = operate_view.get_sampling_rate(0)
        assert sampling_rate == '32kHz'

    @staticmethod
    def test_get_snr(init_test_view):
        """获取音频文件SNR值"""
        operate_case, operate_view = init_test_view
        data = api.read_excel('test_get_snr')
        case_name = data.get('case_name')
        audio_name = data.get('audio_name')
        info_name = data.get('info_name')
        operate_case.open_case(case_name)
        snr_value = operate_case.get_audio_info(audio_name, info_name)
        time.sleep(3)
        assert snr_value

    @staticmethod
    def test_get_mos(init_test_view):
        """测试获取音频文件MOS值"""
        operate_case, operate_view = init_test_view
        data = api.read_excel('test_get_mos')
        case_name = data.get('case_name')
        audio_name = data.get('audio_name')
        info_name = data.get('info_name')
        operate_case.open_case(case_name)
        time.sleep(1)
        mos_value = operate_case.get_audio_info(audio_name, info_name)
        time.sleep(3)
        assert mos_value


if __name__ == '__main__':
    pytest.main()
