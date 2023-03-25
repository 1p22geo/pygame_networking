import pygame
import board
import math
from DHCP_server import DHCP_server
from host import Host
from router import Router
from router_interface import Router_interface

class Handler():
    def __init__(self):
        self.dragged = -1
        self.button = -1
        self.selected = -1
        
    def handle_event(self, event: pygame.event.Event, board:board.Board):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if self.selected >= 0:
                if isinstance(board.objects[self.selected], DHCP_server):
                    selectedpos = board.objects[self.selected].rect.center
                    pos = pygame.mouse.get_pos()
                    button1pos = [selectedpos[0], selectedpos[1] - 60]
                    dist = math.sqrt((pos[0] - button1pos[0])**2 + (pos[1] - button1pos[1])**2)
                    if dist <= 15:
                        board.objects[self.selected].config()
                elif issubclass(type(board.objects[self.selected]),Router):
                    selectedpos = board.objects[self.selected].rect.center
                    pos = pygame.mouse.get_pos()
                    button1pos = [selectedpos[0] + 30, selectedpos[1] - 100]
                    dist = math.sqrt((pos[0] - button1pos[0])**2 + (pos[1] - button1pos[1])**2)
                    if dist <= 15:
                        board.objects[self.selected].add_interface(board)
                    selectedpos = board.objects[self.selected].rect.center
                    pos = pygame.mouse.get_pos()
                    button1pos = [selectedpos[0] - 30, selectedpos[1] - 100]
                    dist = math.sqrt((pos[0] - button1pos[0])**2 + (pos[1] - button1pos[1])**2)
                    if dist <= 15:
                        board.objects[self.selected].start_app()
                elif issubclass(type(board.objects[self.selected]),Router_interface):
                    selectedpos = board.objects[self.selected].rect.center
                    pos = pygame.mouse.get_pos()
                    button1pos = [selectedpos[0]+30, selectedpos[1] - 60]
                    dist = math.sqrt((pos[0] - button1pos[0])**2 + (pos[1] - button1pos[1])**2)
                    if dist <= 15:
                        board.objects[self.selected].send_DHCP(board)
                    selectedpos = board.objects[self.selected].rect.center
                    pos = pygame.mouse.get_pos()
                    button1pos = [selectedpos[0]-30, selectedpos[1] - 60]
                    dist = math.sqrt((pos[0] - button1pos[0])**2 + (pos[1] - button1pos[1])**2)
                    if dist <= 15:
                        board.objects[self.selected].config()
                elif issubclass(type(board.objects[self.selected]),Host) and board.objects[self.selected].DHCP_configured:
                    selectedpos = board.objects[self.selected].rect.center
                    pos = pygame.mouse.get_pos()
                    button1pos = [selectedpos[0] + 40, selectedpos[1] - 60]
                    dist = math.sqrt((pos[0] - button1pos[0])**2 + (pos[1] - button1pos[1])**2)
                    if dist <= 15:
                        board.objects[self.selected].send(board)
                    button2pos = [selectedpos[0] - 40, selectedpos[1] - 60]
                    dist = math.sqrt((pos[0] - button2pos[0])**2 + (pos[1] - button2pos[1])**2)
                    if dist <= 15:
                        board.objects[self.selected].packet()
                    selectedpos = board.objects[self.selected].rect.center
                    pos = pygame.mouse.get_pos()
                    button1pos = [selectedpos[0], selectedpos[1] - 60]
                    dist = math.sqrt((pos[0] - button1pos[0])**2 + (pos[1] - button1pos[1])**2)
                    if dist <= 15:
                        board.objects[self.selected].send_DHCP(board)
                elif issubclass(type(board.objects[self.selected]),Host):
                    selectedpos = board.objects[self.selected].rect.center
                    pos = pygame.mouse.get_pos()
                    button1pos = [selectedpos[0], selectedpos[1] - 60]
                    dist = math.sqrt((pos[0] - button1pos[0])**2 + (pos[1] - button1pos[1])**2)
                    if dist <= 15:
                        board.objects[self.selected].send_DHCP(board)
                    
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