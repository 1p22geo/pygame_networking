import pygame

class Item():
    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.__id = -1
        self.selectable = True
        self.image = pygame.image.load('host.png')
    
    def assign_id(self, newid):
        self.__id = newid
    
    def get_id(self):
        return self.__id

    def check_click(self, click):
        clicked = pygame.Rect.collidepoint(self.rect, click)
        """ if clicked:
            self.click() """
        return clicked
    
    def click(self, button, board):
        print("Object {} clicked!".format(self.__id))
    
    def dragged(self, pos, button):
        if button == 1:
            self.rect.center = pos
        
    def dragto(self, pos, button, board):
        print("Dragged to {0} with button {1}".format(pos, button))