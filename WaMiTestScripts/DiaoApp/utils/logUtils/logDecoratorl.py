# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2022/7/6 16:30
    @Project : httpFrame
    @File : logDecoratorl.py
====================================='''
from functools import wraps
from utils.logUtils.getLog import *

logger = getLog().logOut()

def log_decorator(switch: bool=True):
    """
    封装日志装饰器, 打印请求信息
    :param switch: 定义日志开关
    :return:
    """
    # 判断参数类型是否是 int 类型
    if isinstance(switch, bool):
        def decorator(func):
            @wraps(func)
            def swapper(*args, **kwargs):
                res = func(*args,**kwargs)

                # 判断日志为开启状态，才打印日志
                if switch:
                    if res is not None:
                        _dependent_case = kwargs['model'].dependence_case
                        # 判断如果有依赖数据，则展示
                        if _dependent_case is True:
                            _dependent_case = kwargs['model'].dependence_case
                        else:
                            _dependent_case = "暂无依赖用例数据"

                        _is_run = kwargs['model'].is_run
                        # 判断正常打印的日志，控制台输出绿色
                        if _is_run is None or _is_run is True:
                            logger.info(
                                f"\n>>===============================正在执行第{kwargs['case_num']}条用例======================================>>\n"
                                f"测试标题: {kwargs['model'].test_title}\n"
                                f"请求方式: {kwargs['model'].method}\n"
                                f"请求头:   {kwargs['model'].headers}\n"
                                f"请求路径: {kwargs['model'].url}\n"
                                f"传参方式： {kwargs['model'].req_params_type}\n"
                                f"请求内容: {kwargs['model'].data}\n"
                                f"依赖测试用例: {_dependent_case}\n"
                                f"接口响应内容: {kwargs['res'].text}\n"
                                f"接口响应时长: {kwargs['res'].elapsed.total_seconds()} s\n"
                                f"Http状态码: {kwargs['res'].status_code}\n"
                                f"断言方式：{kwargs['model'].assert_options}\n"
                                f"期望结果：{kwargs['model'].assert_value}\n"
                                f"实际结果：{kwargs['asserData']}\n"
                                f">>==============================第{kwargs['case_num']}条用例执行完毕=======================================>>"
                            )
                        else:
                            # 跳过执行的用例，控制台输出黄色
                            logger.warning(
                                f"\n=================================================================================\n"
                                "该条用例跳过执行.\n"
                                f"测试标题: {kwargs['model'].test_title}\n"
                                f"请求方式: {kwargs['model'].method}\n"
                                f"请求头:   {kwargs['model'].headers}\n"
                                f"请求路径: {kwargs['model'].url}\n"
                                f"传参方式： {kwargs['model'].req_params_type}\n"
                                f"请求内容: {kwargs['model'].data}\n"
                                f"依赖测试用例: {_dependent_case}\n"
                                "================================================================================="
                            )
                    return res
                else:
                    return res
            return swapper

        return decorator
    else:
        raise TypeError("日志开关只能为 Ture 或者 False")