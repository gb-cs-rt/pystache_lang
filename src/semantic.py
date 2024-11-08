from utils import CharacterIterator
from termcolor import colored

class Semantic:

    def __init__(self, tree, code):
        self.tree = tree
        self.code = CharacterIterator(code)
        self.type_hash = [{"entradaNumero": "FUNC_NUMBER", "entradaReal": "FUNC_DOUBLE"}]
        self.all_scopes = []
        self.forVezesX = 0

    def scope_control(self, state, func=False):
        if state == "enter":
            if func:
                actual_scope = self.type_hash[-1].copy()
                self.all_scopes.append(actual_scope.copy())
                self.type_hash.append({"entradaNumero": "FUNC_NUMBER", "entradaReal": "FUNC_DOUBLE"})
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

            if node.value == "cmdID":
                self.check_cmdID(node)

            if node.value == "cmdPrint":
                self.check_cmdPrint(node)
                        
            if node.value == "cmdFor":
                self.check_cmdFor(node, "enter")

            if node.value == "cmdWhile":
                self.check_cmdWhile(node, "enter")

            if node.value == "cmdIf":
                self.check_cmdIf(node, "enter")

            if node.value == "cmdDefFunc":
                id_token = node.children[1]
                token_type = self.check_cmdDefFunc(node.children[6])
                if id_token.value.lexema not in self.type_hash[-1]:
                    self.type_hash[-1][id_token.value.lexema] = f"FUNC_VOID" if token_type == "VOID" else f"FUNC_DOUBLE"
                    self.scope_control("enter", func=True)
                    self.declareFuncParams(node)
                else:
                    self.error(f"função '{id_token.value.lexema}' já declarada,", id_token.value.linha)

        for child in node.children:
            self.check(child)

        if node.type == "rule":
            if node.value == "cmdFor":
                self.check_cmdFor(node, "exit")
            if node.value == "cmdIf" or node.value == "cmdFor" or node.value == "cmdDefFunc" or node.value == "cmdWhile":
                self.scope_control("exit")

    def check_cmdID(self, node):
        if node.children[2].children[0].value == "cmdAtrib":

            if node.children[2].children[0].children[0].value == "atribComOp":
                if node.children[0].value.lexema not in self.type_hash[-1]:
                    self.error(f"variável '{node.children[0].value.lexema}' não declarada,", node.children[0].value.linha)

            id_token = node.children[0]
            token_type = self.check_cmdAtrib(node.children[2].children[0])

            if len(node.children[1].children) > 0:
                if id_token.value.lexema not in self.type_hash[-1]:
                    self.error(f"variável '{id_token.value.lexema}' não declarada,", id_token.value.linha)
            if id_token.value.lexema not in self.type_hash[-1]:
                self.type_hash[-1][id_token.value.lexema] = token_type
            else:
                if len(node.children[1].children) > 0:
                    if self.type_hash[-1][id_token.value.lexema][:4] != "LIST":
                        self.error(f"variável '{id_token.value.lexema}' não é uma lista,", id_token.value.linha)
                    if self.type_hash[-1][id_token.value.lexema].split("_")[0] == "LIST":
                        if self.type_hash[-1][id_token.value.lexema].split("_")[1] != token_type:
                            self.error(f"lista '{id_token.value.lexema}' já declarada com outro tipo", id_token.value.linha)
                elif self.type_hash[-1][id_token.value.lexema] != token_type:
                    if node.children[2].children[0].children[0].value == "atribComOp" and node.children[2].children[0].children[0].children[0].children[0].value.tipo == "DIV_INT_ASSIGN":
                        if self.type_hash[-1][id_token.value.lexema] == "NUMBER" and token_type == "DOUBLE" or self.type_hash[-1][id_token.value.lexema] == "DOUBLE" and token_type == "NUMBER":
                            return
                        else:
                            self.error(f"variável '{id_token.value.lexema}' já declarada com outro tipo,", id_token.value.linha)
                    else:
                        self.error(f"variável '{id_token.value.lexema}' já declarada com outro tipo,", id_token.value.linha)
        elif node.children[2].children[0].children[0].value == "chamadaFuncao":
            if node.children[0].value.lexema not in self.type_hash[-1]:
                self.error(f"função '{node.children[0].value.lexema}' não declarada,", node.children[0].value.linha)
            

    def declareFuncParams(self, node):
        params = []
        self.get_params(node.children[3], params)
        for param in params:
            if param in self.type_hash[-1]:
                self.error(f"parâmetro '{param}' já declarado,", node.children[0].value.linha)
            self.type_hash[-1][param] = "NUMBER"

    def check_cmdAtrib(self, node):

        elements = []
        listLevel = [0]
        listDimensions = []
        floatDiv = [False]
        mod = [False]
        self.get_elements(node, elements, listDimensions, listLevel, floatDiv, mod)

        return self.check_elements(elements, listDimensions, floatDiv[0], mod[0])
    
    def check_cmdPrint(self, node):
        elements = []
        self.get_elements(node.children[2], elements, False, False, False, False)
        self.check_IDs(elements)

    def check_IDs(self, elements):
        for element in elements:
            if element.value.tipo == "ID":
                if element.value.lexema not in self.type_hash[-1]:
                    self.error(f"variável '{element.value.lexema}' não declarada neste escopo,", element.value.linha)

    def onlyNumbers(self, elements):
        for element in elements:
            if element.value.tipo == "ID":
                if element.value.lexema not in self.type_hash[-1]:
                    self.error(f"variável '{element.value.lexema}' não declarada neste escopo,", element.value.linha)
                else:
                    if self.type_hash[-1][element.value.lexema] != "NUMBER":
                        self.error(f"variável '{element.value.lexema}' não é um inteiro,", element.value.linha)
            else:
                if element.value.tipo != "NUMBER":
                    self.error(f"expressão com tipos incompatíveis,", element.value.linha)
    
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

    def check_cmdIf(self, node, state):

        if state == "enter":
            elements = []
            self.get_elements(node.children[1], elements, False, False, False, False)
            self.check_IDs(elements)
    
    def check_cmdFor(self, node, state):

        if state == "enter":
            elements = []
            insideFuncParams = [False]
            self.get_elements(node.children[1], elements, False, False, False, False, insideFuncParams)
            self.onlyNumbers(elements)
        
        if node.children[1].children[0].value == "forVezes" or node.children[1].children[0].value == "forIntervalo":
            if state == "enter":
                self.forVezesX += 1
                if f"x{self.forVezesX}" not in self.type_hash[-1]:
                    self.type_hash[-1][f"x{self.forVezesX}"] = "NUMBER"
                elif self.type_hash[-1][f"x{self.forVezesX}"] != "NUMBER":
                    self.error(f"variável 'x{self.forVezesX}' já declarada,", node.children[0].children[0].linha)
            else:
                self.forVezesX -= 1
        elif node.children[1].children[0].value == "forSendo":
            if state == "enter":
                if node.children[1].children[0].children[1].value.lexema in self.type_hash[-1]:
                    if self.type_hash[-1][node.children[1].children[0].children[1].value.lexema] != "NUMBER":
                        self.error(f"variável '{node.children[1].children[0].children[1].value.lexema}' já declarada como não inteiro,", node.children[1].children[0].children[1].value.linha)
                self.type_hash[-1][node.children[1].children[0].children[1].value.lexema] = "NUMBER"

    def get_elements(self, node, elements, listDimensions, listLevel, floatDiv, mod, insideFuncParams=[False]):
        if node.type == "rule":
            if node.value == "lista":
                listLevel[0] += 1
                listDimensions.append(listLevel[0])

            if node.value == "chamadaFuncao":
                insideFuncParams[0] = True

            if node.value == "elemento" and not insideFuncParams[0]:

                if len(node.children) > 1 and len(node.children[1].children) > 0:
                    if node.children[1].children[0].children[0].value == "chamadaFuncao":
                        if node.children[0].value.lexema not in self.type_hash[-1]:
                            self.error(f"função '{node.children[0].value.lexema}' não declarada neste escopo,", node.children[0].value.linha)
                        if self.type_hash[-1][node.children[0].value.lexema][:4] != "FUNC":
                            self.error(f"variável '{node.children[0].value.lexema}' não é uma função,", node.children[0].value.linha)
                    elif node.children[1].children[0].children[0].value == "acessoLista":
                        if node.children[0].value.lexema not in self.type_hash[-1]:
                            self.error(f"variável '{node.children[0].value.lexema}' não declarada neste escopo,", node.children[0].value.linha)
                        if self.type_hash[-1][node.children[0].value.lexema][:4] != "LIST":
                            self.error(f"variável '{node.children[0].value.lexema}' não é uma lista,", node.children[0].value.linha)

                elements.append(node.children[0])
            if node.value == "cmdInput":
                elements.append(node.children[0])
            if node.value == "opMul":
                if node.children[0].value.tipo == "DIV":
                    floatDiv[0] = True
                if node.children[0].value.tipo == "MOD":
                    mod[0] = True

            for child in node.children:
                self.get_elements(child, elements, listDimensions, listLevel, floatDiv, mod)

            if node.value == "chamadaFuncao":
                insideFuncParams[0] = False
            if node.value == "lista":
                listLevel[0] -= 1
        

    def get_params(self, node, params):
        if node.type == "token":
            if node.value.tipo == "ID":
                params.append(node.value.lexema)
        else:
            for child in node.children:
                self.get_params(child, params)

    def check_elements(self, elements, listDimensions, floatDiv, mod):

        if len(elements) == 0:
            if len(listDimensions) > 0:
                return f"LIST_VOID_{max(listDimensions)}"
            return None
        
        first_token = elements[0].value
        if first_token.tipo == "ID":
            if first_token.lexema not in self.type_hash[-1]:
                self.error(f"variável '{first_token.lexema}' não declarada neste escopo,", first_token.linha)
                return None

            
            token_type = self.type_hash[-1][first_token.lexema]
        else:
            token_type = first_token.tipo

        if token_type == "RESERVED_ENTRADA":
            token_type = "STRING"
        elif token_type == "FUNC_NUMBER":
            token_type = "NUMBER"
        elif token_type == "FUNC_DOUBLE":
            token_type = "DOUBLE"
        elif token_type.split("_")[0] == "LIST":

            list_type = token_type.split("_")[1]

            if list_type == "STRING":
                return "STRING"
            elif list_type == "NUMBER":
                return "NUMBER"
            elif list_type == "DOUBLE":
                return "DOUBLE"
        elif token_type == "FUNC_VOID":
            self.error(f"função não retorna valor,", first_token.linha)
        
        for element in elements:
            if element.value.tipo == "ID":
                if element.value.lexema not in self.type_hash[-1]:
                    self.error(f"variável '{element.value.lexema}' não declarada neste escopo,", element.value.linha)

                if self.type_hash[-1][element.value.lexema] == "FUNC_NUMBER":
                    element_type = "NUMBER"
                elif self.type_hash[-1][element.value.lexema] == "FUNC_DOUBLE":
                    element_type = "DOUBLE"
                else:
                    element_type = self.type_hash[-1][element.value.lexema]
            elif element.value.tipo == "RESERVED_ENTRADA":
                element_type = "STRING"
            else:
                element_type = element.value.tipo

            if element_type != token_type:

                if len(listDimensions) > 0:
                    self.error(f"lista não pode conter tipos diferentes,", element.value.linha)
                elif (token_type == "NUMBER" and element_type == "DOUBLE") or (token_type == "DOUBLE" and element_type == "NUMBER"):
                    token_type = "DOUBLE"
                else:
                    self.error(f"expressão com tipos incompatíveis,", element.value.linha)
        
        if len(listDimensions) > 0:
            return f"LIST_{token_type}_{max(listDimensions)}"
        if floatDiv:
            return "DOUBLE"
        if mod:
            self.onlyNumbers(elements)
        if token_type == "RESERVED_ENTRADA":
            return "STRING"
        else:
            return token_type
        
    def check_cmdWhile(self, node, state):
            
        if state == "enter":
            elements = []
            self.get_elements(node.children[1], elements, False, False, False, False)
            self.check_IDs(elements)
    
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