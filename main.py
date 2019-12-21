import pygame
from pygame.locals import *
from menu import Menu
from gamestack import GameStack
import config

pygame.init()
pygame.font.init()


def main():
    config.game_stack = GameStack()
    pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    pygame.display.set_caption("Reversi")
    config.game_stack.AddToStack(Menu())

    while not config.game_stack.EmptyStack():
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                config.game_stack.PopToStack()
            else:
                config.game_stack.Event(event)

        config.game_stack.Update()
        config.game_stack.Draw()
        pygame.display.update()


main()
