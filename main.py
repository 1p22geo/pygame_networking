import pygame
from addRouter import AddRouter
from addServer import AddServer
from display import Display
from board import Board
from addButton import AddButton
from addRepeater import AddRepeater
from addSwitch import AddSwitch
from eventhandler import Handler
from addDHCP import AddDHCP
pygame.init()

size = width, height = 840, 520
display = Display(size)
board = Board()
clock = pygame.time.Clock()
handler = Handler()


button = AddButton(pygame.Rect(25,30,50,50))
board.add_object(button)

button = AddRepeater(pygame.Rect(20,100,60,60))
board.add_object(button)

button = AddSwitch(pygame.Rect(20,170,60,60))
board.add_object(button)

button = AddDHCP(pygame.Rect(10,240,80,80))
board.add_object(button)

button = AddRouter(pygame.Rect(25,330,50,50))
board.add_object(button)

button = AddServer(pygame.Rect(20,400,60,80))
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