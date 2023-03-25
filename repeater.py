import pygame
from host import Host
from board import Board
from packet import Packet
from DHCP_discover import DHCP_discover
from DHCP_offer import DHCP_offer
from ARPrequest import ARPrequest
from ARPresponse import ARPresponse

class Repeater(Host):
    def __init__(self, rect, mac):
        super().__init__(rect, None)
        self.image = pygame.image.load('repeater.png')
        self.selectable = False
    def forward_packet(self, packet, link, board:Board):
        if isinstance(packet, DHCP_discover):
            packet2 = DHCP_discover(self.rect.center, board.objects[link], packet.l2)
            board.add_packet(packet2)
        elif isinstance(packet, DHCP_offer):
            packet2 = DHCP_offer(self.rect.center, board.objects[link], packet.l2, packet.l3, packet.mask, packet.gateway)
            board.add_packet(packet2)
        elif isinstance(packet,ARPresponse):
            packet2 = ARPresponse(self.rect.center, board.objects[link], packet.l2, packet.l3)
            board.add_packet(packet2)
        elif isinstance(packet,ARPrequest):
            packet2 = ARPrequest(self.rect.center, board.objects[link], packet.l2[0], packet.l3[0], packet.l3[1])
            board.add_packet(packet2)
        elif isinstance(packet, Packet):
            packet2 = Packet(self.rect.center, board.objects[link], packet.l2, packet.l3)
            packet2.payload = packet.payload
            board.add_packet(packet2)

    def receive(self, packet, board:Board):
        for link in self.links:
            linked = board.objects[link]
            if linked.rect.center != packet.startpos:
                self.forward_packet(packet, link,board)
    
    def send(self, board):
        pass

    
    def drawSelected(self, screen):
        pass