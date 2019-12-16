import pygame
from pygame.locals import *
pygame.init()
pygame.font.init()
import os, sys
import config
from board import Board
from player import Player
from menu import Menu
from gamestack import GameStack
import config



def WinCheck():
    won = False
    return won

def main():    
    config.gamestack = GameStack()
    pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    pygame.display.set_caption("Reversi")
    config.gamestack.AddToStack(Menu())

    while config.gamestack.EmptyStack() == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                config.gamestack.PopToStack()
            else:
                config.gamestack.Event(event)

        config.gamestack.Update()
        config.gamestack.Draw()
        pygame.display.update()

main()