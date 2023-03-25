import pygame
from board import Board
from host import Host
from packet import Packet
import appJar


class Server(Host):
    def __init__(self, rect, mac):
        super().__init__(rect, mac)
        self.image = pygame.image.load('server.png')
        self.content = ''

    def receive(self, packet, board:Board):
        if type(packet) == Packet:
            self.target = packet.l3[0]
            super().send(board, self.content)
        else:
            super().receive(packet, board)
    def press(self, button):
        if button == 'Cancel':
            self.app.stop()
            self.app = False
        else:
            self.content = self.app.getTextArea("Response :")
            self.app.stop()
            self.app = False
        

    def config(self):
        self.app = appJar.gui()
        self.app.addLabel("title", "Input static response")
        self.app.addTextArea("Response :")
        self.app.addButtons(["Submit", "Cancel"], self.press)
        self.app.go()

    def drawSelected(self, screen):
        button1pos = [self.rect.center[0] +20, self.rect.center[1] - 60]
        rect = pygame.Rect(0,0,30,30)
        rect.center = button1pos
        screen.blit(self.dhcpimg, rect)
        button2pos = [self.rect.center[0] - 20, self.rect.center[1] - 60]
        rect = pygame.Rect(0,0,30,30)
        rect.center = button2pos
        screen.blit(self.packetimg, rect)
        tablepos = [self.rect.centerx + 70, self.rect.centery - 50]
        if self.DHCP_configured:
            
            height = 300
            pygame.draw.rect(screen, (255,255,255),pygame.Rect(tablepos[0], tablepos[1], 150, height))
            pygame.draw.rect(screen, (0,0,0),pygame.Rect(tablepos[0], tablepos[1], 150, height), 2)
            font = pygame.font.SysFont(None, 20, False)
            img = font.render(str("ARP cache"), True, (0,0,0))
            rect = img.get_rect()
            rect.center = [tablepos[0] + 75, tablepos[1] + 10]
            screen.blit(img, rect)
            ypos = 10
            for oip,omac in self.ARP.items():
                if ypos > height:
                    break
                ypos += 15
                font = pygame.font.SysFont(None, 20, False)
                img = font.render(str(oip), True, (0,0,0))
                screen.blit(img, (tablepos[0] + 10, tablepos[1] + ypos))
                img = font.render(str(omac), True, (0,0,0))
                rect = img.get_rect()
                rect.topright = [tablepos[0] + 140, tablepos[1] + ypos]
                screen.blit(img, rect)