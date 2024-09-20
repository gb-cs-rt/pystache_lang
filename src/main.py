from compiler import Token, Lexer
from pprint import pp
import argparse

def main():

    parser = argparse.ArgumentParser(description='Compiler for the Pystache language')
    parser.add_argument("file", nargs="?", default=None, type=str)
    args = parser.parse_args()

    file = args.file if args.file else "src/test.pyst"

    data = open(file, "r").read()
    lexer = Lexer(data)
    tokens = lexer.getTokens()
    pp(tokens)

if __name__ == '__main__':
    main()