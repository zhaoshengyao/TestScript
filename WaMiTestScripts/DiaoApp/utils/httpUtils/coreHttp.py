# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2022/3/23 17:01
    @Project : python_study
    @File : coreHttp.py
====================================='''
import requests, json


class coreHttp:

    def send_http(self, method, req_params_type, url=None, data=None, headers=None, **kwargs):
        '''
        :param method:
        :param url:
        :param data:
        :param headers:
        :param kwargs:
        :return:
        '''
        if req_params_type == 'json':
            try:
                datas = eval(eval(json.dumps(data, ensure_ascii=False)))  # 不要把汉字转为ascll码
            except Exception as e:
                raise Exception("无法转换为JSON，请检查输入格式!", e)
            res = getattr(requests, method)(url, json=datas, headers=headers, **kwargs)
        elif req_params_type == 'data':
            res = getattr(requests, method)(url, data=eval(data), headers=headers, **kwargs)
        else:
            if data:
                res = getattr(requests, method)(url, params=eval(data), headers=headers, **kwargs)
            else:
                res = getattr(requests, method)(url,  headers=headers, **kwargs)

        res.encoding = 'utf-8'
        return res
