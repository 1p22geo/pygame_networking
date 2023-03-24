import pygame
from item import Item
from DHCP_server import DHCP_server
from board import Board
from dhcp import generator

class AddDHCP(Item):
    def __init__(self, rect):
        super().__init__(rect)
        self.selectable = False
        self.image = pygame.image.load('DHCPserver.png')

    def dragto(self, pos, button, board:Board):
        newrect = pygame.Rect(0,0, 80, 80)
        newrect.center = pos
        mac = generator.new_host()
        newitem = DHCP_server(newrect,mac)
        board.add_object(newitem)
    
    def dragged(self, pos, button):
        pass