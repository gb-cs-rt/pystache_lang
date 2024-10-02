# ========================================
# >>>>>>>>>>> Classe Rules <<<<<<<<<<<<<<<
# ========================================

class Rules:

    def __init__(self, parser):
        self.parser = parser

        self.nextToken = parser.nextToken
        self.matchLexema = parser.matchLexema
        self.matchTipo = parser.matchTipo
        self.firstFollow = parser.firstFollow
        self.eof = parser.eof
        self.error = parser.error
        self.endBlock = parser.endBlock

    # ============== REGRAS ==================
        
    def prog(self):
        # prog -> bloco
        print("-> prog")
        return True if self.bloco() and self.eof() else self.error("prog")
    
    def bloco(self):
        # bloco -> cmd bloco | ε
        print("-> bloco")
        if self.cmd():
            return True if self.eof() or self.endBlock() or self.bloco() else self.error("bloco")
    
    def cmd(self):
        # cmd -> cmdIf
        print("-> cmd")
        # print(self.parser.token)
        if self.firstFollow("RESERVED_SE"):
            return self.cmdIf()
        if self.firstFollow("RESERVED_PASSE"):
            return self.matchTipo("RESERVED_PASSE")
        
        return self.error("cmd")
    
    def cmdIf(self):
        # cmdIf -> RESERVED_SE condicao RESERVED_ENTAO INDENT bloco DEDENT cmdElse
        print("-> cmdIf")
        return True if self.matchTipo("RESERVED_SE") and self.condicao() and self.matchTipo("RESERVED_ENTAO") and self.matchTipo("INDENT") and self.bloco() and self.matchTipo("DEDENT") and self.cmdElse() else self.error("cmdIf")
    
    def cmdElse(self):
        # cmdElse -> RESERVED_SENAO INDENT bloco DEDENT | ε
        print("-> cmdElse")
        if self.matchTipo("RESERVED_SENAO"):
            return True if self.matchTipo("INDENT") and self.bloco() and self.matchTipo("DEDENT") else self.error("cmdElse")
        return True
    
    def condicao(self):
        # condicao -> relacao opLogico relacao | relacao
        print("-> condicao")
        if self.relacao():
            if self.firstFollow("AND") or self.firstFollow("OR"):
                return True if self.opLogico() and self.relacao() else self.error("condicao")
            return True
        
    def relacao(self):
        # relacao -> expressao opRelacional expressao | expressao
        print("-> relacao")
        if self.expressao():
            if self.firstFollow("GREATER") or self.firstFollow("LESS") or self.firstFollow("EQUALS") or self.firstFollow("DIFFERENT") or self.firstFollow("GREATER_EQUAL") or self.firstFollow("LESS_EQUAL"):
                return True if self.opRelacional() and self.expressao() else self.error("relacao")
            return True
        
    def opRelacional(self):
        # opRelacional -> GREATER | LESS | EQUALS | DIFFERENT | GREATER_EQUAL | LESS_EQUAL
        print("-> opRelacional")
        return True if self.matchTipo("GREATER") or self.matchTipo("LESS") or self.matchTipo("EQUALS") or self.matchTipo("DIFFERENT") or self.matchTipo("GREATER_EQUAL") or self.matchTipo("LESS_EQUAL") else self.error("opRelacional")
    
    def opLogico(self):
        # opLogico -> AND | OR
        print("-> opLogico")
        return True if self.matchTipo("AND") or self.matchTipo("OR") else self.error("opLogico")
    
    def expressao(self):
        # expressao -> termo opAd termo | termo
        print("-> expressao")
        if self.termo():
            if self.firstFollow("PLUS") or self.firstFollow("MINUS"):
                return True if self.opAd() and self.termo() else self.error("expressao")
            return True
        
    def opAd(self):
        # opAd -> PLUS | MINUS
        print("-> opAd")
        return True if self.matchTipo("PLUS") or self.matchTipo("MINUS") else self.error("opAd")
    
    def termo(self):
        # termo -> fator opMul fator | fator
        print("-> termo")
        if self.fator():
            if self.firstFollow("MULT") or self.firstFollow("DIV"):
                return True if self.opMul() and self.fator() else self.error("termo")
            return True
        
    def opMul(self):
        # opMul -> MULT | DIV
        print("-> opMul")
        return True if self.matchTipo("MULT") or self.matchTipo("DIV") else self.error("opMul")
    
    def fator(self):
        # fator -> NUM | DOUBLE | ID | OPEN_PARENTHESIS expressao CLOSE_PARENTHESIS
        print("-> fator")
        if self.matchTipo("NUM") or self.matchTipo("DOUBLE") or self.matchTipo("ID"):
            return True
        elif self.matchTipo("OPEN_PARENTHESIS"):
            return True if self.expressao() and self.matchTipo("CLOSE_PARENTHESIS") else self.error("fator")
        
        return self.error("fator")

# ========================================
# >>>>>>>>>>> Classe Parser <<<<<<<<<<<<<
# ========================================

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.token = tokens.pop(0)
        self.rules = Rules(self)  # Pass the Parser instance to Rules

    def nextToken(self):
        if len(self.tokens) > 0:
            self.token = self.tokens.pop(0)
        else:
            print("Fim do arquivo.")

    def matchLexema(self, lexema):
        if self.token.lexema == lexema:
            self.nextToken()
            return True
        return False

    def matchTipo(self, tipo):
        if self.token.tipo == tipo:
            print(f"-- match --> {self.token}")
            self.nextToken()
            return True
        return False

    def firstFollow(self, tipo):
        return self.token.tipo == tipo

    def eof(self):
        return self.token.tipo == "EOF"

    def error(self, rule):
        print(f"Erro na regra {rule}")

    def endBlock(self):
        return self.token.tipo == "DEDENT"

    def parse(self):
        return self.rules.prog()