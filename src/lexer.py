from abc import ABC, abstractmethod
from utils import CharacterIterator, Character
from termcolor import colored

# ====================================
# >>>>>>>>>> Classe Token <<<<<<<<<<<<
# ====================================

class Token:

    def __init__(self, tipo, lexema, linha=None, index=None):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.index = index

    def __str__(self):
        return f"<{self.tipo}, {self.lexema}, line {self.linha}>"
    
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
                if code.next() == '/':
                    code.next()
                    return Token("DIV_INT", "//")
                else:
                    return Token("DIV", "/")
            case '%':
                code.next()
                return Token("MOD", "%")
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

                    pos = code.getIndex()
                    if code.next() == '.' and code.next() == '.': 
                        code.setIndex(pos)
                        return Token("NUMBER", number)
                    else:
                        code.setIndex(pos)
                    
                    number += code.current()
                    if not Character.isDigit(code.next()):
                        return None
                    else:
                        number += self.readNumber(code)

                    if self.endNumber(code):

                        if code.current() == '.':
                            pos = code.getIndex()
                            if code.next() == '.' and code.next() == '.': 
                                code.setIndex(pos)
                                return Token("DOUBLE", number)
                            else:
                                code.setIndex(pos)
                                return None

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
                match code.current():
                    case '=':
                        if Character.isAllowedAfterRelational(code.next()):
                            return Token("EQUALS", "=")
                    case '<':
                        code.next()
                        if code.current() == '=':
                            if Character.isAllowedAfterRelational(code.next()):
                                return Token("LESS_EQUAL", "<=")
                            
                        if Character.isAllowedAfterRelational(code.current()):
                            return Token("LESS", "<")
                    case '>':
                        code.next()
                        if code.current() == '=':
                            if Character.isAllowedAfterRelational(code.next()):
                                return Token("GREATER_EQUAL", ">=")
                            
                        if Character.isAllowedAfterRelational(code.current()):
                            return Token("GREATER", ">")
                    case '!':
                        code.next()
                        if code.current() == '=':
                            if Character.isAllowedAfterRelational(code.next()):
                                return Token("DIFFERENT", "!=")
                    case _:
                        return None
                    
# ====================================
# >>>> Classe AssignmentOperator <<<<<
# ====================================
                    
class AssignmentOperator(AFD):
    
    def evaluate(self, code: CharacterIterator) -> Token:
        match code.current():
            case ':':
                code.next()
                return Token("ASSIGN", ":")
            case '+':
                code.next()
                if code.current() == ':':
                    code.next()
                    return Token("PLUS_ASSIGN", "+:")
            case '-':
                code.next()
                if code.current() == ':':
                    code.next()
                    return Token("MINUS_ASSIGN", "-:")
            case '*':
                code.next()
                if code.current() == ':':
                    code.next()
                    return Token("MULT_ASSIGN", "*:")
            case '/':
                code.next()
                if code.current() == ':':
                    code.next()
                    return Token("DIV_ASSIGN", "/:")
                elif code.current() == '/':
                    code.next()
                    if code.current() == ':':
                        code.next()
                        return Token("DIV_INT_ASSIGN", "//:")
            case '%':
                code.next()
                if code.current() == ':':
                    code.next()
                    return Token("MOD_ASSIGN", "%:")
            case '^':
                code.next()
                if code.current() == ':':
                    code.next()
                    return Token("POW_ASSIGN", "^:")
            case _:
                return None
            
# ====================================
# >>>>>>>>>>> Classe String <<<<<<<<<<
# ====================================
            
class String(AFD):
    
        def evaluate(self, code: CharacterIterator) -> Token:
            if code.current() == '"':
                code.next()
                string = self.readString(code)
                if code.current() == '"':
                    code.next()
                    return Token("STRING", f"\"{string}\"")
            return None
    
        def readString(self, code: CharacterIterator) -> str:
            string = ""
            while code.current() != '"':
                if code.current() == "\n":
                    return None

                string += code.current()
                code.next()
            return string
    
        def endString(self, code: CharacterIterator) -> bool:
            return Character.isAllowedAfterID(code.current())

# ====================================
# >>>>>>> Classe ReservedWords <<<<<<<
# ====================================

class ReservedWords(AFD):

    def evaluate(self, code: CharacterIterator) -> Token:
        self.reservedWords = ["se", "senao", "enquanto", "entao", "exiba", "entrada", "repita", "vezes", "de", "ate", "sendo", "funcao", "retorne", "passe", "passo"]

        text_to_evaluate = ""

        while code.current() != None and code.current() != ' ' and code.current() != '\n' and code.current() != '.' and code.current() != '(' and code.current() != ')' and code.current() != ',':
            text_to_evaluate += code.current()
            code.next()
        
        if text_to_evaluate in self.reservedWords:
            return Token(f"RESERVED_{text_to_evaluate.upper()}", text_to_evaluate)
        return None
    
class Boolean(AFD):

    def evaluate(self, code: CharacterIterator) -> Token:
        self.boolean = ["Verdadeiro", "Falso"]

        text_to_evaluate = ""

        while code.current() != None and code.current() != ' ' and code.current() != '\n' and code.current() != '.' and code.current() != '(' and code.current() != ')' and code.current() != ',':
            text_to_evaluate += code.current()
            code.next()
        
        if text_to_evaluate in self.boolean:
            return Token("BOOL", text_to_evaluate)
        return None

# ====================================
# >>>>>>>>> Classe Comma <<<<<<<<<<<
# ====================================

class Comma(AFD):
    
    def evaluate(self, code: CharacterIterator) -> Token:
        if code.current() == ',':
            code.next()
            return Token("COMMA", ",")
        return None
    
# ====================================
# >>>>>>> Classe LogicalOperator <<<<<
# ====================================
    
class LogicalOperator(AFD):
        
        def evaluate(self, code: CharacterIterator) -> Token:
            match code.current():
                case '&':
                    code.next()
                    return Token("AND", "&")
                case '|':
                    code.next()
                    return Token("OR", "|")
                case '!':
                    code.next()
                    return Token("NOT", "!")
                
# ====================================
# >>>>>>>>> Classe ScopeStart <<<<<<<<
# ====================================
                
class ScopeStart(AFD):

    def evaluate(self, code: CharacterIterator) -> Token:
        if code.current() == "." and code.next() == "." and code.next() == ".":
            code.next()
            return Token("SCOPE_START", "...")
        return None
    
# ====================================
# >>>>>>>>> Classe Bracket <<<<<<<<<<<
# ====================================

class Bracket(AFD):
    
        def evaluate(self, code: CharacterIterator) -> Token:
            match code.current():
                case '[':
                    code.next()
                    return Token("OPEN_BRACKET", "[")
                case ']':
                    code.next()
                    return Token("CLOSE_BRACKET", "]")
                case _:
                    return None
            
# ====================================
# >>>>>>>>>> Classe Lexer <<<<<<<<<<<
# ====================================

class Lexer:

    def __init__(self, code):
        self.tokens = []
        self.afds = [ReservedWords(),
                     Boolean(),
                     String(),
                     AssignmentOperator(),
                     ScopeStart(),
                     MathOperator(),
                     Number(),
                     Parentheses(),
                     Bracket(),
                     ID(),
                     RelationalOperator(),
                     Comma(),
                     LogicalOperator()]
        self.code = CharacterIterator(code)
        self.ident = 0

    def skipComment(self):

        found = False
        pos = self.code.getIndex()
        if self.code.current() == '-' and self.code.next() == '=' and self.code.next() == '|':
            found = True
            while self.code.current() != None and self.code.current() != '\n':               
                self.code.next()
            
        else:
            self.code.setIndex(pos)

        return found

    def verifyIdent(self):

        self.code.next()
        space_count = 0

        while self.code.current() == ' ' or self.code.current() == '\t':

            if self.code.current() == '\t':
                space_count += 4
            else:
                space_count += 1

            self.code.next()

        self.code.previous()

        ident_level = space_count // 4

        if ident_level > self.ident:
            difference = ident_level - self.ident
            for _ in range(difference):
                self.tokens.append(Token("INDENT", None, self.code.getLineNumber(), self.code.getIndex()))

            self.ident = ident_level

        elif ident_level < self.ident:    
            difference = self.ident - ident_level
            for _ in range(difference):
                self.tokens.append(Token("DEDENT", None, self.code.getLineNumber(), self.code.getIndex()))

            self.ident = ident_level

    def skipWhitespace(self):

        found = False
        while self.code.current() == ' ' or self.code.current() == '\n':

            found = True

            if self.code.current() == '\n':
                self.verifyIdent()
            
            self.code.next()

        return found


    def getTokens(self) -> list:

        while (self.code.current() != None):

            accepted = False
            
            while self.skipWhitespace() or self.skipComment():
                pass

            if (self.code.current() == None):
                break

            for afd in self.afds:
                pos = self.code.getIndex()
                token = afd.evaluate(self.code)
                if token != None:
                    token.linha = self.code.getLineNumber()
                    token.index = pos
                    self.tokens.append(token)
                    accepted = True
                    break
                else:
                    self.code.setIndex(pos)

            if not accepted:
                self.logError()
                return None
        
        self.verifyIdent()
        self.tokens.append(Token("EOF", "$", self.code.getLineNumber(), self.code.getIndex()))
        return self.tokens
    
    def logError(self):
        
        lineInfo = self.code.getErrorInfo()
        print(f"Erro Léxico: Token '{lineInfo['unexpectedToken']}' não identificado na linha {lineInfo['lineNumber']}:")
        print(lineInfo["fullLine"][0:lineInfo["errorStart"]] + colored(lineInfo['unexpectedToken'], 'red') + lineInfo["fullLine"][lineInfo["errorEnd"] + 1:])