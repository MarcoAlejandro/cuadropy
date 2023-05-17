"""
    This file contains the Lexer for ClangUchiha's CUADRO
    implementation
"""
from sly import Parser
from src.lexer import CuadroLex


class CuadroParser(Parser):
    """The Parser definition for our CUADRO implementation

    The Grammar is declared using the SLY library specification:
        https://sly.readthedocs.io/en/latest/sly.html#parsing-example

    Our implementation of CUADRO is represented by logical lines.
    Thus, our Start Symbol for the grammar of a logical line
    is the function `expr`.

    A `expr` can be any of the valid CUADRO instructions.
    """

    tokens = CuadroLex.tokens

    # AST node types

    AST_PROGRAM = "cuadro"

    AST_EXPRESSIONS = "expressions"

    AST_NODE_TITLE_HEADER = "title-header"
    AST_NODE_INGREDIENTS_HEADER = "ingredients-header"
    AST_NODE_RECIPE_HEADER = "recipe-header"

    AST_NODE_INGREDIENT_DECLARATION = "ingredient-declaration"
    AST_NODE_FUNCTION_BASED_DECLARATION = "variable-declaration"

    AST_FUNCTION_CALL = "function-call"

    AST_ARGLIST = "args-list"
    AST_ARGS = "args"
    AST_ARGUMENT = "argument"

    AST_UNIT = "unit"
    AST_NUMBER = "number"
    AST_QUANTITY = "quantity"
    AST_STRING = "string"

    AST_IDENTIFIER = "identifier"

    # cuadro : expressions

    @_("expressions")
    def cuadro(self, p):
        # return (self.AST_PROGRAM, p.expressions[1])
        return p.expressions[1]

    # expressions : expr
    #             | expressions expr

    @_("expr")
    def expressions(self, p):
        return (self.AST_EXPRESSIONS, [p.expr])

    @_("expressions expr")
    def expressions(self, p):
        return (self.AST_EXPRESSIONS, p.expressions[1] + [p.expr])

    # top level expresions that CUADRO supports
    # expr : HEADER
    #      | declaration END_LINE
    #      | funct_call END_LINE

    @_("HEADER")
    def expr(self, p):
        if p.HEADER.count("#") == 2:
            return (self.AST_NODE_TITLE_HEADER, p.HEADER.replace("#", ""))
        elif p.HEADER.count("#") == 4:
            return (self.AST_NODE_INGREDIENTS_HEADER, p.HEADER.replace("#", ""))
        elif p.HEADER.count("#") == 6:
            return (self.AST_NODE_RECIPE_HEADER, p.HEADER.replace("#", ""))

    @_("declaration END_LINE", "funct_call END_LINE")
    def expr(self, p):
        return p[0]

    # declaration : IDENTIFIER ASSIGN quantity
    #             | IDENTIFIER ASSIGN funct_call

    @_("IDENTIFIER ASSIGN quantity")
    def declaration(self, p):
        return (
            self.AST_NODE_INGREDIENT_DECLARATION,
            p.IDENTIFIER,
            p.quantity,
        )

    @_("IDENTIFIER ASSIGN funct_call")
    def declaration(self, p):
        return (
            self.AST_NODE_FUNCTION_BASED_DECLARATION,
            p.IDENTIFIER,
            p.funct_call,
        )

    # funct_call : IDENTIFIER arglist

    @_("IDENTIFIER arglist")
    def funct_call(self, p):
        return (self.AST_FUNCTION_CALL, p.IDENTIFIER, p.arglist[1])

    # arglist : OPEN_PARENT args CLOSE_PARENT

    @_("OPEN_PARENT args CLOSE_PARENT")
    def arglist(self, p):
        return (self.AST_ARGLIST, p.args[1])

    # args : argument
    #      | argument COMMA args
    #      | empty

    @_("argument")
    def args(self, p):
        return (self.AST_ARGS, [p.argument[1]])

    @_("argument COMMA args")
    def args(self, p):
        return (self.AST_ARGS, [p.argument[1]] + p.args[1])

    @_("empty")
    def args(self, p):
        return (self.AST_ARGS, [])

    # argument : funct_call
    #          | identifier
    #          | string
    #          | quantity

    @_("funct_call", "identifier", "string", "quantity")
    def argument(self, p):
        return (self.AST_ARGUMENT, p[0])

    # string : STRING

    @_("STRING")
    def string(self, p):
        return (self.AST_STRING, p.STRING)

    # quantity : number unit

    @_("number unit")
    def quantity(self, p):
        return (self.AST_QUANTITY, p.number[1], p.unit[1])

    # number : FLOAT
    #        | INTEGER

    @_("FLOAT", "INTEGER")
    def number(self, p):
        return (self.AST_NUMBER, p[0])

    # unit : GR_UNIT
    #      | MLTS_UNIT
    #      | CARDINAL_UNIT
    #      | empty

    @_("GR_UNIT", "MLTS_UNIT", "CARDINAL_UNIT")
    def unit(self, p):
        return (self.AST_UNIT, p[0])

    @_("empty")  # default
    def unit(self, p):
        return (self.AST_UNIT, CuadroLex.CARDINAL_UNIT)

    # identifier : IDENTIFIER

    @_("IDENTIFIER")
    def identifier(self, p):
        return (self.AST_IDENTIFIER, p.IDENTIFIER)

    # empty : epsilon

    @_("")
    def empty(self, p):
        pass
