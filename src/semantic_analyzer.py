from typing import List, Dict
from parser.parser import CuadroParser
import abc


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


class CookingStep(abc.ABC):
    def __init__(self, step: str, ingredients_table, *ingredients):
        self.step: str = step
        self.ingredients_table = ingredients_table
        self.ingredients: List[str] = list(ingredients)

    @classmethod
    @abc.abstractmethod
    def lexical_name(cls) -> str:
        pass

    def validate_ingredients(self):
        for ing in self.ingredients:
            if ing not in self.ingredients_table:
                raise RuntimeError(f"Ingredient {ing} was used but never declared")

            if not self.ingredients_table[ing].is_usable():
                raise RuntimeError(f"Cooking step {self.step} can't use ingredient {ing}. Did you already used it?")

    def do(self):
        # At this point somebody should have used `validate_ingredients`
        # Children classes can implement additional logic on top of this one
        for ing in self.ingredients:
            self.ingredients_table[ing].use()


class Fillet(CookingStep):
    def __init__(self, ingredients_table, *ingredients):
        super(Fillet, self).__init__(self.__class__.__name__, ingredients_table, ingredients)

    @classmethod
    def lexical_name(cls) -> str:
        return "filetear"


class Season(CookingStep):
    def __init__(self, ingredients_table, *ingredients):
        super(Season, self).__init__(self.__class__.__name__, ingredients_table, ingredients)

    @classmethod
    def lexical_name(cls) -> str:
        return "sazonar"


class Fry(CookingStep):
    def __init__(self, ingredients_table, *ingredients):
        super(Fry, self).__init__(self.__class__.__name__, ingredients_table, ingredients)

    @classmethod
    def lexical_name(cls) -> str:
        return "sarten"


class Mix(CookingStep):
    def __init__(self, ingredients_table, *ingredients):
        super(Mix, self).__init__(self.__class__.__name__, ingredients_table, ingredients)

    @classmethod
    def lexical_name(cls) -> str:
        return "mezclar"


class SemanticAnalyzer:
    def __init__(
        self,
        asts: List
    ):
        self._INGREDIENTS: Dict[str, Ingredient] = {}
        self.process_ingredients(asts)

        self._COOKING_STEPS: Dict[str, CookingStep] = {
            Fillet.lexical_name(): Fillet,
            Season.lexical_name(): Season,
            Fry.lexical_name(): Fry,
            Mix.lexical_name(): Mix
        }

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

    def validate_cooking_steps(self, asts: List):
        """Validates the existence of function calls in the program. """
        for ast in asts:
            if ast[0] == CuadroParser.AST_NODE_FUNCTION_BASED_DECLARATION:
                funct_call = ast[2]
                funct_call_name = funct_call[1]
                if funct_call_name not in self._COOKING_STEPS:
                    raise RuntimeError(f"Calling unknown Cooking Step: {funct_call_name}")





