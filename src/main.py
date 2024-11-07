#!/usr/bin/python3
from lexer import Lexer
from parser import Parser
from semantic import Semantic
from converter import Converter
from pprint import pp
import argparse
import os
import subprocess

def main():

    parser = argparse.ArgumentParser(description='Compiler for the Pystache language')
    parser.add_argument("file", nargs="?", default=None, type=str)
    parser.add_argument("-tree", nargs="?", default=False, type=bool)
    parser.add_argument("-tokens", nargs="?", default=False, type=bool)
    args = parser.parse_args()

    if args.file is None:
        print("Nenhum arquivo providenciado")
        return

    data = open(args.file, "r").read()
    lexer = Lexer(data)
    tokens = lexer.getTokens()

    if tokens:

        if args.tokens is not False:
            pp(tokens)

        parser = Parser(tokens.copy(), data)
        parserResult, parserTree = parser.parse()

        if args.tree is not False:
            parserTree.print_tree()

        if parserResult:
            # print("Sintaxe correta.")

            semantic = Semantic(parserTree, data)
            semanticResult, typeHash = semantic.run()

            if args.tree is not False:
                pp(typeHash)

            if semanticResult:

                # print("Semântica correta.")
                converter = Converter(parserTree, typeHash)
                converter.convert()

                compile_result = subprocess.run(["g++", "output.cpp", "-o", "output"])
                if compile_result.returncode == 0:
                    subprocess.run(["./output"])

if __name__ == '__main__':
    main()