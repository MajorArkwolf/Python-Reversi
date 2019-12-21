import pygame
import gamestack
import config
from board import Board
from player import Player

class FontBox:
    white,black,green,dgreen = (255,255,255),(0,0,0),(79,185,8),(50,114,7)
    minx = 0
    miny = 0
    maxx = 0
    maxy = 0
    oldsize = (0, 0)
    textObject = None
    hover = False

    def Update(self):
        screensize = pygame.display.get_surface().get_size()
        mouse = pygame.mouse.get_pos()

        if mouse[0] > self.minx and mouse[0] < self.maxx and mouse[1] > self.miny and mouse[1] < self.maxy:
            self.textObject = self.txtobj.render(self.text, 1, self.dgreen)
            self.hover = True
        elif self.hover:
            self.textObject = self.txtobj.render(self.text, 1, self.white)
            self.hover = False

        if screensize != self.oldsize:
            newSize = [0, 0]
            newSize[0] = screensize[0] - self.oldsize[0]
            newSize[1] = screensize[1] - self.oldsize[1]
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


    def GetSize(self):
        return (self.maxx, self.maxy)

    def ClickOn(self):
        mouse = pygame.mouse.get_pos()
        if mouse[0] > self.minx and mouse[0] < self.maxx and mouse[1] > self.miny and mouse[1] < self.maxy:
            return True
        else:
            return False

    def __init__(self, textName, size):
        self.txtobj = pygame.font.SysFont("playgame", 100)
        self.oldsize = size
        size = self.txtobj.size(textName)
        self.maxx = size[0]
        self.maxy = size[1]
        self.text = textName
        self.textObject = self.txtobj.render(textName, 1, self.white)
       
        
class Menu:
    white,black,green,dgreen = (255,255,255),(0,0,0),(79,185,8),(50,114,7)

    def Draw(self):
        renderer = pygame.display.get_surface()
        renderer.fill(self.green)
        self.pg.Draw(renderer)
        self.p1.Draw(renderer)
        self.p2.Draw(renderer)
        self.exit.Draw(renderer)


    def OffsetPoint(self, size):
        screensize = pygame.display.get_surface().get_size()
        x = int((screensize[0] - size[0]) / 2)
        y = int((screensize[1] - size[1]) / 2)
        return (x, y)

    def Update(self):
        self.pg.Update()
        self.p1.Update()
        self.p2.Update()
        self.exit.Update()

    def Event(self, event):
        if pygame.mouse.get_pressed()[0] == True:
            if self.pg.ClickOn():
                config.gamestack.AddToStack(Board(8 , 8))
                config.gamestack.GetItem().player1 = Player(1)
                config.gamestack.GetItem().player2 = Player(2)
            elif self.p1.ClickOn():
                print("this will swapper")
            elif self.p2.ClickOn():
                print("this will swapper2")
            elif self.exit.ClickOn():
                config.gamestack.PopToStack()

    def __init__(self):
        renderer = pygame.display.get_surface()
        size = renderer.get_size()
        self.pg = FontBox("Play Game", size)
        moveMe = self.OffsetPoint(self.pg.GetSize())
        self.pg.MoveText((moveMe[0], moveMe[1] / 4))
        self.p1 = FontBox("Player 1", size)
        self.p1.MoveText((moveMe[0], ((moveMe[1] / 4 ) * 3)))
        self.p2 = FontBox("Player 2", size)
        self.p2.MoveText((moveMe[0], ((moveMe[1] / 4 ) * 5)))
        self.exit = FontBox("Exit", size)
        self.exit.MoveText((moveMe[0], ((moveMe[1] / 4 ) * 7)))
