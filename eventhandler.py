import pygame
import board
import math
from traverse import Traverser

class Handler():
    def __init__(self):
        self.dragged = -1
        self.button = -1
        self.selected = -1
        
    def handle_event(self, event: pygame.event.Event, board:board.Board):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if self.selected >= 0:
                selectedpos = board.objects[self.selected].rect.center
                pos = pygame.mouse.get_pos()
                button1pos = [selectedpos[0], selectedpos[1] - 60]
                dist = math.sqrt((pos[0] - button1pos[0])**2 + (pos[1] - button1pos[1])**2)
                if dist <= 10:
                    for link in board.objects[self.selected].links:
                        linked = board.objects[link]
                        packet = Traverser(board.objects[self.selected].rect.center, linked.rect.center)
                        board.add_packet(packet)
            self.selected = -1
            for obj in board.objects:
                if obj.check_click(pygame.mouse.get_pos()):
                    self.dragged = obj.get_id()
                    self.button = event.button
        if event.type == pygame.MOUSEMOTION:
            if self.dragged >= 0 :
                board.objects[self.dragged].dragged(pygame.mouse.get_pos(), self.button)
        if event.type == pygame.MOUSEBUTTONUP:
            

            if (self.dragged >= 0):
                self.selected = self.dragged
                board.objects[self.dragged].click(self.button, board)
                board.objects[self.dragged].dragto(pygame.mouse.get_pos(), self.button, board)
                self.dragged = -1
                self.button = -1