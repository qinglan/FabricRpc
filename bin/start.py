#!/usr/bin/evn python3
# -*- coding:utf-8 -*-
'''程序启动入口'''
__author__ = 'zween'
__mtime__ = '18-1-5'
import sys, re
from conf import setting

sys.path.insert(0, setting.BASE_DIR)
from core import client


class RpcManage(object):
    def __init__(self):
        self.task_info = {}  # rpc任务字典

    def check_task(self):
        '获取指定的任务结果'
        for t, v in self.task_info.items():
            print('任务Id:', t, '主机IP:', v['IP'], '执行命令:', v['cmd'], '回调队列:', v['queue_name'])
        choice = input('请输入要查看的任务Id:').strip()
        if choice in self.task_info:
            objC = client.RpcClient(self.rpcserver)
            result = objC.get_response(self[choice]['queue_name'], self[choice])
            print('命令返回结果:', result)
            self[choice]['Result'] = result
        else:
            print('输入有误:任务Id不存在')

    def check_all(self):
        '显示所有的任务'
        print('显示所有任务'.center(30, '#'))
        for t, v in self.task_info.items():
            print('任务Id:{0}'.format(t).center(30, '-'))
            print('主机IP:', v['IP'], '执行命令:', v['cmd'], '结果:', v['Result'])
        else:
            print('当前没有任务')

    def execmd(self):
        '''输入命令并调用run函数'''
        print('请输入要执行的命令,如:run "df -h" --hosts 192.168.3.55 10.4.3.4')
        text = input('>>>:').strip()
        # 分解输入的内容,结果为:['run ', '"df -h"', '', None, ' 192.168.3.55 10.4.3.4']
        params = re.split('--hosts|(".*")\s+', text)
        print('分解命令结果:', params)
        if hasattr(self, params[0].strip()):
            self.run(params[1].strip(), params[4].strip())
        else:
            print('输入有误:函数run不存在')

    def run(self, cmd, ips):
        '''
        执行命令的函数：将命令和单个IP一一组合发送
        :param cmd:执行的命令
        :param ips:主机列表 192.168.1.x 192.168.1.x
        '''
        hosts = ips.split()  # IP主机列表
        for h in hosts:
            objC = client.RpcClient(self.rpcserver)
            retval = objC(cmd, h)
            print('任务Id:', retval[0], '回调队列:', retval[1])
            self.task_info[retval[0]] = {'queue_name': retval[1], 'IP': h, 'cmd': cmd, 'Result': None}

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
