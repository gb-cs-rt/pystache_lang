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

    def getLineInfo(self):

        line_start = self.string.rfind("\n", 0, self.index) + 1
        line_end = self.string.find("\n", self.index)
        full_line = self.string[line_start: line_end if line_end != -1 else None]
        
        return {
            'lineNumber': self.string.count("\n", 0, self.index) + 1,
            'column': self.index - line_start,
            'lineString': full_line
        }


class Character:

    @staticmethod
    def isDigit(char):
        if type(char) == str:
            return char.isdigit()
        return False

    @staticmethod
    def isID(char):
        if type(char) == str:
            return char.isalpha() or char == "_" or char.isdigit()
        return False