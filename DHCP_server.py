import pygame
from host import Host
import random
from DHCP_discover import DHCP_discover
from DHCP_offer import DHCP_offer
from board import Board
import appJar

class DHCP_server(Host):
    def __init__(self, rect:pygame.Rect, mac:str, IP:str):
        super().__init__(rect, mac)
        self.image = pygame.image.load('DHCPserver.png')
        self.mac = mac
        self.IP = '22.33.44.5'.split('.')
        self.mask = '/24' # will be something like /24 or /16
        self.gateway = '22.33.44.1'.split('.')
        self.range = (100,255)
        self.hosts = [None, None]
        self.hosts[0] = '.'.join(self.IP)
        self.hosts[1] = '.'.join(self.gateway)
    def recieve(self, packet, board:Board):
        adress = None
        if isinstance(packet, DHCP_discover):
            if self.mask == '/24':
                adress = self.IP[:]
                while '.'.join(adress) in self.hosts:
                    adress[-1] = str(random.randint(self.range[0], self.range[1]))
            else:
                raise Exception('Wrong subnet mask')
            for link in self.links:
                linked = board.objects[link]
                
                packet2 = DHCP_offer(self.rect.center, linked, (self.mac, packet.l2[0]), (tuple(self.IP), adress), self.mask, self.gateway)
                board.add_packet(packet2)
    def press(self, button):
        if button == 'Cancel':
            self.app.stop()
            self.app = False
        else:
            self.IP = self.app.getEntry("IP adress :").split('.')
            self.mask = self.app.getEntry("Subnet mask :")
            self.gateway = self.app.getEntry("Default gateway :").split('.')
            self.app.stop()
            self.app = False
            self.hosts[0] = '.'.join(self.IP)
            self.hosts[1] = '.'.join(self.gateway)
        

    def config(self):
        self.app = appJar.gui()
        self.app.addLabel("title", "DHCP server configuration")
        self.app.addLabelEntry("Subnet mask :")
        self.app.addLabelEntry("Default gateway :")
        self.app.addLabelEntry("IP adress :")
        self.app.addButtons(["Submit", "Cancel"], self.press)
        self.app.go()

    def drawSelected(self, screen):
        button1pos = [self.rect.center[0], self.rect.center[1] - 60]
        rect = pygame.Rect(0,0,30,30)
        rect.center = button1pos
        screen.blit(self.dhcpimg, rect)
    def drawOptions(self, screen):
        font = pygame.font.SysFont(None, 25, False)
        img = font.render('.'.join(self.IP), True, (0,0,0), (255,255,255))
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