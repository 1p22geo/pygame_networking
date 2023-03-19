import pygame
import item

class Linkable(item.Item):
    def __init__(self, rect):
        super().__init__(rect)
        self.links = []

    
    def dragto(self, pos, button, board):
        if button == 3:
            for o in board.objects:
                if issubclass(type(o), Linkable):
                    if o.check_click(pos):
                        if o.get_id() in self.links:
                            del self.links[self.links.index(o.get_id())]
                            del o.links[o.links.index(self.get_id())]
                        else:
                            self.links.append(o.get_id())
                            o.links.append(self.get_id())