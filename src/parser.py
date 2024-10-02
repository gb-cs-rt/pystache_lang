from utils import TokenIterator

# ========================================
# >>>>>>>>>>> Classe Rules <<<<<<<<<<<<<<<
# ========================================

class Rules:

    def __init__(self, tokens):
        self.tokens = tokens
        self.token = tokens.pop(0)

    def nextToken(self):
        if len(self.tokens) > 0:
            self.token = self.tokens.pop(0)
        else:
            print("Fim do arquivo.")

    def matchLexema(self, lexema):
        self.nextToken()
        return True if self.token.lexema == lexema else False

    def matchTipo(self, tipo):
        if self.token.tipo == tipo:
            self.nextToken()
            return True
        return False

    def firstFollow(self, tipo):
        return True if self.token.tipo == tipo else False

    def eof(self):
        return True if self.token.tipo == "EOF" else False

    def error(self, rule):
        print(f"Erro na regra {rule}")
        exit()

    # ============== REGRAS ==================
        
    def prog(self):
        return True if self.bloco() and self.eof() else self.error("prog")
    
    def bloco(self):
        if self.cmd():
            return True if self.eof() or self.bloco() else self.error("bloco")
    
    def cmd(self):
        if self.firstFollow("RESERVED_SE"):
            return self.cmdIf()
        
        return self.error("cmd")
    
    def cmdIf(self):
        return True if self.matchTipo("RESERVED_SE") and self.matchTipo("RESERVED_ENTAO") else self.error("cmdIf")

# ========================================
# >>>>>>>>>>> Classe Parser <<<<<<<<<<<<<
# ========================================

class Parser:

    def __init__(self, tokens):
        self.rules = Rules(tokens)

    def parse(self):
        return self.rules.prog()