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
        self.resource = None
        self.method = None
        self.body = None
        self.receivedfrom = (None, None)
        self.ARP = {} # nooo i don't want to do ARP cache
        self.sendimg = pygame.image.load('send.png')
        self.packetimg = pygame.image.load('packet.png')
        self.dhcpimg = pygame.image.load('DHCP.png')
        self.closeimg = pygame.image.load('close.png')
    
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
            if 'server' in packet.payload.keys():
                self.receivedfrom = (packet.l3[0].str + self.resource,packet.payload['server'])

    def press(self, button):
        if button == 'Cancel':
            self.app.stop()
            self.app = False
        else:
            host = self.app.getEntry("URL adress :").split('/')
            self.target = IP(host[0])
            if len(host) >= 1:
                self.resource = '/'+'/'.join(host[1:])
            else:
                self.resource = '/'
            self.method = self.app.getEntry("Method :")
            self.body = self.app.getEntry("Body :")
            self.app.stop()
            self.app = False
        

    def packet(self):
        self.app = appJar.gui()
        self.app.addLabel("title", "Request details")
        self.app.addLabelEntry("URL adress :")
        self.app.addLabelEntry("Method :")
        self.app.addLabelEntry("Body :")
        self.app.addButtons(["Submit", "Cancel"], self.press)
        self.app.go()

    def send(self, board:Board, *args):
        if args:
            server = args[0]
        else:
            server = None
        if self.resource:
            resource = self.resource
            method = self.method
            body = self.body
        else:
            resource = '/'
            method = 'GET'
            body = ''
        for link in self.links:
            linked = board.objects[link]
            if self.IP.check(self.target, self.mask):
                if self.target.str in self.ARP.keys():
                    packet = Packet(self.rect.center, linked, (self.mac, self.ARP[self.target.str]), (self.IP, self.target), server=server, resource=resource, method=method, body=body)
                    board.add_packet(packet)
                else:
                    # Send ARP request
                    packet = ARPrequest(self.rect.center, linked, self.mac, self.IP, self.target)
                    board.add_packet(packet)
                    self.waitingforARP.append((Packet(self.rect.center, linked, (self.mac, '<MISSING>'), (self.IP, self.target), server=server, resource=resource, method=method, body=body), self.target))
            else:
                #use default gateway
                if self.gateway.str in self.ARP.keys():
                    packet = Packet(self.rect.center, linked, (self.mac, self.ARP[self.gateway.str]), (self.IP, self.target), server=server, resource=resource, method=method, body=body)
                    board.add_packet(packet)
                else:
                    # Send ARP request
                    packet = ARPrequest(self.rect.center, linked, self.mac, self.IP, self.gateway)
                    board.add_packet(packet)
                    self.waitingforARP.append((Packet(self.rect.center, linked, (self.mac, '<MISSING>'), (self.IP, self.target), server=server, resource=resource, method=method, body=body), self.gateway))
    
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
    def drawSelected(self, screen:pygame.surface.Surface):
        if self.receivedfrom[0]:
            tablepos = (self.rect.center[0] - 150, self.rect.center[1] - 280)
            WIDTH = 300
            pygame.draw.rect(screen, (255,255,255),pygame.Rect(tablepos[0], tablepos[1], WIDTH, 200))
            pygame.draw.rect(screen, (0,0,0),pygame.Rect(tablepos[0], tablepos[1], WIDTH, 200), 2)
            font = pygame.font.SysFont(None, 20, False)
            img = font.render(self.receivedfrom[0], True, (0,0,0))
            rect = img.get_rect()
            rect.center = (self.rect.centerx, self.rect.centery-300)
            screen.blit(img, rect)
            if self.receivedfrom[1]:
                padding = 0
                for line in self.receivedfrom[1].split('\n'):
                    indexofbracket = line.find('>')
                    if indexofbracket > 0:
                        markup = line[:indexofbracket].split('; ')
                        data = {}
                        keys = []
                        try:
                            for entry in markup:
                                record = entry.split(':')
                                data[record[0]] = record[1]
                                keys.append(record[0])
                            if 'font' in keys:
                                fontsize = int(data['font'])
                            else:
                                fontsize = 20
                            if 'color' in keys:
                                color = eval(data['color'])
                            else:
                                color = (0,0,0)
                            if 'align' in keys:
                                align = data['align']
                            else:
                                align = 'left'
                            if 'padding' in keys:
                                addedpadding =  int(data['padding'])
                            else:
                                addedpadding = 0
                        except Exception as e:
                            print(e)
                            fontsize = 20
                            color = (0,0,0)
                            addedpadding = 0
                            align = 'left'
                        font = pygame.font.SysFont(None, fontsize, False)
                        img = font.render(str(line[indexofbracket+1:]), True, color)
                        rect = img.get_rect()
                        match align:
                            case 'left':
                                rect.topleft = (tablepos[0] + 5, tablepos[1] + 5 + padding)
                            case 'right':
                                rect.topright = (tablepos[0] + WIDTH - 5, tablepos[1] + 5 + padding )
                            case 'center':
                                rect.topleft = (tablepos[0] + WIDTH/2 - rect.width/2, tablepos[1] + 5 +padding)
                        screen.blit(img, rect)
                        padding += fontsize * 1/2 + addedpadding
                    else:
                        font = pygame.font.SysFont(None, 20, False)
                        img = font.render(str(line), True, (0,0,0))
                        screen.blit(img, (tablepos[0] + 5, tablepos[1] + 5 + padding))
                        padding += 20
            
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