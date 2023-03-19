import pygame
from item import Item
from linkable import Linkable
from board import Board

class AddButton(Item):
    def __init__(self, rect):
        super().__init__(rect)
        self.selectable = False

    def dragto(self, pos, button, board:Board):
        newrect = pygame.Rect(0,0, 50, 50)
        newrect.center = pos
        newitem = Linkable(newrect)
        board.add_object(newitem)
    
    def dragged(self, pos, button):
        pass