import pygame
from display import Display
from board import Board
from addButton import AddButton
from addRepeater import AddRepeater
from eventhandler import Handler
pygame.init()

size = width, height = 640, 480
display = Display(size)
board = Board()
clock = pygame.time.Clock()
handler = Handler()


button = AddButton(pygame.Rect(10,170,50,50))
board.add_object(button)

button = AddRepeater(pygame.Rect(5,230,50,50))
board.add_object(button)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        else:
            handler.handle_event(event, board)
    if not running:
        break
    
    display.draw(board, handler.selected)
    clock.tick(20)