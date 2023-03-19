import pygame
from linkable import Linkable
from traverse import Traverser
from board import Board

class Host(Linkable):
    def __init__(self, rect, mac, IP, mask):
        super().__init__(rect)
        self.mac = mac
        self.IP = IP.split('.')
        self.mask = mask.split('.')
    
    def recieve(self, packet, board):
        print('Recieved a packet at {}'.format('.'.join(self.IP)))

    def send(self, board:Board):
        for link in self.links:
            linked = board.objects[link]
            packet = Traverser(self.rect.center, linked)
            board.add_packet(packet)