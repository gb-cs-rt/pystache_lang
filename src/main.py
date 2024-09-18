from compiler import Token, Lexer
from pprint import pp

def main():

    data = open("src/specifications.spl", "r").read()
    lexer = Lexer(data)
    tokens = lexer.getTokens()
    pp(tokens)


if __name__ == '__main__':
    main()