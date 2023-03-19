import appJar
import pygame
from linkable import Linkable
from packet import Packet
from board import Board
from DHCP_discover import DHCP_discover
from DHCP_offer import DHCP_offer

class Host(Linkable):
    def __init__(self, rect, mac):
        super().__init__(rect)
        self.app = False
        self.mac = mac
        self.IP = ()
        self.mask = None
        self.gateway = None
        self.new_packet_data = ('ffff', None)
        self.DHCP_configured = False
        self.sendimg = pygame.image.load('send.png')
        self.packetimg = pygame.image.load('packet.png')
        self.dhcpimg = pygame.image.load('DHCP.png')
    
    def send_DHCP(self, board:Board):
        for link in self.links:
            linked = board.objects[link]
            
            packet = DHCP_discover(self.rect.center, linked, (self.mac, 'ffff'))
            board.add_packet(packet)
            
    def recieve(self, packet, board:Board):
        if isinstance(packet, DHCP_offer):
            self.IP = packet.l3[1]
            self.mask = packet.mask
            self.gateway = packet.gateway
            self.DHCP_configured = True
        elif packet.l3 and self.IP and (packet.l3[1] == '.'.join(self.IP)):
            print('Recieved a packet at {}'.format('.'.join(self.IP)))

    def press(self, button):
        if button == 'Cancel':
            self.app.stop()
            self.app = False
        else:
            ip = self.app.getEntry("MAC adress :")
            mac = self.app.getEntry("IP adress :")
            self.new_packet_data = (ip, mac)
            self.app.stop()
            self.app = False
        

    def packet(self):
        self.app = appJar.gui()
        self.app.addLabel("title", "Select packet destination")
        self.app.addLabelEntry("MAC adress :")
        self.app.addLabelEntry("IP adress :")
        self.app.addButtons(["Submit", "Cancel"], self.press)
        self.app.go()

    def send(self, board:Board):
        for link in self.links:
            linked = board.objects[link]
            
            packet = Packet(self.rect.center, linked, (self.mac, self.new_packet_data[0]), (self.IP, self.new_packet_data[1]))
            board.add_packet(packet)
    
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
    def drawSelected(self, screen):
        if self.DHCP_configured:
            button1pos = [self.rect.center[0] +40, self.rect.center[1] - 60]
            rect = pygame.Rect(0,0,30,30)
            rect.center = button1pos
            screen.blit(self.sendimg, rect)
            button1pos = [self.rect.center[0], self.rect.center[1] - 60]
            rect = pygame.Rect(0,0,30,30)
            rect.center = button1pos
            screen.blit(self.dhcpimg, rect)
            button2pos = [self.rect.center[0] - 40, self.rect.center[1] - 60]
            rect = pygame.Rect(0,0,30,30)
            rect.center = button2pos
            screen.blit(self.packetimg, rect)
        else:
            button1pos = [self.rect.center[0], self.rect.center[1] - 60]
            rect = pygame.Rect(0,0,30,30)
            rect.center = button1pos
            screen.blit(self.dhcpimg, rect)