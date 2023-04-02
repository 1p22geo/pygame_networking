import pygame

class Item():
    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.__id = -1
        self.selectable = True
        self.image = 'host.png'
    
    def assign_id(self, newid):
        self.__id = newid
    
    def get_id(self):
        return self.__id

    def check_click(self, click):
        clicked = pygame.Rect.collidepoint(self.rect, click)
        return clicked
    
    def click(self, button, board):
        pass
    
    def dragged(self, pos, button):
        if button == 1:
            self.rect.center = pos
        
    def dragto(self, pos, button, board):
        pass

    def drawOptions(self, screen):
        pass
    def drawSelected(self, screen):
        pass