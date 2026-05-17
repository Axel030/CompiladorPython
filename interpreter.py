from parser import Declaracion, Asignacion, Imprimir, Si, Mientras, Literal, Variable, Binaria
from token_type import TokenType


class Interpreter:
    def __init__(self):
        self.variables = {}
        self.salida = []

    def ejecutar(self, sentencias):
        for sentencia in sentencias:
            self.ejecutar_sentencia(sentencia)

        return "\n".join(self.salida)

    def ejecutar_sentencia(self, sentencia):
        if isinstance(sentencia, Declaracion):
            self.variables[sentencia.nombre] = self.evaluar(sentencia.expresion)

        elif isinstance(sentencia, Asignacion):
            self.variables[sentencia.nombre] = self.evaluar(sentencia.expresion)

        elif isinstance(sentencia, Imprimir):
            valor = self.evaluar(sentencia.expresion)
            self.salida.append(str(valor))

        elif isinstance(sentencia, Si):
            if self.evaluar(sentencia.condicion):
                for s in sentencia.cuerpo:
                    self.ejecutar_sentencia(s)
            else:
                for s in sentencia.cuerpo_sino:
                    self.ejecutar_sentencia(s)

        elif isinstance(sentencia, Mientras):
            contador_seguridad = 0

            while self.evaluar(sentencia.condicion):
                for s in sentencia.cuerpo:
                    self.ejecutar_sentencia(s)

                contador_seguridad += 1

                if contador_seguridad > 1000:
                    self.salida.append("Error: posible ciclo infinito detenido")
                    break

    def evaluar(self, expr):
        if isinstance(expr, Literal):
            return expr.valor

        if isinstance(expr, Variable):
            return self.variables.get(expr.nombre)

        if isinstance(expr, Binaria):
            izquierda = self.evaluar(expr.izquierda)
            derecha = self.evaluar(expr.derecha)
            operador = expr.operador.tipo

            if operador == TokenType.SUMA:
                return izquierda + derecha

            if operador == TokenType.RESTA:
                return izquierda - derecha

            if operador == TokenType.MULTIPLICACION:
                return izquierda * derecha

            if operador == TokenType.DIVISION:
                return izquierda / derecha

            if operador == TokenType.MAYOR:
                return izquierda > derecha

            if operador == TokenType.MENOR:
                return izquierda < derecha

            if operador == TokenType.MAYOR_IGUAL:
                return izquierda >= derecha

            if operador == TokenType.MENOR_IGUAL:
                return izquierda <= derecha

            if operador == TokenType.IGUALDAD:
                return izquierda == derecha

            if operador == TokenType.DIFERENTE:
                return izquierda != derecha

        return None