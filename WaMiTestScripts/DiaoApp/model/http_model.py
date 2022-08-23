# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2022/3/25 10:40
    @Project : python_study
    @File : http_model.py
====================================='''


class http_model:
    # 用例标题
    case_num = None
    # 用例描述
    test_title = None

    url = None
    # 请求方式
    method = None
    # 测试数据
    data = None
    # 请求头部
    headers = None
    # 提取数据
    extract = None
    # 断言数据
    assert_data = None
    # 断言方式
    assert_options = None
    # 断言值
    assert_value = None
    # 是否需要提取值
    is_need = None

    # 是否执行
    is_run = None
    # 依赖用例编号
    dependence_case = None

    # 需要更新字段
    update_key = None
    # 上次提取的值
    last_value = None
    # 请求数据类型
    req_params_type = None
    # 接口描述
    detail = None
    # 存储结果、测试时间、测试人员的表格号-->   {result_num:[1,2],test_date_num:[2,2]}
    tester_msg = None

    # 用例sheet
    sheet_name = None