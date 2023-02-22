"""
    This file contains the Lexer for ClangUchiha's CUADRO
    implementation
"""
from sly import Lexer, Parser


class CuadroLex(Lexer):
    """
    We declare the tokens for our language.

    We should declare all the tokens in a plain set!

    With the tokens we later define grammars based on non-terminals and
        terminal tokens.

    """
    tokens = {
        'WHITESPACE', 'SECTION_OPEN', 'NUMBER', 'FREE_TEXT', 'ASSIGN',
        'LPAREN', 'RPAREN', 'EOL',
    }

    # TOKENS
    WHITESPACE = r'\s\s*'
    SECTION_OPEN = r'#'
    NUMBER = r'\d+'
    FREE_TEXT = r'[a-zA-Z][a-zA-Z\s]*'
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    EOL = r';'

    # Ignored pattern because we use logical lines with EOL
    ignore_newline = r'\n+'
    ignore = '\t'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


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
