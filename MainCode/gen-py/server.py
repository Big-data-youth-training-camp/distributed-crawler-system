import json
from proj import Transmit
from proj.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import socket


class TransmitHandler:

    count: int 

    def __init__(self):
        self.log = {}
        self.count = 0
    
    def getCount(self):
        return self.count
        

    def start(self, msg):
        print("s(" + msg + ")")
        self.count = self.count + 1
        print(self.count)
        return json.dumps(msg)
    
    def finish(self, msg):
        print("f(" + msg + ")")
        self.count = self.count - 1
        print(self.count)
        return json.dumps(msg)
        

    

if __name__=="__main__":
    handler = TransmitHandler()
    processor = Transmit.Processor(handler)
    transport = TSocket.TServerSocket('127.0.0.1', 8000)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    print("Starting python server...")
    server.serve()

    
