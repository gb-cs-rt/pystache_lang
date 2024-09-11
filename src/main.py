from compiler import Token, Lexer
from pprint import pp

def main():

    data = " 23443.28943534 (5)  9soma_@ + 34 + 9 -\n 54*4 / 2 ^ 3"
    lexer = Lexer(data)
    tokens = lexer.getTokens()

    print(tokens)

if __name__ == '__main__':
    main()