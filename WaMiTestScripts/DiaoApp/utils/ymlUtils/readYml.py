# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2021/9/26 10:55
    @Project : Project
    @File : readYml.py
====================================='''
import yaml

from utils.logUtils.getLog import *


path = os.path.join(os.path.dirname(os.path.dirname(__file__)))+'/TestData'
log = getLog().logOut()

def readYml(filename='test.yml'):
    '''读取yaml文件'''
    filepath = path+'/'+filename
    try:
        with open(filepath,'r',encoding='utf-8') as f:
            yaml_data_dic = yaml.load(f.read()) # 把读取出来的数据转成dict
            log.info("读取成功，读取数据：{}".format(yaml_data_dic))
            return yaml_data_dic

    except Exception as e:
        log.info('读取失败' + filepath, e)


def update_yaml(key=None, value=None, filename='test.yml'):
    '''
    先读取后写入
    :param key: 需要修改的key
    :param value: 需要修改的值
    :param filename: 文件名
    :return:
    '''
    filepath = path + '/' + filename
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            yaml_data_dic = yaml.load(f.read())
            log.info("读取成功，更新前数据：{}".format(yaml_data_dic))

            # 修改的值
            yaml_data_dic[key] = value
            with open(filepath, 'w', encoding='utf-8') as w_f:
                # 写入
                yaml.dump(yaml_data_dic, w_f,allow_unicode=True)
                log.info("数据更新成功，更新后数据：{}".format(yaml_data_dic))

    except Exception as e:
        log.info('更新文件失败' + filepath, e)