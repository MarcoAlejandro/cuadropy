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
    """
# Salmón al Horno #

## Ingredientes a utilizar ##
lomo_salmon = 2cu;
mayonesa = 80 gr;
clara_huevo = 1cu;
limon = 1cu;
sal = 10gr;


### Pasos para preparar ###
encender_horno (200) ; // Encender estufa a 200 grados.
limpiar(lomo_salmon, "Sin escamas por favor") ;
limpiar(ajo, "Pelar el diente de ajo");
ralladura_ajo = rallar(ajo, .5);
ralladura_limon = rallar(limon, 1);
mezcla_aderezo = mezclar(ralladura_ajo, mayonesa, ralladura_limon);
mecla_aderezo = mezclar(clara_huevo, mezcla_aderezo) ;
lomo_salmon_napado = napar(salmon, mezcla_aderezo) ;
hornear(lomo_salmon_napado, 10) ;
""",
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
