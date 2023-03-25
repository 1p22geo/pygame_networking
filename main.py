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

size = width, height = 1280, 720
display = Display(size)
board = Board()
clock = pygame.time.Clock()
handler = Handler()


button = AddButton(pygame.Rect(25,130,50,50))
board.add_object(button)

button = AddRepeater(pygame.Rect(20,200,60,60))
board.add_object(button)

button = AddSwitch(pygame.Rect(20,270,60,60))
board.add_object(button)

button = AddDHCP(pygame.Rect(10,340,80,80))
board.add_object(button)

button = AddRouter(pygame.Rect(25,430,50,50))
board.add_object(button)

button = AddServer(pygame.Rect(20,500,60,80))
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