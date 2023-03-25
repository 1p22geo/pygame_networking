import pygame
from linkable import Linkable
from board import Board
from DHCP_discover import DHCP_discover
from DHCP_offer import DHCP_offer
from ARPrequest import ARPrequest
from ARPresponse import ARPresponse

class Display():
    def __init__(self, size):
        self.screen = pygame.display.set_mode(size)
        self.screensize = size
        self.sendimg = pygame.image.load('send.png')
        self.packetimg = pygame.image.load('packet.png')
    def draw(self, board:Board, selected):
        self.screen.fill((255,255,255))
        for item in board.objects:
            if issubclass(type(item), Linkable):
                for link in item.links:
                    pygame.draw.line(self.screen, (0,0,0), item.rect.center, board.objects[link].rect.center, 5)
        for packet in board.get_packets():
            if isinstance(packet, DHCP_discover):
                pygame.draw.rect(self.screen, (0,120,0), pygame.Rect(packet.pos[0] - 5, packet.pos[1] - 5, 10, 10))
                font = pygame.font.SysFont(None, 15, False)
                img = font.render('D', True, (0,255,0))
                rect = img.get_rect()
                rect.bottomleft = [packet.pos[0] + 3, packet.pos[1] - 3]
                self.screen.blit(img, rect)
            elif isinstance(packet, DHCP_offer):
                pygame.draw.rect(self.screen, (0,120,0), pygame.Rect(packet.pos[0] - 5, packet.pos[1] - 5, 10, 10))
                font = pygame.font.SysFont(None, 15, False)
                img = font.render('O', True, (0,255,0))
                rect = img.get_rect()
                rect.bottomleft = [packet.pos[0] + 3, packet.pos[1] - 3]
                self.screen.blit(img, rect)
            elif isinstance(packet, ARPrequest):
                pygame.draw.rect(self.screen, (0,0,255), pygame.Rect(packet.pos[0] - 5, packet.pos[1] - 5, 10, 10))
                font = pygame.font.SysFont(None, 15, False)
                img = font.render(str(packet.l3[1]), True, (0,255,0))
                rect = img.get_rect()
                rect.bottomleft = [packet.pos[0] + 3, packet.pos[1] - 3]
                self.screen.blit(img, rect)
            elif isinstance(packet, ARPresponse):
                pygame.draw.rect(self.screen, (0,0,255), pygame.Rect(packet.pos[0] - 5, packet.pos[1] - 5, 10, 10))
                font = pygame.font.SysFont(None, 15, False)
                img = font.render(str(packet.l3[0]) + ' - ' + str(packet.l2[0]), True, (0,255,0))
                rect = img.get_rect()
                rect.bottomleft = [packet.pos[0] + 3, packet.pos[1] - 3]
                self.screen.blit(img, rect)
            else:
                pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(packet.pos[0] - 5, packet.pos[1] - 5, 10, 10))
                font = pygame.font.SysFont(None, 15, False)
                img = font.render(str(packet.l3[0]) + ' - ' + str(packet.l3[1]), True, (0,0,0))
                rect = img.get_rect()
                rect.bottomleft = [packet.pos[0] + 3, packet.pos[1] - 3]
                self.screen.blit(img, rect)
                img = font.render(str(packet.l2[0]) + ' - ' + str(packet.l2[1]), True, (0,0,0))
                rect = img.get_rect()
                rect.bottomleft = [packet.pos[0] + 3, packet.pos[1] - 15]
                self.screen.blit(img, rect)
            packet.move()
            if packet.reached:
                packet.dest.receive(packet, board)
                board.del_packet(packet.get_id())
        
        for item in board.get_objects():
            pygame.draw.rect(self.screen, (255,255,255), item.rect)
            self.screen.blit(item.image, item.rect)
            item.drawOptions(self.screen)
        if selected >= 0:
             
             board.objects[selected].drawSelected(self.screen)
            


        pygame.display.flip()
