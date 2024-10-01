from utils import TokenIterator

# ========================================
# >>>>>>>>>>> Classe Parser <<<<<<<<<<<<<
# ========================================

class Parser:

    def __init__(self, tokens):
        self.tokens = TokenIterator(tokens)
        