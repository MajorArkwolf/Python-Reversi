import pygame
from pygame.locals import *

class FontBox:
    white, black, green, dark_green = (255, 255, 255), (0, 0, 0), (79, 185, 8), (50, 114, 7)
    minx = 0
    miny = 0
    maxx = 0
    maxy = 0
    oldsize = (0, 0)
    textObject = None
    moveable = False

    def Update(self):
        screensize = pygame.display.get_surface().get_size()

        if screensize != self.oldsize and self.moveable:
            x = screensize[0] - self.oldsize[0]
            y = screensize[1] - self.oldsize[1]
            newSize = [x, y]
            self.minx += int(newSize[0] / 2)
            self.maxx += int(newSize[0] / 2)
            self.miny += int(newSize[1] / 2)
            self.maxy += int(newSize[1] / 2)
            self.oldsize = screensize

    def Draw(self, renderer):
        renderer.blit(self.textObject, (self.minx, self.miny))

    def MoveText(self, size):
            self.maxx = size[0] + (self.maxx - self.minx)
            self.maxy = size[1] + (self.maxy - self.miny)
            self.minx = size[0]
            self.miny = size[1]

    def ChangeText(self, newText, newColor = (255,255,255)):
        self.textObject = self.txtobj.render(newText, 1, newColor)
        self.txtobj = pygame.font.SysFont(newText, self.fontsize)
        size = self.txtobj.size(newText)
        self.maxx = size[0] + self.minx
        self.maxy = size[1] + self.miny

    def GetSize(self):
        return (self.maxx, self.maxy)

    def MakeMoveable(self, move):
        self.moveable = move

    def ReturnMinMax(self):
        return (self.maxx - self.minx, self.maxy - self.miny)

    def __init__(self, textName, fontsize, size):
        self.fontsize = fontsize
        self.txtobj = pygame.font.SysFont(textName, self.fontsize)
        self.oldsize = size
        size = self.txtobj.size(textName)
        self.maxx = size[0]
        self.maxy = size[1]
        self.text = textName
        self.textObject = self.txtobj.render(textName, 1, self.white)