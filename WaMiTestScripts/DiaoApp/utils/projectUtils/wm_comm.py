# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2022/6/24 17:09
    @Project : httpFrame
    @File : wm_comm.py
====================================='''
import time,requests,hashlib

from DiaoApp.cfg.cfg import *


class comn:

    def set_md5(self,str):
        '''
        转化md5
        :param str:
        :return:
        '''
        md5 = hashlib.md5()
        md5.update(str.encode('utf-8'))
        return md5.hexdigest()


    def get_pic_num(self,phone):
        '''获取图形验证码'''
        time_str = str(int(time.time()))
        api = '/Ctrls/NumberVerifyCode'
        data = {
            "phone": phone,
            "timespan": time_str
        }
        res = requests.get(config['url'] + api, params=data, headers=self.get_headers())
        if res:
            print("图形验证码获取成功")
        else:
            print("图形验证码错误")


    def send_code(self,phone):
        api = '/Ctrls/SendPhoneCode'
        data = {
            "phone": phone,
            "code": "123456"
        }
        res = requests.post(config['url'] + api, params=data, headers=self.get_headers())
        if res.json()['success'] is True:
            print("请求手机号：{} 发送成功！".format(phone))
        else:
            time.sleep(1)  # 发送短信报错请求频繁，等待1s
            requests.post(config['url'] + api, params=data, headers=self.get_headers())


    def get_headers(self):
        time_str = str(int(time.time()))
        headers = {
            "accesstoken": self.set_md5(time_str + config['sc']),
            "timespan": time_str
        }
        return headers