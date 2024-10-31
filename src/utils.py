from termcolor import colored

# ========================================
# >>>>>>> Classe CharacterIterator <<<<<<<
# ========================================

class CharacterIterator:

    def __init__(self, string):
        self.string = string
        self.index = 0

    def current(self):
        if self.index < len(self.string) and self.index >= 0:
            return self.string[self.index]
        return None
    
    def next(self):
        if self.index < len(self.string):
            self.index += 1
        return self.current()
    
    def previous(self):
        if self.index >= 0:
            self.index -= 1
        return self.current()
        
    def getIndex(self):
        return self.index
    
    def setIndex(self, index):
        self.index = index

    def getLineNumber(self):
        return self.string.count("\n", 0, self.index) + 1

    def getErrorInfo(self):

        line_start = self.string.rfind("\n", 0, self.index) + 1
        errorStart = self.index

        unexpectedToken = ""
        while self.current() != None and self.current() != ' ' and self.current() != '\n':
            unexpectedToken += self.current()
            self.next()

        line_end = self.string.find("\n", self.index)
        errorEnd = self.index - 1
        full_line = self.string[line_start: line_end if line_end != -1 else None]
        
        return {
            'lineNumber': self.string.count("\n", 0, self.index) + 1,
            'fullLine': full_line,
            'errorStart': errorStart - line_start,
            'errorEnd': errorEnd - line_start,
            'unexpectedToken': unexpectedToken
        }

# ========================================
# >>>>>>>>>>> Classe Character <<<<<<<<<<<
# ========================================

class Character:

    @staticmethod
    def isDigit(char):
        if type(char) == str:
            return char.isdigit()
        return False
    
    @staticmethod
    def isAlpha(char):
        if type(char) == str:
            return char.isalpha()
        return False

    @staticmethod
    def isAllowedInID(char):
        if type(char) == str:
            return (char.isalpha()) or (char == "_") or (char.isdigit())
        return False
    
    @staticmethod
    def isAllowedAfterID(char):
        return char in [' ', '\n', '(', ')', '+', '-', '*', '/', '^', '=', '<', '>', '!', ':', ',', None, '&', '|', '[', ']']
    
    @staticmethod
    def isAllowedAfterNumber(char):
        return char in [' ', '\n', '(', ')', '+', '-', '*', '/', '^', '.', None, '=', '<', '>', '!', '&', '|', ',', ':', '[', ']']
    
    @staticmethod
    def isAllowedAfterRelational(char):
        return char in [' ', '\n', '(', ')', '+', '-', '*', '/', '^', None] or Character.isDigit(char) or Character.isAlpha(char)

# ========================================
# >>>>>>>>> Classe TreeNode <<<<<<<<<<<<<
# ========================================

class TreeNode:
    def __init__(self, id, value, parent=None):
        self.id = id
        self.value = value
        self.type = None
        self.parent = parent
        self.children = []
        self.enter = ""
        self.exit = ""

        if self.value == "X Erro!":
            self.type = "error"
        elif type(self.value) == str:
            self.type = "rule"
        else:
            self.type = "token"

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def print_node(self, level=0, is_last=False, prefix=""):
        if level == 0:
            indent = prefix + ("   " if is_last else "│  ")
        else:
            indent = prefix + ("└─ " if is_last else "├─ ")
        
        #print(f"{indent}{colored(self.value, 'red')}") if self.value == "X Erro!" else print(f"{indent}{self.value}")
        if self.type == "error":
            print(f"{indent}{colored(self.value, 'red')}")
        elif self.type == "rule":
            print(f"{indent}{colored(self.value, 'green')}")
        else:
            print(f"{indent}{self.value}")
        
        for i, child in enumerate(self.children):
            child.print_node(level + 1, i == len(self.children) - 1, prefix + ("   " if is_last else "│  "))

# ========================================
# >>>>>>>>>>>> Classe Tree <<<<<<<<<<<<<<<
# ========================================

class Tree:
    def __init__(self):
        self.root = None
        self.current_node = None
        self.node_counter = 0

    def create_node(self, value, parent=None):
        self.node_counter += 1
        return TreeNode(self.node_counter, value, parent)

    def add_rule_node(self, rule_value):
        new_node = self.create_node(rule_value, self.current_node)
        if self.root is None:
            self.root = new_node
        else:
            self.current_node.add_child(new_node)
        self.current_node = new_node

    def add_terminal_node(self, terminal_value):
        new_node = self.create_node(terminal_value, self.current_node)
        self.current_node.add_child(new_node)

    def end_rule_node(self):
        if self.current_node is not None:
            self.current_node = self.current_node.parent

    def print_tree(self):
        if self.root is not None:
            print("\nÁrvore Sintática:")
            self.root.print_node(is_last=True)
        else:
            print("Tree is empty.")