from packet import Packet

class ARPrequest(Packet):
    def __init__(self, pos: tuple, dest, srcmac, srcip, destip):
        super().__init__(pos, dest, (srcmac, 'ffff'), (srcip, destip))