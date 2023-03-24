import pygame
from DHCP_offer import DHCP_offer
from board import Board
from host import Host


class Router_interface(Host):
    def __init__(self, rect, mac, router, if_id):
        super().__init__(rect, mac)
        self.router = router
        self.id = if_id
        self.image = pygame.image.load('switch.png')
    def dragged(self, pos, button):
        pass
    def receive(self, packet, board:Board):
        if isinstance(packet, DHCP_offer):
            if packet.l2[1] == self.mac:
                self.IP = packet.l3[1]
                self.mask = packet.mask
                self.gateway = packet.gateway
                self.DHCP_configured = True
        else :
            board.objects[self.router].receive(packet,board, self.id)
    def drawOptions(self, screen):
        font = pygame.font.SysFont(None, 25, False)
        img = font.render(self.IP.str, True, (0,0,0), (255,255,255))
        rect = img.get_rect()
        rect.center = [self.rect.center[0], self.rect.center[1] + 50]
        screen.blit(img, rect)
        font = pygame.font.SysFont(None, 20, False)
        img = font.render(self.mac, True, (0,0,0), (255,255,255))
        rect = img.get_rect()
        rect.center = [self.rect.center[0], self.rect.center[1] + 70]
        screen.blit(img, rect)
        font = pygame.font.SysFont(None, 20, False)
        img = font.render(str(self.get_id()), True, (0,0,0), (255,255,255))
        rect = img.get_rect()
        rect.center = [self.rect.center[0] + 35, self.rect.center[1] - 35]
        screen.blit(img, rect)
        font = pygame.font.SysFont(None, 30, False)
        img = font.render('IF'+str(self.id), True, (0,0,0), (255,255,255))
        rect = img.get_rect()
        rect.center = [self.rect.center[0], self.rect.center[1] - 35]
        screen.blit(img, rect)
    def drawSelected(self, screen):
        button1pos = [self.rect.center[0], self.rect.center[1] - 60]
        rect = pygame.Rect(0,0,30,30)
        rect.center = button1pos
        screen.blit(self.dhcpimg, rect)