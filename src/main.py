from compiler import Token, Lexer
from pprint import pp

def main():

    data = " 2 + 34 + 9 -\n 54*4 / 2 ^ 3"
    lexer = Lexer(data)
    tokens = lexer.getTokens()

    pp(tokens)

if __name__ == '__main__':
    main()