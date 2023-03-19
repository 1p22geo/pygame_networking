from packet import Packet
class DHCP_discover(Packet):
    def __init__(self, pos: tuple, dest, l2):
        super().__init__(pos, dest, l2, None)