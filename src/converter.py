from utils import Tree

class Translator:
    
    def translate(self, node, state):

        if node.type == "rule":
            return self.translate_rule(node.value, state)
        else:
            return self.translate_token(node.value, state)

    def translate_rule(self, rule, state):

        if rule == "prog":
            return self.prog(state)
        elif rule == "cmd":
            return self.cmd(state)
        else:
            return ""
        
    def translate_token(self, token, state):
        
        if state == "enter":
            
            if token.tipo == "ASSIGN":
                return " = "
            elif token.tipo == "INDENT":
                return " {\n"
            elif token.tipo == "DEDENT":
                return "}"
            elif token.tipo == "RESERVED_SE":
                return "if ("
            elif token.tipo == "RESERVED_ENTAO":
                return ")"
            elif token.tipo == "RESERVED_SENAO":
                return "else"
            elif token.tipo == "RESERVED_EXIBA":
                return "printf"
            elif token.tipo == "OPEN_BRACKET":
                return "{"
            elif token.tipo == "CLOSE_BRACKET":
                return "}"
            else:
                return token.lexema

        elif state == "exit":
            return ""

    def prog(self, state):
        if state == "enter":
            return "int main() {\n"
        elif state == "exit":
            return "return 0;\n}\n"

    def cmd(self, state):
        if state == "enter":
            return ""
        elif state == "exit":
            return ";\n"

class Converter:
    def __init__(self, tree):
        self.tree = tree
        self.translator = Translator()

    def pre_order(self, node):
        
        self.write(node, "enter")

        for child in node.children:
            self.pre_order(child)
        
        self.write(node, "exit")

    def write(self, node, state):
        file = open("output.cpp", "a")
        file.write(self.translator.translate(node, state))
        file.close()

    def create_file(self):
        file = open("output.cpp", "w")
        file.write("#include <iostream>\n")
        file.write("#include <string>\n")
        file.write("#include <vector>\n")
        file.write("#include <cstdio>\n")
        file.write("#include <map>\n\n")
        file.write("using namespace std;\n\n")
        file.close()
    
    def convert(self):
        self.create_file()
        self.pre_order(self.tree.root)
