"""
    This file contains the Lexer for ClangUchiha's CUADRO
    implementation
"""
from sly import Parser
from src.lexer import CuadroLex


class CuadroParser(Parser):
    """The Parser definition for our CUADRO implementation
    """
    tokens = CuadroLex.tokens

    # AST node types
    AST_NODE_TITLE_HEADER='title-header'
    AST_NODE_INGREDIENTS_HEADER='ingredients-header'
    AST_NODE_RECIPE_HEADER='recipe-header'
    AST_NODE_INGREDIENT_DECLARATION='ingredient-declaration'

    # CUADRO must recognize Section headers
    @_('HEADER')
    def code(self, p):
        if p.HEADER.count('#') == 2:
            return (self.AST_NODE_TITLE_HEADER, p.HEADER.replace('#', ''))
        elif p.HEADER.count('#') == 4:
            return (self.AST_NODE_INGREDIENTS_HEADER, p.HEADER.replace('#', ''))
        elif p.HEADER.count('#') == 6:
            return (self.AST_NODE_RECIPE_HEADER, p.HEADER.replace('#', ''))

    @_('IDENTIFIER ASSIGN NUMBER GR_UNIT')
    def code(self, p):
        return (self.AST_NODE_INGREDIENT_DECLARATION, p.IDENTIFIER, p.NUMBER, p.GR_UNIT)



if __name__ == '__main__':
    lxr = CuadroLex()
    psr = CuadroParser()

    # Test 1
    text = '# Pollo ASADO con BeRenJenas#'
    result = psr.parse(lxr.tokenize(text))
    print(result)
    print('\n')
    # TEST 2
    text = 'atun_fresco=1000gr'
    result = psr.parse(lxr.tokenize(text))
    print(result)
