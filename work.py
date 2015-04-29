# work.py
# 
# The client program. Run home.py first before running this.
#
#     Author: Yuxuan Chen
#       Date: April 28, 2015
#
 
from twisted.internet import reactor, protocol

class CommandConn(protocol.Protocol):
    def __init__(self):
        self.data_conn = DataConn()
        self.data_conn_factory = DataConnFactory(self.data_conn)
    
    def dataReceived(self, data):
        if data == "new client":
            reactor.connectTCP("student02.cse.nd.edu", 29994, self.data_conn_factory)
                            
class CommandConnFactory(protocol.ClientFactory):
    protocol = CommandConn

class DataConn(protocol.Protocol):
    def __init__(self):        
        self.service_conn = 1    

    def dataReceived(self, data):
        self.service_conn.transport.write(data)

    def connectionMade(self):
        self.service_conn_factory = ServiceConnFactory(self)
        reactor.connectTCP("student03.cse.nd.edu", 22, self.service_conn_factory)

class DataConnFactory(protocol.ClientFactory):
    def __init__(self, data_conn):
        self.data_conn = data_conn
    
    def buildProtocol(self, addr):
        return self.data_conn

class ServiceConn(protocol.Protocol):
    def __init__(self, data_conn):
        self.data_conn = data_conn
        self.data_conn.service_conn = self
    
    def dataReceived(self, data):
        self.data_conn.transport.write(data)

class ServiceConnFactory(protocol.ClientFactory):    
    def __init__(self, data_conn):
        self.data_conn = data_conn

    def buildProtocol(self, addr):
        return ServiceConn(self.data_conn)

def main():
    reactor.connectTCP("student02.cse.nd.edu", 8000, CommandConnFactory())
    reactor.run()

if __name__ == '__main__':
    main()
