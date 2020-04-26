#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Austin
# date: 2020/3/27
import pyorient


class OrientHandler:
    def __init__(self, host, port, user, pwd):
        self.client = pyorient.OrientDB(host, port)
        self.cur = self.client.connect(user=user, password=pwd)

    def __del__(self):
        self.client.close()

    def create_db(self, db_name):
        if not self.client.db_exists(db_name, pyorient.STORAGE_TYPE_PLOCAL):
            self.client.db_create(db_name, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_PLOCAL)
        self.open_db(db_name)

    def open_db(self, db_name):
        self.client.db_open(db_name, "admin", "admin")

    def drop_db(self, db_name):
        self.client.db_drop(db_name)

    def execute(self, sql):
        self.client.command(sql)

    def search(self, sql):
        return self.client.query(sql)

    def create_class(self, class_name, class_type):
        self.client.command('CREATE CLASS {c} IF NOT EXISTS EXTENDS {t}'.format(c=class_name, t=class_type))

    def drop_class(self, class_name):
        self.client.command('DROP CLASS {c} UNSAFE'.format(c=class_name))

    # property_type is in (String, integer, DATE)
    def create_property(self, class_name, property_name, property_type):
        self.client.command('CREATE PROPERTY {c}.`{p}` IF NOT EXISTS {t}'.format(c=class_name, p=property_name, t=property_type))

    def insert_dict(self, class_name, property_value_dict):
        self.client.command('INSERT INTO {c} Content {p}'.format(c=class_name, p=property_value_dict))

    def insert_tuple(self, class_name, property_tuple, value_tuple):
        property_str = ','.join(property_tuple)
        sql = 'INSERT INTO {c} ({p}) VALUES {v}'.format(c=class_name, p=property_str, v=value_tuple)
        self.client.command(sql)

    def delete_vertex(self):
        pass

    def delete_edge(self):
        pass

    def delete_index(self):
        pass


if __name__ == '__main__':
    o = OrientHandler('10.2.196.57', 2424, 'root', 'root')
    o.open_db('bid')
    res = o.search('match {class: company, as:c} return c.@fields')
    for r in res:
        print(r.oRecordData['fields'])


# db_list
# db_size
# db_count_records

# delete vertex from Class_Name where id = xxx

# match {as:c, class:Company, where:(id="qjzbgg_t20200310_1203627")}.outE(){as:p, class:Purchase}.outV(){as:v}
# return c.id, v.id, $pathElements








