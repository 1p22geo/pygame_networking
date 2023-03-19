import pygame
from item import Item
from host import Host
from board import Board
import random
from dhcp import generator

class AddButton(Item):
    def __init__(self, rect):
        super().__init__(rect)
        self.selectable = False
        self.hosts = 0

    def dragto(self, pos, button, board:Board):
        newrect = pygame.Rect(0,0, 50, 50)
        newrect.center = pos
        mac = generator.new_host()
        newitem = Host(newrect,mac)
        self.hosts += 1
        board.add_object(newitem)
    
    def dragged(self, pos, button):
        pass