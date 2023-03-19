import pygame
from linkable import Linkable
from board import Board

class Display():
    def __init__(self, size):
        self.screen = pygame.display.set_mode(size)
        self.screensize = size
        self.sendimg = pygame.image.load('send.png')
    def draw(self, board:Board, selected):
        self.screen.fill((255,255,255))
        
        if selected >= 0:
             
             self.draw_selected_dialog(board, selected)
        for item in board.objects:
            if issubclass(type(item), Linkable):
                for link in item.links:
                    pygame.draw.line(self.screen, (0,0,0), item.rect.center, board.objects[link].rect.center, 5)
        for item in board.get_objects():
            pygame.draw.rect(self.screen, (255,255,255), item.rect)
            self.screen.blit(item.image, item.rect)
        for packet in board.get_packets():
            pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(packet.pos[0] - 5, packet.pos[1] - 5, 10, 10))
            packet.move()
            if packet.reached:
                packet.dest.recieve(packet, board)
                board.del_packet(packet.get_id())


        pygame.display.flip()

    def draw_selected_dialog(self, board:Board, selected):
         selectedobject = board.objects[selected]
         pos = selectedobject.rect.center
         if selectedobject.selectable:
            button1pos = [pos[0], pos[1] - 60]
            rect = pygame.Rect(0,0,30,30)
            rect.center = button1pos
            self.screen.blit(self.sendimg, rect)

            font = pygame.font.SysFont(None, 30, False)
            img = font.render('.'.join(selectedobject.IP), True, (0,0,0))
            rect = img.get_rect()
            rect.center = [pos[0], pos[1] + 40]
            self.screen.blit(img, rect)
            font = pygame.font.SysFont(None, 20, False)
            img = font.render(selectedobject.mac, True, (0,0,0))
            rect = img.get_rect()
            rect.center = [pos[0], pos[1] + 60]
            self.screen.blit(img, rect)