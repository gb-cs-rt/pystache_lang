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
        if self.firstFollow("RESERVED_SE"):
            return self.cmdIf(node)
        if self.firstFollow("RESERVED_PASSE"):
            return self.matchTipo("RESERVED_PASSE", node)
        return self.error(node)

    def cmdIf(self, parent_node):
        # cmdIf -> RESERVED_SE condicao RESERVED_ENTAO INDENT bloco DEDENT cmdElse
        node = self.addNode("cmdIf", parent_node)
        return True if self.matchTipo("RESERVED_SE", node) and self.condicao(node) and self.matchTipo("RESERVED_ENTAO", node) and self.matchTipo("INDENT", node) and self.bloco(node) and self.matchTipo("DEDENT", node) and self.cmdElse(node) else self.error(node)

    def cmdElse(self, parent_node):
        # cmdElse -> RESERVED_SENAO INDENT bloco DEDENT | ε
        node = self.addNode("cmdElse", parent_node)
        if self.matchTipo("RESERVED_SENAO", node):
            return True if self.matchTipo("INDENT", node) and self.bloco(node) and self.matchTipo("DEDENT", node) else self.error(node)
        return True

    def condicao(self, parent_node):
        # condicao -> relacao opLogico relacao | relacao
        node = self.addNode("condicao", parent_node)
        if self.relacao(node):
            if self.firstFollow("AND") or self.firstFollow("OR"):
                return True if self.opLogico(node) and self.relacao(node) else self.error(node)
            return True

    def relacao(self, parent_node):
        # relacao -> valor opRelacional valor | valor
        node = self.addNode("relacao", parent_node)
        if self.valor(node):
            if self.firstFollow("GREATER") or self.firstFollow("LESS") or self.firstFollow("EQUALS") or self.firstFollow("DIFFERENT") or self.firstFollow("GREATER_EQUAL") or self.firstFollow("LESS_EQUAL"):
                return True if self.opRelacional(node) and self.valor(node) else self.error(node)
            return True
        return self.error(node)

    def valor(self, parent_node):
        # valor -> expressao | lista | STRING | BOOL
        node = self.addNode("valor", parent_node)
        if self.firstFollow("STRING") or self.firstFollow("BOOL"):
            return True if self.matchTipo("STRING", node) or self.matchTipo("BOOL", node) else self.error(node)
        if self.firstFollow("OPEN_BRACKET"):
            return True if self.lista(node) else self.error(node)
        return True if self.expressao(node) else self.error(node)

    def opRelacional(self, parent_node):
        # opRelacional -> GREATER | LESS | EQUALS | DIFFERENT | GREATER_EQUAL | LESS_EQUAL
        node = self.addNode("opRelacional", parent_node)
        return True if self.matchTipo("GREATER", node) or self.matchTipo("LESS", node) or self.matchTipo("EQUALS", node) or self.matchTipo("DIFFERENT", node) or self.matchTipo("GREATER_EQUAL", node) or self.matchTipo("LESS_EQUAL", node) else self.error(node)

    def opLogico(self, parent_node):
        # opLogico -> AND | OR
        node = self.addNode("opLogico", parent_node)
        return True if self.matchTipo("AND", node) or self.matchTipo("OR", node) else self.error(node)

    def expressao(self, parent_node):
        # expressao -> termo opAd termo | termo
        node = self.addNode("expressao", parent_node)
        if self.termo(node):
            if self.firstFollow("PLUS") or self.firstFollow("MINUS"):
                return True if self.opAd(node) and self.termo(node) else self.error(node)
            return True

    def opAd(self, parent_node):
        # opAd -> PLUS | MINUS
        node = self.addNode("opAd", parent_node)
        return True if self.matchTipo("PLUS", node) or self.matchTipo("MINUS", node) else self.error(node)

    def termo(self, parent_node):
        # termo -> fator opMul fator | fator
        node = self.addNode("termo", parent_node)
        if self.fator(node):
            if self.firstFollow("MULT") or self.firstFollow("DIV"):
                return True if self.opMul(node) and self.fator(node) else self.error(node)
            return True

    def opMul(self, parent_node):
        # opMul -> MULT | DIV
        node = self.addNode("opMul", parent_node)
        return True if self.matchTipo("MULT", node) or self.matchTipo("DIV", node) else self.error(node)

    def fator(self, parent_node):
        # fator -> NUM | DOUBLE | ID | OPEN_PARENTHESIS expressao CLOSE_PARENTHESIS
        node = self.addNode("fator", parent_node)
        if self.matchTipo("NUMBER", node) or self.matchTipo("DOUBLE", node) or self.matchTipo("ID", node):
            return True
        elif self.matchTipo("OPEN_PARENTHESIS", node):
            return True if self.expressao(node) and self.matchTipo("CLOSE_PARENTHESIS", node) else self.error(node)
        
        return self.error(node)

    def lista(self, parent_node):
        # lista -> OPEN_BRACKET corpoLista CLOSE_BRACKET
        node = self.addNode("lista", parent_node)
        return True if self.matchTipo("OPEN_BRACKET", node) and self.corpoLista(node) and self.matchTipo("CLOSE_BRACKET", node) else self.error(node)

    def corpoLista(self, parent_node):
        # corpoLista -> valor entradaLista | ε
        node = self.addNode("corpoLista", parent_node)
        if self.valor(node):
            return True if self.entradaLista(node) else self.error(node)
        return True

    def entradaLista(self, parent_node):
        # entradaLista -> COMMA valor entradaLista | ε
        node = self.addNode("entradaLista", parent_node)
        if self.matchTipo("COMMA", node):
            return True if self.valor(node) and self.entradaLista(node) else self.error(node)
        return True
    
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

        return result, self.tree