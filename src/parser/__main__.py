"""
Try it with `python -m src.parser`
"""

from src.lexer import CuadroLex
from . import CuadroParser

lxr = CuadroLex()
psr = CuadroParser()

cases = [
    "# Pollo ASADO con BeRenJenas#",
    "atun_fresco=1000gr;",
    "hervir(docena_huevos);",
    "hervir(docena_huevos, pollo_desmenuzado);",
    "mezclar(hervir(docena_huevos, pollo_desmenuzado));",
    "mezclar(aderezo_mezcla, pimienta_10, queso_pecorino, hervir(docena_huevos, pollo_desmenuzado));",
    "mezclar(hervir(docena_huevos, pollo_desmenuzado), aderezo_mezcla);",
]

for data in cases:
    print("#" * 30)
    result = psr.parse(lxr.tokenize(data))
    print(result)
    print("\n")
