import pygame

class Menu:
    white,black,green,dgreen = (255,255,255),(0,0,0),(79,185,8),(50,114,7)

    def Draw(self):
        renderer = pygame.display.get_surface()
        renderer.fill(self.green)

    def Update(self):
        print("I update :D")

    def Event(self, event):
        print("I check events")

    def __init__(self):
        self.mainmenu = pygame.font.Font(pygame.font.SysFont(, (50, 50))