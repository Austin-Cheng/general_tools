#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Austin
# date: 2020/4/27
from general_tools.acam import WordTree
from general_tools.database_handle.mysql_handle import MysqlHandler
from general_tools.database_handle import mysql_11


class AddressParser:
    base_whole = None
    base_part = None
    tree = None

    def __init__(self, address_str):
        self.address_str = address_str
        self.zone = {}

    @classmethod
    def cls_init(cls):
        mysql = MysqlHandler(**mysql_11)
        cls.base_whole = mysql.read('select distinct dq_name, dq_parent, dq_level from district_relation')
        cls.base_part = [d[0] for d in cls.base_whole]
        cls.tree = WordTree()
        cls.tree.build(cls.base_part)

    def extract_zone(self):
        res = self.tree.search_multi(self.address_str)
        for key in res.keys():
            if self.base_whole[key][2] == 3:
                self.zone['zone_3'] = self.base_whole[key][0]
            if self.base_whole[key][2] == 2:
                self.zone['zone_2'] = self.base_whole[key][0]
            if self.base_whole[key][2] == 1:
                self.zone['zone_1'] = self.base_whole[key][1]


if __name__ == '__main__':
    AddressParser.cls_init()
    ap = AddressParser('北京市海淀区万泉庄万柳光大西园6号楼')
    ap.extract_zone()
    print(ap.zone)

