import pygame
from linkable import Linkable
from board import Board
from host import Host
from switch import Switch

class Display():
    def __init__(self, size):
        self.screen = pygame.display.set_mode(size)
        self.screensize = size
        self.sendimg = pygame.image.load('send.png')
        self.packetimg = pygame.image.load('packet.png')
    def draw(self, board:Board, selected):
        self.screen.fill((255,255,255))
        
        if selected >= 0:
             
             board.objects[selected].draw_selected(self.screen)
        for item in board.objects:
            if issubclass(type(item), Linkable):
                for link in item.links:
                    pygame.draw.line(self.screen, (0,0,0), item.rect.center, board.objects[link].rect.center, 5)
        for item in board.get_objects():
            pygame.draw.rect(self.screen, (255,255,255), item.rect)
            self.screen.blit(item.image, item.rect)
            item.drawOptions(self.screen, selected)
            
        for packet in board.get_packets():
            pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(packet.pos[0] - 5, packet.pos[1] - 5, 10, 10))
            packet.move()
            if packet.reached:
                packet.dest.recieve(packet, board)
                board.del_packet(packet.get_id())


        pygame.display.flip()
