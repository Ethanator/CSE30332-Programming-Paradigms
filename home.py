# home.py
#
# The server program.
#
#     Author: Yuxuan Chen
#       Date: April 28, 2015
#

from twisted.internet import reactor, protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Factory

class CommandConn(protocol.Protocol):
    def connectionMade(self):
        reactor.listenTCP(9409, ClientConnFactory(self))

class CommandConnFactory(Factory):
    def buildProtocol(self, addr):
        return CommandConn()

class ClientConn(protocol.Protocol):
    def __init__(self, command_conn):
        self.command_conn = command_conn
        self.data_conn = 1

    def dataReceived(self, data):
        self.data_conn.transport.write(data)

    def connectionMade(self):
        self.command_conn.transport.write("new client")
        reactor.listenTCP(29994, DataConnFactory(self))    

class ClientConnFactory(Factory):
    def __init__(self, command_conn):
        self.command_conn = command_conn
    
    def buildProtocol(self, addr):
        return ClientConn(self.command_conn)

class DataConn(protocol.Protocol):
    def __init__(self, client_conn):
        self.client_conn = client_conn
        self.client_conn.data_conn = self
    
    def dataReceived(self, data):
        self.client_conn.transport.write(data)

class DataConnFactory(Factory):
    def __init__(self, client_conn):
        self.client_conn = client_conn    

    def buildProtocol(self, addr):
        return DataConn(self.client_conn)

def main():
    reactor.listenTCP(8000, CommandConnFactory())
    reactor.run()

if __name__ == "__main__":
    main()
