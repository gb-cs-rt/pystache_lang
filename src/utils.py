class CharacterIterator:

    def __init__(self, string):
        self.string = string
        self.index = 0

    def current(self):
        if self.index < len(self.string) and self.index >= 0:
            return self.string[self.index]
        return None
    
    def next(self):
        if self.index < len(self.string):
            self.index += 1
        return self.current()
    
    def previous(self):
        if self.index >= 0:
            self.index -= 1
        return self.current()
        
    def getIndex(self):
        return self.index
    
    def setIndex(self, index):
        self.index = index

    def getLine(self):
        lines = self.string[:self.index].split("\n")
        full_line = lines[-1] + self.string[self.index:].split("\n")[0]

        return (len(lines), full_line)
    
    def getColumn(self):
        lines = self.string[:self.index].split("\n")
        return len(lines[-1])

class Character:

    @staticmethod
    def isDigit(char):
        if type(char) == str:
            return char.isdigit()
        return False