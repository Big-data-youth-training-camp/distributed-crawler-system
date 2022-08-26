import socket
import threading
import os
import multiprocessing
import sys
import json
import threading
import time
from proj import Transmit
from proj.ttypes import *
from proj.constants import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 9999))
s.listen(5)
cnt = 0
n = 0
hashSet = set()
transport = TSocket.TSocket('127.0.0.1', 8000)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = Transmit.Client(protocol)
# Connect!
transport.open()
def crawlProcess(link, client):
    cmd = 'python3 crawl.py ' + 'https://www.shuishi.com' + link
    print(cmd)
    os.system(cmd)
    client.finish('finish')
def tcplink(sock, addr, cnt, client):
    print('Accept new connection from %s:%s...' % addr)
    while True:
        data = sock.recv(1024)
        s = data.decode('utf-8')
        links = s.split('https://www.shuishi.com')
        if len(links) >= 2:
            for i in (1, len(links) - 1):
                if links[i] not in hashSet:
                    hashSet.add(links[i])
                    cnt = cnt + 1
                    print ('cnt',cnt)
                    print (links[i])
                    print (client.getCount())
                    while client.getCount() >= 5:
                        time.sleep(5)
                        continue
                    client.start('start')
                    t1 = threading.Thread(target=crawlProcess, args=(links[i],client,))
                    t1.start()
        if data.decode('utf-8') == 'exit':
            break
    sock.close()
while True:
    sock, addr = s.accept()
    t = threading.Thread(target=tcplink, args=(sock, addr, cnt, client))
    t.start()
    if cnt > 100:
        break
