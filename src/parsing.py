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
    is the function `code_expr`.

    A `code_expr` can be any of the valid CUADRO instructions.
    """

    tokens = CuadroLex.tokens

    # AST node types
    AST_NODE_TITLE_HEADER = "title-header"
    AST_NODE_INGREDIENTS_HEADER = "ingredients-header"
    AST_NODE_RECIPE_HEADER = "recipe-header"
    AST_NODE_INGREDIENT_DECLARATION = "ingredient-declaration"
    AST_FUNCTION_CALL_EOL = "function-call-eol"
    AST_FUNCTION_CALL = "function-call"
    AST_FUNCTION_ARGS = "function-args"

    # CUADRO must recognize Section headers
    @_("HEADER")
    def code_expr(self, p):
        if p.HEADER.count("#") == 2:
            return (self.AST_NODE_TITLE_HEADER, p.HEADER.replace("#", ""))
        elif p.HEADER.count("#") == 4:
            return (self.AST_NODE_INGREDIENTS_HEADER, p.HEADER.replace("#", ""))
        elif p.HEADER.count("#") == 6:
            return (self.AST_NODE_RECIPE_HEADER, p.HEADER.replace("#", ""))

    # Ingredient declaration
    @_("IDENTIFIER ASSIGN INTEGER GR_UNIT END_LINE")
    def code_expr(self, p):
        return (
            self.AST_NODE_INGREDIENT_DECLARATION,
            p.IDENTIFIER,
            p.INTEGER,
            p.GR_UNIT,
        )

    @_("IDENTIFIER OPEN_PARENT")
    def open_funct(self, p):
        return p.IDENTIFIER

    # Function calls
    @_('open_funct arglist CLOSE_PARENT END_LINE')
    def code_expr(self, p):
        return (
            self.AST_FUNCTION_CALL_EOL,
            [p.open_funct, p.arglist]
        )

    @_('IDENTIFIER')
    def arglist(self, p):
        return (
            self.AST_FUNCTION_ARGS,
            [p.IDENTIFIER]
        )

    @_('open_funct arglist CLOSE_PARENT')
    def funct_call(self, p):
        return (
            self.AST_FUNCTION_CALL,
            [p.open_funct, p.arglist]
        )

    # arguments list declaration
    @_('IDENTIFIER COMMA IDENTIFIER')
    def arglist(self, p):
        return (
            self.AST_FUNCTION_ARGS,
            [p.IDENTIFIER0, p.IDENTIFIER1]
        )

    @_('funct_call')
    def arglist(self, p):
        return (
            self.AST_FUNCTION_CALL,
            [p.funct_call[1][0], p.funct_call[1][1]]
        )

    @_('funct_call COMMA arglist')
    def arglist(self, p):
        return (
            self.AST_FUNCTION_CALL,
            [p.funct_call[1][0], p.funct_call[1][1], p.arglist]
        )

    @_('arglist COMMA IDENTIFIER')
    def arglist(self, p):
        return (
            self.AST_FUNCTION_ARGS,
            p.arglist[1].append(p.IDENTIFIER)  # Appends the to identifiers from arglist eval
        )

    @_('IDENTIFIER COMMA arglist')
    def arglist(self, p):
        return (
            self.AST_FUNCTION_ARGS,
            [p.IDENTIFIER] + p.arglist[1]
        )



if __name__ == "__main__":
    lxr = CuadroLex()
    psr = CuadroParser()

    # Test 1
    text = "# Pollo ASADO con BeRenJenas#"
    result = psr.parse(lxr.tokenize(text))
    print(result)
    print("\n")
    # TEST 2
    text = "atun_fresco=1000gr;"
    result = psr.parse(lxr.tokenize(text))
    print(result)

    # Test 2
    print('#' * 30)
    text = "hervir(docena_huevos);"
    result = psr.parse(lxr.tokenize(text))
    print(result)

    # Test 3
    print('#' * 30)
    text = "hervir(docena_huevos, pollo_desmenuzado);"
    result = psr.parse(lxr.tokenize(text))
    print(result)

    # Test 4
    print('#' * 30)
    text = "mezclar(hervir(docena_huevos, pollo_desmenuzado));"
    result = psr.parse(lxr.tokenize(text))
    print(result)


    # Test 5
    print('#' * 30)
    text = "mezclar(aderezo_mezcla, pimienta_10, queso_pecorino, hervir(docena_huevos, pollo_desmenuzado));"
    result = psr.parse(lxr.tokenize(text))
    print(result)


    # Test 6
    print('#' * 30)
    text = "mezclar(hervir(docena_huevos, pollo_desmenuzado), aderezo_mezcla);"
    result = psr.parse(lxr.tokenize(text))
    print(result)

