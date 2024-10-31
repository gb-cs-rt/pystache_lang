from utils import Tree, CharacterIterator
from termcolor import colored

class Semantic:

    def __init__(self, tree, code):
        self.tree = tree
        self.code = CharacterIterator(code)
        self.type_hash = {}

    def check(self, node):
        if node.type == "rule":
            if node.value == "cmdID" and node.children[1].children[0].value == "cmdAtrib":
                id_token = node.children[0]
                token_type = self.check_cmdAtrib(node.children[1].children[0])

                if id_token.value.lexema not in self.type_hash:
                    self.type_hash[id_token.value.lexema] = token_type

        for child in node.children:
            self.check(child)

    def check_cmdAtrib(self, node):
        elements = []
        isList = [False]
        self.get_elements(node, elements, isList)
        return self.check_elements(elements, isList[0])

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

    def check_elements(self, elements, isList):

        if len(elements) == 0:
            if isList:
                return "LIST_VOID"
            return None
        
        first_token = elements[0].value
        if first_token.tipo == "ID":
            if first_token.lexema not in self.type_hash:
                self.error(f"variável {first_token.lexema} não declarada", first_token.linha)
                return None
            
            token_type = self.type_hash[first_token.lexema]
        else:
            token_type = first_token.tipo

        for element in elements:
            if element.value.tipo == "ID":
                if element.value.lexema not in self.type_hash:
                    self.error(f"variável {element.value.lexema} não declarada", element.value.linha)
                element_type = self.type_hash[element.value.lexema]
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
            return True, self.type_hash
        except:
            return False, None