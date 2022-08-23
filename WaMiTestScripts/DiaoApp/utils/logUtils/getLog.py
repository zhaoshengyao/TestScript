# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2021/9/26 10:52
    @Project : Project
    @File : getLog.py
====================================='''
import os,  time
import logging,  colorlog

from logging import handlers
from pythonjsonlogger.jsonlogger import JsonFormatter  # python-json-logger
from DiaoApp.cfg.cfg import config


class getLog:

    def __init__(self, level=logging.INFO):
        """创建日志器"""
        self.log = logging.getLogger()
        self.log.setLevel(level)
        # 防止日志重复输出
        self.log.handlers.clear()  # 一、每次运行结束，清空handlers
        # self.log.handlers = []  # 二、每次调用，设置hanlers为空
        # self.path = os.path.join(os.path.dirname(os.path.dirname(__file__))) + '/Logs'  # 打开日志文件夹路径
        self.path = config['logpath']
        self.log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }
        # 判断目录是否存在
        isExists = os.path.exists(self.path)
        if not isExists:
            os.makedirs(self.path)

    def outPut_by_file(self, level=logging.INFO, type="time"):
        """文件处理器
        type:  # time：通过时间阶段日志文件；size：通过文件大小阶段日志文件
        默认通过时间隔断
        """
        if type.upper() == "TIME":
            # when: 间隔的时间单位：s:秒，m:分，h:小时,d:天，w:每周(interval == 0 ,代表星期一),midnight:每天凌晨
            # backCount: 备份文件的个数，如果超过这个个数，就会自动删除
            # :param level: 日志级别，默认DEBUG
            self.f_hand = handlers.TimedRotatingFileHandler(
                filename=r'{}/日志记录{}.log'.format(self.path, time.strftime('%Y%m%d')), when="midnight",
                backupCount=5,
                encoding='utf-8')

        elif type.upper() == "SIZE":
            self.f_hand = handlers.RotatingFileHandler(
                filename=r'{}/日志记录{}.log'.format(self.path, time.strftime('%Y%m%d')), mode='a',
                maxBytes=10 * 1024 * 1024,
                encoding='utf-8', backupCount=3)

        self.f_hand.setLevel(level)
        # 格式器 ：以json 格式写入文件
        fmt = '[%(asctime)s][%(filename)s]: [%(funcName)] [%(levelname)s]: %(lineno)d-->>%(message)s'
        self.f_hand.setFormatter(
            JsonFormatter(fmt=fmt, json_ensure_ascii=False))  # json_ensure_ascii=False 避免中文乱码

        return self.f_hand

    def outPut_by_stream(self, level=logging.INFO):
        """控制台输出"""
        self.s_hand = logging.StreamHandler()  # 通过不同级别，设置不同颜色--目前尚未实现
        self.s_hand.setLevel(level)
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s [%(asctime)s]-[%(filename)s]-[line:%(lineno)d] %(levelname)s-->: %(message)s',
            log_colors=self.log_colors_config)
        self.s_hand.setFormatter(formatter)

        return self.s_hand

    def logOut(self):
        self.log.addHandler(self.outPut_by_file())
        self.log.addHandler(self.outPut_by_stream())

        return self.log

# if __name__ == '__main__':
#     lo = getLog().logOut()
#     lo.info("111111")
#     lo.debug("2222222")
#     lo.error("333333")
#     lo.critical("444444")
#     lo.warning("5555555")