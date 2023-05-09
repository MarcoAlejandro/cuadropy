from src.lexer import CuadroLex
from src.parser import CuadroParser


class CuadroFileProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.lxr = CuadroLex()
        self.parser = CuadroParser()

    def process_file(self):
        with open(self.filename, "r") as f:
            for line in f:
                result = self.parser.parse(self.lxr.tokenize(line))
                print(result)
