# mi_token.py
class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return f"{self.tipo.name}({self.valor}) [L{self.linea}, C{self.columna}]"