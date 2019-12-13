from node import Node
from player import Player

import pygame

class Board:
    white,black,green,dgreen = (255,255,255),(0,0,0),(79,185,8),(50,114,7)
    nodeList = []
    xsize = 0
    ysize = 0
    boardSize = 0
    padding = 0
    selectedNode = 0
    player1 = None
    player2 = None
    currentTurn = None
    playerSwap = False

    def BuildNodes(self):            
        for y in range (0, self.ysize):
            for x in range (0, self.xsize):
                node = Node(x, y)
                self.nodeList.append(node)

    def CalcXPadding(self, size):
        return int((size[0] - self.boardSize) / 2)
    
    def CalcYPadding(self, size):
        return int(size[1] * ((1 - self.padding)/2))

    def CalcGridSize(self, size):
        return self.boardSize / self.xsize

    def Draw(self, size, renderer):
        self.renderer = renderer
        self.DrawBoard(size)
        self.DrawPeice(size)        
        pygame.display.flip()
        return self.renderer

    def DrawBoard(self, size):
        self.padding = 0.9
        self.boardSize = size[1] * self.padding
        pygame.draw.rect(self.renderer, self.green,[self.CalcXPadding(size), self.CalcYPadding(size) , self.boardSize, self.boardSize])
        gridSize = self.CalcGridSize(size)
        for x in range (0 , self.xsize):
            for y in range (0, self.ysize):
                if ((x + y) % 2):
                    left = self.CalcXPadding(size) + gridSize * x
                    top = self.CalcYPadding(size) + gridSize * y
                    pygame.draw.rect(self.renderer, self.dgreen, [left, top, gridSize, gridSize])

    def DrawPeice(self, size):
        for node in self.nodeList:
            if (node.m_player != 0):
                gridSize = self.CalcGridSize(size)
                left = int(self.CalcXPadding(size) + gridSize * node.m_x + (gridSize / 2))
                top = int(self.CalcYPadding(size) + gridSize * node.m_y + (gridSize / 2))
                pos = [left, top]
                radius = int(gridSize / 2)
                if (node.m_player == 1):
                    pygame.draw.circle(self.renderer, self.white, pos, radius)
                if (node.m_player == 2):
                    pygame.draw.circle(self.renderer, self.black, pos, radius)

    def DrawSelected(self, size):
        if isinstance(self.selectedNode, Node):
            yellow = (255, 255, 0)
            gridSize = self.CalcGridSize(size)
            left = int(self.CalcXPadding(size) + gridSize * self.selectedNode.m_x)
            top = int(self.CalcYPadding(size) + gridSize * self.selectedNode.m_y)
            pygame.draw.rect(self.renderer, yellow,[left, top , gridSize, gridSize])

    def Update(self):
        if self.currentTurn == None:
            self.currentTurn = self.player1
        if self.playerSwap == True:
            if self.currentTurn.GetPlayerID() == 1:
                self.currentTurn = self.player2
            elif self.currentTurn.GetPlayerID() == 2:
                self.currentTurn = self.player1
            self.playerSwap = False

    def PlayerSelectNode(self, cords, playerid):
        node = self.GetSelectedNode(cords)
        if isinstance(node, Node):
            if node.m_player == playerid:
                self.selectedNode = node
                return node
            else:
                self.selectedNode = None
                return None

    def GetSelectedNode(self, cords):
        index = self.xsize * cords[1] + cords[0]
        node = self.nodeList[index]
        return node

    def DeselectNode(self):
        self.selectedNode = None

    def ModChip(self, nodes, playerid):
        for nodeCord in nodes:
            node = self.GetSelectedNode(nodeCord)
            index = self.xsize * node.m_y + node.m_x
            self.nodeList[index].m_player = playerid

    def StraightLineCheck(self, cords, playerid):
        startingNode = self.GetSelectedNode(cords)
        validMove = False
        nodes = []

        #Up Check
        for y in range(startingNode.m_y - 1, -1, -1):
            checkNode = self.GetSelectedNode((startingNode.m_x, y))
            if checkNode.m_player == self.currentTurn.GetPlayerID():
                break
            elif checkNode.m_player == 0:
                nodes = []
                break
            elif y == 0 and checkNode.m_player != playerid:
                nodes = []
                break
            else:
                nodes.append((startingNode.m_x, y))

        if len(nodes) >= 1:
            nodes.append((startingNode.m_x, startingNode.m_y))
            self.ModChip(nodes, self.currentTurn.GetPlayerID())
            validMove = True
            nodes = []
        else:
            nodes = []

        #Down Check
        for y in range(startingNode.m_y + 1, self.ysize):
            checkNode = self.GetSelectedNode((startingNode.m_x, y))
            if checkNode.m_player == self.currentTurn.GetPlayerID():
                break
            elif checkNode.m_player == 0:
                nodes = []
                break
            elif y == self.ysize -1 and checkNode.m_player != playerid:
                nodes = []
                break
            else:
                nodes.append((startingNode.m_x, y))

        if len(nodes) >= 1:
            nodes.append((startingNode.m_x, startingNode.m_y))
            self.ModChip(nodes, self.currentTurn.GetPlayerID())
            validMove = True
            nodes = []
        else:
            nodes = [] 

        if len(nodes) >= 1:
            nodes.append((startingNode.m_x, startingNode.m_y))
            self.ModChip(nodes, self.currentTurn.GetPlayerID())
            validMove = True
            nodes = []
        else:
            nodes = []

        #Left Check
        for x in range(startingNode.m_x - 1, -1, -1):
            checkNode = self.GetSelectedNode((x, startingNode.m_y))
            if checkNode.m_player == self.currentTurn.GetPlayerID():
                break
            elif checkNode.m_player == 0:
                nodes = []
                break
            elif x == 0 and checkNode.m_player != playerid:
                nodes = []
                break
            else:
                nodes.append((x,startingNode.m_y))

        if len(nodes) >= 1:
            nodes.append((startingNode.m_x, startingNode.m_y))
            self.ModChip(nodes, self.currentTurn.GetPlayerID())
            validMove = True
            nodes = []
        else:
            nodes = []

        #Right Check
        for x in range(startingNode.m_x + 1, self.xsize):
            checkNode = self.GetSelectedNode((x, startingNode.m_y))
            if checkNode.m_player == self.currentTurn.GetPlayerID():
                break
            elif checkNode.m_player == 0:
                nodes = []
                break
            elif x == self.xsize -1 and checkNode.m_player != playerid:
                nodes = []
                break
            else:
                nodes.append((x,startingNode.m_y))

        if len(nodes) >= 1:
            nodes.append((startingNode.m_x, startingNode.m_y))
            self.ModChip(nodes, self.currentTurn.GetPlayerID())
            validMove = True
            nodes = []
        else:
            nodes = []

        return validMove
        


    def DiagonalLineCheck(self, cords, playerid):
        validMove = True
        #diagnal Top Left
        

        return validMove


    def AttemptMove(self, cords, playerid):
        trueValid = False
        if(self.GetSelectedNode(cords).m_player == 0):
            valid = []
            valid[0] = self.StraightLineCheck(cords, playerid)
            valid[1] = self.DiagonalLineCheck(cords, playerid)

            if (valid[0] or valid[1]):
                trueValid = True
        return trueValid

    def __init__(self, screen, xsize = 10, ysize = 10):
        self.xsize = xsize
        self.ysize = ysize
        self.BuildNodes()
        self.selectedNode == None
        location = xsize * 4 + 3
        self.nodeList[location].ChangePlayer(2)
        location = xsize * 4 + 4
        self.nodeList[location].ChangePlayer(1)
        location = xsize * 3 + 3
        self.nodeList[location].ChangePlayer(1)
        location = xsize * 3 + 4
        self.nodeList[location].ChangePlayer(2)
