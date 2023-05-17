from typing import List

from src.lexer import CuadroLex
from src.parser import CuadroParser


class CuadroFrontend:
    """The CuadroFrontend will be in charge of
    processing the input file and communicate:
        - Lexycal Errors
        - Parsing Erros

    If everything is OK, it will pass the in-memory
    information to the Semantic Analysis module.
    """
    def __init__(self, filename):
        self.filename = filename
        self.lxr = CuadroLex()
        self.parser = CuadroParser()

    def process_file(self):
        tokens = []
        with open(self.filename, "r") as f:
            try:
                for line in f:
                    result = self.lxr.tokenize(line)
                    tokens.append(result)
            except Exception as e:
                # TODO: Handle the possible erros as strong types
                print(f"Syntax Error error: {e} ")
                raise SyntaxError(e.message)

        # Up to this point, the lexycal analysis was successful
        return tokens

    def generate_asts(self, tokens: List):
        asts = []
        for tok in tokens:
            ast = self.parser.parse(tok)
            asts.append(ast[0])
        return asts
