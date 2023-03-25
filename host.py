from DHCP_discover import DHCP_discover
from ARPresponse import ARPresponse
from ARPrequest import ARPrequest
from DHCP_offer import DHCP_offer
from linkable import Linkable
from packet import Packet
from board import Board
from IP import IP
import appJar
import pygame

class Host(Linkable):
    def __init__(self, rect, mac):
        super().__init__(rect)
        self.app = False
        self.mac = mac
        self.IP = IP(())
        self.mask = None
        self.gateway = IP(())
        self.new_packet_data = ('ffff', None)
        self.DHCP_configured = False
        self.target = ()
        self.waitingforARP = []
        self.ARP = {} # nooo i don't want to do ARP cache
        self.sendimg = pygame.image.load('send.png')
        self.packetimg = pygame.image.load('packet.png')
        self.dhcpimg = pygame.image.load('DHCP.png')
    
    def send_DHCP(self, board:Board):
        for link in self.links:
            linked = board.objects[link]
            
            packet = DHCP_discover(self.rect.center, linked, (self.mac, 'ffff'))
            board.add_packet(packet)
            
    def receive(self, packet, board:Board):
        if isinstance(packet, DHCP_offer):
            if packet.l2[1] == self.mac:
                self.IP = packet.l3[1]
                self.mask = packet.mask
                self.gateway = packet.gateway
                self.DHCP_configured = True
        elif isinstance(packet, ARPresponse):
            self.ARP[packet.l3[0].str] = packet.l2[0]
            if packet.l2[1] == self.mac:
                for p in self.waitingforARP:
                    if p[1].str == packet.l3[0].str:
                        newpacket = p[0]
                        newpacket.l2 = (newpacket.l2[0], packet.l2[0])
                        board.add_packet(newpacket)
        elif isinstance(packet, ARPrequest):
            self.ARP[packet.l3[0].str] = packet.l2[0]
            if packet.l3 and self.IP and (packet.l3[1].str == self.IP.str):
                for link in self.links:
                    linked = board.objects[link]
                    packet2 = ARPresponse(self.rect.center, linked, (self.mac, packet.l2[0]), (self.IP,packet.l3[0]))
                    board.add_packet(packet2)
        elif packet.l3 and self.IP and (packet.l3[1].str == self.IP.str):
            print('received a packet at {}'.format(self.IP.str))

    def press(self, button):
        if button == 'Cancel':
            self.app.stop()
            self.app = False
        else:
            ip = self.app.getEntry("IP adress :")
            self.target = IP(ip)
            self.app.stop()
            self.app = False
        

    def packet(self):
        self.app = appJar.gui()
        self.app.addLabel("title", "Select packet destination")
        self.app.addLabelEntry("IP adress :")
        self.app.addButtons(["Submit", "Cancel"], self.press)
        self.app.go()

    def send(self, board:Board):
        for link in self.links:
            linked = board.objects[link]
            if self.IP.check(self.target, self.mask):
                if self.target.str in self.ARP.keys():
                    packet = Packet(self.rect.center, linked, (self.mac, self.ARP[self.target.str]), (self.IP, self.target))
                    board.add_packet(packet)
                else:
                    # Send ARP request
                    packet = ARPrequest(self.rect.center, linked, self.mac, self.IP, self.target)
                    board.add_packet(packet)
                    self.waitingforARP.append((Packet(self.rect.center, linked, (self.mac, '<MISSING>'), (self.IP, self.target)), self.target))
            else:
                #use default gateway
                if self.gateway.str in self.ARP.keys():
                    packet = Packet(self.rect.center, linked, (self.mac, self.ARP[self.gateway.str]), (self.IP, self.target))
                    board.add_packet(packet)
                else:
                    # Send ARP request
                    packet = ARPrequest(self.rect.center, linked, self.mac, self.IP, self.gateway)
                    board.add_packet(packet)
                    self.waitingforARP.append((Packet(self.rect.center, linked, (self.mac, '<MISSING>'), (self.IP, self.target)), self.gateway))
    
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
        img = font.render(self.gateway.str, True, (0,0,0), (255,255,255))
        rect = img.get_rect()
        rect.center = [self.rect.center[0], self.rect.center[1] + 90]
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
            tablepos = [self.rect.centerx + 70, self.rect.centery - 50]
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
        else:
            button1pos = [self.rect.center[0], self.rect.center[1] - 60]
            rect = pygame.Rect(0,0,30,30)
            rect.center = button1pos
            screen.blit(self.dhcpimg, rect)