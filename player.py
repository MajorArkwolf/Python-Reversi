import pygame
from node import Node

class Player:

    def OnLeftClick(self, mouse, board, size):
        cord = self.GetNodeCord(mouse, board, size)
        print(cord)
        if cord is not None:
            if board.AttemptMove(cord, self.playerid):
                board.playerSwap = True

        return board

    def OnRightClick(self, mouse, board, size):
        board.DeselectNode()
        self.selectedNode = None
        return board

    def GetNodeCord(self, mouse, board, size):
        xpad = board.CalcXPadding(size)
        ypad = board.CalcYPadding(size)
        gridSize = board.CalcGridSize(size)
        if((mouse[0] - xpad) / gridSize >= 0): 
            x = int((mouse[0] - xpad) / gridSize)
        else:
            x = -1
        if ((mouse[1] - ypad) / gridSize >= 0):
            y = int((mouse[1] - ypad) / gridSize)
        else:
            y = -1
        if (x >= 0 and x < board.xsize):
            if (y >= 0 and y < board.ysize):
                return (x , y)
        return None

    def IsPlayer(self):
        return True

    def GetPlayerID(self):
        return self.playerid

    def __init__(self, playerid, node = None):
        self.playerid = playerid
        self.selectedNode = node
