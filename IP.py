class IP():
    def __init__(self, addr):
        self.tuple:tuple = tuple()
        self.str:str = str()
        if isinstance(addr, str):
            self.tuple:tuple = tuple(addr.split('.'))
            self.str:str = addr
        elif isinstance(addr, tuple):
            self.tuple:tuple = tuple(addr)
            self.str:str = '.'.join(addr)
        elif isinstance(addr, list):
            self.tuple:tuple = tuple(addr)
            self.str:str = '.'.join(addr)
        elif isinstance(addr, IP) :
            self.tuple:tuple = tuple(addr.tuple)
            self.str:str = addr.str
        else:
            self.tuple:tuple = ()
            self.str:str = str('')
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
    def __str__(self):
        return self.str
    def __repr__(self) -> str:
        return 'IP(\'' + self.str + '\')'