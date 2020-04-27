#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Austin
# date: 2020/4/23
import re


class MoneyParser:
    def __init__(self, money_sentence):
        self.money_sentence = money_sentence
        self.__cap_money_list = []
        self.__digit_money_list = []
        self.__money_list = []

    @property
    def money_list(self):
        return self.__money_list

    def money_extract(self):
        pat1 = '(\d+\.?\d*[万元亿百千]+)'
        pat2 = '[壹贰叁肆伍陆柒捌玖拾佰仟亿角分零万元]{3,}'
        self.__digit_money_list = re.findall(pat1, self.money_sentence)
        self.__cap_money_list = re.findall(pat2, self.money_sentence)
        self.money_unify()

    def money_unify(self):
        for cap_money in self.__cap_money_list:
            self.__money_list.append(self.cap_money_unify(cap_money))
        for digit_money in self.__digit_money_list:
            self.__money_list.append(self.digit_money_unify(digit_money))

    @staticmethod
    def digit_money_unify(money_str):
        digits = float(re.search('(\d+\.?\d*)', money_str).group(1))
        if '万' in money_str:
            digits *= 10000
        elif '亿' in money_str:
            digits *= 100000000
        return round(digits, 2)

    @staticmethod
    def cap_money_unify(money_str):
        caps = '壹贰叁肆伍陆柒捌玖'
        cap_dict = {'壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9}
        units = '分角元拾佰仟万亿'
        unit_order = {'分': 1, '角': 2, '元': 3, '拾': 4, '佰': 5, '仟': 6, '万': 7, '亿': 8}
        unit_value = {'分': 0.01, '角': 0.1, '元': 1, '拾': 10, '佰': 100, '仟': 1000, '万': 10000, '亿': 100000000}
        entire = 0
        cur_digit = 0
        pre_unit = 100
        flag = 1
        for w in money_str:
            if w in caps:
                cur_digit = cap_dict[w]
                flag = 1
            elif w in units:
                cur_unit = unit_order[w]
                if not flag:
                    entire *= unit_value[w]
                else:
                    if cur_unit > pre_unit:
                        entire = (entire + cur_digit) * unit_value[w]
                    else:
                        entire += cur_digit * unit_value[w]
                pre_unit = cur_unit
                flag = 0
        return round(entire, 2)


if __name__ == '__main__':
    from general_tools.database_handle.mysql_handle import MysqlHandler
    from general_tools.database_handle import mysql_57
    mysql = MysqlHandler(**mysql_57)
    data = mysql.read('select distinct content from bid_split where item like "%金额%"')
    for d in data:
        if d[0] == '323.8158万元':
            print('waiting')
        money = MoneyParser(d[0])
        money.money_extract()
        print(d[0], money.money_list)

