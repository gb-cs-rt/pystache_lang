class Translator:

    def __init__(self, type_hash, scope_pile):
        self.type_hash = type_hash
        self.scope_pile = scope_pile
        self.lastId = None
        self.isPrint = False
        self.isWhile = False
        self.isSendo = False
        self.sendoID = None
        self.funcParam = False
        self.forVezesX = 0
        self.stopTranslation = False
        self.isAcessoLista = False
        self.scopeID = 0
    
    def translate(self, node, state, function=False):

        if node.type == "rule":
            translation = self.translate_rule(node, state, function)
        else:
            translation = self.translate_token(node, state)

        if self.stopTranslation:
            return ""
        else:
            return translation

    def translate_rule(self, node, state, function=False):

        rule = node.value

        if rule == "prog":
            return self.prog(state)
        elif rule == "cmd":
            return self.cmd(node, state)
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
        elif rule == "forVezes":
            return self.forVezes(node, state)
        elif rule == "forIntervalo":
            return self.forIntervalo(node, state)
        elif rule == "forSendo":
            return self.forSendo(node, state)
        elif rule == "cmdFor":
            return self.cmdFor(state)
        elif rule == "cmdWhile":
            return self.cmdWhile(state)
        elif rule == "valor":
            return self.valor(node, state)
        elif rule == "cmdDefFunc":
            return self.cmdDefFunc(node, state, function)
        elif rule == "listaParametros":
            return self.listaParametros(node, state, function)
        elif rule == "fator":
            return self.fator(node, state)
        elif rule == "acessoLista":
            return self.acessoLista(node, state)
        elif rule == "cmdIf":
            return self.cmdIf(node, state)
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
                if self.isAcessoLista:
                    return "["
                return "{"
            elif token.tipo == "CLOSE_BRACKET":
                if self.isAcessoLista:
                    return "]"
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
            elif token.tipo == "RESERVED_PASSE":
                return "pass"
            elif token.tipo == "DIV_INT":
                return " / "
            elif token.tipo == "DIV":
                return " / (float)"
            elif token.tipo == "EQUALS":
                return " == "
            elif token.tipo == "BOOL":
                if token.lexema == "verdadeiro":
                    return "true"
                elif token.lexema == "falso":
                    return "false"
            elif token.tipo == "RESERVED_REPITA":
                return "for "
            elif token.tipo == "RESERVED_VEZES":
                return f"; x{self.forVezesX}++) "
            elif token.tipo == "RESERVED_DE":
                return "= "
            elif token.tipo == "RESERVED_ATE":
                if not self.isSendo:
                    return f"; x{self.forVezesX} <= "
                else:
                    return f"; {self.sendoID} <= "
            elif token.tipo == "RESERVED_PASSO":
                if not self.isSendo:
                    return f"; x{self.forVezesX} = x{self.forVezesX} + "
                else:
                    return f"; {self.sendoID} = {self.sendoID} + "
            elif token.tipo == "RESERVED_SENDO":
                return "(int "
            elif token.tipo == "RESERVED_ENQUANTO":
                return "while ("
            elif token.tipo == "RESERVED_FUNCAO":
                return ""
            elif token.tipo == "RESERVED_RETORNE":
                return "return "
            elif token.tipo == "ID" and self.funcParam:
                self.scope_pile[-1][token.lexema] = True
                return f"int {token.lexema}"
            elif token.tipo == "RESERVED_PARE":
                return "break"
            elif token.tipo == "POW":
                return ", "
            else:
                return token.lexema

        elif state == "exit":
            return ""
        
    def translate_type(self, lexema):
        # print("-- TRANSLATE TYPE --")
        # print(f"lexema: {lexema}, scopeID: {self.scopeID}")
        # pp(self.type_hash[self.scopeID])
        # print("---------------------")
        tipo = self.type_hash[self.scopeID][lexema]
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
        elif tipo == "BOOL":
            return "bool "
        elif tipo == "FUNC_VOID":
            return "void "
        elif tipo == "FUNC_NUMBER":
            return "int "
        elif tipo == "FUNC_DOUBLE":
            return "double "
        else:
            return ""

    def prog(self, state):
        if state == "enter":
            return "\nint main() {\n"
        elif state == "exit":
            return "return 0;\n}\n"

    def cmd(self, node, state):
        if state == "enter":
            return ""
        elif state == "exit":
            if node.children[0].value == "cmdDefFunc":
                return ""
            return ";\n"
        
    def cmdID(self, node, state):
        
        if state == "enter":
            if node.children[2].children[0].children[0].value == "atribComum":
                if node.children[0].value.lexema not in self.scope_pile[-1]:
                    self.scope_pile[-1][node.children[0].value.lexema] = True
                    # print("linha", node.children[0].value.linha)
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
                if node.children[0].value.tipo == "ID" and self.type_hash[self.scopeID][node.children[0].value.lexema] == "STRING":
                    return f'.c_str()'
                else:
                    return ""
            else:
                return ""
            
    def cmdFor(self, state):
        if state == "enter":
            self.scopeID += 1
            actual_scope = self.scope_pile[-1]
            self.scope_pile.append(actual_scope.copy())
            self.forVezesX += 1
            return ""
        elif state == "exit":
            self.scopeID += 1
            self.scope_pile.pop()
            self.forVezesX -= 1
            return ""
        
    def forVezes(self, node, state):
        if state == "enter":
            return f"(int x{self.forVezesX} = 0; x{self.forVezesX} < "
        elif state == "exit":
            return ""
        
    def forIntervalo(self, node, state):
        if state == "enter":
            if not self.isSendo:
                return f"(int x{self.forVezesX} "
            else:
                return ""
        elif state == "exit":
            if len(node.children[4].children) == 0:
                if self.isSendo:
                    return f"; {self.sendoID}++)"
                else:
                    return f"; x{self.forVezesX}++) "
            else:
                return ")"
            
    def forSendo(self, node, state):
        if state == "enter":
            self.isSendo = True
            self.sendoID = node.children[1].value.lexema
            return ""
        elif state == "exit":
            self.isSendo = False
            self.sendoID = None
            return ""
        
    def cmdWhile(self, state):
        if state == "enter":
            self.scopeID += 1
            actual_scope = self.scope_pile[-1]
            self.scope_pile.append(actual_scope.copy())
            self.isWhile = True
            return ""
        elif state == "exit":
            self.scopeID += 1
            self.scope_pile.pop()
            return ""
        
    def valor(self, node, state):
        if state == "enter":
            return ""
        elif state == "exit":
            if self.isWhile:
                self.isWhile = False
                return f")"
            else:
                return ""
            
    def cmdDefFunc(self, node, state, function=False):
        if state == "enter":
            if not function:
                self.stopTranslation = True
            # print("linha: ", node.children[1].value.linha)
            return self.translate_type(node.children[1].value.lexema)
        elif state == "exit":
            self.stopTranslation = False
            self.scopeID += 1
            self.scope_pile.pop()
            if function:
                return "\n\n"
            else:
                return ""
            
    def fator(self, node, state):
        if state == "enter":
            if len(node.children) == 1:
                return ""
            if node.children[1].value == "opPow":
                return "pow("
            return ""
        elif state == "exit":
            if len(node.children) == 1:
                return ""
            if node.children[1].value == "opPow":
                return ")"
            return ""
        
    def listaParametros(self, node, state, function=False):
        if state == "enter":
            self.scopeID += 1
            self.scope_pile.append({"entradaNumero": True, "entradaDouble": True})
            if function:
                self.funcParam = True
            return ""
        elif state == "exit":
            self.funcParam = False
            return ""
        
    def acessoLista(self, node, state):
        if state == "enter":
            self.isAcessoLista = True
            return ""
        elif state == "exit":
            self.isAcessoLista = False
            return ""
        
    def cmdIf(self, node, state):
        if state == "enter":
            self.scopeID += 1
            actual_scope = self.scope_pile[-1]
            self.scope_pile.append(actual_scope.copy())
            return ""
        elif state == "exit":
            self.scopeID += 1
            self.scope_pile.pop()
            return ""
            
class Converter:
    def __init__(self, tree, type_hash):
        self.tree = tree
        self.type_hash = type_hash
        self.scope_pile = [{}]
        self.translator = Translator(self.type_hash, self.scope_pile)
        self.defFunc = [False]

    def translate_functions(self, node):

        if node.type == "rule" and node.value == "cmdDefFunc":
            self.defFunc = [True]

        if self.defFunc[0]:
            self.write(node, "enter", True)

            for child in node.children:
                self.translate_functions(child)
            
            self.write(node, "exit", True)
        else:
            for child in node.children:
                self.translate_functions(child)

        if node.type == "rule" and node.value == "cmdDefFunc":
            self.defFunc = [False]

    def pre_order(self, node):
        
        self.write(node, "enter")

        for child in node.children:
            self.pre_order(child)
        
        self.write(node, "exit")

    def write(self, node, state, function=False):
        file = open("output.cpp", "a")
        file.write(self.translator.translate(node, state, function))
        file.close()

    def create_file(self):
        file = open("output.cpp", "w")
        file.write("#include <iostream>\n")
        file.write("#include <string>\n")
        file.write("#include <vector>\n")
        file.write("#include <cstdio>\n")
        file.write("#include <cmath>\n\n")
        file.write("using namespace std;\n\n")
        file.write("#define pass (void)0\n\n")
        file.write("string userInput(string message = \"\") {\n")
        file.write("    string input;\n")
        file.write('    cout << message;\n')
        file.write("    cin >> input;\n")
        file.write("    return input;\n")
        file.write("}\n\n")
        file.write("int entradaNumero(string message = \"\") {\n")
        file.write("    int input;\n")
        file.write('    cout << message;\n')
        file.write("    cin >> input;\n")
        file.write("    return input;\n")
        file.write("}\n\n")
        file.write("double entradaReal(string message = \"\") {\n")
        file.write("    double input;\n")
        file.write('    cout << message;\n')
        file.write("    cin >> input;\n")
        file.write("    return input;\n")
        file.write("}\n\n")
        file.close()
    
    def convert(self):
        self.create_file()
        self.translate_functions(self.tree.root)
        self.translator.scopeID = 0
        self.pre_order(self.tree.root)