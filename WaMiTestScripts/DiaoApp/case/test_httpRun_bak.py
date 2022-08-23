# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2022/3/24 14:47
    @Project : python_study
    @File : httpRun.py
====================================='''

import allure
import jsonpath
import pytest

from DiaoApp.utils.excelUtils.excel_reader import *
from DiaoApp.utils.httpUtils.coreHttp import *
from DiaoApp.utils.logUtils.getLog import *
from DiaoApp.utils.projectUtils.wm_comm import *


class Test_case:
    logger = getLog().logOut()
    # 返回的数据
    contentData = {}
    read = readExcel()
    models = read.read_data_op()
    logger.info("-----------------------开始执行测试------------------------")
    logger.info("总共读取用例：{}条".format(len(models)))

    def teardown_class(self):
        self.read.save()
        self.logger.info("测试结果保存完毕，路径为：{}".format(config['savepath']))

    @allure.title("")  # 断言完成，更新标题
    @pytest.mark.parametrize("model", models)
    def test_send_http(self, model, **kwargs):
        '''
        :model:传入的数据对象
        :param kwargs:
        :return:
        '''
        self.logger.info(">>-----------------正在执行第{}条用例------------------->>".format(self.models.index(model) + 1))
        self.logger.info("当前请求url为:{}".format(model.url))
        self.logger.info("当前请求方式为：{}".format(model.method))
        self.logger.info("当前传参方式为：{}".format(model.req_params_type))
        self.logger.info("当前传入的数据为：{}".format(model.__dict__['data']))
        if model.is_need:  # 判断是否需要抽取的值
            if self.contentData:
                for value in model.last_value.split(","):
                    data_value = self.contentData[value]

                    # 低傲app  不适用传统header传参方式
                    # if model.req_params_type == 'data':
                    #     model.data = eval(model.data)
                    #     model.data.update({token:data_value})
                    # elif model.req_params_type == 'json':
                    #     model.headers = eval(model.headers)
                    #     model.headers.update({token:data_value})
                    # elif model.req_params_type == 'params':

                    #  低傲app，需要根据时间戳生成headers
                    if value == config['res_code']:
                        model.headers = comn().get_headers()
                        model.headers[config['token']] = data_value  # 更新token到headers

                    else:
                        model.headers = comn().get_headers()

                self.logger.info("原数据请求头为：{}".format(model.__dict__['headers']))

            else:
                raise Exception("期望全局变量中有数据，但是没有拿到数据")

        else:
            #  低傲app，需要根据时间戳生成headers
            model.headers = comn().get_headers()
            self.logger.info("当前传入的请求头为：{}".format(model.headers))

        ch = coreHttp()

        res = ch.send_http(model.method, model.req_params_type, model.url, model.data, model.headers, **kwargs)

        self.logger.info("接口响应状态：{}".format(res.status_code))
        self.logger.info("接口响应时间：{} s".format(res.elapsed.total_seconds()))  # 接口总响应时间：s
        self.logger.info("接口响应值为：{}".format(res.json()))

        # 抽取要传递给下一个接口的数据
        if model.extract != None and model.extract != '':
            # for ex in eval(model.extract):  # eval把字符串转成列表
            for ex in model.extract.split(','):  # 通过split把需要传递的元素字符串转换成列表进行遍历
                if ex in res.json().keys():
                    res_data = jsonpath.jsonpath(res.json(), '$..' + ex)
                    self.contentData.update({ex: res_data[0]})
        # 通过长度断言
        if model.assert_data.startswith('len'):
            asserData = [len(jsonpath.jsonpath(res.json(), '$..' + model.assert_data.split('(')[1][:-1])[0])]
        else:
            data_assert = jsonpath.jsonpath(res.json(), '$..' + model.assert_data)
            if str(data_assert) == 'False':  # 处理空值，防止报错
                asserData = ['返回数据格式与提取格式不一致，请检查返回数据是否正确！']
            else:
                asserData = jsonpath.jsonpath(res.json(), '$..' + model.assert_data)

        # 断言日志
        self.logger.info("断言方式为：{}".format(model.assert_options))
        self.logger.info("期望结果为：{}".format(model.assert_value))
        self.logger.info("实际结果为：{}".format(asserData[0]))

        # 进行断言
        try:
            if model.assert_options == "相等":
                assert asserData[0] == model.assert_value
            elif model.assert_options == "包含":
                assert asserData
            elif model.assert_options == "大于":
                assert asserData[0] < model.assert_value
            elif model.assert_options == "小于":
                assert asserData[0] > model.assert_value
            else:
                assert asserData[0] != model.assert_value

            self.logger.info("---------------------断言完成----------------------")
            allure.dynamic.title(model.test_title)  # 断言完成，更新allure标题

            # 断言完成，填写Excel用例中的数据
            self.write_reslut(model, "PASS")

        except Exception as e:
            self.logger.error("---------------------断言失败----------------------")
            allure.dynamic.title(model.test_title)  # 断言完成，更新标题
            self.write_reslut(model, "FAILD")
            raise e  # 保持异常状态，pytest判定为失败

        self.logger.info("---------------------第{}条用例执行完毕----------------------".format(self.models.index(model) + 1))

    def write_reslut(self, model, msg):
        '''把测试结果写入Excel'''
        self.read.write_value(model.sheet_name, model.tester_msg['result_num'][0], model.tester_msg['result_num'][1],
                              msg)
        self.read.write_value(model.sheet_name, model.tester_msg['test_date_num'][0],
                              model.tester_msg['test_date_num'][1],
                              time.strftime('%Y-%m-%d', time.localtime(time.time())))
        self.read.write_value(model.sheet_name, model.tester_msg['tester_num'][0], model.tester_msg['tester_num'][1],
                              config['tester'])


if __name__ == '__main__':
    pytest.main(['test_httpRun_bak.py', "-s", "--alluredir", './report/report'])
    os.system('allure serve ./report/report')
