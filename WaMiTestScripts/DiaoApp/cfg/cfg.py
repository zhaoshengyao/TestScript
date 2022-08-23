# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2022/3/29 15:44
    @Project : python_study
    @File : cfg.py
====================================='''
import os

if os.getcwd().endswith('DiaoApp'):
    jb_path = os.getcwd()
else:
    jb_path = os.getcwd().split('DiaoAPP')[0] + 'DiaoApp'

# 配置信息
config = {
    # 用例路径
    "filepath": jb_path + r'\data\case1.xlsx',
    # 测试excel报告路径
    "savepath": jb_path + r'\report\reportData',
    # 測試報告保存路徑
    "report_path": jb_path + r'\report',
    # 日志保存路径
    "logpath": jb_path + r'\Logs',
    # 请求路径
    "url": "http://110.80.137.11:8059",
    # token字段名
    "res_code": "code",
    "token": "TOKEN",
    # accesstoken生成条件
    "sc": "6r51iej1zfD4QuXm",
    # 测试人员
    "tester": "Yao",
    # 测试项目
    "project_name": "低傲app-主流程",
    # 邮箱配置
    "sender": ['lingtest2020@126.com', 'JEOOPAJFINZDEULG'],
    # 收件人
    "receiver": ["863758206@qq.com", "594432448@qq.com"],
    # 是否发送邮件
    "is_send_email": False
}
