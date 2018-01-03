#!/usr/bin/evn python3
# -*- coding:utf-8 -*-
'''RPC服务端'''
__author__ = 'zween'
__mtime__ = '18-1-4'
import pika
import configparser
import socket
import paramiko
from conf import setting


class Server(object):
    def __init__(self, qname):
        conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = conn.channel()
        self.channel.queue_declare(queue=qname)
        self.channel.basic_consume(self.on_request, queue=qname)

        self.config = configparser.ConfigParser()  # 打开主机配置文件
        self.config.read(setting.DB_Path)

    def exec(self, action):
        '''连接远程主机并执行命令'''
        cmd, ip = action.split()
        for section in self.config.sections():  # 遍历host.ini文件查找指定IP的账号、密码、端口
            if ip in self.config.options(section):  # todo:待验证
                loginname = self.config[section]['UserName']
                passwd = self.config[section]['Password']
                port = int(self.config[section]['Port'])
                # 使用paramiko连接远程主机并执行命令
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                # 连接服务器
                ssh.connect(hostname=ip, port=port, username=loginname, password=passwd)
                # 执行命令
                stdin, stdout, stderr = ssh.exec_command(cmd)
                errmsg = stderr.read()
                result = errmsg if not errmsg else stdout.read()  # todo 是否需求解码
                ssh.close()
                break
        else:
            result = '[%s] IP地址不存在' % ip
        return result

    def on_request(self, ch, method, props, body):
        '''回调函数'''
        result = self.exec(body)
        print('Execute Result:', result)
        ch.basic_publish(exchange='', routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(result))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __call__(self, *args, **kwargs):
        print('[*] Waiting for rpc connection. To exit press CTRL+C')
        self.channel.start_consuming()


if __name__ == '__main__':
    serverName = socket.gethostname()  # 获取主机名
    serverIp = socket.gethostbyname(serverName)  # 获取主机IP
    print('server name:', serverName, 'IP:', serverIp)
    rpcserver = Server(serverIp)
    rpcserver()
