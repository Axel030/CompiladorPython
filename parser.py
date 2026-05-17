from token_type import TokenType


class ErrorSintactico:
    def __init__(self, mensaje, linea, columna):
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f"{self.mensaje} en L{self.linea}, C{self.columna}"


class Literal:
    def __init__(self, valor, tipo):
        self.valor = valor
        self.tipo = tipo


class Variable:
    def __init__(self, nombre, token):
        self.nombre = nombre
        self.token = token


class Binaria:
    def __init__(self, izquierda, operador, derecha):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha


class Declaracion:
    def __init__(self, tipo_dato, nombre, expresion, token):
        self.tipo_dato = tipo_dato
        self.nombre = nombre
        self.expresion = expresion
        self.token = token


class Asignacion:
    def __init__(self, nombre, expresion, token):
        self.nombre = nombre
        self.expresion = expresion
        self.token = token


class Imprimir:
    def __init__(self, expresion):
        self.expresion = expresion


class Si:
    def __init__(self, condicion, cuerpo, cuerpo_sino=None):
        self.condicion = condicion
        self.cuerpo = cuerpo
        self.cuerpo_sino = cuerpo_sino or []


class Mientras:
    def __init__(self, condicion, cuerpo):
        self.condicion = condicion
        self.cuerpo = cuerpo


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errores = []

    def analizar(self):
        sentencias = []

        while not self.coincide(TokenType.EOF):
            sentencia = self.sentencia()
            if sentencia:
                sentencias.append(sentencia)
            else:
                self.avanzar()

        return sentencias, self.errores

    def sentencia(self):
        if self.es_tipo_dato():
            return self.declaracion()

        if self.coincide(TokenType.IDENTIFICADOR):
            return self.asignacion()

        if self.coincide(TokenType.PRINT):
            return self.imprimir()

        if self.coincide(TokenType.IF):
            return self.sentencia_si()

        if self.coincide(TokenType.WHILE):
            return self.sentencia_mientras()

        self.error("Sentencia no reconocida", self.actual())
        return None

    def declaracion(self):
        tipo_token = self.avanzar()
        nombre = self.consumir(TokenType.IDENTIFICADOR, "Se esperaba un identificador")

        self.consumir(TokenType.ASIGNACION, "Se esperaba '=' en la declaración")
        expresion = self.expresion()
        self.consumir(TokenType.FIN_SENTENCIA, "Se esperaba ';;' al final de la declaración")

        return Declaracion(
            tipo_token.valor,
            nombre.valor if nombre else "",
            expresion,
            tipo_token
        )

    def asignacion(self):
        nombre = self.avanzar()

        self.consumir(TokenType.ASIGNACION, "Se esperaba '=' en la asignación")
        expresion = self.expresion()
        self.consumir(TokenType.FIN_SENTENCIA, "Se esperaba ';;' al final de la asignación")

        return Asignacion(nombre.valor, expresion, nombre)

    def imprimir(self):
        self.avanzar()

        self.consumir(TokenType.PARENTESIS_ABRE, "Se esperaba '(' después de imprimir")
        expresion = self.expresion()
        self.consumir(TokenType.PARENTESIS_CIERRA, "Se esperaba ')' después de imprimir")
        self.consumir(TokenType.FIN_SENTENCIA, "Se esperaba ';;' después de imprimir")

        return Imprimir(expresion)

    def sentencia_si(self):
        self.avanzar()

        self.consumir(TokenType.PARENTESIS_ABRE, "Se esperaba '(' después de si")
        condicion = self.expresion()
        self.consumir(TokenType.PARENTESIS_CIERRA, "Se esperaba ')' después de la condición")

        cuerpo = self.bloque()
        cuerpo_sino = []

        if self.coincide(TokenType.ELSE):
            self.avanzar()
            cuerpo_sino = self.bloque()

        return Si(condicion, cuerpo, cuerpo_sino)

    def sentencia_mientras(self):
        self.avanzar()

        self.consumir(TokenType.PARENTESIS_ABRE, "Se esperaba '(' después de mientras")
        condicion = self.expresion()
        self.consumir(TokenType.PARENTESIS_CIERRA, "Se esperaba ')' después de la condición")

        cuerpo = self.bloque()

        return Mientras(condicion, cuerpo)

    def bloque(self):
        self.consumir(TokenType.LLAVE_ABRE, "Se esperaba '{' para abrir el bloque")

        sentencias = []

        while not self.coincide(TokenType.LLAVE_CIERRA) and not self.coincide(TokenType.EOF):
            sentencia = self.sentencia()
            if sentencia:
                sentencias.append(sentencia)
            else:
                self.avanzar()

        self.consumir(TokenType.LLAVE_CIERRA, "Se esperaba '}' para cerrar el bloque")

        return sentencias

    def expresion(self):
        return self.igualdad()

    def igualdad(self):
        expr = self.comparacion()

        while self.coincide(TokenType.IGUALDAD) or self.coincide(TokenType.DIFERENTE):
            operador = self.avanzar()
            derecha = self.comparacion()
            expr = Binaria(expr, operador, derecha)

        return expr

    def comparacion(self):
        expr = self.termino()

        while (
            self.coincide(TokenType.MAYOR)
            or self.coincide(TokenType.MENOR)
            or self.coincide(TokenType.MAYOR_IGUAL)
            or self.coincide(TokenType.MENOR_IGUAL)
        ):
            operador = self.avanzar()
            derecha = self.termino()
            expr = Binaria(expr, operador, derecha)

        return expr

    def termino(self):
        expr = self.factor()

        while self.coincide(TokenType.SUMA) or self.coincide(TokenType.RESTA):
            operador = self.avanzar()
            derecha = self.factor()
            expr = Binaria(expr, operador, derecha)

        return expr

    def factor(self):
        expr = self.primario()

        while self.coincide(TokenType.MULTIPLICACION) or self.coincide(TokenType.DIVISION):
            operador = self.avanzar()
            derecha = self.primario()
            expr = Binaria(expr, operador, derecha)

        return expr

    def primario(self):
        token = self.actual()

        if self.coincide(TokenType.NUMERO_ENTERO):
            self.avanzar()
            return Literal(int(token.valor), "int")

        if self.coincide(TokenType.NUMERO_DECIMAL):
            self.avanzar()
            return Literal(float(token.valor), "double")

        if self.coincide(TokenType.TEXTO):
            self.avanzar()
            return Literal(token.valor, "string")

        if self.coincide(TokenType.TRUE):
            self.avanzar()
            return Literal(True, "bool")

        if self.coincide(TokenType.FALSE):
            self.avanzar()
            return Literal(False, "bool")

        if self.coincide(TokenType.IDENTIFICADOR):
            self.avanzar()
            return Variable(token.valor, token)

        if self.coincide(TokenType.PARENTESIS_ABRE):
            self.avanzar()
            expr = self.expresion()
            self.consumir(TokenType.PARENTESIS_CIERRA, "Se esperaba ')' después de la expresión")
            return expr

        self.error("Se esperaba una expresión válida", token)
        self.avanzar()
        return Literal(None, "desconocido")

    def consumir(self, tipo, mensaje):
        if self.coincide(tipo):
            return self.avanzar()

        self.error(mensaje, self.actual())
        return None

    def coincide(self, tipo):
        return self.actual().tipo == tipo

    def actual(self):
        return self.tokens[self.pos]

    def avanzar(self):
        token = self.actual()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token

    def error(self, mensaje, token):
        self.errores.append(ErrorSintactico(mensaje, token.linea, token.columna))

    def es_tipo_dato(self):
        return (
            self.coincide(TokenType.INT)
            or self.coincide(TokenType.DOUBLE)
            or self.coincide(TokenType.BOOL)
            or self.coincide(TokenType.STRING)
        )