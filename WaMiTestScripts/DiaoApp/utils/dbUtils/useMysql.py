# -*- coding: utf-8 -*-
'''=====================================
    @Author : Daniel
    @Date : 2021/9/26 10:56
    @Project : Project
    @File : useMysql.py
====================================='''
import pymysql

from pymysql import converters
from utils.logUtils.getLog import *

class useMysql():
    def __init__(self, host, user, pwd, db, port, charset='utf8', autocommit=True):
        """数据库信息
        autocommit=True 直接提交
        """
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port
        self.charset = charset
        self.autocommit = autocommit
        self.log = getLog().logOut()

    def connect(self):
        '''获取连接信息'''
        # 把二进制转化为整形
        converions = converters.conversions
        converions[pymysql.FIELD_TYPE.BIT] = lambda x: '0' if '\x00' else '1'

        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db=self.db,
                                    conv=converions)
        self.cursor = self.conn.cursor()
        return self.cursor, self.conn

    def get_index_dict(self):
        """获取数据库对应表中的字段名"""
        index_dict = dict()
        index = 0
        for desc in self.cursor.description:
            index_dict[desc[0]] = index
            index = index + 1
        self.log.info("数据库字段为：{}".format(index_dict))
        return index_dict

    def get_dict_data_sql(self,data):
        """根据表中字段名，把查询结果转化成dict格式（默认是tuple格式）"""
        index_dict = self.get_index_dict()

        self.res = []
        for data_i in data:
            res_i = dict()
            for inde_i in index_dict:
                res_i[inde_i] = str(data_i[index_dict[inde_i]]) #把查询结果转成dict
            self.res.append(res_i)
        self.log.info("查询出的数据为：{}".format(self.res))

        self.cursor.close()
        self.conn.close()
        self.log.info("数据库操作完成，连接关闭。。。")
        return self.res

    def query_sql(self, sql, size=0):
        """
        :param sql: sql语句
        :param size: sql条数
        :return:
        """
        self.cursor, self.conn = self.connect()
        self.sql = sql.lower().strip()
        type = self.sql.split()[0]  # 获取操作类型
        self.log.info("将要执行的sql为：{}".format(self.sql))
        # 查询
        if self.sql.startswith('select'):
            count = self.cursor.execute(sql) #条数
            # print(count)
            self.log.info("本次执行【{}】操作，共计查询{}条".format(type,count))
            self.cursor.execute(sql)

            if size == 0:
                self.data = self.cursor.fetchall() #展示所有
                self.get_dict_data_sql(self.data)
                return count,self.data

            else:
                self.data = self.cursor.fetchmany(size) #只展示前size条
                self.get_dict_data_sql(self.data)
                return count,self.data

        # 增加、修改、删除
        elif self.sql.startswith('insert') or self.sql.startswith('update') or self.sql.startswith('delete'):
            # try:
            #     count = self.cursor.execute(sql)
            #     # print(count)
            #     self.cursor.execute(sql)
            #     self.conn.commit()
            #     self.log.info("本次执行【{}】操作,共【{}】次，提交完成。。。".format(type,count))
            # except Exception as err_msg:
            #     self.conn.rollback()
            #     self.log.error(err_msg)
            #     self.log.info("本次【{}】操作失败，执行回滚操作。。。".format(type))

            count = self.cursor.execute(sql)
            # print(count)
            self.cursor.execute(sql)
            self.conn.commit()
            self.log.info("本次执行【{}】操作,共【{}】次，提交完成。。。".format(type, count))

        self.cursor.close()
        self.conn.close()