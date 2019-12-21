class GameStack:
    game_stack = []
    stackSize = 0

    def Event(self, event):
        if self.stackSize > 0:
            self.game_stack[self.stackSize - 1].Event(event)

    def AddToStack(self, new_item):
        self.game_stack.append(new_item)
        self.stackSize += 1

    def Draw(self):
        if self.stackSize > 0:
            self.game_stack[self.stackSize - 1].Draw()

    def Update(self):
        if self.stackSize > 0:
            self.game_stack[self.stackSize - 1].Update()

    def PopToStack(self):
        del self.game_stack[self.stackSize - 1]
        self.stackSize -= 1

    def EmptyStack(self):
        if self.stackSize <= 0:
            return True
        else:
            return False

    def GetItem(self):
        return self.game_stack[self.stackSize - 1]

    def __init__(self, item=None):
        if item != None:
            self.game_stack.append(item)
            self.stackSize += 1
        else:
            self.game_stack = []
