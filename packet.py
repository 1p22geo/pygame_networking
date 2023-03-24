from traverse import Traverser

class Packet(Traverser):
    '''
    l2 - second layer header - tuple of two elements
        source MAC adress : string
        destination MAC adress : string
    l3 - third layer header - another tuple
        source IP : IP()
        destionation IP : IP()
    '''
    def __init__(self, pos:tuple, dest, l2, l3, **kwargs):
        super().__init__(pos, dest)
        self.startpos = pos
        self.l2 = l2
        self.l3 = l3
        self.payload = kwargs
        
