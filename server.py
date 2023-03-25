import pygame
from board import Board
from host import Host
from packet import Packet


class Server(Host):
    def __init__(self, rect, mac):
        super().__init__(rect, mac)
        self.image = pygame.image.load('server.png')

    def receive(self, packet, board:Board):
        if type(packet) == Packet:
            self.target = packet.l3[0]
            super().send(board)
        else:
            super().receive(packet, board)