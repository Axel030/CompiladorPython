# token_type.py
from enum import Enum, auto

class TokenType(Enum):
    INT = auto()
    DOUBLE = auto()
    BOOL = auto()
    STRING = auto()

    IF = auto()
    ELSE = auto()
    WHILE = auto()
    PRINT = auto()

    TRUE = auto()
    FALSE = auto()

    IDENTIFICADOR = auto()
    NUMERO_ENTERO = auto()
    NUMERO_DECIMAL = auto()
    TEXTO = auto()

    ASIGNACION = auto()
    SUMA = auto()
    RESTA = auto()
    MULTIPLICACION = auto()
    DIVISION = auto()

    MAYOR = auto()
    MENOR = auto()
    MAYOR_IGUAL = auto()
    MENOR_IGUAL = auto()
    IGUALDAD = auto()
    DIFERENTE = auto()

    PARENTESIS_ABRE = auto()
    PARENTESIS_CIERRA = auto()
    LLAVE_ABRE = auto()
    LLAVE_CIERRA = auto()

    FIN_SENTENCIA = auto()
    EOF = auto()
    FOR = auto()