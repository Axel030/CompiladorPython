# compiler_service.py
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from interpreter import Interpreter
from token_type import TokenType


class CompilerService:
    def compilar(self, codigo):
        lexer = Lexer(codigo)
        tokens, errores_lexicos = lexer.analizar()

        parser = Parser(tokens)
        ast, errores_sintacticos = parser.analizar()

        semantic = SemanticAnalyzer()
        errores_semanticos = semantic.analizar(ast)

        errores = {
            "lexicos": errores_lexicos,
            "sintacticos": errores_sintacticos,
            "semanticos": errores_semanticos
        }

        hay_errores = (
            errores_lexicos or
            errores_sintacticos or
            errores_semanticos
        )

        salida = ""

        if not hay_errores:
            interpreter = Interpreter()
            salida = interpreter.ejecutar(ast)

        return tokens, errores, salida