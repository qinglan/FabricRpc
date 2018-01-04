#!/usr/bin/evn python3
# -*- coding:utf-8 -*-
'''程序启动入口'''
__author__ = 'zween'
__mtime__ = '18-1-5'
import sys
from conf import setting

sys.path.insert(0, setting.BASE_DIR)


class RpcManage(object):
    def __init__(self):
        pass

    def check_task(self, taskid):
        '''
        获取指定的任务结果
        :param taskid:任务id
        '''
        pass

    def check_all(self):
        '显示所有的任务'
        pass

    def run(self, action):
        '''
        执行命令的函数
        :param action:命令格式如 ls 192.168.1.x
        '''
        pass

    def __call__(self, *args, **kwargs):
        '显示菜单;调用run函数执行命令'
        pass
