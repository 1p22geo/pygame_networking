import pygame
from item import Item
from router import Router
from board import Board
from dhcp import generator

class AddRouter(Item):
    def __init__(self, rect):
        super().__init__(rect)
        self.selectable = False
        self.image = pygame.image.load('switch.png')

    def dragto(self, pos, button, board:Board):
        newrect = pygame.Rect(0,0, 60, 60)
        newrect.center = pos
        mac = generator.new_host()
        newitem = Router(newrect,mac)
        board.add_object(newitem)
    
    def dragged(self, pos, button):
        pass