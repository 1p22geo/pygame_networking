from packet import Packet

class ARPresponse(Packet):
    def __init__(self, pos: tuple, dest, l2, l3):
        super().__init__(pos, dest, l2, l3)