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

    def execmd(self, ):
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


if __name__ == '__main__':
    rpc = RpcManage()
    menu_text = {
        '1': '显示所有任务',
        '2': '获取指定任务',
        '3': '执行命令'
    }
    menu_option = {
        '1': rpc.check_all,
        '2': rpc.check_task,
        '3': rpc.execmd
    }
    print('FabricRPC主机管理'.center(30, '*'))
    while True:
        for k, v in menu_text:
            print(k, v)
        choice = input('请选择菜单项[q=退出]:').strip()
        if choice == 'q': break
        if choice in menu_text:
            func = menu_option[choice]
            func()
        else:
            print('输入有误:菜单项不存在')
    pass
