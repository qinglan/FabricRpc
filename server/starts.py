# -*- coding:utf-8 -*-
# !/usr/bin/env python3
'''RPC服务端启动入口'''
__author__ = 'zween'
__mtime__ = '2018/1/12'

import sys
from conf import setting

sys.path.insert(0, setting.BASE_DIR)
from server import host, rpcserver

menu_text = {
    '1': '主机管理',
    '2': '启动RPCServer'
}
menu_option = {
    '1': host.Host,
    '2': rpcserver.RpcServer
}

if __name__ == '__main__':
    print('RPC服务端'.center(30, '*'))
    while True:
        for k, v in menu_text.items():
            print(k, v)
        choice = input('请选择菜单项[q=退出]:')
        if choice == 'q': break
        if choice in menu_text:
            func = menu_option[choice]
            obj = func()  # 执行init方法
            obj()  # 调用call方法
        else:
            print('输入有误:菜单项不存在')
    print('exit now.')
