#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Austin
# date: 2020/3/27
import configparser


conf = configparser.ConfigParser()
conf.read('D:\\ad_work\db_config')

orient_57 = {
    'host': conf.get('orient_57', 'host'),
    'port': int(conf.get('orient_57', 'port')),
    'user': conf.get('orient_57', 'user'),
    'pwd': conf.get('orient_57', 'pwd')
}

mysql_57 = {
    'host': conf.get('mysql_57', 'host'),
    'port': int(conf.get('mysql_57', 'port')),
    'database': conf.get('mysql_57', 'database'),
    'user': conf.get('mysql_57', 'user'),
    'password': conf.get('mysql_57', 'password'),
    'charset': conf.get('mysql_57', 'charset')
}

bert_153 = {
    'ip': conf.get('bert_153', 'ip'),
    'ner_model_dir': conf.get('bert_153', 'ner_model_dir'),
    'show_server_config': conf.getboolean('bert_153', 'show_server_config'),
    'check_version': conf.getboolean('bert_153', 'check_version'),
    'check_length': conf.getboolean('bert_153', 'check_length'),
    'mode': conf.get('bert_153', 'mode')
}


if __name__ == '__main__':
    print(mysql_57)
