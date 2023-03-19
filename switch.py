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
        if not (packet.l2[0] in self.table.keys()):
            for link in self.links:
                if board.objects[link].rect.center == packet.startpos:
                    self.table[board.objects[link].mac] = link

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

    
    def draw_selected(self, screen):
        pass