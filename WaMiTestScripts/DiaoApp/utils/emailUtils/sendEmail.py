# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2021/9/26 10:56
    @Project : Project
    @File : sendEmail.py
====================================='''
import zmail

from DiaoApp.cfg.cfg import config
from DiaoApp.utils.otherUtils.allureReportData import CaseCount, allureFileClean


class sendEmail:

    def __init__(self):
        '''
        设置邮件内容
        :param subject: 主题
        :param content_text: 正文
        :param attachments: 附件
        '''
        # self.subject = subject  # 主题
        # self.content_text = content_text  # 正文
        # self.attachments = attachments  # 附件

        self.getData = config['receiver'] # 收件人
        self.send_user = config['sender']  # 发件人、授权码
        self.name = config['project_name']
        self.allureData = CaseCount()
        self.PASS = self.allureData.pass_count()
        self.FAILED = self.allureData.failed_count()
        self.BROKEN = self.allureData.broken_count()
        self.SKIP = self.allureData.skipped_count()
        self.TOTAL = self.allureData.total_count()
        self.RATE = self.allureData.pass_rate()
        self.CaseDetail = allureFileClean().get_failed_cases_detail()

    def send_email(self, cc=None):
        '''
        配置发送、接收、抄送人员
        :param sender: 发送人
        :param receiver: 接收人
        :param cc: 抄送人
        :return:
        '''
        msg = {
            'subject': config['project_name']+"--接口自动化报告",
            'content_text': """
            各位同事, 大家好:
                自动化用例执行完成，执行结果如下:
                用例运行总数: {} 个
                通过用例个数: {} 个
                失败用例个数: {} 个
                异常用例个数: {} 个
                跳过用例个数: {} 个
                成  功   率: {} %
    
            {}
    
            **********************************
            jenkins地址：https://121.xx.xx.47:8989/login
            详细情况可登录jenkins平台查看，非相关负责人员可忽略此消息。谢谢。
            """.format(self.TOTAL, self.PASS, self.FAILED, self.BROKEN, self.SKIP, self.RATE, self.CaseDetail)
            # 'attachments': self.attachments
        }
        # 1、创建发送邮件的服务
        self.emailServer = zmail.server(*self.send_user)
        # 2、发送邮件
        self.emailServer.send_mail(self.getData, msg, cc=cc)