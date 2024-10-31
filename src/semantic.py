from utils import Tree

class Semantic:

    def __init__(self, tree):
        self.tree = tree
        self.type_hash = {}

    def check(self, node):
        if node.type == "rule":
            if node.value == "cmdID" and node.children[1].children[0].value == "cmdAtrib":
                id_token = node.children[0]
                token_type = self.check_cmdAtrib(node.children[1].children[0])
                self.type_hash[id_token.value.lexema] = token_type

        for child in node.children:
            self.check(child)

    def check_cmdAtrib(self, node):
        elements = []
        # i must create a recursive method that can find all rules of value "elemento" and add to the elements list
        self.get_elements(node, elements)
        return self.check_elements(elements)

    def get_elements(self, node, elements):
        if node.type == "rule":
            if node.value == "elemento":
                elements.append(node.children[0])
            for child in node.children:
                self.get_elements(child, elements)

    def check_elements(self, elements):
        # all elements are tokens
        # all tokens must have the same type (token.tipo)

        if len(elements) == 0:
            return None
        
        first_token = elements[0].value
        if first_token.tipo == "ID":
            if first_token.lexema not in self.type_hash:
                print(f"variable {first_token} not declared")
                return None
            token_type = self.type_hash[first_token.lexema]
        else:
            token_type = elements[0].value.tipo

        for element in elements:
            if element.value.tipo == "ID":
                if element.value.lexema not in self.type_hash:
                    print(f"variable {element.value} not declared")
                    return None
                if self.type_hash[element.value.lexema] != token_type:
                    print(self.type_hash[element.value.lexema])
                    print(token_type)
                    print("different types")
                    return None
            elif element.value.tipo != token_type:
                print("different types")
                return None
        
        return token_type