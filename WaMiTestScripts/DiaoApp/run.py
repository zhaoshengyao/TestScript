# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2022/6/28 10:42
    @Project : httpFrame
    @File : run.py
====================================='''

import pytest
from DiaoApp.utils.logUtils.getLog import *
from DiaoApp.cfg.cfg import config
from DiaoApp.utils.emailUtils.sendEmail import sendEmail

os.chdir(os.getcwd())
logger = getLog().logOut()


def run():
    # 从配置文件中获取项目名称
    try:
        logger.info(
            """
                             _    _         _      _____         _
              __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
             / _` | '_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
            | (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
             \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
                  |_|
                  开始执行【{}】项目测试...
                """.format(config['project_name'])
        )

        pytest.main(['./case/test_httpRun.py', "-s", "--alluredir", './report/report'])
        os.system('allure serve ./report/report')

        # pytest.main(['-sv','./case/test_httpRun.py',
        #              '--alluredir', './report/tmp', "--clean-alluredir"])
        # os.system(r"allure generate ./report/tmp -o ./report/html --clean")

        """
                   --reruns: 失败重跑次数
                   --count: 重复执行次数
                   -v: 显示错误位置以及错误的详细信息
                   -s: 等价于 pytest --capture=no 可以捕获print函数的输出
                   -q: 简化输出信息
                   -m: 运行指定标签的测试用例
                   -x: 一旦错误，则停止运行
                   --maxfail: 设置最大失败次数，当超出这个阈值时，则不会在执行测试用例
                    "--reruns=3", "--reruns-delay=2"
                   """

        if config['is_send_email'] == True:
            sendEmail().send_email()

    except Exception:
        # 如有异常，相关异常发送邮件
        logger.error("运行错误！！！")
        raise


if __name__ == '__main__':
    run()