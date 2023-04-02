from DHCP_discover import DHCP_discover
from ARPresponse import ARPresponse
from ARPrequest import ARPrequest
from DHCP_offer import DHCP_offer
from packet import Packet
from board import Board
from host import Host
import pygame
import copy

class Switch(Host):
    def __init__(self, rect, mac):
        super().__init__(rect, mac)
        self.table = {}
        self.image = 'switch.png'

    def send():
        pass
    def packet():
        pass
    def forward_packet(self, packet, link, board:Board):
        if isinstance(packet, DHCP_discover):
            packet2 = DHCP_discover(self.rect.center, board.objects[link], packet.l2)
            board.add_packet(packet2)
        elif isinstance(packet, DHCP_offer):
            packet2 = DHCP_offer(self.rect.center, board.objects[link], packet.l2, packet.l3, packet.mask, packet.gateway)
            board.add_packet(packet2)
        elif isinstance(packet,ARPresponse):
            packet2 = ARPresponse(self.rect.center, board.objects[link], packet.l2, packet.l3)
            board.add_packet(packet2)
        elif isinstance(packet,ARPrequest):
            packet2 = ARPrequest(self.rect.center, board.objects[link], packet.l2[0], packet.l3[0], packet.l3[1])
            board.add_packet(packet2)
        elif isinstance(packet, Packet):
            packet2 = Packet(self.rect.center, board.objects[link], packet.l2, packet.l3)
            packet2.payload = packet.payload
            board.add_packet(packet2)


    def receive(self, packet:Packet, board:Board):
        if not (packet.l2[0] in self.table.keys()):
            for link in self.links:
                if board.objects[link].rect.center == packet.startpos:
                    self.table[packet.l2[0]] = link
        if isinstance(packet, DHCP_offer) and packet.l2[1] == self.mac:
            self.IP = packet.l3[1]
            self.mask = packet.mask
            self.gateway = packet.gateway
            self.DHCP_configured = True
        elif packet.l2[1] == 'ffff':
            for link in self.links:
                if board.objects[link].rect.center != packet.startpos:
                    self.forward_packet(packet, link, board)
        elif packet.l2[1] in self.table.keys():
            link = self.table[packet.l2[1]]
            self.forward_packet(packet, link, board)
        else:
            for link in self.links:
                if board.objects[link].rect.center != packet.startpos:
                    self.forward_packet(packet, link, board)

    def drawSelected(self, screen):
        button1pos = [self.rect.center[0], self.rect.center[1] - 60]
        rect = pygame.Rect(0,0,30,30)
        rect.center = button1pos
        screen.blit(pygame.image.load(self.dhcpimg), rect)
        tablepos = [self.rect.centerx + 70, self.rect.centery - 50]
        height = 300
        pygame.draw.rect(screen, (255,255,255),pygame.Rect(tablepos[0], tablepos[1], 150, height))
        pygame.draw.rect(screen, (0,0,0),pygame.Rect(tablepos[0], tablepos[1], 150, height), 2)
        font = pygame.font.SysFont(None, 20, False)
        img = font.render(str("Routing table"), True, (0,0,0))
        rect = img.get_rect()
        rect.center = [tablepos[0] + 75, tablepos[1] + 10]
        screen.blit(img, rect)
        ypos = 10
        for mac,link in self.table.items():
            if ypos > height:
                break
            ypos += 15
            font = pygame.font.SysFont(None, 20, False)
            img = font.render(str(mac), True, (0,0,0))
            screen.blit(img, (tablepos[0] + 10, tablepos[1] + ypos))
            img = font.render('Port '+str(self.links.index(link)), True, (0,0,0))
            rect = img.get_rect()
            rect.topright = [tablepos[0] + 140, tablepos[1] + ypos]
            screen.blit(img, rect)