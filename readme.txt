功能需求：
基于RabbitMQ rpc实现的主机管理

可以对指定机器异步的执行多个命令
例子：
>>:run "df -h" --hosts 192.168.3.55 10.4.3.4
task id: 45334
>>: check_task 45334
>>:
注意，每执行一条命令，即立刻生成一个任务ID,不需等待结果返回，通过命令check_task TASK_ID来得到任务结果


目录结构：
FabricRPC
    ├ client   # rpc客户端
    |   └ startc.py         #客户端启动入口
    |   └ rpcclient.py      # 客户端rpc类
    ├ server   # rpc服务端
    |   └ starts.py         # 服务端启动入口
    |   └ rpcserver.py      # 服务端rpc类
    |   └ host.py           # 主机管理类
    ├ conf   # rpc服务端配置文件
    |   └ setting.py     # 项目根目录和数据库ini文件路径
    ├ db   # 主机配置信息文件
    |   └ host.ini     # 数据结构:节点名[ip,port,username,password]



===============================================
老师在运行可先启动主机管理，添加远程linux主机
===============================================

功能说明：

一、客户端client
1、启动入口startc.py，运行时首先要求输入RPC服务器的IP，这里是将服务器的RPC服务器的IP作为queue name，测试时输入RPC服务器运行时显示的ip即可
2、输入RPC服务器的IP后显示菜单项：
    1）显示所有任务：循环task_info字典，显示所有的任务信息

    2）获取指定任务：先显示当前的任务列表，然后提示输入任务id，通过task_info字典中保存的实例对象调用get_response方法获取远程执行的结果并且显示

    3）执行命令：
    按格式run "df -h" --hosts 192.168.3.55，输入命令后，会通过re.split分解命令，然后将命令和ip列表传入run函数中
    --1：run函数循环ip列表将命令和单个Ip作为元组传入RpcClient实例类的call方法中，并返回uuid和随机queue,同时将uuid、随机queue、ip、执行的命令、RpcClient实例保存在task_info字典中
    --2：上一条命令输入完毕后可以再次输入下一条命令，直到输入q退出循环


========================================================================================================
rpcclient类说明：因测试的时候rpc客户端和服务器在同一台电脑上，所以rpcclient类的
构造函数里写的是localhost：self.conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
原本是想的是客户端和服务器是不同的电脑（客户端连接到rpc服务端，通过
    credentials = pika.PlainCredentials('alex', 'alex3714')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.211.55.5',5672,'/',credentials))
）认证，
但家里没有太多的电脑，【所以老师测试的时候请注意这一点，尽量在一台电脑上】
========================================================================================================

二、服务端server
1、启动入口starts.py，运行时显示菜单：1 主机管理，2 启动RPCServer
2、主机管理：是服务端先将能远程连接的主机的信息保存在.ini文件中，当客户端发送命令时查找指定的主机的账户信息，然后通过paramiko远程连接并执行命令


三、主机管理：增删改查主机账号信息