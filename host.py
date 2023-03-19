import appJar
import pygame
from linkable import Linkable
from packet import Packet
from board import Board

class Host(Linkable):
    def __init__(self, rect, mac, IP, mask):
        super().__init__(rect)
        self.app = False
        self.mac = mac
        self.IP = IP.split('.')
        self.mask = mask.split('.')
        self.new_packet_data = ('ffff', '192.168.50.0')
    
    def recieve(self, packet, board):
        if packet.l3[1] == '.'.join(self.IP):
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
    
    def drawOptions(self, screen, selected):
        font = pygame.font.SysFont(None, 25, False)
        img = font.render('.'.join(self.IP), True, (0,0,0))
        rect = img.get_rect()
        rect.center = [self.rect.center[0], self.rect.center[1] + 50]
        screen.blit(img, rect)
        font = pygame.font.SysFont(None, 20, False)
        img = font.render(self.mac, True, (0,0,0))
        rect = img.get_rect()
        rect.center = [self.rect.center[0], self.rect.center[1] + 70]
        screen.blit(img, rect)
    def draw_selected(self, screen):
        button1pos = [self.rect.center[0] +20, self.rect.center[1] - 60]
        rect = pygame.Rect(0,0,30,30)
        rect.center = button1pos
        screen.blit(self.sendimg, rect)
        button2pos = [self.rect.center[0] - 20, self.rect.center[1] - 60]
        rect = pygame.Rect(0,0,30,30)
        rect.center = button2pos
        screen.blit(self.packetimg, rect)