from fpdf import FPDF

from src.semantic_analyzer import SemanticAnalyzer, CookingStep, Ingredient


class OutputGenerator:
    def __init__(
        self,
        filename,
        semantic_analyzer: SemanticAnalyzer
    ):
        self.filename = filename
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        self._semantic_analyzer = semantic_analyzer

    def _add_title(self, title):
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=16, style='B')
        self.pdf.cell(0, 10, title, ln=1, align='C')

    def _add_text(self, text):
        self.pdf.write(10, text)

    def _add_newline(self):
        self.pdf.ln()

    def save(self):
        self.pdf.output(self.filename)

    def _out_recipe_title(self, ast):
        self._add_title(ast[1])

    def _out_ingredient_declaration(self, ast):
        self._add_text(f"Ingrediente -> {ast[1]}, {ast[2][1]}{ast[2][2]}")

    def _out_cooking_step(self, step: CookingStep, depth=0):
        for i in range(depth*2):
            self._add_text('\t')

        self._add_text(f"Paso: {step.lexical_name}: ")
        self._add_newline()
        for ing in step.ingredients:
            if isinstance(ing, Ingredient):
                self._add_text(ing.name)
                self._add_newline()
            elif isinstance(ing, CookingStep):
                self._out_cooking_step(ing)
