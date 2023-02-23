"""
    This file contains the Lexer for ClangUchiha's CUADRO
    implementation
"""
from sly import Lexer, Parser



class CuadroParser(Parser):
    tokens = CuadroLex.tokens

    def __init__(self):
        self.names = {}

    @_('SECTION_OPEN WHITESPACE FREE_TEXT EOL')
    def section_title(self, title):
        self.recipe_title=title

if __name__ == '__main__':
    lxr = CuadroLex()
    psr = CuadroParser()

    # If silent, success
    psr.parse(lxr.tokenize('#  pollo asado con gengibre;'))
