#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Austin
# date: 2020/4/7
import pymysql


class MysqlHandler:
    def __init__(self, host, database, user, password, charset, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.charset = charset
        self.port = port
        self.con = self.connect()

    def connect(self):
        con = pymysql.connect(host=self.host, database=self.database, user=self.user,
                              password=self.password, charset=self.charset)
        return con

    def read(self, sql):
        cur = self.con.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        return data

    def insert(self, table_name, column_list, value_list, condition=''):
        cur = self.con.cursor()
        column_str = ','.join(column_list)
        value_format = ', '.join(['%s'] * len(value_list))
        sql = 'insert into {t} ({c}) VALUES ({v}) {o}'.format(t=table_name, c=column_str, v=value_format, o=condition)
        cur.execute(sql, value_list)
        self.con.commit()
        cur.close()

    def execute(self, sql):
        cur = self.con.cursor()
        cur.execute(sql)
        self.con.commit()
        cur.close()

    def __del__(self):
        self.con.close()


