import pygame
from host import Host
from packet import Packet
from board import Board

class Switch(Host):
    def __init__(self, rect, mac, IP, mask):
        super().__init__(rect, mac, IP, mask)
        self.table = {}
        '''
        The routing table of the switch
        ...or sth like that
        Assigns link numbers to MAC adresses
        ARP cache - not today!
        '''
    
        self.image = pygame.image.load('switch.png')
    def send():
        pass
    def packet():
        pass
    
    def recieve(self, packet:Packet, board:Board):
        print(packet.l2, packet.l3)
        if not (packet.l2[0] in self.table.keys()):
            for link in self.links:
                if board.objects[link].rect.center == packet.startpos:
                    self.table[packet.l2[0]] = link
        packet2 = None
        if packet.l2[1] == 'ffff':
            for link in self.links:
                if board.objects[link].rect.center != packet.startpos:
                    packet2 = Packet(self.rect.center, board.objects[link], packet.l2, packet.l3)
                    board.add_packet(packet2)
        elif packet.l2[1] in self.table.keys():
            link = self.table[packet.l2[1]]
            packet2 = Packet(self.rect.center, board.objects[link], packet.l2, packet.l3)
            board.add_packet(packet2)
        else:
            for link in self.links:
                if board.objects[link].rect.center != packet.startpos:
                    packet2 = Packet(self.rect.center, board.objects[link], packet.l2, packet.l3)
                    board.add_packet(packet2)
        print(packet2.l2, packet2.l3)
    
    def drawSelected(self, screen):
        tablepos = [self.rect.centerx + 70, self.rect.centery - 50]
        pygame.draw.rect(screen, (255,255,255),pygame.Rect(tablepos[0], tablepos[1], 150, 200))
        pygame.draw.rect(screen, (0,0,0),pygame.Rect(tablepos[0], tablepos[1], 150, 200), 2)
        font = pygame.font.SysFont(None, 20, False)
        img = font.render(str("Routing table"), True, (0,0,0))
        rect = img.get_rect()
        rect.center = [tablepos[0] + 75, tablepos[1] + 10]
        screen.blit(img, rect)
        ypos = 0
        for mac,link in self.table.items():
            ypos += 25
            font = pygame.font.SysFont(None, 30, False)
            img = font.render(str(mac), True, (0,0,0))
            screen.blit(img, (tablepos[0] + 10, tablepos[1] + ypos))
            img = font.render('host '+str(link), True, (0,0,0))
            rect = img.get_rect()
            rect.topright = [tablepos[0] + 140, tablepos[1] + ypos]
            screen.blit(img, rect)