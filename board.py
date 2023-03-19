import pygame
from item import Item

class Board():
    def __init__(self):
        self.objects = []
        self.packets = []
    def add_object(self, obj):
        try:
            obj_id = self.objects.index(False)
            self.objects[obj_id] = obj
        except:
            obj_id = len(self.objects)
            self.objects.append(obj)
        self.objects[obj_id].assign_id(obj_id)
        return obj_id
    def del_object(self, oid):
        o = self.objects[oid]
        self.objects[oid] = False
        return o
    def add_packet(self, obj):
        try:
            obj_id = self.packets.index(False)
            self.packets[obj_id] = obj
        except:
            obj_id = len(self.packets)
            self.packets.append(obj)
        self.packets[obj_id].assign_id(obj_id)
        return obj_id
    def del_packet(self, oid):
        o = self.packets[oid]
        self.packets[oid] = False
        return o
    def get_objects(self):
        arr = []
        for obj in self.objects:
            if obj != False:
                arr.append(obj)
        return arr
    def get_packets(self):
        arr = []
        for obj in self.packets:
            if obj != False:
                arr.append(obj)
        return arr