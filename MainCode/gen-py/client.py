
import sys
import json 
from proj import Transmit
from proj.ttypes import *
from proj.constants import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


transport = TSocket.TSocket('127.0.0.1', 8000)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = Transmit.Client(protocol)
# Connect!
transport.open()


msg = client.start("start")
msg_test = client.finish("finish")
print(msg_test)
print(msg)
num = client.getCount()
print(num)
transport.close()

