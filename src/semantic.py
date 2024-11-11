from utils import CharacterIterator, DictList
from termcolor import colored

class Semantic:

    def __init__(self, tree, code):
        self.tree = tree
        self.code = CharacterIterator(code)
        self.type_hash = [{"entradaNumero": "FUNC_NUMBER", "entradaReal": "FUNC_DOUBLE", "inserir": "FUNC_VOID", "remover": "FUNC_VOID", "tamanho": "FUNC_NUMBER", "paraNumero": "FUNC_NUMBER", "paraReal": "FUNC_DOUBLE", "paraTexto": "FUNC_STRING"}]
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
            token_type = self.check_cmdAtrib(node.children[2].children[0], id_token.value.lexema)

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
            if node.children[0].value.lexema == "inserir":
                foundID = []
                self.getID(node.children[2].children[0].children[0].children[1], foundID)

                insertType = []
                self.getInsertionType(node.children[2].children[0].children[0].children[1].children[1], insertType)

                if foundID[0] not in self.type_hash[-1]:
                    self.error(f"variável '{foundID[0]}' não declarada,", node.children[0].value.linha)
                if insertType[0] != self.type_hash[-1][foundID[0]].split("_")[1]:
                    self.error(f"tipo de inserção incompatível com tipo da lista,", node.children[0].value.linha)
            

    def declareFuncParams(self, node):
        params = []
        self.get_params(node.children[3], params)
        for param in params:
            if param in self.type_hash[-1]:
                self.error(f"parâmetro '{param}' já declarado,", node.children[0].value.linha)
            self.type_hash[-1][param] = "NUMBER"

    def check_cmdAtrib(self, node, id):

        elements = []
        listLevel = [0]
        listDimensions = []
        acessosLista = DictList()
        floatDiv = [False]
        mod = [False]
        self.get_elements(node, elements, listDimensions, listLevel, acessosLista, floatDiv, mod)

        return self.check_elements(id, elements, listDimensions, acessosLista, floatDiv[0], mod[0])
    
    def check_cmdPrint(self, node):
        elements = []
        acessosLista = DictList()
        self.get_elements(node.children[2], elements, False, False, acessosLista, False, False, isPrint=[True])
        self.check_IDs(elements, acessosLista)

    def check_IDs(self, elements, acessosLista={}):
        for element in elements:
            if element.value.tipo == "ID":
                if element.value.lexema not in self.type_hash[-1]:
                    self.error(f"variável '{element.value.lexema}' não declarada neste escopo,", element.value.linha)
                if self.type_hash[-1][element.value.lexema][:4] == "LIST":

                    list_dimension = self.type_hash[-1][element.value.lexema].split("_")[2]

                    if element.value.lexema in acessosLista:
                        if isinstance(acessosLista[element.value.lexema], list):
                            for dim in acessosLista[element.value.lexema]:
                                if dim > int(list_dimension):
                                    self.error(f"dimensão da lista '{element.value.lexema}' incompatível,", element.value.linha)
                        else:
                            if acessosLista[element.value.lexema] > int(list_dimension):
                                self.error(f"dimensão da lista '{element.value.lexema}' incompatível,", element.value.linha)

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
            self.get_elements(node.children[1], elements, False, False, False, False, False)
            self.check_IDs(elements)
    
    def check_cmdFor(self, node, state):

        if state == "enter":
            elements = []
            insideFuncParams = [False]
            self.get_elements(node.children[1], elements, False, False, False, False, False, insideFuncParams)
            self.onlyNumbers(elements)
        
        if node.children[1].children[0].value == "forVezes" or node.children[1].children[0].value == "forIntervalo":
            if state == "enter":
                self.forVezesX += 1
                if f"x{self.forVezesX}" not in self.type_hash[-1]:
                    self.type_hash[-1][f"x{self.forVezesX}"] = "NUMBER"
                elif self.type_hash[-1][f"x{self.forVezesX}"] != "NUMBER":
                    self.error(f"variável 'x{self.forVezesX}' já declarada como não inteiro,", node.children[0].value.linha)
            else:
                self.forVezesX -= 1
        elif node.children[1].children[0].value == "forSendo":
            if state == "enter":
                if node.children[1].children[0].children[1].value.lexema in self.type_hash[-1]:
                    if self.type_hash[-1][node.children[1].children[0].children[1].value.lexema] != "NUMBER":
                        self.error(f"variável '{node.children[1].children[0].children[1].value.lexema}' já declarada como não inteiro,", node.children[1].children[0].children[1].value.linha)
                self.type_hash[-1][node.children[1].children[0].children[1].value.lexema] = "NUMBER"

    def getAcessosLista(self, id, node, qtdAcessos):
        if node.type == "rule":
            if node.value == "acessoLista":
                    qtdAcessos[0] += 1

        for child in node.children:
            self.getAcessosLista(id, child, qtdAcessos)

    def get_elements(self, node, elements, listDimensions, listLevel, acessosLista, floatDiv, mod, insideFuncParams=[False], isPrint=[False]):
        if node.type == "rule":
            if node.value == "lista":
                listLevel[0] += 1
                listDimensions.append(listLevel[0])

            if node.value == "chamadaFuncao" and not isPrint[0]:
                insideFuncParams[0] = True

            if node.value == "acessoLista" and not isPrint[0]:
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

                        qtdAcessos = [0]
                        self.getAcessosLista(node.children[0].value.lexema, node.children[1].children[0], qtdAcessos)
                        
                        acessosLista[node.children[0].value.lexema] = qtdAcessos[0]

                elements.append(node.children[0])
            if node.value == "cmdInput":
                elements.append(node.children[0])
            if node.value == "opMul":
                if node.children[0].value.tipo == "DIV":
                    floatDiv[0] = True
                if node.children[0].value.tipo == "MOD":
                    mod[0] = True

            for child in node.children:
                self.get_elements(child, elements, listDimensions, listLevel, acessosLista, floatDiv, mod, insideFuncParams, isPrint)

            if node.value == "chamadaFuncao":
                insideFuncParams[0] = False
            if node.value == "acessoLista":
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

    def check_elements(self, id, elements, listDimensions, acessosLista, floatDiv, mod):

        if len(elements) == 0:
            if len(listDimensions) > 0:
                insertType = []
                self.searchForInsert(self.tree.root, id, insertType)

                if insertType:
                    return f"LIST_{insertType[0]}_{max(listDimensions)}"

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
        elif token_type == "FUNC_STRING":
            token_type = "STRING"
        elif token_type[:4] == "LIST":

            list_type = token_type.split("_")[1]
            list_dimension = token_type.split("_")[2]

            if first_token.lexema in acessosLista:
                dimResultante = 0
                if isinstance(acessosLista[first_token.lexema], list):
                    for dim in acessosLista[first_token.lexema]:
                        if dim > int(list_dimension):
                            self.error(f"dimensão da lista '{first_token.lexema}' incompatível,", first_token.linha)
                        else:
                            dimResultante = int(list_dimension) - dim
                else:
                    if acessosLista[first_token.lexema] > int(list_dimension):
                        self.error(f"dimensão da lista '{first_token.lexema}' incompatível,", first_token.linha)
                    else:
                        dimResultante = int(list_dimension) - acessosLista[first_token.lexema]

                if dimResultante > 0:
                    list_type = f"LIST_{list_type}_{dimResultante}"
                else:
                    list_type = list_type

                token_type = list_type
            else:
                token_type = token_type

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
                elif self.type_hash[-1][element.value.lexema] == "FUNC_STRING":
                    element_type = "STRING"
                elif self.type_hash[-1][element.value.lexema][:4] == "LIST":

                    list_type = self.type_hash[-1][element.value.lexema].split("_")[1]
                    list_dimension = self.type_hash[-1][element.value.lexema].split("_")[2]

                    if element.value.lexema in acessosLista:
                        dimResultante = 0
                        if isinstance(acessosLista[element.value.lexema], list):
                            for dim in acessosLista[element.value.lexema]:
                                if dim > int(list_dimension):
                                    self.error(f"dimensão da lista '{element.value.lexema}' incompatível,", element.value.linha)
                                else:
                                    dimResultante = int(list_dimension) - dim
                        else:
                            if acessosLista[element.value.lexema] > int(list_dimension):
                                self.error(f"dimensão da lista '{element.value.lexema}' incompatível,", element.value.linha)
                            else:
                                dimResultante = int(list_dimension) - acessosLista[element.value.lexema]

                        if dimResultante > 0:
                            list_type = f"LIST_{list_type}_{dimResultante}"
                        else:
                            list_type = list_type

                        element_type = list_type
                    else:
                        element_type = self.type_hash[-1][element.value.lexema]
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
        
    def searchForInsert(self, node, id, insertType):
        if node.type == "rule":
            if node.value == "cmdID":
                if node.children[0].value.lexema == "inserir":
                    foundID = []
                    self.getID(node.children[2].children[0].children[0].children[1], foundID)

                    if foundID[0] == id:
                        self.getInsertionType(node.children[2].children[0].children[0].children[1].children[1], insertType)

        for child in node.children:
            self.searchForInsert(child, id, insertType)

    def getID(self, node, foundID):
        if node.type == "rule":
            if node.value == "elemento":
                if node.children[0].value.tipo == "ID":
                    foundID.append(node.children[0].value.lexema)
        
        for child in node.children:
            self.getID(child, foundID)
        
    def getInsertionType(self, node, insertType):
        if node.type == "rule":
            if node.value == "elemento":
                if node.children[0].value.tipo == "ID":
                    if node.children[0].value.lexema not in self.type_hash[-1]:
                        self.error(f"variável '{node.children[0].value.lexema}' não declarada neste escopo,", node.children[0].value.linha)
                    insertType.append(self.type_hash[-1][node.children[0].value.lexema])
                else:
                    insertType.append(node.children[0].value.tipo)

        for child in node.children:
            self.getInsertionType(child, insertType)
        
    def check_cmdWhile(self, node, state):
            
        if state == "enter":
            elements = []
            self.get_elements(node.children[1], elements, False, False, False, False, False)
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
            # import traceback
            # traceback.print_exc()
            print(e)
            return False, None