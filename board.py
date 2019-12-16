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
    player1 = None
    player2 = None
    currentTurn = None
    playerSwap = False
    player1Score = 0
    player2Score = 0

    def BuildNodes(self):            
        for y in range (0, self.ysize):
            for x in range (0, self.xsize):
                self.nodeList.append(Node(x, y, 0))

    def CalcXPadding(self, size):
        return int((size[0] - self.boardSize) / 2)
    
    def CalcYPadding(self, size):
        return int(size[1] * ((1 - self.padding)/2))

    def CalcGridSize(self, size):
        return self.boardSize / self.xsize

    def Draw(self):
        self.renderer = pygame.display.get_surface()
        size = self.renderer.get_size()
        self.renderer.fill(self.black)
        self.DrawBoard(size)
        self.DrawPeice(size)        
        pygame.display.flip()

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
        self.ScoreCheck()

    def ScoreCheck(self):
        p1score = 0
        p2score = 0
        for node in self.nodeList:
            if node.m_player == 1:
                p1score += 1
            elif node.m_player == 2:
                p2score += 1
        self.player1Score = p1score
        self.player2Score = p2score

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

    def MoveCheck(self, cords, playerid):
        validMove = False
        nodes = []
        #Up Check
        nodes += self.LineCheck(cords, 'e', 'n', playerid)

        #Down Check
        nodes += self.LineCheck(cords, 'e', 'p', playerid)

        #Left Check
        nodes += self.LineCheck(cords, 'n', 'e', playerid)

        #Right Check
        nodes += self.LineCheck(cords, 'p', 'e', playerid)

        #Down and Right
        nodes += self.LineCheck(cords, 'p', 'p', playerid)

        #Up and Right
        nodes += self.LineCheck(cords, 'p', 'n', playerid)

        #Up and Left
        nodes += self.LineCheck(cords, 'n', 'n', playerid)

        #Down and Left
        nodes += self.LineCheck(cords, 'n', 'p', playerid)

        if len(nodes) >= 1:
            nodes.append(cords)
            self.ModChip(nodes, self.currentTurn.GetPlayerID())
            validMove = True
            nodes = []

        return validMove
        
    def LineCheck(self, cords, xpos, ypos, playerid):
        nodes = []
        newCords = cords
        while 1:
            if(xpos == 'p'):
                x = newCords[0] + 1
            elif(xpos == 'n'):
                x = newCords[0] - 1
            else:
                x = newCords[0]

            if(ypos == 'p'):
                y = newCords[1] + 1
            elif(ypos == 'n'):
                y = newCords[1] - 1
            else:
                y = newCords[1]

            newCords = (x, y)

            if newCords[0] < 0 or newCords[0] >= self.xsize or newCords[1] < 0 or newCords[1] >= self.ysize:
                del nodes[:]
                break
            elif self.GetSelectedNode(newCords).m_player == self.currentTurn.GetPlayerID():
                break
            elif self.GetSelectedNode(newCords).m_player == 0:
                del nodes[:]
                break
            else:
                nodes.append(newCords)
        return nodes

    def AttemptMove(self, cords, playerid):
        trueValid = False
        if(self.GetSelectedNode(cords).m_player == 0):
            valid = (self.MoveCheck(cords, playerid))
            if (valid):
                trueValid = True
        return trueValid

    def Event(self, event):
        if self.currentTurn.IsPlayer():
            if pygame.mouse.get_pressed()[0] == True:
                self = self.currentTurn.OnLeftClick(pygame.mouse.get_pos(), self, pygame.display.get_surface().get_size())
            elif pygame.mouse.get_pressed()[2] == True:
                self = self.currentTurn.OnRightClick(pygame.mouse.get_pos(), self, pygame.display.get_surface().get_size())

    def __init__(self, xsize = 10, ysize = 10):
        self.xsize = xsize
        self.ysize = ysize
        self.BuildNodes()
        location = ysize * int((xsize / 2)) + int((ysize / 2) -1)
        self.nodeList[location].ChangePlayer(2)
        location = ysize * int(xsize / 2) + int(ysize / 2)
        self.nodeList[location].ChangePlayer(1)
        location = ysize * int((xsize / 2) - 1) + int((ysize / 2) -1)
        self.nodeList[location].ChangePlayer(1)
        location = ysize * int((xsize / 2) - 1) + int(ysize / 2)
        self.nodeList[location].ChangePlayer(2)

    def __del__(self):
        del self.nodeList[:]
