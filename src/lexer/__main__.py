"""
Try it with `python -m src.lexer`
"""
from . import CuadroLex


lxr = CuadroLex()

cases = [
    "# Pollo con Arroz #",
    "## Ingredientes ##",
    "### Pasos a seguir ###",
    "atun_enlatado = 1cu;",
    "tomate_rojo = 1000ml;",
    "200.",
    "200",
    ".200",
    "200.021",
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
mezcla_aderezo = mezclar([ralladura_ajo, mayonesa, ralladura_limon]);
mecla_aderezo = mezclar([clara_huevo, mezcla_aderezo]) ;
lomo_salmon_napado = napar(salmon, mezcla_aderezo) ;
hornear(lomo_salmon_napado, 10) ;
""",
]


for data in cases:
    print(f"TEST: '{data}' ")
    for tok in lxr.tokenize(data):
        print("type=%r, value=%r" % (tok.type, tok.value))
    print("\n\n")
