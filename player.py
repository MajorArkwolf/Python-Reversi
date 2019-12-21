import pygame
from pygame.locals import *
from node import Node


class Player:

    def OnLeftClick(self, mouse, board, size):
        cord = self.GetNodeCord(mouse, board, size)
        # print(cord)
        if cord is not None:
            if board.AttemptMove(cord, self.player_id):
                board.playerSwap = True

        return board

    def OnRightClick(self, mouse, board, size):
        return

    def GetNodeCord(self, mouse, board, size):
        x_pad = board.CalcXPadding(size)
        y_pad = board.CalcYPadding(size)
        gridSize = board.CalcGridSize(size)
        if (mouse[0] - x_pad) / gridSize >= 0:
            x = int((mouse[0] - x_pad) / gridSize)
        else:
            x = -1
        if (mouse[1] - y_pad) / gridSize >= 0:
            y = int((mouse[1] - y_pad) / gridSize)
        else:
            y = -1
        if 0 <= x < board.x_size:
            if 0 <= y < board.y_size:
                return x, y
        return None

    def IsPlayer(self):
        return True

    def GetPlayerID(self):
        return self.player_id

    def __init__(self, player_id, node=None):
        self.player_id = player_id
        self.selectedNode = node
