"""
    This file contains the Lexer for ClangUchiha's CUADRO
    implementation.
"""
from sly import Lexer


class CuadroLex(Lexer):
    """The Lexer contains the declaration for ALL THE POSSIBLE TOKENS of our
    language.

    TODO: Read all this doc
        https://sly.readthedocs.io/en/latest/sly.html#writing-a-lexer
        to ensure that we are not using something in a bad way.
    """

    """
    In CUADRO, all lines end with a `;` char.
    
    Note: There are some lines that do not require the `;`:
        - Sections Headers don't require `;`
        
    We use assignments.
    And Parenthesis
    """
    WHITESPACE = r'\s\s*'
    END_LINE = r";"
    ASSIGN = r"="
    OPEN_PARENT = r"\("
    CLOSE_PARENT = r"\)"

    """
    In CUADRO, 3 main sections are always required.
        1. Title section: All recipes should have a title! An example: 
            " # Salmón con Papas horneado #"
        
        2. Ingredients Section
            " ## Ingredientes ##"
            
        3. Recipe Section
            " ### Instrucciones ###"
    """
    HEADER = r"\#{1,3}\s*[a-zA-Z][a-zA-Z\s]*\s*\#{1,3}"

    """
    We need to recognize numbers to represent quiantities 
    of the ingredients. 
    
    We also need to recognize measurement units
    """
    NUMBER = r"\d+"
    MLTS_UNIT = r"ml"
    GR_UNIT = r'gr'
    CARDINAL_UNIT = r'un'

    """
    In CUADRO, identifiers can be used to declare variable names! 
    For example: 
        " atun_fresco = 1000g; "
    """
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

    tokens = {
        "HEADER",
        "IDENTIFIER",
        "END_LINE",
        "WHITESPACE",
        "ASSIGN",
        "OPEN_PARENT",
        "CLOSE_PARENT",
        "NUMBER",
        "MLTS_UNIT",
        "GR_UNIT",
        "CARDINAL_UNIT",
    }

    # Ignored pattern because we use logical lines with EOL
    ignore_newline = r'\n+'
    ignore = '\t'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

    ######### Match Actions for this Lexer ###########################

    # Numbers should have numeric value
    @_(r"\d+")
    def NUMBER(self, t):
        t.value = int(t.value)
        return t


if __name__ == '__main__':
    lxr = CuadroLex()

    data = '# Pollo con Arroz #'
    print(f"TEST 1: '{data}' ")
    for tok in lxr.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
    print('\n')

    data = '## Ingredientes ##'
    print(f"TEST 2: '{data}' ")
    for tok in lxr.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
    print('\n')

    data = '### Pasos a seguir ###'
    print(f"TEST 1: '{data}' ")
    for tok in lxr.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
    print('\n')

    data = 'atun_enlatado = 1un;'
    print(f"TEST 1: '{data}' ")
    for tok in lxr.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
    print('\n')

    data = 'tomate_rojo = 1000ml;'
    print(f"TEST 1: '{data}' ")
    for tok in lxr.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
    print('\n')

