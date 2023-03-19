from packet import Packet
class DHCP_offer(Packet):
    def __init__(self, pos: tuple, dest, l2, l3, mask, gateway):
        super().__init__(pos, dest, l2, l3)
        self.mask = mask
        self.gateway = gateway