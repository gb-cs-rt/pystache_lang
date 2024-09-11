from abc import ABC, abstractmethod
from utils import CharacterIterator, Character
from termcolor import colored

# ====================================
# >>>>>>>>>> Classe Token <<<<<<<<<<<<
# ====================================

class Token:

    def __init__(self, tipo, lexema):
        self.tipo = tipo
        self.lexema = lexema

    def __str__(self):
        return f"< {self.tipo}, {self.lexema} >"
    
    def __repr__(self) -> str:
        return self.__str__()

# ====================================
# >>>>>>>>>> Classe AFD <<<<<<<<<<<<<<
# ====================================

class AFD(ABC):

    @abstractmethod
    def evaluate(self, code: CharacterIterator) -> Token:
        pass

# ====================================
# >>>>>>> Classe MathOperator <<<<<<<<
# ====================================

class MathOperator(AFD):

    def evaluate(self, code: CharacterIterator) -> Token:
        match code.current():
            case '+':
                code.next()
                return Token("PLUS", "+")
            case '-':
                code.next()
                return Token("MINUS", "-")
            case '*':
                code.next()
                return Token("MULT", "*")
            case '^':
                code.next()
                return Token("POW", "^")
            case '/':
                code.next()
                return Token("DIV", "/")
            case _:
                return None
            
# ====================================
# >>>>>>>>> Classe Number <<<<<<<<<<<
# ====================================
            
class Number(AFD):

    def evaluate(self, code: CharacterIterator) -> Token:
        if Character.isDigit(code.current()) or code.current() == '.':
            number = self.readNumber(code)

            if self.endNumber(code):

                if code.current() == '.':
                    
                    number += code.current()
                    if not Character.isDigit(code.next()):
                        return None
                    else:
                        number += self.readNumber(code)

                    if self.endNumber(code):
                        return Token("DOUBLE", number)

                return Token("NUMBER", number)
        return None

    def readNumber(self, code: CharacterIterator) -> str:
        number = ""
        while Character.isDigit(code.current()):
            number += code.current()
            code.next()
        return number
    
    def endNumber(self, code: CharacterIterator) -> bool:
        return Character.isAllowedAfterNumber(code.current())

# ====================================
# >>>>>>>>> Classe Parentheses <<<<<<<
# ====================================

class Parentheses(AFD):
    
        def evaluate(self, code: CharacterIterator) -> Token:
            match code.current():
                case '(':
                    code.next()
                    return Token("OPEN_PARENTHESIS", "(")
                case ')':
                    code.next()
                    return Token("CLOSE_PARENTHESIS", ")")
                case _:
                    return None

# ====================================
# >>>>>>>>>>> Classe ID <<<<<<<<<<<<<<
# ====================================

class ID(AFD):

    def evaluate(self, code: CharacterIterator) -> Token:
        
        if Character.isAllowedInID(code.current()) and not Character.isDigit(code.current()):
            id = self.readID(code)
            if self.endID(code):
                return Token("ID", id)
            return None
        
        return None
    
    def readID(self, code: CharacterIterator) -> str:
        id = ""
        while Character.isAllowedInID(code.current()):
            id += code.current()
            code.next()
        return id
    
    def endID(self, code: CharacterIterator) -> bool:
        return Character.isAllowedAfterID(code.current())
        
# ====================================
# >>>> Classe RelationalOperator <<<<<
# ====================================
        
class RelationalOperator(AFD):
        
            def evaluate(self, code: CharacterIterator) -> Token:
                if code.current() == '=':
                    if code.next() == '=':
                        if Character.isAllowedAfterEqual(code.next()):
                            return Token("EQUALS", "==")
                        return None
                    else:
                        if Character.isAllowedAfterEqual(code.current()):
                            return Token("ASSIGN", "=")
                    
                return None
            
# ====================================
# >>>>>>>>>> Classe Lexer <<<<<<<<<<<
# ====================================

class Lexer:

    def __init__(self, code):
        self.tokens = []
        self.afds = [MathOperator(),
                     Number(),
                     Parentheses(),
                     ID(),
                     RelationalOperator()]
        self.code = CharacterIterator(code)
        self.line = 1

    def skipWhitespace(self):
        while self.code.current() == ' ' or self.code.current() == '\n':
            self.code.next()

    def getTokens(self) -> list:

        while (self.code.current() != None):

            accepted = False
            self.skipWhitespace()

            if (self.code.current() == None):
                break

            for afd in self.afds:
                pos = self.code.getIndex()
                token = afd.evaluate(self.code)
                if token != None:
                    self.tokens.append(token)
                    accepted = True
                    break
                else:
                    self.code.setIndex(pos)

            if not accepted:
                self.logError()
                return None
        
        self.tokens.append(Token("EOF", "$"))
        return self.tokens
    
    def logError(self):
        
        lineInfo = self.code.getLineInfo()
        print(f"Error: Unexpected character '{self.code.current()}' at line {lineInfo['lineNumber']}:")
        print(lineInfo["lineString"][0:lineInfo["column"]] + colored(self.code.current(), 'red') + lineInfo["lineString"][lineInfo["column"] + 1:] + "\n")