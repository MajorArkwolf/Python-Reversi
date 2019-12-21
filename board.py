from node import Node
from player import Player
from gamefont import FontBox

import pygame


class Board:
    white, black, green, dgreen = (255, 255, 255), (0, 0, 0), (79, 185, 8), (50, 114, 7)
    nodeList = []
    xsize = 0
    ysize = 0
    boardSize = 0
    padding = 0
    player1 = None
    player2 = None
    currentTurn = None
    playerSwap = False
    won = False
    player1Score = 0
    player2Score = 0

    def BuildNodes(self):
        for y in range(0, self.ysize):
            for x in range(0, self.xsize):
                self.nodeList.append(Node(x, y, 0))

    def CalcXPadding(self, size):
        return int((size[0] - self.boardSize) / 2)

    def CalcYPadding(self, size):
        return int(size[1] * ((1 - self.padding) / 2))

    def CalcGridSize(self, size):
        return self.boardSize / self.xsize

    def Draw(self):
        self.renderer = pygame.display.get_surface()
        size = self.renderer.get_size()
        self.renderer.fill(self.black)
        self.DrawBoard(size)
        self.DrawPeice(size)
        self.turnText.Draw(self.renderer)
        self.whiteText.Draw(self.renderer)
        self.blackText.Draw(self.renderer)
        self.winner.Draw(self.renderer)
        pygame.display.flip()

    def DrawBoard(self, size):
        self.padding = 0.9
        self.boardSize = size[1] * self.padding
        pygame.draw.rect(self.renderer, self.green,
                         [self.CalcXPadding(size), self.CalcYPadding(size), self.boardSize, self.boardSize])
        gridSize = self.CalcGridSize(size)
        for x in range(0, self.xsize):
            for y in range(0, self.ysize):
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
            pygame.draw.rect(self.renderer, yellow, [left, top, gridSize, gridSize])

    def Update(self):
        self.ScoreCheck()

        if self.WinCheck() and self.won is False:
            self.Winner()
            self.won = True

        if self.won is False:
            if self.currentTurn is None:
                self.currentTurn = self.player1
            if self.playerSwap:
                self.playerSwap = False
                if self.currentTurn.GetPlayerID() == 1:
                    self.currentTurn = self.player2
                    self.turnText.ChangeText("Turn: Blacks")
                elif self.currentTurn.GetPlayerID() == 2:
                    self.currentTurn = self.player1
                    self.turnText.ChangeText("Turn: Whites")

            if not self.ValidMoveCheck(self.currentTurn.GetPlayerID()):
                self.playerSwap = True

        self.turnText.Update()
        self.whiteText.Update()
        self.blackText.Update()
        self.winner.Update()

    def WinCheck(self):
        check1 = False
        check2 = False
        for node in self.nodeList:
            if node.m_player == 0:
                check1 = True
                break

        if self.ValidMoveCheck(1) or self.ValidMoveCheck(2):
            check2 = True

        if check1 and check2:
            return False
        else:
            return True

    def Winner(self):
        size = self.renderer.get_size()
        if self.player1Score > self.player2Score:
            self.winner.ChangeText("White Wins!", (255, 0, 0))
        elif self.player1Score < self.player2Score:
            self.winner.ChangeText("Black Wins!", (255, 0, 0))
        else:
            self.winner.ChangeText("Draw!", (255, 0, 0))
        fontsize = self.winner.ReturnMinMax()
        self.winner.MoveText((size[0] / 2 - (fontsize[0] / 2), size[1] / 2 - (fontsize[1] / 2)))

    def ScoreCheck(self):
        p1score = 0
        p2score = 0
        for node in self.nodeList:
            if node.m_player == 1:
                p1score += 1
            elif node.m_player == 2:
                p2score += 1
        self.whiteText.ChangeText("White: " + str(p1score))
        self.blackText.ChangeText("Black: " + str(p2score))
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

    def ValidMoveCheck(self, playerid):
        valid_move = False
        nodes = []
        for node in self.nodeList:
            if node.m_player == 0:
                cords = (node.m_x, node.m_y)
                # Up Check
                nodes += self.LineCheck(cords, 'e', 'n', playerid)

                # Down Check
                nodes += self.LineCheck(cords, 'e', 'p', playerid)

                # Left Check
                nodes += self.LineCheck(cords, 'n', 'e', playerid)

                # Right Check
                nodes += self.LineCheck(cords, 'p', 'e', playerid)

                # Down and Right
                nodes += self.LineCheck(cords, 'p', 'p', playerid)

                # Up and Right
                nodes += self.LineCheck(cords, 'p', 'n', playerid)

                # Up and Left
                nodes += self.LineCheck(cords, 'n', 'n', playerid)

                # Down and Left
                nodes += self.LineCheck(cords, 'n', 'p', playerid)

        if len(nodes) >= 1:
            valid_move = True
            nodes = []

        return valid_move

    def MoveCheck(self, cords, playerid):
        valid_move = False
        nodes = []
        # Up Check
        nodes += self.LineCheck(cords, 'e', 'n', playerid)

        # Down Check
        nodes += self.LineCheck(cords, 'e', 'p', playerid)

        # Left Check
        nodes += self.LineCheck(cords, 'n', 'e', playerid)

        # Right Check
        nodes += self.LineCheck(cords, 'p', 'e', playerid)

        # Down and Right
        nodes += self.LineCheck(cords, 'p', 'p', playerid)

        # Up and Right
        nodes += self.LineCheck(cords, 'p', 'n', playerid)

        # Up and Left
        nodes += self.LineCheck(cords, 'n', 'n', playerid)

        # Down and Left
        nodes += self.LineCheck(cords, 'n', 'p', playerid)

        if len(nodes) >= 1:
            nodes.append(cords)
            self.ModChip(nodes, self.currentTurn.GetPlayerID())
            valid_move = True
            nodes = []

        return valid_move

    def LineCheck(self, cords, xpos, ypos, playerid):
        nodes = []
        newCords = cords
        while 1:
            if (xpos == 'p'):
                x = newCords[0] + 1
            elif (xpos == 'n'):
                x = newCords[0] - 1
            else:
                x = newCords[0]

            if (ypos == 'p'):
                y = newCords[1] + 1
            elif (ypos == 'n'):
                y = newCords[1] - 1
            else:
                y = newCords[1]

            newCords = (x, y)

            if newCords[0] < 0 or newCords[0] >= self.xsize or newCords[1] < 0 or newCords[1] >= self.ysize:
                del nodes[:]
                break
            elif self.GetSelectedNode(newCords).m_player == playerid:
                break
            elif self.GetSelectedNode(newCords).m_player == 0:
                del nodes[:]
                break
            else:
                nodes.append(newCords)
        return nodes

    def AttemptMove(self, cords, playerid):
        trueValid = False
        if (self.GetSelectedNode(cords).m_player == 0):
            valid = (self.MoveCheck(cords, playerid))
            if (valid):
                trueValid = True
        return trueValid

    def Event(self, event):
        if self.currentTurn.IsPlayer():
            if pygame.mouse.get_pressed()[0] == True:
                self = self.currentTurn.OnLeftClick(pygame.mouse.get_pos(), self,
                                                    pygame.display.get_surface().get_size())
            elif pygame.mouse.get_pressed()[2] == True:
                self = self.currentTurn.OnRightClick(pygame.mouse.get_pos(), self,
                                                     pygame.display.get_surface().get_size())

    def __init__(self, xsize=10, ysize=10):
        self.xsize = xsize
        self.ysize = ysize
        self.BuildNodes()
        location = ysize * int((xsize / 2)) + int((ysize / 2) - 1)
        self.nodeList[location].ChangePlayer(2)
        location = ysize * int(xsize / 2) + int(ysize / 2)
        self.nodeList[location].ChangePlayer(1)
        location = ysize * int((xsize / 2) - 1) + int((ysize / 2) - 1)
        self.nodeList[location].ChangePlayer(1)
        location = ysize * int((xsize / 2) - 1) + int(ysize / 2)
        self.nodeList[location].ChangePlayer(2)
        self.turnText = FontBox("Turn: Whites", 40, pygame.display.get_surface().get_size())
        self.whiteText = FontBox("White: 2", 40, pygame.display.get_surface().get_size())
        self.whiteText.MoveText((0, 50))
        self.blackText = FontBox("Black: 2", 40, pygame.display.get_surface().get_size())
        self.blackText.MoveText((0, 100))
        self.winner = FontBox("", 100, pygame.display.get_surface().get_size())
        self.winner.MakeMoveable(True)

    def __del__(self):
        del self.nodeList[:]
