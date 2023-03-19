import pygame
from host import Host
from board import Board
from packet import Packet

class Repeater(Host):
    def __init__(self, rect, mac, IP, mask):
        super().__init__(rect, mac, IP, mask)
        self.image = pygame.image.load('repeater.png')
        self.mac = mac
        self.IP = IP.split('.')
        self.mask = mask.split('.')
    
    def recieve(self, packet:Packet, board:Board):
        for link in self.links:
            linked = board.objects[link]
            if linked.rect.center != packet.startpos:
                packet2 = Packet(self.rect.center, linked, packet.l2, packet.l3)
                board.add_packet(packet2)
    
    def send(self, board):
        pass