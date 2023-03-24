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

    tokens = {
        "END_LINE",
        "ASSIGN",
        "OPEN_PARENT",
        "CLOSE_PARENT",
        "OPEN_SQUARE_BRACKETS",
        "CLOSE_SQUARE_BRACKETS",
        "HEADER",
        "IDENTIFIER",
        "STRING",
        "FLOAT",
        "INTEGER",
        "COMMA",
        "MLTS_UNIT",
        "GR_UNIT",
        "CARDINAL_UNIT",
        # "WHITESPACE",
    }

    """
    In CUADRO, all lines end with a `;` char.
    
    Note: There are some lines that do not require the `;`:
        - Sections Headers don't require `;`
        
    We use assignments.
    And Parenthesis
    """
    END_LINE = r";"
    ASSIGN = r"="
    COMMA = r","
    OPEN_PARENT = r"\("
    CLOSE_PARENT = r"\)"
    OPEN_SQUARE_BRACKETS = r"\["
    CLOSE_SQUARE_BRACKETS = r"\]"

    """
    In CUADRO, 3 main sections are always required.
        1. Title section: All recipes should have a title! An example: 
            " # Salmón con Papas horneado #"
        
        2. Ingredients Section
            " ## Ingredientes ##"
            
        3. Recipe Section
            " ### Instrucciones ###"
    """
    HEADER = r"\#{1,3}\s*[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s]*\s*\#{1,3}"

    """
    We need to recognize numbers to represent quiantities 
    of the ingredients.

    We also need to recognize measurement units
    """

    @_(r"\.\d+", r"\d+\.\d*")
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r"\d+")
    def INTEGER(self, t):
        t.value = int(t.value)
        return t

    MLTS_UNIT = r"ml"
    GR_UNIT = r"gr"
    CARDINAL_UNIT = r"un"

    STRING = r"\"[a-zA-Z0-9À-ÿ\s]*\""

    """
    In CUADRO, identifiers can be used to declare variable names!
    For example:
        " atun_fresco = 1000g; "
    """
    IDENTIFIER = r"[a-zA-Z_][a-zA-Z0-9_]*"

    """
    We are identifiying whitespaces
    """
    # WHITESPACE = r"\s+"

    # Ignored pattern because we use logical lines with EOL
    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")

    ignore_whitespaces = r"\s+"
    ignore_comments = r"//.*"
    ignore = "\t"

    #  ##################### Match Actions for this Lexer #####################

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
