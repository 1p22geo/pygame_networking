import appJar
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