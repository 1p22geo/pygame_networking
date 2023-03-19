import pygame, math

class Traverser():
    def __init__(self, pos:tuple, target:tuple):
        self.pos = pos
        self.target = target
        self.reached = False
    
    def assign_id(self, newid):
        self.__id = newid
    
    def get_id(self):
        return self.__id

    def move(self):
        if math.sqrt((self.pos[0]-self.target[0])**2+(self.pos[1]-self.target[1])**2) < 5:
            self.reached = True
            return
        vec = [self.target[0] - self.pos[0], self.target[1] - self.pos[1]]
        length = math.sqrt((vec[0]**2) + (vec[1]**2))
        scale = 3/length

        newvec = [scale*vec[0] , scale*vec[1]]

        self.pos = (self.pos[0] + newvec[0], self.pos[1] + newvec[1])
