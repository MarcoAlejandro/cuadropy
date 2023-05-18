import pprint
import click
from src.frontend import CuadroFrontend
from src.output_generator import OutputGenerator
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

    sem_analyzer.validate_ast()

    # We can start to semantically evaluate the instructions,
    # And maybe even generate the output code.
    cooking_steps = []
    for ast in asts:
        if ast[0] == CuadroParser.AST_NODE_FUNCTION_BASED_DECLARATION:
            cooking_steps.append(sem_analyzer.process_cooking_step(ast))

    print("Semantic Analysis completed. Let's generate output")

    og = OutputGenerator("out.pdf", sem_analyzer)

    for ast in asts:
        og.generate(ast)
    for cs in cooking_steps:
        og.generate(cs)
    og.write()
    print("Output has been generated")


if __name__ == "__main__":
    run()
