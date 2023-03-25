import pygame
from item import Item
from board import Board
from dhcp import generator
from server import Server

class AddServer(Item):
    def __init__(self, rect):
        super().__init__(rect)
        self.selectable = False
        self.image = pygame.image.load('server.png')
        

    def dragto(self, pos, button, board:Board):
        newrect = pygame.Rect(0,0, 60, 80)
        newrect.center = pos
        mac = generator.new_host()
        newitem = Server(newrect,mac)
        board.add_object(newitem)
    
    def dragged(self, pos, button):
        pass