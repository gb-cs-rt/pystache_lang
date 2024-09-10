from abc import ABC, abstractmethod
from utils import CharacterIterator, Character

class Token:

    def __init__(self, tipo, lexema):
        self.tipo = tipo
        self.lexema = lexema

    def __str__(self):
        return f"< {self.tipo}, {self.lexema} >"
    
    def __repr__(self) -> str:
        return self.__str__()
    
class AFD(ABC):

    @abstractmethod
    def evaluate(self, code: CharacterIterator) -> Token:
        pass

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
            
class Number(AFD):

    def evaluate(self, code: CharacterIterator) -> Token:
        if Character.isDigit(code.current()):
            number = self.readNumber(code)
            
            if self.endNumber(code):
                return Token("NUMBER", number)
        return None

    def readNumber(self, code: CharacterIterator) -> str:
        number = ""
        while Character.isDigit(code.current()):
            number += code.current()
            code.next()
        return number
    
    def endNumber(self, code: CharacterIterator) -> bool:
        return code.current() == None or not Character.isDigit(code.current())
            
class Lexer:

    def __init__(self, code):
        self.tokens = []
        self.afds = [MathOperator(), Number()]
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
            print(f"Error: Unexpected character '{self.code.current()}' at line {self.code.getLine()[0]}:")
            print(self.code.getLine()[1])
            print(" " * self.code.getColumn() + "^")