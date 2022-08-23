# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2022/3/24 14:47
    @Project : python_study
    @File : httpRun.py
====================================='''

import jsonpath, pytest, allure, time, json, random

from DiaoApp.utils.httpUtils.coreHttp import *
from DiaoApp.utils.excelUtils.excel_reader import *
from DiaoApp.utils.projectUtils.wm_comm import *
from DiaoApp.utils.logUtils.logDecoratorl import *
from DiaoApp.utils.otherUtils.Tools import *


class Test_case:
    # 返回的数据
    contentData = {}
    read = readExcel()
    models = read.read_data_op()
    logger.info("\n===========================开始执行测试===========================\n")
    logger.info("总共读取用例：{}条".format(len(models)))

    def teardown_class(self):
        self.read.save()
        logger.info("测试结果保存完毕，路径为：{}".format(config['savepath']))

    @classmethod
    @log_decorator()
    def check_params(self, *args, **kwargs):
        '''
        调用日志装饰器
        '''
        return args, kwargs

    @allure.title("")  # 断言完成，更新标题
    @pytest.mark.parametrize("model", models)
    def test_send_http(self, model, **kwargs):
        '''
        :model:传入的数据对象
        :param kwargs:
        :return:
        '''
        # 记录当前用例顺序
        case_num = self.models.index(model) + 1

        allure.step(f"请求URL: {model.url}")
        allure.step(f"请求方式: {model.method}")
        allure.step(f"请求头: {model.headers}")
        allure.step(f"请求数据: {model.data}")
        allure.step(f"依赖数据: {model.dependence_case}")
        allure.step(f"预期数据: {model.assert_value}")

        model.headers = comn().get_headers()
        if model.is_need:  # 判断是否需要抽取的值
            if self.contentData:
                print(self.contentData)
                # 获取登录token并传入header
                model.headers = comn().get_headers()
                model.headers[config['token']] = self.contentData[config['res_code']]

                # 通过切片获取需要取的值，因为code在第一个所以下标从1往后取
                last_value_list = model.last_value.split(",")[1:]
                for i in range(len(last_value_list)):
                    value = last_value_list[i]
                    data_value = self.contentData[value]

                    # 修改data中需要更新的字段
                    # 注：case中update_key中的值必须与对应last_value中code后的值以及顺序一致
                    if model.update_key is not None:
                        up_key_list = model.update_key.split(",")
                        up_key = up_key_list[i]
                        model.data = json.loads(model.data)
                        model.data[up_key] = str(data_value)
                        model.data = json.dumps(model.data)
                # for value in model.last_value.split(",")[1:]:
                #     data_value = self.contentData[value]

                    # 低傲app  不适用传统header传参方式
                    # if model.req_params_type == 'data':
                    #     model.data = eval(model.data)
                    #     model.data.update({token:data_value})
                    # elif model.req_params_type == 'json':
                    #     model.headers = eval(model.headers)
                    #     model.headers.update({token:data_value})
                    # elif model.req_params_type == 'params':

                    #  低傲app，需要根据时间戳生成headers
                    # if value == config['res_code']:
                    #     model.headers[config['token']] = data_value  # 更新token到headers
                    # else:
                    # 更新data中需要获取的字段
                    # if model.update_key is not None:
                    #     for up_key in model.update_key.split(","):
                    #         model.data = json.loads(model.data)
                    #         model.data[up_key] = data_value
                    #         model.data = json.dumps(model.data)

            else:
                raise Exception("期望全局变量中有数据，但是没有拿到数据")

        else:
            #  低傲app，需要根据时间戳生成headers
            model.headers = comn().get_headers()

        ch = coreHttp()
        time.sleep(2)
        res = ch.send_http(model.method, model.req_params_type, model.url, model.data, model.headers, **kwargs)

        if res.status_code == 200:
            # 抽取要传递给下一个接口的数据
            if model.extract is not None and model.extract != '':
                # for ex in eval(model.extract):  # eval把字符串转成列表

                for ex in model.extract.split(','):  # 通过split把需要传递的元素字符串转换成列表进行遍历
                    deep_data = Tools().findKey(ex, res.json())
                    # if deep_data:
                    #     self.contentData.update({ex: deep_data[0]})
                    try:
                        x = random.randint(0, len(deep_data)-1)
                        if deep_data:
                            self.contentData.update({ex: deep_data[x]})
                    except Exception as e:
                        raise e
            # 通过长度断言
            if model.assert_data.startswith('len'):
                asserData = [len(jsonpath.jsonpath(res.json(), '$..' + model.assert_data.split('(')[1][:-1])[0])]
            else:
                data_assert = jsonpath.jsonpath(res.json(), '$..' + model.assert_data)
                if str(data_assert) == 'False':  # 处理空值，防止报错
                    asserData = ['返回数据格式与提取格式不一致，请检查返回数据是否正确！']
                else:
                    asserData = jsonpath.jsonpath(res.json(), '$..' + model.assert_data)

            # 进行断言
            try:
                if model.assert_options == "相等":
                    assert asserData[0] == model.assert_value
                elif model.assert_options == "包含":
                    assert model.assert_value in asserData[0]
                elif model.assert_options == "大于":
                    assert asserData[0] < model.assert_value
                elif model.assert_options == "小于":
                    assert asserData[0] > model.assert_value
                else:
                    assert asserData[0] != model.assert_value

                allure.dynamic.title(model.test_title)  # 断言完成，更新allure标题

                # 断言完成，填写Excel用例中的数据
                self.write_reslut(model, "PASS")
                kwargs_data = {
                    "res": res,
                    "asserData": asserData,
                    "case_num": case_num,
                    "model": model
                }

                self.check_params(**kwargs_data)

            except Exception as e:
                allure.dynamic.title(model.test_title)  # 断言完成，更新标题
                self.write_reslut(model, "FAILD")
                logger.error(e)
                kwargs_data = {
                    "res": res,
                    "asserData": asserData,
                    "case_num": case_num,
                    "model": model
                }
                self.check_params(**kwargs_data)
                raise e  # 保持异常状态，pytest判定为失败

        else:
            asserData = res.json()

            try:
                assert res.status_code == 200
            except Exception as e:
                allure.dynamic.title(model.test_title)
                msg = "Error\n" + res.text
                self.write_reslut(model, msg)
                logger.error(e)
                kwargs_data = {
                    "res": res,
                    "asserData": asserData,
                    "case_num": case_num,
                    "model": model
                }
                self.check_params(**kwargs_data)
                raise e


    def write_reslut(self, model, msg):
        '''把测试结果写入Excel'''
        self.read.write_value(model.sheet_name,
                              model.tester_msg['result_num'][0],
                              model.tester_msg['result_num'][1],
                              msg)
        self.read.write_value(model.sheet_name,
                              model.tester_msg['test_date_num'][0],
                              model.tester_msg['test_date_num'][1],
                              time.strftime('%Y-%m-%d',time.localtime(time.time())))
        self.read.write_value(model.sheet_name,
                              model.tester_msg['tester_num'][0],
                              model.tester_msg['tester_num'][1],
                              config['tester'])

# if __name__ == '__main__':
#     pytest.main(['test_httpRun.py', "-s", "--alluredir", '../report/report'])
#     os.system('allure serve ../report/report')
