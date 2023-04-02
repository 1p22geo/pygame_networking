class TCPHeader():
    def __init__(self, srcport=65535, destport=7, flags=''):
        self.srcport = srcport
        self.destport = destport
        self.flags = flags.split('')