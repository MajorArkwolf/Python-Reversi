class Node:

    m_x = 0
    m_y = 0
    m_player = 0

    def __init__(self, x = 0, y = 0, player = 0):
        self.m_x = x
        self.m_y = y
        self.m_player = player

    def ChangePlayer(self, playerid):
        self.m_player = playerid