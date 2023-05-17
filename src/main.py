import click
import pprint

import click

from src.frontend import CuadroFrontend
from src.semantic_analyzer import SemanticAnalyzer
from src.parser import CuadroParser


@click.command()
@click.argument("filename", type=click.Path(exists=True))
def run(filename):
    tokens = CuadroFrontend(filename).process_file()
    asts = CuadroFrontend(filename).generate_asts(tokens)

    print("Program ASTS: ")
    for ast in asts:
        print(ast)

    print("\n")
    # Parse ingredients declaration
    pp = pprint.PrettyPrinter(indent=4)
    sem_analyzer = SemanticAnalyzer(asts)
    print("Ingredients identifiers table: ")
    pp.pprint(sem_analyzer._INGREDIENTS)

    # Validates the function calls in cooking steps
    sem_analyzer.validate_cooking_steps(asts)

    # We can start to semantically evaluate the instructions,
    # And maybe even generate the output code.
    for ast in asts:
        if ast[0] == CuadroParser.AST_NODE_FUNCTION_BASED_DECLARATION:
            sem_analyzer.process_cooking_step(ast)

    print("Semantic Analysis completed. Let's generate output")


if __name__ == '__main__':
    run()


