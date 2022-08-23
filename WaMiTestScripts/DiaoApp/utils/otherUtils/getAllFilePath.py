# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2022/7/27 17:28
    @Project : httpFrame
    @File : getAllFilePath.py
====================================='''
import os
from cfg.cfg import config

def get_all_files(file_path):
    """
    获取文件路径
    :param file_path: 目录路径
    :return:
    """
    filename = []
    # 获取所有文件下的子文件名称
    for root, dirs, files in os.walk(file_path):
        for filePath in files:
            path = os.path.join(root, filePath)
            filename.append(path)
    return filename

# print(config['report_path']+r'\html\test-cases')
# print(get_all_files(config['report_path']+r'\html\data\test-cases'))