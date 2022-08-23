# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2022/7/6 16:34
    @Project : httpFrame
    @File : runTimeDecoratorl.py
====================================='''
from utils.logUtils.getLog import *

logger = getLog().logOut()

def execution_duration(number: int):
    """
    封装统计函数执行时间装饰器
    :param number: 函数预计运行时长
    :return:
    """
    # 判断参数类型是否是 int 类型
    if isinstance(number, int):
        def decorator(func):
            def swapper(*args, **kwargs):
                res = func(*args,model = kwargs['model'])
                run_time = round(res.elapsed.total_seconds())
                # 计算时间戳毫米级别，如果时间大于number，则打印 函数名称 和运行时间
                if run_time > number:
                    logger.error(
                        "\n=================================================================================\n"
                        "测试用例执行时间较长，请关注.\n"
                        "函数运行时间:{0} ms\n"
                        "测试用例相关数据: {1}\n"
                        "================================================================================="
                        .format(run_time, func(*args, **kwargs)))

                return res

            return swapper

        return decorator
    else:
        raise TypeError("参数类型不正确")