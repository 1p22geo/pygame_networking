class IP():
    def __init__(self, addr):
        if isinstance(addr, str):
            self.tuple = addr.split('.')
            self.str = addr
        if isinstance(addr, tuple):
            self.tuple = addr
            self.str = '.'.join(addr)
        if isinstance(addr, list):
            self.tuple = tuple(addr)
            self.str = '.'.join(addr)
        if isinstance(addr, IP) :
            self.tuple = addr.tuple
            self.str = addr.str
    def check(self, addr, *args):
        if len(args) >= 1:
            # we have a subnet mask - args[0]
            ip = IP(addr)
            match args[0]:
                case '/24':
                    return self.tuple[:3] == ip.tuple[:3]
                case '/16':
                    return self.tuple[:2] == ip.tuple[:2]
                case '/8':
                    return self.tuple[:1] == ip.tuple[:1]
                case '/0':
                    return True

        else:
            # we don't have a mask - we check for identical adresses ( /32 mask, if you will)
            return self.tuple == ip.tuple