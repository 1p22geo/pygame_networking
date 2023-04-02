from host import Host
import random

class TCPClient(Host):
    def __init__(self, rect, mac):
        super().__init__(rect, mac)
        self.ports = {}
        # maps port number to service
        # for listening ports
        # in this case the raw text to be returned by this port
        self.connectports = list(range(49152, 65535))
        self.connections = {}
        # maps port number to connected IP adress
        # for dynamic, ephemeral ports
    def connect(self, IP, port):
        conn_port = random.choice(self.connectports)
        self.connectports.remove(conn_port)
        self.connections[conn_port] = (IP, port)