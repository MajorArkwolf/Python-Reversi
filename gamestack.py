class GameStack:
    gamestack = []
    stackSize = 0

    def Event(self, event):
        self.gamestack[self.stackSize - 1].Event(event)


    def AddToStack(self, newItem):
        self.gamestack.append(newItem)
        self.stackSize += 1

    def Draw(self):
        if self.stackSize > 0:
            self.gamestack[self.stackSize - 1].Draw()

    def Update(self):
        if self.stackSize > 0:
            self.gamestack[self.stackSize - 1].Update()

    def PopToStack(self):
        self.gamestack.pop()
        self.stackSize -= 1
    
    def EmptyStack(self):
        if(self.stackSize <= 0):
            return True
        else:
            return False

    def GetItem(self):
        return self.gamestack[self.stackSize -1]

    def __init__(self, item = None):
        if (item != None):
            self.gamestack.append(item)
            self.stackSize += 1
        else:
            self.gamestack = []