import pygame
from DHCP_offer import DHCP_offer
from IP import IP
from board import Board
from host import Host
import appJar


class Router_interface(Host):
    def __init__(self, rect, mac, router, if_id):
        super().__init__(rect, mac)
        self.router = router
        self.id = if_id
        self.image = 'routerIF.png'
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
        pass
    def drawSelected(self, screen):
        font = pygame.font.SysFont(None, 25, False)
        img = font.render(self.IP.str, True, (0,0,0), (255,255,255))
        rect = img.get_rect()
        rect.center = [self.rect.center[0], self.rect.center[1] + 35]
        screen.blit(img, rect)
        font = pygame.font.SysFont(None, 20, False)
        img = font.render(self.mac, True, (0,0,0), (255,255,255))
        rect = img.get_rect()
        rect.center = [self.rect.center[0], self.rect.center[1] + 50]
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
        button1pos = [self.rect.center[0]+30, self.rect.center[1] - 60]
        rect = pygame.Rect(0,0,30,30)
        rect.center = button1pos
        screen.blit(pygame.image.load(self.dhcpimg), rect)
        button1pos = [self.rect.center[0]-30, self.rect.center[1] - 60]
        rect = pygame.Rect(0,0,30,30)
        rect.center = button1pos
        screen.blit(pygame.image.load(self.packetimg), rect)
    def press(self, button):
        if button == 'Cancel':
            self.app.stop()
            self.app = False
        else:
            self.IP = IP(self.app.getEntry("IP adress :"))
            self.app.stop()
            self.app = False
        

    def config(self):
        #print("aa")
        self.app = appJar.gui()
        self.app.addLabel("title", "Router interface configuration")
        self.app.addLabelEntry("IP adress :")
        self.app.addButtons(["Submit", "Cancel"], self.press)
        self.app.go()