from utils import Tree, CharacterIterator
from termcolor import colored

# ========================================
# >>>>>>>>>>> Classe Rules <<<<<<<<<<<<<<<
# ========================================

class Rules:
    def __init__(self, parser):
        self.parser = parser
        self.tree = parser.tree
        self.nextToken = parser.nextToken
        self.matchLexema = parser.matchLexema
        self.matchTipo = parser.matchTipo
        self.firstFollow = parser.firstFollow
        self.checkNext = parser.checkNext
        self.eof = parser.eof
        self.error = parser.error
        self.endBlock = parser.endBlock
        self.addNode = parser.addNode
        self.setRoot = parser.setRoot

    # ============== REGRAS ==================

    def prog(self):
        # prog -> bloco
        node = self.setRoot()
        return True if self.bloco(node) and self.eof() else self.error(node)

    def bloco(self, parent_node):
        # bloco -> cmd bloco | ε
        node = self.addNode("bloco", parent_node)
        if self.cmd(node):
            return True if self.eof() or self.endBlock() or self.bloco(node) else self.error(node)

    def cmd(self, parent_node):
        # cmd -> cmdIf
        node = self.addNode("cmd", parent_node)
        if self.firstFollow("RESERVED_SE"): return self.cmdIf(node)
        if self.firstFollow("RESERVED_PASSE"): return self.matchTipo("RESERVED_PASSE", node) 
        if self.firstFollow("RESERVED_PARE"): return self.matchTipo("RESERVED_PARE", node)
        if self.firstFollow("ID"): return self.cmdID(node)
        if self.firstFollow("RESERVED_REPITA"): return self.cmdFor(node)
        if self.firstFollow("RESERVED_ENQUANTO"): return self.cmdWhile(node)
        if self.firstFollow("RESERVED_RETORNE"): return self.cmdReturn(node)
        if self.firstFollow("RESERVED_FUNCAO"): return self.cmdDefFunc(node)
        if self.firstFollow("RESERVED_EXIBA"): return self.cmdPrint(node)
        if self.firstFollow("RESERVED_ENTRADA"): return self.cmdInput(node)
        return self.error(node)
    
    def acessoListaOp(self, parent_node):
        # acessoListaOp -> acessoLista acessoListaOp | ε
        node = self.addNode("acessoListaOp", parent_node)
        if self.firstFollow("OPEN_BRACKET"):
            return True if self.acessoLista(node) and self.acessoListaOp(node) else self.error(node)
        return True

    def cmdID(self, parent_node):
        # cmdID -> ID acessoListaOp complemento
        node = self.addNode("cmdID", parent_node)
        return True if self.matchTipo("ID", node) and self.acessoListaOp(node) and self.complemento(node) else self.error(node)

    def cmdIf(self, parent_node):
        # cmdIf -> RESERVED_SE valor RESERVED_ENTAO INDENT bloco DEDENT cmdElse
        node = self.addNode("cmdIf", parent_node)
        return True if self.matchTipo("RESERVED_SE", node) and self.valor(node) and self.matchTipo("RESERVED_ENTAO", node) and self.matchTipo("INDENT", node) and self.bloco(node) and self.matchTipo("DEDENT", node) and self.cmdElse(node) else self.error(node)

    def cmdElse(self, parent_node):
        # cmdElse -> RESERVED_SENAO INDENT bloco DEDENT | ε
        node = self.addNode("cmdElse", parent_node)
        if self.matchTipo("RESERVED_SENAO", node):
            return True if self.matchTipo("INDENT", node) and self.bloco(node) and self.matchTipo("DEDENT", node) else self.error(node)
        return True

    def complemento(self, parent_node):
        # complemento -> cmdAtrib | composicao
        node = self.addNode("complemento", parent_node)
        if self.firstFollow("OPEN_PARENTHESIS") or self.firstFollow("OPEN_BRACKET"):
            return True if self.composicao(node) else self.error(node)
        return True if self.cmdAtrib(node) else self.error(node)

    def valor(self, parent_node):
        # valor -> expressaoLogica | lista | cmdPrint | cmdInput
        node = self.addNode("valor", parent_node)
        if self.firstFollow("OPEN_BRACKET"):
            return True if self.lista(node) else self.error(node)
        if self.firstFollow("RESERVED_EXIBA"):
            return True if self.cmdPrint(node) else self.error(node)
        if self.firstFollow("RESERVED_ENTRADA"):
            return True if self.cmdInput(node) else self.error(node)
        return True if self.expressaoLogica(node) else self.error(node)
    
    def expressaoLogica(self, parent_node):
        # expressaoLogica -> expressaoRelacional (opLogico expressaoRelacional)*
        node = self.addNode("expressaoLogica", parent_node)
        if self.expressaoRelacional(node):
            while self.firstFollow("AND") or self.firstFollow("OR"):
                if not (self.opLogico(node) and self.expressaoRelacional(node)):
                    return self.error(node)
            return True
        return self.error(node)
    
    def expressaoRelacional(self, parent_node):
        # expressaoRelacional -> expressaoAritmetica (opRelacional expressaoAritmetica)*
        node = self.addNode("expressaoRelacional", parent_node)
        if self.expressaoAritmetica(node):
            while self.firstFollow("GREATER") or self.firstFollow("LESS") or self.firstFollow("EQUALS") or self.firstFollow("DIFFERENT") or self.firstFollow("GREATER_EQUAL") or self.firstFollow("LESS_EQUAL"):
                if not (self.opRelacional(node) and self.expressaoAritmetica(node)):
                    return self.error(node)
            return True
        return self.error(node)
    
    def expressaoAritmetica(self, parent_node):
        # expressaoAritmetica -> termo (opAd termo)*
        node = self.addNode("expressaoAritmetica", parent_node)
        if self.termo(node):
            while self.firstFollow("PLUS") or self.firstFollow("MINUS"):
                if not (self.opAd(node) and self.termo(node)):
                    return self.error(node)
            return True
        return self.error(node)

    def opRelacional(self, parent_node):
        # opRelacional -> GREATER | LESS | EQUALS | DIFFERENT | GREATER_EQUAL | LESS_EQUAL
        node = self.addNode("opRelacional", parent_node)
        return True if self.matchTipo("GREATER", node) or self.matchTipo("LESS", node) or self.matchTipo("EQUALS", node) or self.matchTipo("DIFFERENT", node) or self.matchTipo("GREATER_EQUAL", node) or self.matchTipo("LESS_EQUAL", node) else self.error(node)

    def opLogico(self, parent_node):
        # opLogico -> AND | OR
        node = self.addNode("opLogico", parent_node)
        return True if self.matchTipo("AND", node) or self.matchTipo("OR", node) else self.error(node)
    
    def opAd(self, parent_node):
        # opAd -> PLUS | MINUS
        node = self.addNode("opAd", parent_node)
        return True if self.matchTipo("PLUS", node) or self.matchTipo("MINUS", node) else self.error(node)

    def termo(self, parent_node):
        # termo -> fator (opMul fator)*
        node = self.addNode("termo", parent_node)
        if self.fator(node):
            while self.firstFollow("MULT") or self.firstFollow("DIV") or self.firstFollow("DIV_INT") or self.firstFollow("MOD"):
                if not (self.opMul(node) and self.fator(node)):
                    return self.error(node)
            return True
        return self.error(node)

    def opMul(self, parent_node):
        # opMul -> MULT | DIV | DIV_INT | MOD
        node = self.addNode("opMul", parent_node)
        return True if self.matchTipo("MULT", node) or self.matchTipo("DIV", node) or self.matchTipo("DIV_INT", node) or self.matchTipo("MOD", node) else self.error(node)
    
    def fator(self, parent_node):
        # fator -> elemento (opPow elemento)*
        node = self.addNode("fator", parent_node)
        if self.elemento(node):
            while self.firstFollow("POW"):
                if not (self.opPow(node) and self.elemento(node)):
                    return self.error(node)
            return True
        return self.error(node)

    def elemento(self, parent_node):
        # elemento -> NUM | DOUBLE | ID X | OPEN_PARENTHESIS expressaoLogica CLOSE_PARENTHESIS | STRING | BOOL
        node = self.addNode("elemento", parent_node)
        if self.matchTipo("ID", node) and self.X(node):
            return True
        elif self.matchTipo("NUMBER", node) or self.matchTipo("DOUBLE", node) or self.matchTipo("STRING", node) or self.matchTipo("BOOL", node):
            return True
        elif self.matchTipo("OPEN_PARENTHESIS", node):
            return True if self.expressaoLogica(node) and self.matchTipo("CLOSE_PARENTHESIS", node) else self.error(node)
        return self.error(node)

    def X(self, parent_node):
        # X -> composicao | ε
        node = self.addNode("X", parent_node)
        if self.firstFollow("OPEN_BRACKET") or self.firstFollow("OPEN_PARENTHESIS"):
            return True if self.composicao(node) else self.error(node)
        return True

    def composicao(self, parent_node):
        # composicao -> acessoLista acessoListaOp | chamadaFuncao
        node = self.addNode("composicao", parent_node)
        if self.firstFollow("OPEN_BRACKET"):
            return True if self.acessoLista(node) and self.acessoListaOp(node) else self.error(node)
        if self.firstFollow("OPEN_PARENTHESIS"):
            return True if self.chamadaFuncao(node) else self.error(node)
        return True

    def chamadaFuncao(self, parent_node):
        # chamadaFuncao -> OPEN_PARENTHESIS corpoLista CLOSE_PARENTHESIS
        node = self.addNode("chamadaFuncao", parent_node)
        return True if self.matchTipo("OPEN_PARENTHESIS", node) and self.corpoLista(node) and self.matchTipo("CLOSE_PARENTHESIS", node) else self.error(node)

    def lista(self, parent_node):
        # lista -> OPEN_BRACKET corpoLista CLOSE_BRACKET
        node = self.addNode("lista", parent_node)
        return True if self.matchTipo("OPEN_BRACKET", node) and self.corpoLista(node) and self.matchTipo("CLOSE_BRACKET", node) else self.error(node)

    def corpoLista(self, parent_node):
        # corpoLista -> valor entradaLista | ε
        node = self.addNode("corpoLista", parent_node)
        if self.firstFollow("CLOSE_BRACKET") or self.firstFollow("CLOSE_PARENTHESIS"):
            return True
        return True if self.valor(node) and self.entradaLista(node) else self.error(node)

    def entradaLista(self, parent_node):
        # entradaLista -> COMMA valor entradaLista | ε
        node = self.addNode("entradaLista", parent_node)
        if self.matchTipo("COMMA", node):
            return True if self.valor(node) and self.entradaLista(node) else self.error(node)
        return True
    
    def cmdAtrib(self, parent_node):
        # cmdAtrib -> atribComum | atribComOp
        node = self.addNode("cmdAtrib", parent_node)
        if self.firstFollow("ASSIGN"):
            return True if self.atribComum(node) else self.error(node)
        return True if self.atribComOp(node) else self.error(node)
    
    def atribComum(self, parent_node):
        # atribComum -> ASSIGN valor
        node = self.addNode("atribComum", parent_node)
        return True if self.matchTipo("ASSIGN", node) and self.valor(node) else self.error(node)
    
    def atribComOp(self, parent_node):
        # atribComOp -> assignOp valor
        node = self.addNode("atribComOp", parent_node)
        return True if self.assignOp(node) and self.valor(node) else self.error(node)
    
    def assignOp(self, parent_node):
        # assignOp -> PLUS_ASSIGN | MINUS_ASSIGN | MULT_ASSIGN | DIV_ASSIGN | DIV_INT_ASSIGN | MOD_ASSIGN | POW_ASSIGN
        node = self.addNode("assignOp", parent_node)
        return True if self.matchTipo("PLUS_ASSIGN", node) or self.matchTipo("MINUS_ASSIGN", node) or self.matchTipo("MULT_ASSIGN", node) or self.matchTipo("DIV_ASSIGN", node) or self.matchTipo("DIV_INT_ASSIGN", node) or self.matchTipo("MOD_ASSIGN", node) or self.matchTipo("POW_ASSIGN", node) else self.error(node)
    
    def cmdFor(self, parent_node):
        # cmdFor -> RESERVED_REPITA variavelFor INDENT bloco DEDENT
        node = self.addNode("cmdFor", parent_node)
        return True if self.matchTipo("RESERVED_REPITA", node) and self.variavelFor(node) and self.matchTipo("INDENT", node) and self.bloco(node) and self.matchTipo("DEDENT", node) else self.error(node)
    
    def variavelFor(self, parent_node):
        # variavelFor -> forVezes | forIntervalo | forSendo
        node = self.addNode("variavelFor", parent_node)
        if self.firstFollow("RESERVED_DE"):
            return True if self.forIntervalo(node) else self.error(node)
        if self.firstFollow("RESERVED_SENDO"):
            return True if self.forSendo(node) else self.error(node)
        return True if self.forVezes(node) else self.error(node)
    
    def forVezes(self, parent_node):
        # forVezes -> expressaoAritmetica RESERVED_VEZES
        node = self.addNode("forVezes", parent_node)
        return True if self.expressaoAritmetica(node) and self.matchTipo("RESERVED_VEZES", node) else self.error(node)
    
    def forIntervalo(self, parent_node):
        # forIntervalo -> RESERVED_DE expressaoAritmetica RESERVED_ATE expressaoAritmetica passoFor
        node = self.addNode("forIntervalo", parent_node)
        return True if self.matchTipo("RESERVED_DE", node) and self.expressaoAritmetica(node) and self.matchTipo("RESERVED_ATE", node) and self.expressaoAritmetica(node) and self.passoFor(node) else self.error(node)
    
    def passoFor(self, parent_node):
        # passoFor -> RESERVED_PASSO expressaoAritmetica | ε
        node = self.addNode("passoFor", parent_node)
        if self.matchTipo("RESERVED_PASSO", node):
            return True if self.expressaoAritmetica(node) else self.error(node)
        return True
    
    def forSendo(self, parent_node):
        # forSendo -> RESERVED_SENDO ID forIntervalo
        node = self.addNode("forSendo", parent_node)
        return True if self.matchTipo("RESERVED_SENDO", node) and self.matchTipo("ID", node) and self.forIntervalo(node) else self.error(node)

    def cmdWhile(self, parent_node):
        # cmdWhile -> RESERVED_ENQUANTO valor INDENT bloco DEDENT
        node = self.addNode("cmdWhile", parent_node)
        return True if self.matchTipo("RESERVED_ENQUANTO", node) and self.valor(node) and self.matchTipo("INDENT", node) and self.bloco(node) and self.matchTipo("DEDENT", node) else self.error(node)

    def cmdReturn(self, parent_node):
        # cmdReturn -> RESERVED_RETORNE valorRetorno
        node = self.addNode("cmdReturn", parent_node)
        return True if self.matchTipo("RESERVED_RETORNE", node) and self.valorRetorno(node) else self.error(node)
    
    def cmdDefFunc(self, parent_node):
        # cmdDefFunc -> RESERVED_FUNCAO ID OPEN_PARENTHESIS listaParametros CLOSE_PARENTHESIS INDENT bloco DEDENT
        node = self.addNode("cmdDefFunc", parent_node)
        return True if self.matchTipo("RESERVED_FUNCAO", node) and self.matchTipo("ID", node) and self.matchTipo("OPEN_PARENTHESIS", node) and self.listaParametros(node) and self.matchTipo("CLOSE_PARENTHESIS", node) and self.matchTipo("INDENT", node) and self.bloco(node) and self.matchTipo("DEDENT", node) else self.error(node)
    
    def listaParametros(self, parent_node):
        # listaParametros -> ID entradaListaParam | ε
        node = self.addNode("listaParametros", parent_node)
        if self.matchTipo("ID", node):
            return True if self.entradaListaParam(node) else self.error(node)
        return True
    
    def entradaListaParam(self, parent_node):
        # entradaListaParam -> COMMA ID entradaListaParam | ε
        node = self.addNode("entradaListaParam", parent_node)
        if self.matchTipo("COMMA", node):
            return True if self.matchTipo("ID", node) and self.entradaListaParam(node) else self.error(node)
        return True
    
    def valorRetorno(self, parent_node):
        # valorRetorno -> valor | ε
        node = self.addNode("valorRetorno", parent_node)
        if self.eof() or self.endBlock():
            return True
        return True if self.valor(node) else self.error(node)

    def acessoLista(self, parent_node):
        # acessoLista -> OPEN_BRACKET expressaoAritmetica CLOSE_BRACKET
        node = self.addNode("acessoLista", parent_node)
        return True if self.matchTipo("OPEN_BRACKET", node) and self.expressaoAritmetica(node) and self.matchTipo("CLOSE_BRACKET", node) else self.error(node)

    def cmdPrint(self, parent_node):
        # cmdPrint -> RESERVED_EXIBA OPEN_PARENTHESIS corpoLista CLOSE_PARENTHESIS
        node = self.addNode("cmdPrint", parent_node)
        return True if self.matchTipo("RESERVED_EXIBA", node) and self.matchTipo("OPEN_PARENTHESIS", node) and self.corpoLista(node) and self.matchTipo("CLOSE_PARENTHESIS", node) else self.error(node)
    
    def cmdInput(self, parent_node):
        # cmdInput -> RESERVED_ENTRADA OPEN_PARENTHESIS corpoLista CLOSE_PARENTHESIS
        node = self.addNode("cmdInput", parent_node)
        return True if self.matchTipo("RESERVED_ENTRADA", node) and self.matchTipo("OPEN_PARENTHESIS", node) and self.corpoLista(node) and self.matchTipo("CLOSE_PARENTHESIS", node) else self.error(node)
    
    def opPow(self, parent_node):
        # opPow -> POW
        node = self.addNode("opPow", parent_node)
        return True if self.matchTipo("POW", node) else self.error(node)
# ========================================
# >>>>>>>>>>> Classe Parser <<<<<<<<<<<<<
# ========================================

class Parser:

    def __init__(self, tokens, code):

        self.tokens = tokens
        self.token = tokens.pop(0)
        self.code = CharacterIterator(code)

        self.tree = Tree()
        self.rules = Rules(self)

    def nextToken(self):
        if len(self.tokens) > 0:
            self.token = self.tokens.pop(0)
        else:
            print("Fim do arquivo.")

    def matchTipo(self, tipo, parent_node):
        if self.token.tipo == tipo:
            terminal_node = self.tree.create_node(self.token, parent_node)
            parent_node.add_child(terminal_node)
            self.nextToken()
            return True
        return False

    def matchLexema(self, lexema, parent_node):
        if self.token.lexema == lexema:
            terminal_node = self.tree.create_node(self.token, parent_node)
            parent_node.add_child(terminal_node)
            self.nextToken()
            return True
        return False

    def firstFollow(self, tipo):
        return self.token.tipo == tipo
    
    def checkNext(self, tipo):
        return self.tokens[0].tipo == tipo

    def eof(self):
        return self.token.tipo == "EOF"

    def error(self, node):
        terminal_node = self.tree.create_node(f"X Erro!", node)
        node.add_child(terminal_node)
        # print(f"!-> Error in rule {node.value} at line {self.token.linha}")

        if self.token.tipo == "EOF":
            self.code.string += "$"
            self.code.setIndex(len(self.code.string) - 1)
        else:
            self.code.setIndex(self.token.index)
        
        lineInfo = self.code.getErrorInfo()
        print(f"Erro Sintático: token '{self.token.lexema}' do tipo '{self.token.tipo}' inesperado na linha {lineInfo['lineNumber']}, regra \"{node.value}\":")
        print(lineInfo["fullLine"][0:lineInfo["errorStart"]] + colored(lineInfo['unexpectedToken'], 'red') + lineInfo["fullLine"][lineInfo["errorEnd"] + 1:])

        raise Exception()

    def endBlock(self):
        return self.token.tipo == "DEDENT"
    
    def addNode(self, value, parent_node):
        node = self.tree.create_node(value, parent_node)
        parent_node.add_child(node)
        return node
    
    def setRoot(self):
        node = self.tree.create_node("prog", None)
        self.tree.root = node
        return node

    def parse(self):
        try:
            result = self.rules.prog()
        except:
            result = False

        # result = self.rules.prog()

        return result, self.tree