import pygame
from board import Board
from host import Host
from packet import Packet
import appJar


class Server(Host):
    def __init__(self, rect, mac):
        super().__init__(rect, mac)
        self.image = pygame.image.load('server.png')
        self.get = ''
        self.code = ''
        self.getcode = ''
        self.database = []

    def receive(self, packet, board:Board):
        if type(packet) == Packet:
            #print('HTTP {0} {1}\n{2}'.format(packet.payload['method'], packet.payload['resource'], packet.payload['body']))
            if packet.payload['method'] == 'POST':
                db = self.database
                host = packet.l3[0].str
                try:
                    exec(self.code)
                    response = '200 OK'
                except:
                    response = '500 Server error'
            elif packet.payload['method'] == 'GET':
                db = self.database
                host = packet.l3[0].str
                try:
                    exec(self.getcode)
                    #print('Code worked')
                    response = eval(self.get)
                    #print('Expression worked')
                except Exception as e:
                    #print(e)
                    response = '500 Server error'
                
            self.target = packet.l3[0]
            super().send(board, response)
        else:
            super().receive(packet, board)
    def press(self, button):
        if button == 'Cancel':
            self.app.stop()
            self.app = False
        else:
            self.code = self.app.getTextArea("Code to execute for POST requests: ")
            self.getcode = self.app.getTextArea("Code to execute before GET requests: ")
            self.get = self.app.getTextArea("Expression to evaluate for GET requests: ")
            #print(self.code, self.getcode, self.get, sep='\n\n\n')
            self.app.stop()
            self.app = False
        

    def config(self):
        self.app = appJar.gui('Server configuration', '720x800')
        self.app.setStretch('column')
        self.app.setSticky('nws')
        self.app.addLabel("title", "Server configuration")
        self.app.addHorizontalSeparator()
        self.app.setStretch('both')
        self.app.setSticky('news')
        self.app.startTabbedFrame('Code')
        with self.app.tab('Intro'):
            self.app.addLabel("desc1", "The global variable 'db' is an array.")
            self.app.addLabel("desc2", "Its state is retained between requests.")
            self.app.addLabel("desc3", "Use it to store information between them.")
            self.app.addLabel("desc5", "The global 'host' is the client's IP.")
        with self.app.tab('POST'):
            self.app.setStretch('column')
            self.app.setSticky('nws')
            self.app.addLabel("title1", "Code to execute for POST requests: ")
            self.app.setStretch('both')
            self.app.setSticky('news')
            self.app.addTextArea("Code to execute for POST requests: ")
        with self.app.tab('GET code'):
            self.app.setStretch('column')
            self.app.setSticky('nws')
            self.app.addLabel("title2", "Code to execute before GET requests: ")
            self.app.setStretch('both')
            self.app.setSticky('news')
            self.app.addTextArea("Code to execute before GET requests: ")
        with self.app.tab('GET expression'):
            self.app.setStretch('column')
            self.app.setSticky('nws')
            self.app.addLabel("title3", "Expression to evaluate for GET requests: ")
            self.app.setStretch('both')
            self.app.setSticky('news')
            self.app.addTextArea("Expression to evaluate for GET requests: ")
            self.app.setStretch('column')
            self.app.setSticky('ews')
            self.app.addLabel("desc4", "The expression must evaluate to a string.")
        
        self.app.stopTabbedFrame()
        self.app.setStretch('column')
        self.app.setSticky('ews')
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