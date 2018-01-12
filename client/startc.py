#!/usr/bin/evn python3
# -*- coding:utf-8 -*-
'''程序启动入口'''
__author__ = 'zween'
__mtime__ = '18-1-5'
import os, sys, re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
from client import rpcclient


class RpcManage(object):
    def __init__(self):
        self.task_info = {}  # rpc任务字典

    def check_task(self):
        '获取指定的任务结果'
        for t, v in self.task_info.items():
            print('任务Id:', t, '主机IP:', v['IP'], '执行命令:', v['cmd'], '回调队列:', v['queue_name'])
        while True:
            choice = input('请输入要查看的任务Id[q=退出]:').strip()
            if choice == 'q': break
            if choice in self.task_info:
                objC = self.task_info[choice]['Instance']  # rpcclient.RpcClient(self.rpcserver)
                result = objC.get_response(choice, self.task_info[choice]['queue_name'])
                print('\033[32;1m命令返回结果:\033[0m', result.decode())
                self.task_info[choice]['Result'] = result
            else:
                print('输入有误:任务Id不存在')

    def check_all(self):
        '显示所有的任务'
        print('\033[33;1m显示所有任务\033[0m'.center(30, '#'))
        if any(self.task_info):
            for t, v in self.task_info.items():
                print('任务Id:{0}'.format(t).center(60, '-'))
                print('主机IP:', v['IP'], '执行命令:', v['cmd'], '结果:', v['Result'])
        else:
            print('\033[31;1m当前没有任务\033[0m')

    def execmd(self):
        '''输入命令并调用run函数'''
        print('请输入要执行的命令,如:run "df -h" --hosts 192.168.3.55 10.4.3.4')
        while True:
            text = input('>>>[q=退出]:').strip()
            if text == 'q': break
            # 分解输入的内容,结果为:['run ', '"df -h"', '', None, ' 192.168.3.55 10.4.3.4']
            params = re.split('--hosts|(".*")\s+', text)
            print('\033[34;1m分解命令结果:\033[0m', params)
            if hasattr(self, params[0].strip()):
                self.run(params[1].strip(), params[4].strip())
            else:
                print('输入有误:函数run不存在')

    def run(self, cmd, ips):
        '''
        执行命令的函数
        :param cmd:执行的命令
        :param ips:主机列表 192.168.1.x 192.168.1.x
        '''
        hosts = ips.split()  # IP主机列表
        for ip in hosts:
            objC = rpcclient.RpcClient(self.rpcserver)
            uid, qname = objC(cmd, ip)  # 将命令和单个IP一一组合发送
            print('任务Id:', uid, '回调队列:', qname)
            self.task_info[uid] = {'queue_name': qname, 'IP': ip, 'cmd': cmd, 'Result': None, 'Instance': objC}

    def __call__(self, *args, **kwargs):
        '显示菜单'
        menu_text = {
            '1': '显示所有任务',
            '2': '获取指定任务',
            '3': '执行命令'
        }
        menu_option = {
            '1': self.check_all,
            '2': self.check_task,
            '3': self.execmd
        }
        print('FabricRPC主机管理'.center(30, '*'))
        self.rpcserver = input('请输入RPC服务器IP:').strip()
        while True:
            for k, v in menu_text.items():
                print(k, v)
            choice = input('请选择菜单项[q=退出]:').strip()
            if choice == 'q': break
            if choice in menu_text:
                func = menu_option[choice]
                func()
            else:
                print('输入有误:菜单项不存在')
        print('app exit now.')


if __name__ == '__main__':
    rpc = RpcManage()
    rpc()
