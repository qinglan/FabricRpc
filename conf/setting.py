#!/usr/bin/evn python3
# -*- coding:utf-8 -*-
'''系统参数配置'''
__author__ = 'zween'
__mtime__ = '2018-1-4'

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_Path = os.path.join(BASE_DIR, 'db', 'host.ini')  # 数据库.ini文件保存位置
