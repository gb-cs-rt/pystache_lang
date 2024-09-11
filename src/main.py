from compiler import Token, Lexer
from pprint import pp

def main():

    data = open("src/test.txt", "r").read()
    lexer = Lexer(data)
    tokens = lexer.getTokens()

    print(tokens)

if __name__ == '__main__':
    main()