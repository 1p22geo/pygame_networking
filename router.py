import pygame
from board import Board
from host import Host
from router_interface import Router_interface
from packet import Packet
from dhcp import generator


class Router(Host):
    def __init__(self, rect, mac):
        super().__init__(rect, mac)
        self.interfaces = []
        self.routingtable = {}
        '''
        key - a tuple including an IP adress (tuple) and a subnet mask (i.e. /24)
        value - a tuple including the interface ID and a destination MAC adress
                if the destination MAC is ffff, the router needs to perform ARP.
        '''
    def add_interface(self, board:Board):
        mac = generator.new_host()
        interface = Router_interface(pygame.Rect(0,0,50,50), mac, self.get_id())
        board.add_object(interface)
        self.interfaces.append(interface)

        self.update_interfaces()
    def update_interfaces(self):
        match len(self.interfaces):
            case 0 :
                pass
            case 1:
                self.interfaces[0].rect.center = (self.rect[0], self.rect[1] - 50)
            case 2:
                self.interfaces[0].rect.center = (self.rect[0] - 50, self.rect[1])
                self.interfaces[1].rect.center = (self.rect[0] + 50, self.rect[1])
            case 3:
                self.interfaces[0].rect.center = (self.rect[0] - 0.866*50, self.rect[1] + 25)
                self.interfaces[1].rect.center = (self.rect[0] + 0.866*50, self.rect[1] + 25)
                self.interfaces[2].rect.center = (self.rect[0], self.rect[1] - 50)
            case 4:
                self.interfaces[0].rect.center = (self.rect[0] - 35, self.rect[1] - 35)
                self.interfaces[1].rect.center = (self.rect[0] + 35, self.rect[1] - 35)
                self.interfaces[0].rect.center = (self.rect[0] - 35, self.rect[1] + 35)
                self.interfaces[1].rect.center = (self.rect[0] + 35, self.rect[1] + 35)
            case _:
                raise Exception('Too much interfaces')
    def recieve(self, packet, board: Board, interface):
        packet_route = None
        for route in self.routingtable.keys():
            if self.check_route(packet.l3[1], route):
                packet_route = route
        route = self.routingtable[packet_route]