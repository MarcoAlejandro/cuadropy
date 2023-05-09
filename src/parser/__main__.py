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
    "atun_hervido=hervir(atun_fresco);",
    "hervir(docena_huevos);",
    "hervir(docena_huevos, pollo_desmenuzado);",
    "mezclar(hervir(docena_huevos, pollo_desmenuzado));",
    "mezclar(aderezo_mezcla, pimienta_10, queso_pecorino, hervir(docena_huevos, pollo_desmenuzado), aceite);",
    "mezclar(hervir(docena_huevos, pollo_desmenuzado), aderezo_mezcla);",
    "mezclar(hervir(), aderezo_mezcla);",
    "atun_fresco=1000gr;atun_fresco=1000gr;",
]

for data in cases:
    print("#" * 30)

    print("### Program")
    print(data)

    tokens = lxr.tokenize(data)
    # print("### Tokens")
    # for tok in lxr.tokenize(data):
    #     print("type=%r, value=%r" % (tok.type, tok.value))

    expressions = psr.parse(tokens)
    print("### Expresisons")
    for expr in expressions:
        print(expr)

    print("\n")
