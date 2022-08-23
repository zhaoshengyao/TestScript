# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2022/7/27 17:19
    @Project : httpFrame
    @File : allureReportData.py
====================================='''
import json
from DiaoApp.utils.otherUtils.getAllFilePath import get_all_files
from DiaoApp.cfg.cfg import config


class allureFileClean:

    def get_testcases(self):
        '''
        獲取所有用例數據
        '''
        files = []
        for i in get_all_files(config['report_path'] + r'\html\data\test-cases'):
            with open(i, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
                files.append(data)
        # print(files)
        return files

    def get_failed_case(self):
        """ 获取到所有失败的用例标题和用例代码路径"""
        error_case = []
        for i in self.get_testcases():
            if i['status'] == 'failed' or i['status'] == 'broken':
                error_case.append((i['name'], i['fullName']))
        # print(error_case)
        return error_case

    def get_failed_cases_detail(self):
        """ 返回所有失败的测试用例相关内容 """
        data = self.get_failed_case()
        # 判断有失败用例，则返回内容
        if len(data) >= 1:
            values = "失败用例:\n"
            values += "        **********************************\n"
            for i in data:
                values += "        " + i[0] + ":" + i[1] + "\n"
            # print(values)
            return values
        else:
            # 如果没有失败用例，则返回False
            return ""

    @classmethod
    def get_case_count(cls):
        """ 统计用例数量 """
        fil_name = config['report_path'] + r'\html\widgets\summary.json'
        with open(fil_name, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
        # print(data)
        return data


class CaseCount:
    def __init__(self):
        self.AllureData = allureFileClean()

    def pass_count(self) -> int:
        """用例成功数"""
        return self.AllureData.get_case_count()['statistic']['passed']

    def failed_count(self) -> int:
        """用例失败数"""
        return self.AllureData.get_case_count()['statistic']['failed']

    def broken_count(self) -> int:
        """用例异常数"""
        return self.AllureData.get_case_count()['statistic']['broken']

    def skipped_count(self) -> int:
        """用例跳过数"""
        return self.AllureData.get_case_count()['statistic']['skipped']

    def total_count(self) -> int:
        """用例总数"""
        return self.AllureData.get_case_count()['statistic']['total']

    def pass_rate(self) -> float:
        """用例成功率"""
        # 四舍五入，保留2位小数
        try:
            pass_rate = round(self.pass_count() / self.total_count() * 100, 2)
            return pass_rate
        except ZeroDivisionError:
            return 0.00

    def get_times(self):
        """用例执行时长"""
        run_time = round(self.AllureData.get_case_count()['time']['duration'] / 1000, 2)
        return run_time
