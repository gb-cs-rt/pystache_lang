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

    def getErrorInfo(self):

        line_start = self.string.rfind("\n", 0, self.index) + 1
        errorStart = self.index

        unexpectedToken = ""
        while self.current() != None and self.current() != ' ' and self.current() != '\n':
            unexpectedToken += self.current()
            self.next()

        line_end = self.string.find("\n", self.index)
        errorEnd = self.index - 1
        full_line = self.string[line_start: line_end if line_end != -1 else None]
        
        return {
            'lineNumber': self.string.count("\n", 0, self.index) + 1,
            'fullLine': full_line,
            'errorStart': errorStart - line_start,
            'errorEnd': errorEnd - line_start,
            'unexpectedToken': unexpectedToken
        }


class Character:

    @staticmethod
    def isDigit(char):
        if type(char) == str:
            return char.isdigit()
        return False
    
    @staticmethod
    def isAlpha(char):
        if type(char) == str:
            return char.isalpha()
        return False

    @staticmethod
    def isAllowedInID(char):
        if type(char) == str:
            return (char.isalpha()) or (char == "_") or (char.isdigit())
        return False
    
    @staticmethod
    def isAllowedAfterID(char):
        return char in [' ', '\n', '(', ')', '+', '-', '*', '/', '^', '=', '<', '>', '!', ':', ',', None]
    
    @staticmethod
    def isAllowedAfterNumber(char):
        return char in [' ', '\n', '(', ')', '+', '-', '*', '/', '^', '.', None, '=', '<', '>', '!', '&', '|', ',']
    
    @staticmethod
    def isAllowedAfterRelational(char):
        return char in [' ', '\n', '(', ')', '+', '-', '*', '/', '^', None] or Character.isDigit(char) or Character.isAlpha(char)