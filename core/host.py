#!/usr/bin/evn python3
# -*- coding:utf-8 -*-
'''服务器端主机管理'''
__author__ = 'zween'
__mtime__ = '18-1-4'

import configparser, os
from conf import setting


class Host(object):
    def __init__(self):
        print('RPC Host主机管理'.center(30, '*'))
        self.config = configparser.ConfigParser()
        if os.path.isfile(setting.DB_Path):  # 检查数据库文件是否存在
            self.checkexist = True
        else:
            self.checkexist = False

    def list(self):
        '''主机列表'''
        if not self.__checkdb(): return
        self.config.read(setting.DB_Path)
        for s in self.config.sections():
            print('主机名:%s\tIP:%s\tPort:%s\tUserName:%s\tPassword:%s' % (
            s, self.config[s]['IP'], self.config[s]['Port'], self.config[s]['UserName'], self.config[s]['Password']))

    def create(self):
        '''添加主机'''
        while True:
            hostname = input('主机名[q-退出]:').strip()
            if hostname == 'q': break
            ip = input('IP:').strip()
            port = input('Port:').strip()
            username = input('UserName:').strip()
            password = input('Password:').strip()

            self.config[hostname] = {}
            self.config[hostname]['IP'] = ip
            self.config[hostname]['Port'] = port
            self.config[hostname]['UserName'] = username
            self.config[hostname]['Password'] = password

            with open(setting.DB_Path, 'w') as configfile:
                self.config.write(configfile)
                self.checkexist = True
                print('添加主机[%s]成功' % hostname)

    def modify(self):
        '''修改主机信息'''
        if not self.__checkdb(): return
        hostname = input('请输入要修改主机名:').strip()
        self.config.read(setting.DB_Path)
        if hostname in self.config:
            ip = input('IP:').strip()
            port = input('Port:').strip()
            username = input('UserName:').strip()
            password = input('Password:').strip()

            self.config.set(hostname, 'IP', ip)
            self.config.set(hostname, 'Port', port)
            self.config.set(hostname, 'UserName', username)
            self.config.set(hostname, 'Password', password)
            self.config.write(open(setting.DB_Path, 'w'))
            print('修改主机[%s]信息成功' % hostname)
        else:
            print('输入有误:该主机[%s]不存在.' % hostname)

    def delhost(self):
        '''删除指定的主机'''
        if not self.__checkdb(): return
        hostname = input('请输入要删除的主机名:').strip()
        self.config.read(setting.DB_Path)
        if hostname in self.config:
            self.config.remove_section(hostname)
            self.config.write(open(setting.DB_Path, 'w'))
            print('删除主机[%s]成功' % hostname)
        else:
            print('输入有误:该主机[%s]不存在.' % hostname)

    def __checkdb(self):
        '''检查主机数据库是否存在'''
        if not self.checkexist:
            print('主机列表为空,请先添加主机.')
            return False
        else:
            return True


if __name__ == '__main__':
    h = Host()
    menu_text = {
        '1': '主机列表',
        '2': '添加主机',
        '3': '修改主机',
        '4': '删除主机'
    }
    menu_option = {
        '1': h.list,
        '2': h.create,
        '3': h.modify,
        '4': h.delhost
    }
    while True:
        for k, v in menu_text.items():
            print(k, v)
        action = input('请选择菜单项[q-退出]:').strip()
        if action == 'q': break
        if action in menu_text:
            func = menu_option[action]
            func()
            print('sep line'.center(33,'-'))
        else:
            print('输入有误:菜单项不存在')
