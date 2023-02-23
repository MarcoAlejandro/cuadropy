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
        'WHITESPACE',
        'SECTION_OPEN',
        'NUMBER',
        'IDENTIFIER',
        'SECTION_TEXT',
        'INGREDIENT_DECLARATION_LINE_START',
        'ASSIGN',
        'LPAREN',
        'RPAREN',
        'EOL',
    }

    # TOKENS
    SECTION_TEXT = r'#\s\s*[a-zA-Z][a-zA-Z\s]*'
    WHITESPACE = r'\s\s*'
    SECTION_OPEN = r'#'
    NUMBER = r'\d+'
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    EOL = r';'
    INGREDIENT_DECLARATION_LINE_START=r'>'

    # Ignored pattern because we use logical lines with EOL
    ignore_newline = r'\n+'
    ignore = '\t'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


if __name__ == '__main__':
    lxr = CuadroLex()
    data = '### Pollo con Arroz;'
    print("TEST 1")
    for tok in lxr.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))

    data = ">    atun_enlatado;"
    print("\nTEST 2")
    for tok in lxr.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
