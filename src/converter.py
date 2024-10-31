from utils import Tree

class Translator:

    def __init__(self, type_hash, declaration_hash):
        self.type_hash = type_hash
        self.declaration_hash = declaration_hash
        self.lastId = None
        self.isPrint = False
    
    def translate(self, node, state):

        if node.type == "rule":
            return self.translate_rule(node, state)
        else:
            return self.translate_token(node, state)

    def translate_rule(self, node, state):

        rule = node.value

        if rule == "prog":
            return self.prog(state)
        elif rule == "cmd":
            return self.cmd(state)
        elif rule == "cmdID":
            self.lastId = node.children[0].value.lexema
            return self.cmdID(node, state)
        elif rule == "assignOp":
            return self.assignOp(node, self.lastId, state)
        elif rule == "atribComOp":
            return self.atribComOp(node, state)
        elif rule == "cmdPrint":
            return self.cmdPrint(state)
        elif rule == "elemento":
            return self.elemento(node, state)
        else:
            return ""
        
    def translate_token(self, node, state):
        
        token = node.value

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
            elif token.tipo == "RESERVED_ENTRADA":
                return "userInput"
            elif token.tipo == "OPEN_BRACKET":
                return "{"
            elif token.tipo == "CLOSE_BRACKET":
                return "}"
            elif token.tipo == "PLUS_ASSIGN":
                return "+="
            elif token.tipo == "MINUS_ASSIGN":
                return "-="
            elif token.tipo == "MULT_ASSIGN":
                return "*="
            elif token.tipo == "DIV_ASSIGN":
                return "/="
            elif token.tipo == "MOD_ASSIGN":
                return "%="
            elif token.tipo == "DIV_INT_ASSIGN":
                return "= (int)"
            elif token.tipo == "POW_ASSIGN":
                return "= pow("
            else:
                return token.lexema

        elif state == "exit":
            return ""
        
    def translate_type(self, lexema):
        tipo = self.type_hash[lexema]
        if tipo == "NUMBER":
            return "int "
        elif tipo == "DOUBLE":
            return "double "
        elif tipo == "STRING":
            return "string "
        elif tipo == "LIST_VOID":
            return "vector<void*> "
        elif tipo == "LIST_NUMBER":
            return "vector<int> "
        elif tipo == "LIST_DOUBLE":
            return "vector<double> "
        elif tipo == "LIST_STRING":
            return "vector<string> "
        else:
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
        
    def cmdID(self, node, state):
        
        if state == "enter":
            if node.children[1].children[0].children[0].value == "atribComum":
                if node.children[0].value.lexema not in self.declaration_hash:
                    self.declaration_hash[node.children[0].value.lexema] = True
                    return self.translate_type(node.children[0].value.lexema)
                else:
                    return ""
            else:
                # return node.children[0].value.lexema
                return ""
        elif state == "exit":
            return ""
        
    def assignOp(self, node, lastId, state):
        if state == "enter":
            return ""
        elif state == "exit":
            if node.children[0].value.tipo == "POW_ASSIGN":
                return f"{lastId},"
            if node.children[0].value.tipo == "DIV_INT_ASSIGN":
                return f"{lastId}/"
            else:
                return ""
            
    def atribComOp(self, node, state):
        if state == "enter":
            return ""
        elif state == "exit":
            if node.children[0].children[0].value.tipo == "POW_ASSIGN":
                return ")"
            else:
                return ""
            
    def cmdPrint(self, state):
        if state == "enter":
            self.isPrint = True
            return ""
        elif state == "exit":
            self.isPrint = False
            return ""
    
    def elemento(self, node, state):
        if state == "enter":
            return ""
        elif state == "exit":
            if self.isPrint:
                if node.children[0].value.tipo == "ID" and self.type_hash[node.children[0].value.lexema] == "STRING":
                    return f'.c_str()'
                else:
                    return ""
            else:
                return ""

class Converter:
    def __init__(self, tree, type_hash):
        self.tree = tree
        self.type_hash = type_hash
        self.declaration_hash = {}
        self.translator = Translator(self.type_hash, self.declaration_hash)

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
        file.write("#include <cmath>\n")
        file.write("using namespace std;\n\n")
        file.write("string userInput() {\n")
        file.write("    string input;\n")
        file.write('    cout << "Enter a string: ";\n')
        file.write("    cin >> input;\n")
        file.write("    return input;\n")
        file.write("}\n")
        file.close()
    
    def convert(self):
        self.create_file()
        self.pre_order(self.tree.root)
