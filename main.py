import pygame
from pygame.locals import *
pygame.init()
pygame.font.init()
import os, sys
from board import Board
from player import Player
from menu import Menu
from gamestack import GameStack


def WinCheck():
    won = False
    return won

def main():    
    gamestack = GameStack()
    gamestack.AddToStack(Menu())
    screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    pygame.display.set_caption("Reversi")
    gamestack.AddToStack(Menu())
    #gamestack.GetItem().player1 = Player(1)
    #gamestack.GetItem().player2 = Player(2)

    while gamestack.EmptyStack() == False:
        gamestack.Update()
        gamestack.Draw()        

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            else:
                gamestack.Event(event)


        if gamestack.EmptyStack():
            return

main()