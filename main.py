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
from dhcp import generator
import dill
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
            exit(0)
        else:
            handler.handle_event(event, board)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            try:
                filename = input("Name of file: ")
                file = open('saves/{0}'.format(filename), 'wb')
                dill.dump((board, generator), file)
                print("Game saved")
            except:
                print("Saving went wrong")
            finally:
                file.close()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
            try:
                filename = input("Name of file: ")
                file = open('saves/{0}'.format(filename), 'rb')
                board, generator = dill.load(file)
                print("Save restored")
            except:
                print("Restoring save went wrong")
            finally:
                file.close()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            try:
                filename = "quick.sav"
                file = open('saves/{0}'.format(filename), 'wb')
                dill.dump((board, generator), file)
                print("Game saved")
            except:
                print("Saving went wrong")
            finally:
                file.close()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
            try:
                filename = "quick.sav"
                file = open('saves/{0}'.format(filename), 'rb')
                board, generator = dill.load(file)
                print("Save restored")
            except:
                print("Restoring save went wrong")
            finally:
                file.close()
    if not running:
        break
    
    display.draw(board, handler.selected)
    clock.tick(20)