from utils import CharacterIterator
from termcolor import colored
from pprint import pprint as pp

class Semantic:

    def __init__(self, tree, code):
        self.tree = tree
        self.code = CharacterIterator(code)
        self.type_hash = [{"entradaNumero": "FUNC_NUMBER", "entradaDouble": "FUNC_DOUBLE"}]
        self.all_scopes = []
        self.forVezesX = 0

    def scope_control(self, state, func=False):
        if state == "enter":
            if func:
                actual_scope = self.type_hash[-1].copy()
                self.all_scopes.append(actual_scope.copy())
                self.type_hash.append({"entradaNumero": "FUNC_NUMBER", "entradaDouble": "FUNC_DOUBLE"})
            else:
                actual_scope = self.type_hash[-1].copy()
                self.all_scopes.append(actual_scope.copy())
                self.type_hash.append(actual_scope)
        else:
            actual_scope = self.type_hash[-1].copy()
            self.all_scopes.append(actual_scope.copy())
            self.type_hash.pop()

    def check(self, node):
        if node.type == "rule":

            if node.value == "cmdIf" or node.value == "cmdFor" or node.value == "cmdWhile":
                self.scope_control("enter")

            if node.value == "cmdID" and node.children[2].children[0].value == "cmdAtrib":
                id_token = node.children[0]
                token_type = self.check_cmdAtrib(node.children[2].children[0])
                if id_token.value.lexema not in self.type_hash[-1]:
                    self.type_hash[-1][id_token.value.lexema] = token_type
                else:
                    if len(node.children[1].children) > 0:
                        if self.type_hash[-1][id_token.value.lexema][:4] != "LIST":
                            self.error(f"variável '{id_token.value.lexema}' não é uma lista,", id_token.value.linha)
                        if self.type_hash[-1][id_token.value.lexema] != f"LIST_{token_type}":
                            self.error(f"lista '{id_token.value.lexema}' já declarada com outro tipo", id_token.value.linha)
                    elif self.type_hash[-1][id_token.value.lexema] != token_type:
                        self.error(f"variável '{id_token.value.lexema}' já declarada com outro tipo", id_token.value.linha)

            if node.value == "cmdPrint":
                self.check_cmdPrint(node)
                        
            if node.value == "cmdFor":
                self.check_cmdFor(node, "enter")

            if node.value == "cmdDefFunc":
                id_token = node.children[1]
                token_type = self.check_cmdDefFunc(node.children[6].children[0].children[0])
                if id_token.value.lexema not in self.type_hash[-1]:
                    self.type_hash[-1][id_token.value.lexema] = f"FUNC_VOID" if token_type == "VOID" else f"FUNC_DOUBLE"
                    self.scope_control("enter", func=True)
                    self.declareFuncParams(node)
                else:
                    self.error(f"função '{id_token.value.lexema}' já declarada", id_token.value.linha)

        for child in node.children:
            self.check(child)

        if node.type == "rule":
            if node.value == "cmdFor":
                self.check_cmdFor(node, "exit")
            if node.value == "cmdIf" or node.value == "cmdFor" or node.value == "cmdDefFunc" or node.value == "cmdWhile":
                self.scope_control("exit")

    def declareFuncParams(self, node):
        params = []
        self.get_params(node.children[3], params)
        for param in params:
            if param in self.type_hash[-1]:
                self.error(f"parâmetro '{param}' já declarado", node.children[0].value.linha)
            self.type_hash[-1][param] = "NUMBER"

    def check_cmdAtrib(self, node):
        elements = []
        isList = [False]
        self.get_elements(node, elements, isList)
        return self.check_elements(elements, isList[0])
    
    def check_cmdPrint(self, node):
        elements = []
        self.get_elements(node.children[2], elements, False)
        self.check_IDs(elements)

    def check_IDs(self, elements):
        for element in elements:
            if element.value.tipo == "ID":
                if element.value.lexema not in self.type_hash[-1]:
                    self.error(f"variável '{element.value.lexema}' não declarada neste escopo,", element.value.linha)
    
    def check_cmdDefFunc(self, node):
        isReturn = [False]
        self.findReturn(node, isReturn)
        if isReturn[0]:
            return "NUMBER"
        return "VOID"
    
    def findReturn(self, node, isReturn):
        if node.type == "rule":
            if node.value == "cmdReturn":
                if len(node.children[1].children) > 0:
                    isReturn[0] = True

        for child in node.children:
            self.findReturn(child, isReturn)
    
    def check_cmdFor(self, node, state):
        if node.children[1].children[0].value == "forVezes" or node.children[1].children[0].value == "forIntervalo":
            if state == "enter":
                self.forVezesX += 1
                if f"x{self.forVezesX}" not in self.type_hash[-1]:
                    self.type_hash[-1][f"x{self.forVezesX}"] = "NUMBER"
                elif self.type_hash[-1][f"x{self.forVezesX}"] != "NUMBER":
                    self.error(f"variável 'x{self.forVezesX}' já declarada", node.children[0].children[0].linha)
            else:
                self.forVezesX -= 1
        elif node.children[1].children[0].value == "forSendo":
            if state == "enter":
                if node.children[1].children[0].children[1].value.lexema in self.type_hash[-1]:
                    if self.type_hash[-1][node.children[1].children[0].children[1].value.lexema] != "NUMBER":
                        self.error(f"variável '{node.children[1].children[0].children[1].value.lexema}' já declarada como não inteiro", node.children[1].children[0].children[1].value.linha)
                self.type_hash[-1][node.children[1].children[0].children[1].value.lexema] = "NUMBER"

    def get_elements(self, node, elements, isList):
        if node.type == "rule":
            if node.value == "lista":
                isList[0] = True
            if node.value == "elemento":
                elements.append(node.children[0])
            if node.value == "cmdInput":
                elements.append(node.children[0])
            for child in node.children:
                self.get_elements(child, elements, isList)

    def get_params(self, node, params):
        if node.type == "token":
            if node.value.tipo == "ID":
                params.append(node.value.lexema)
        else:
            for child in node.children:
                self.get_params(child, params)

    def check_elements(self, elements, isList):

        if len(elements) == 0:
            if isList:
                return "LIST_VOID"
            return None
        
        first_token = elements[0].value
        if first_token.tipo == "ID":
            if first_token.lexema not in self.type_hash[-1]:
                self.error(f"variável {first_token.lexema} não declarada neste escopo,", first_token.linha)
                return None
            
            token_type = self.type_hash[-1][first_token.lexema]
        else:
            token_type = first_token.tipo

        if token_type == "RESERVED_ENTRADA":
            token_type = "STRING"
        elif token_type == "FUNC_NUMBER":
            return "NUMBER"
        elif token_type == "FUNC_DOUBLE":
            return "DOUBLE"
        elif token_type == "LIST_STRING":
            return "STRING"
        elif token_type == "LIST_NUMBER":
            return "NUMBER"
        elif token_type == "LIST_DOUBLE":
            return "DOUBLE"
        elif token_type == "FUNC_VOID":
            raise Exception("Erro Semântico: função sem retorno na expressão")
        

        for element in elements:
            if element.value.tipo == "ID":
                if element.value.lexema not in self.type_hash[-1]:
                    self.error(f"variável {element.value.lexema} não declarada neste escopo,", element.value.linha)
                element_type = self.type_hash[-1][element.value.lexema]
            elif element.value.tipo == "RESERVED_ENTRADA":
                element_type = "STRING"
            else:
                element_type = element.value.tipo

            if element_type != token_type:
                if isList:
                    self.error(f"lista não pode conter tipos diferentes,", element.value.linha)
                elif (token_type == "NUMBER" and element_type == "DOUBLE") or (token_type == "DOUBLE" and element_type == "NUMBER"):
                    token_type = "DOUBLE"
                else:
                    self.error(f"expressão com tipos incompatíveis", element.value.linha)
        
        if isList:
            return f"LIST_{token_type}"
        if token_type == "RESERVED_ENTRADA":
            return "STRING"
        else:
            return token_type
    
    def error(self, message, line):
        print(f"Erro Semântico: {message} na linha {line}:")
        print(colored(self.code.getLine(line), 'red'))
        raise Exception()
    
    def run(self):
        try:
            self.check(self.tree.root)
            self.all_scopes.append(self.type_hash[-1].copy())
            return True, self.all_scopes
        except Exception as e:
            print(e)
            return False, None
        # self.check(self.tree.root)