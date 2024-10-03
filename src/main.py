#!/usr/bin/python3
from lexer import Lexer
from parser import Parser
from pprint import pp
import argparse

def main():

    parser = argparse.ArgumentParser(description='Compiler for the Pystache language')
    parser.add_argument("file", nargs="?", default=None, type=str)
    parser.add_argument("-tree", nargs="?", default=False, type=bool)
    args = parser.parse_args()

    if args.file is None:
        print("Nenhum arquivo providenciado")
        return

    data = open(args.file, "r").read()
    lexer = Lexer(data)
    tokens = lexer.getTokens()

    if tokens:
        parser = Parser(tokens.copy(), data)
        parserResult, parserTree = parser.parse()

        if args.tree is not False:
            parserTree.print_tree()

        if parserResult: print("Correto!")

if __name__ == '__main__':
    main()