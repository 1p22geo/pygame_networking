import random
class DHCP_gen():
    def __init__(self):
        self.mask = '255.255.255.0'
        self.hosts = 0
        self.macs = ['ffff']
    def new_host(self):
        if self.hosts > 250:
            raise Exception('Too many hosts. DHCP server crashed.')
        mac = 'ffff'
        while mac in self.macs:
            mac = ''.join(random.choices('abcdef1234567890', k=4))
        self.hosts += 1
        return  mac
    
generator = DHCP_gen()