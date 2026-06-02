#semantic.py
from parser import Declaracion, Asignacion, Imprimir, Si, Mientras, Para, Literal, Variable, Binaria
from token_type import TokenType

class ErrorSemantico:
    def __init__(self, mensaje, linea, columna):
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f"{self.mensaje} en L{self.linea}, C{self.columna}"


class SemanticAnalyzer:
    def __init__(self):
        self.tabla_simbolos = {}
        self.errores = []

    def analizar(self, sentencias):
        for sentencia in sentencias:
            self.analizar_sentencia(sentencia)

        return self.errores

    def analizar_sentencia(self, sentencia):
        if isinstance(sentencia, Declaracion):
            self.analizar_declaracion(sentencia)

        elif isinstance(sentencia, Asignacion):
            self.analizar_asignacion(sentencia)

        elif isinstance(sentencia, Imprimir):
            self.obtener_tipo(sentencia.expresion)

        elif isinstance(sentencia, Si):
            tipo_condicion = self.obtener_tipo(sentencia.condicion)

            if tipo_condicion != "bool":
                self.errores.append(ErrorSemantico(
                    "La condición del si debe ser booleana",
                    0,
                    0
                ))

            for s in sentencia.cuerpo:
                self.analizar_sentencia(s)

            for s in sentencia.cuerpo_sino:
                self.analizar_sentencia(s)

        elif isinstance(sentencia, Mientras):
            tipo_condicion = self.obtener_tipo(sentencia.condicion)

            if tipo_condicion != "bool":
                self.errores.append(ErrorSemantico(
                    "La condición del mientras debe ser booleana",
                    0,
                    0
                ))

            for s in sentencia.cuerpo:
                self.analizar_sentencia(s)

        elif isinstance(sentencia, Para):
            self.analizar_sentencia(sentencia.inicializacion)
            tipo_condicion = self.obtener_tipo(sentencia.condicion)

            if tipo_condicion != "bool":
                self.errores.append(ErrorSemantico(
                    "La condición del for debe ser booleana",
                    0,
                    0
                ))

            self.analizar_sentencia(sentencia.incremento)

            for s in sentencia.cuerpo:
                self.analizar_sentencia(s)

    def analizar_declaracion(self, sentencia):
        if sentencia.nombre in self.tabla_simbolos:
            self.errores.append(ErrorSemantico(
                f"La variable '{sentencia.nombre}' ya fue declarada",
                sentencia.token.linea,
                sentencia.token.columna
            ))
            return

        tipo_expresion = self.obtener_tipo(sentencia.expresion)

        if not self.son_compatibles(sentencia.tipo_dato, tipo_expresion):
            self.errores.append(ErrorSemantico(
                f"No se puede asignar '{tipo_expresion}' a una variable de tipo '{sentencia.tipo_dato}'",
                sentencia.token.linea,
                sentencia.token.columna
            ))

        self.tabla_simbolos[sentencia.nombre] = sentencia.tipo_dato

    def analizar_asignacion(self, sentencia):
        if sentencia.nombre not in self.tabla_simbolos:
            self.errores.append(ErrorSemantico(
                f"La variable '{sentencia.nombre}' no fue declarada",
                sentencia.token.linea,
                sentencia.token.columna
            ))
            return

        tipo_variable = self.tabla_simbolos[sentencia.nombre]
        tipo_expresion = self.obtener_tipo(sentencia.expresion)

        if not self.son_compatibles(tipo_variable, tipo_expresion):
            self.errores.append(ErrorSemantico(
                f"No se puede asignar '{tipo_expresion}' a la variable '{sentencia.nombre}' de tipo '{tipo_variable}'",
                sentencia.token.linea,
                sentencia.token.columna
            ))

    def obtener_tipo(self, expr):
        if isinstance(expr, Literal):
            return expr.tipo

        if isinstance(expr, Variable):
            if expr.nombre not in self.tabla_simbolos:
                self.errores.append(ErrorSemantico(
                    f"La variable '{expr.nombre}' no fue declarada",
                    expr.token.linea,
                    expr.token.columna
                ))
                return "desconocido"

            return self.tabla_simbolos[expr.nombre]

        if isinstance(expr, Binaria):
            tipo_izq = self.obtener_tipo(expr.izquierda)
            tipo_der = self.obtener_tipo(expr.derecha)
            operador = expr.operador.tipo

            if operador in [
                TokenType.MAYOR,
                TokenType.MENOR,
                TokenType.MAYOR_IGUAL,
                TokenType.MENOR_IGUAL,
                TokenType.IGUALDAD,
                TokenType.DIFERENTE
            ]:
                return "bool"

            if operador == TokenType.SUMA and tipo_izq == "string" and tipo_der == "string":
                return "string"

            if tipo_izq in ["int", "double"] and tipo_der in ["int", "double"]:
                if tipo_izq == "double" or tipo_der == "double":
                    return "double"
                return "int"

            self.errores.append(ErrorSemantico(
                f"Operación inválida entre '{tipo_izq}' y '{tipo_der}'",
                expr.operador.linea,
                expr.operador.columna
            ))

            return "desconocido"

        return "desconocido"

    def son_compatibles(self, tipo_variable, tipo_expresion):
        if tipo_variable == tipo_expresion:
            return True

        if tipo_variable == "double" and tipo_expresion == "int":
            return True

        return False