from utils import TokenIterator

# ========================================
# >>>>>>>>>>> Classe Rules <<<<<<<<<<<<<<<
# ========================================

class Rules:

    def __init__(self, tokens):
        self.tokens = tokens
        self.token = tokens.pop(0)

    def nextToken(self):
        self.token = self.tokens.pop(0)
        
    def prog(self):
        if Rules.bloco(self):
            if self.token.tipo == "EOF":
                return True
        return False
    
    def bloco(self):
        if Rules.cmd(self):
            if Rules.bloco(self):
                return True
            return True
        return False
    
    def cmd(self):
        if Rules.cmdIf(self):
            return True
        return False
    
    def cmdIf(self):
        if self.token.tipo == "RESERVED_SE":
            self.nextToken()
            if self.token.tipo == "RESERVED_ENTAO":
                self.nextToken()
                return True
            return False
        return False

# ========================================
# >>>>>>>>>>> Classe Parser <<<<<<<<<<<<<
# ========================================

class Parser:

    def __init__(self, tokens):
        self.rules = Rules(tokens)

    def parse(self):
        return self.rules.prog()