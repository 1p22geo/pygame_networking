from ARPrequest import ARPrequest
from ARPresponse import ARPresponse
from router_interface import Router_interface
from dhcp import generator
from packet import Packet
from board import Board
from appJar import gui
from host import Host
from IP import IP
import pygame


class Router(Host):
    def __init__(self, rect, mac):
        super().__init__(rect, mac)
        self.interfaces = []
        self.routingtable = {}
        '''
        key - a tuple including an IP adress (str) and a subnet mask (i.e. /24)
        value - a tuple including the interface ID and a destination IP adress
        '''
        self.routes = []
        '''
        ordering the dictionary
        '''

        
        self.ARP = {}
        self.image = pygame.image.load('router.png')
        self.ifimage = pygame.image.load('DHCP.png')
        self.routeimg = pygame.image.load('route.png')
        self.frame = 'Routes'
        
    def add_interface(self, board:Board):
        if len(self.interfaces) >= 4:
            return
        mac = generator.new_host()
        interface = Router_interface(pygame.Rect(0,0,50,50), mac, self.get_id(), len(self.interfaces))
        board.add_object(interface)
        self.interfaces.append(interface)

        self.update_interfaces()
    
    def drag(self,widget):
        
        #print("Dragged from:", widget)
        self.draggedItem = widget

    def drop(self,widget):
        #print("Dropped on:", widget)
        if len(widget) == 2:
            self.routes.insert(int(widget[1]),self.routes.pop(int(self.draggedItem[1])))
        if widget == 'delete':
            self.routingtable.pop(self.routes[int(self.draggedItem[1])])
            self.routes.pop(int(self.draggedItem[1]))
        self.draw_routes()
        self.draggedItem = None

    def draw_routes(self):
        self.app.openLabelFrame(self.frame)
        self.app.emptyCurrentContainer()
        n = 0
        for route in self.routes:
            self.app.addLabel('a'+str(n), route[0]+route[1] + '    ', column=0, row=n)
            self.app.addLabel('b'+str(n),'   -->   ', column=1, row=n)
            if self.routingtable[route][1]:
                dest = self.routingtable[route][1].str
            else:
                dest = 'DC'
            self.app.addLabel('c'+str(n),  '    IF' +str(self.routingtable[route][0])+'    ', column=2, row=n)
            self.app.addLabel('d'+str(n),dest, column=3, row=n)
            self.app.setLabelDragFunction('a'+str(n), [self.drag, self.drop])
            self.app.setLabelDragFunction('b'+str(n), [self.drag, self.drop])
            self.app.setLabelDragFunction('c'+str(n), [self.drag, self.drop])
            self.app.setLabelDragFunction('d'+str(n), [self.drag, self.drop])
            n+= 1
        self.app.stopLabelFrame()

    def add_route(self,button):
        if button == 'Cancel':
            self.app.hideSubWindow('one')
        else:
            route = (self.app.getEntry('Route: '), self.app.getEntry('Subnet: '))
            destination = self.app.getEntry('Destination: ')
            if destination == 'DC':
                destination = None
            else:
                destination = IP(destination)
            interface = self.app.getEntry('Interface: ')
            if interface[0:2].upper() == 'IF':
                interface = interface[2:]
            dest = (int(interface), destination)
            self.routes.append(route)
            self.routingtable[route] = dest
            self.app.hideSubWindow('one')
        self.draw_routes()

    def start_app(self):
        self.app = gui('Router')
        self.app.startSubWindow("one", modal=True)
        self.app.addLabel("label1", "Configure new route")
        self.app.addLabelEntry('Route: ')
        self.app.addLabelEntry('Subnet: ')
        self.app.addLabelEntry('Destination: ')
        self.app.addLabelEntry('Interface: ')
        self.app.addHorizontalSeparator()
        self.app.addButtons(['Continue', 'Cancel'], self.add_route)
        self.app.stopSubWindow()
        self.app.addLabel('title', 'Router configuration')
        self.app.startLabelFrame(self.frame)
        self.app.addLabel('loading', 'Loading')
        self.app.stopLabelFrame()
        self.draw_routes()
        self.app.startFrame('asdf')
        self.app.addLabel('delete', 'Delete', column=0, row=len(self.routes))
        self.app.addButton('Add route', self.add, column=1,  row=len(self.routes))
        self.app.stopFrame()
        self.app.go()

    def add(self,button):
        self.app.showSubWindow('one')

    def dragged(self, pos, button):
        if button == 1:
            self.rect.center = pos
            self.update_interfaces()

    def update_interfaces(self):
        match len(self.interfaces):
            case 0 :
                pass
            case 1:
                self.interfaces[0].rect.center = (self.rect.center[0], self.rect[1] - 50)
            case 2:
                self.interfaces[0].rect.center = (self.rect.center[0] - 2*50, self.rect.center[1])
                self.interfaces[1].rect.center = (self.rect.center[0] + 2*50, self.rect.center[1])
            case 3:
                self.interfaces[0].rect.center = (self.rect.center[0] - 2*0.866*50, self.rect.center[1] + 2*25)
                self.interfaces[1].rect.center = (self.rect.center[0] + 2*0.866*50, self.rect.center[1] + 2*25)
                self.interfaces[2].rect.center = (self.rect.center[0], self.rect[1] - 50)
            case 4:
                self.interfaces[0].rect.center = (self.rect.center[0] - 2*35, self.rect.center[1] - 2*35)
                self.interfaces[1].rect.center = (self.rect.center[0] + 2*35, self.rect.center[1] - 2*35)
                self.interfaces[2].rect.center = (self.rect.center[0] - 2*35, self.rect.center[1] + 2*35)
                self.interfaces[3].rect.center = (self.rect.center[0] + 2*35, self.rect.center[1] + 2*35)
            case _:
                raise Exception('Too much interfaces')
    def receive(self, packet, board: Board, interface):
        if isinstance(packet, ARPresponse):
            inf = self.interfaces[interface]
            self.ARP[packet.l3[0].str] = packet.l2[0]
            if packet.l2[1] == inf.mac:
                for p in self.waitingforARP:
                    #print(p[1][1], packet.l3)
                    if p[1][1].str == packet.l3[0].str:
                        p[0].l2 = (p[0].l2[0],packet.l2[0])
                        board.add_packet(p[0])
            return
        elif isinstance(packet, ARPrequest):
            self.ARP[packet.l3[0].str] = packet.l2[0]
            inf = self.interfaces[interface]
            if packet.l3 and inf.IP and (packet.l3[1].str == inf.IP.str):
                for link in inf.links:
                    linked = board.objects[link]
                    packet2 = ARPresponse(inf.rect.center, linked, (inf.mac, packet.l2[0]), (inf.IP,packet.l3[0]))
                    board.add_packet(packet2)
            return
        elif type(packet) == Packet:
            
            for route in self.routes:
                if packet.l3[1].check(route[0], route[1]):
                    packet_route = route
                    break
            else:
                return
            route = self.routingtable[packet_route]
            #print("Interface {0} recieved a packet from {1}, forwarding to {2}".format(interface, packet.l3[0], route))
            inf = self.interfaces[route[0]]
            for link in inf.links:
                linked = board.objects[link]
                dest = route[1]
                if not dest:
                    dest = packet.l3[1]
                if dest.str in self.ARP.keys():
                    packet1 = Packet(inf.rect.center, linked, (inf.mac, self.ARP[dest.str]), packet.l3)
                    board.add_packet(packet1)
                else:
                    # Send ARP request
                    arppacket = ARPrequest(inf.rect.center, linked, inf.mac, inf.IP, dest)
                    board.add_packet(arppacket)
                    self.waitingforARP.append((Packet(inf.rect.center, linked, (self.mac, '<MISSING>'), packet.l3), [route[0], dest]))
    def drawSelected(self, screen):
        button1pos = [self.rect.center[0] + 30, self.rect.center[1] - 100]
        rect = pygame.Rect(0,0,30,30)
        rect.center = button1pos
        screen.blit(self.ifimage, rect)
        button1pos = [self.rect.center[0] - 30, self.rect.center[1] - 100]
        rect = pygame.Rect(0,0,30,30)
        rect.center = button1pos
        screen.blit(self.routeimg, rect)
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
    def drawOptions(self, screen):
        pass