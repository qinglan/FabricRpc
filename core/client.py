#!/usr/bin/evn python3
# -*- coding:utf-8 -*-
'''RPC客户端'''
__author__ = 'zween'
__mtime__ = '18-1-4'
import pika
import uuid
import time


class RpcClient(object):
    def __init__(self, serverip):
        '''
        实例化客户端时应该指定rpc服务器IP
        :param serverip: rpc服务器IP
        '''
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=serverip))
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue=serverip)
        self.rpc_queue = serverip  # 同server端,服务器IP作为队列名

    def on_response(self, ch, method, props, body):
        '''回调函数'''
        if self.callback_id == props.correlation_id:
            self.response = body
            ch.basic_ack(delivery_tag=method.delivery_tag)  # 通知结束任务

    def get_response(self, corr_id, callback_queue):
        '''
        在客户端调用获取结果时才接收数据
        :param callback_queue: 回调的queue name
        :param corr_id: 客户端可能不是立即获取返回结果的,所以在此时要传递之前生成的corr_id
        :return:
        '''
        self.response = None
        self.callback_id = corr_id
        self.channel.basic_consume(self.on_response, queue=callback_queue)
        while self.response is None:
            print('Receiving Data:.....')
            time.sleep(0.5)
            self.conn.process_data_events()  # 非阻塞棋模式的start_consuming()
        return self.response

    def __call__(self, *args, **kwargs):
        '''
        调用客户端时传递参数
        :param args: 传递给服务端的命令和ip
        :param kwargs:
        :return:
        '''
        random_queue = self.channel.queue_declare(exclusive=False)  # 产生一个随机的queue
        callback_queue = random_queue.method.queue  # 获取随机的queue name
        corr_id = str(uuid.uuid4())  # 生成一个随机的标识id
        self.channel.basic_publish(exchange='', routing_key=self.rpc_queue,
                                   properties=pika.BasicProperties(reply_to=callback_queue,
                                                                   correlation_id=corr_id),
                                   body=args)  # todo:必需是字符串吗
        print('send data:', args)
        return corr_id, callback_queue  # 返回调的queue name和corr_id


if __name__ == '__main__':
    serverIp = input('请输入RPC服务器IP:').strip()
    print('命令格式:ls 192.168.1.x')
    action = input('请输入执行的命令:').strip()
    rpclient = RpcClient(serverIp)
    rpclient(action)
