from token_type import TokenType
from mi_token import Token

PALABRAS_RESERVADAS = {
    "int": TokenType.INT,
    "double": TokenType.DOUBLE,
    "bool": TokenType.BOOL,
    "string": TokenType.STRING,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "print": TokenType.PRINT,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR
}

class Lexer:
    def __init__(self, codigo):
        self.codigo = codigo
        self.tokens = []
        self.errores = []
        self.pos = 0
        self.linea = 1
        self.columna = 1

    def actual(self):
        if self.pos >= len(self.codigo):
            return "\0"
        return self.codigo[self.pos]

    def avanzar(self):
        if self.actual() == "\n":
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1
        self.pos += 1

    def agregar_token(self, tipo, valor, linea, columna):
        self.tokens.append(Token(tipo, valor, linea, columna))

    def analizar(self):
        while self.actual() != "\0":
            c = self.actual()

            if c.isspace():
                self.avanzar()
                continue

            linea = self.linea
            columna = self.columna

            if c.isalpha() or c == "_":
                self.identificador(linea, columna)
                continue

            if c.isdigit():
                self.numero(linea, columna)
                continue

            if c == '"':
                self.cadena(linea, columna)
                continue

            if c == ";" and self.ver_siguiente() == ";":
                self.avanzar()
                self.avanzar()
                self.agregar_token(TokenType.FIN_SENTENCIA, ";;", linea, columna)
                continue

            if c == "=":
                self.avanzar()
                if self.actual() == "=":
                    self.avanzar()
                    self.agregar_token(TokenType.IGUALDAD, "==", linea, columna)
                else:
                    self.agregar_token(TokenType.ASIGNACION, "=", linea, columna)
                continue

            if c == "!":
                self.avanzar()
                if self.actual() == "=":
                    self.avanzar()
                    self.agregar_token(TokenType.DIFERENTE, "!=", linea, columna)
                else:
                    self.errores.append(f"Simbolo invalido '!' en L{linea}, C{columna}")
                continue

            if c == ">":
                self.avanzar()
                if self.actual() == "=":
                    self.avanzar()
                    self.agregar_token(TokenType.MAYOR_IGUAL, ">=", linea, columna)
                else:
                    self.agregar_token(TokenType.MAYOR, ">", linea, columna)
                continue

            if c == "<":
                self.avanzar()
                if self.actual() == "=":
                    self.avanzar()
                    self.agregar_token(TokenType.MENOR_IGUAL, "<=", linea, columna)
                else:
                    self.agregar_token(TokenType.MENOR, "<", linea, columna)
                continue

            simples = {
                "+": TokenType.SUMA,
                "-": TokenType.RESTA,
                "*": TokenType.MULTIPLICACION,
                "/": TokenType.DIVISION,
                "(": TokenType.PARENTESIS_ABRE,
                ")": TokenType.PARENTESIS_CIERRA,
                "{": TokenType.LLAVE_ABRE,
                "}": TokenType.LLAVE_CIERRA,
            }

            if c in simples:
                self.avanzar()
                self.agregar_token(simples[c], c, linea, columna)
                continue

            self.errores.append(f"Símbolo no valido '{c}' en L{linea}, C{columna}")
            self.avanzar()

        self.tokens.append(Token(TokenType.EOF, "", self.linea, self.columna))
        return self.tokens, self.errores

    def ver_siguiente(self):
        if self.pos + 1 >= len(self.codigo):
            return "\0"
        return self.codigo[self.pos + 1]

    def identificador(self, linea, columna):
        inicio = self.pos

        while self.actual().isalnum() or self.actual() == "_":
            self.avanzar()

        valor = self.codigo[inicio:self.pos]
        tipo = PALABRAS_RESERVADAS.get(valor, TokenType.IDENTIFICADOR)
        self.agregar_token(tipo, valor, linea, columna)

    def numero(self, linea, columna):
        inicio = self.pos

        while self.actual().isdigit():
            self.avanzar()

        if self.actual() == "." and self.ver_siguiente().isdigit():
            self.avanzar()
            while self.actual().isdigit():
                self.avanzar()

            valor = self.codigo[inicio:self.pos]
            self.agregar_token(TokenType.NUMERO_DECIMAL, valor, linea, columna)
        else:
            valor = self.codigo[inicio:self.pos]
            self.agregar_token(TokenType.NUMERO_ENTERO, valor, linea, columna)

    def cadena(self, linea, columna):
        self.avanzar()
        inicio = self.pos

        while self.actual() != '"' and self.actual() != "\0" and self.actual() != "\n":
            self.avanzar()

        if self.actual() != '"':
            self.errores.append(f"Cadena sin cerrar en L{linea}, C{columna}")
            return

        valor = self.codigo[inicio:self.pos]
        self.avanzar()
        self.agregar_token(TokenType.TEXTO, valor, linea, columna)