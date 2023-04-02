import pygame
from item import Item
from repeater import Repeater
from board import Board
from dhcp import generator

class AddRepeater(Item):
    def __init__(self, rect):
        super().__init__(rect)
        self.selectable = False
        self.image = 'repeater.png'

    def dragto(self, pos, button, board:Board):
        newrect = pygame.Rect(0,0, 60, 60)
        newrect.center = pos
        mac = generator.new_host()
        newitem = Repeater(newrect,mac)
        board.add_object(newitem)
    
    def dragged(self, pos, button):
        pass