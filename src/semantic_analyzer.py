from typing import List, Dict
from parser.parser import CuadroParser


class Amount:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __str__(self):
        return f"{self.value}{self.unit}"


class Grams(Amount):
    def __init__(self, value):
        super().__init__(value, "gr")


class Milliliters(Amount):
    def __init__(self, value):
        super().__init__(value, "ml")


class CardinalUnits(Amount):
    def __init__(self, value):
        super().__init__(value, "cu")


class Ingredient:
    """The Ingredient class holds the information of a declared ingredient.

    For the semantic analysis, each Ingredient is identified by an unique
    Lexical identifier.

    The amount
    """
    def __init__(self, name: str, amount: Amount):
        self.name: str = name
        self.amount: Amount = amount
        self._usable: bool = True

    def is_usable(self) -> bool:
        return self._usable

    def use(self):
        self._usable = False


class SemanticAnalyzer:
    def __init__(
        self,
        asts: List
    ):
        self._INGREDIENTS: Dict[str, Ingredient] = {}
        self.process_ingredients(asts)

    def _get_quantity(self, amount, unit):
        if unit == "gr":
            return Grams(amount)

        if unit == "ml":
            return Milliliters(amount)

        # then it's cardinal unit
        return CardinalUnits(amount)

    def process_ingredients(self, asts: List):
        """We process the list of ingredients declaration from the AST nodes.

        Doing this on a single pass over the program, allows to build the _INGREDIENTS
            table of identifiers.
        """
        for ast in asts:
            if ast[0] == CuadroParser.AST_NODE_INGREDIENT_DECLARATION:
                q = self._get_quantity(ast[2][1], ast[2][2])
                ingredient = Ingredient(ast[1], q)

                if ingredient.name in self._INGREDIENTS:
                    raise RuntimeError(f"The identifier {ingredient.name} "
                                       f"must be declared only once.")

                self._INGREDIENTS[ingredient.name] = ingredient


