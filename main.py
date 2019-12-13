import pygame
from pygame.locals import *
pygame.init()
import os, sys
from board import Board
from player import Player


def WinCheck():
    won = False
    return won

def main():
    screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    pygame.display.set_caption("Reversi")
    board = Board(screen, 8, 8)
    running = True  

    board.player1 = Player(1)
    board.player2 = Player(2)

    while running:
        board.Update()
        screen = board.Draw(screen.get_size(), screen)
      

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif board.currentTurn.IsPlayer():
                if pygame.mouse.get_pressed()[0] == True:
                    board = board.currentTurn.OnLeftClick(pygame.mouse.get_pos(), board, screen.get_size())
                elif pygame.mouse.get_pressed()[2] == True:
                    board = board.currentTurn.OnRightClick(pygame.mouse.get_pos(), board, screen.get_size())

main()