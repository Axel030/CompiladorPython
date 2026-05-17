import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from lexer import Lexer
from token_type import TokenType
from parser import Parser
from semantic import SemanticAnalyzer
from interpreter import Interpreter


class AppCompilador:
    def __init__(self, root):
        self.root = root
        self.root.title("Mi Compilador")
        self.root.geometry("1200x750")

        self.tokens_visible = True

        self.crear_interfaz()
        self.cargar_ejemplo()

    def crear_interfaz(self):
        barra = tk.Frame(self.root)
        barra.pack(fill="x", padx=10, pady=5)

        self.btnAnalizar = tk.Button(
            barra,
            text="Compilar / Ejecutar",
            command=self.compilar_codigo,
            bg="#0D6EFD",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5
        )
        self.btnAnalizar.pack(side="left", padx=5)

        self.btnToggleTokens = tk.Button(
            barra,
            text="Ocultar / Mostrar Tokens",
            command=self.toggle_tokens
        )
        self.btnToggleTokens.pack(side="left", padx=5)

        self.paned_principal = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        self.paned_principal.pack(fill="both", expand=True, padx=10, pady=5)

        self.frame_izquierdo = tk.Frame(self.paned_principal)
        self.frame_tokens = tk.Frame(self.paned_principal)

        self.paned_principal.add(self.frame_izquierdo, minsize=500)
        self.paned_principal.add(self.frame_tokens, minsize=300)

        self.paned_vertical = tk.PanedWindow(self.frame_izquierdo, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self.paned_vertical.pack(fill="both", expand=True)

        self.frame_codigo = tk.Frame(self.paned_vertical)
        self.frame_salida = tk.Frame(self.paned_vertical)

        self.paned_vertical.add(self.frame_codigo, minsize=250)
        self.paned_vertical.add(self.frame_salida, minsize=150)

        lbl_codigo = tk.Label(self.frame_codigo, text="Código fuente")
        lbl_codigo.pack(anchor="w")

        self.txtCodigo = ScrolledText(self.frame_codigo, font=("Consolas", 12))
        self.txtCodigo.pack(fill="both", expand=True)

        self.txtCodigo.tag_config("error", background="#ffcccc", underline=True)

        lbl_salida = tk.Label(self.frame_salida, text="Errores / Resultado")
        lbl_salida.pack(anchor="w")

        self.txtSalida = ScrolledText(self.frame_salida, font=("Consolas", 11))
        self.txtSalida.pack(fill="both", expand=True)

        lbl_tokens = tk.Label(self.frame_tokens, text="Tabla de tokens")
        lbl_tokens.pack(anchor="w")

        self.tablaTokens = ttk.Treeview(
            self.frame_tokens,
            columns=("Tipo", "Valor", "Linea", "Columna"),
            show="headings"
        )

        self.tablaTokens.heading("Tipo", text="Tipo")
        self.tablaTokens.heading("Valor", text="Valor")
        self.tablaTokens.heading("Linea", text="Línea")
        self.tablaTokens.heading("Columna", text="Columna")

        self.tablaTokens.column("Tipo", width=140)
        self.tablaTokens.column("Valor", width=140)
        self.tablaTokens.column("Linea", width=70)
        self.tablaTokens.column("Columna", width=70)

        self.tablaTokens.pack(fill="both", expand=True)
        

    def cargar_ejemplo(self):
        codigo = '''int a1 = 1;;
double precio = 10.5;;
bool activo = true;;
string nombre = "Axel";;

if (a1 > 0) {
    print(nombre);;
}

while (a1 < 5) {
    print(a1);;
    a1 = a1 + 1;;
}
'''
        self.txtCodigo.insert("1.0", codigo)

    def toggle_tokens(self):
        if self.tokens_visible:
            self.paned_principal.forget(self.frame_tokens)
            self.tokens_visible = False
        else:
            self.paned_principal.add(self.frame_tokens, minsize=300)
            self.tokens_visible = True

    def compilar_codigo(self):
        self.limpiar_resultados()

        codigo = self.txtCodigo.get("1.0", tk.END)

        lexer = Lexer(codigo)
        tokens, errores_lexicos = lexer.analizar()

        for token in tokens:
            if token.tipo != TokenType.EOF:
                self.tablaTokens.insert(
                    "",
                    "end",
                    values=(token.tipo.name, token.valor, token.linea, token.columna)
                )

        if errores_lexicos:
            self.txtSalida.insert(tk.END, "ERRORES LÉXICOS:\n\n")
            for error in errores_lexicos:
                self.txtSalida.insert(tk.END, f"- {error}\n")
            return

        parser = Parser(tokens)
        ast, errores_sintacticos = parser.analizar()

        if errores_sintacticos:
            self.txtSalida.insert(tk.END, "ERRORES SINTÁCTICOS:\n\n")
            for error in errores_sintacticos:
                self.txtSalida.insert(tk.END, f"- {error}\n")
                self.marcar_linea_error(error.linea)
            return

        semantic = SemanticAnalyzer()
        errores_semanticos = semantic.analizar(ast)

        if errores_semanticos:
            self.txtSalida.insert(tk.END, "ERRORES SEMÁNTICOS:\n\n")
            for error in errores_semanticos:
                self.txtSalida.insert(tk.END, f"- {error}\n")
                self.marcar_linea_error(error.linea)
            return

        interpreter = Interpreter()
        salida = interpreter.ejecutar(ast)

        self.txtSalida.insert(tk.END, "EJECUCIÓN CORRECTA:\n\n")
        self.txtSalida.insert(tk.END, salida if salida.strip() else "El programa no imprimió ningún resultado.")

    def marcar_linea_error(self, linea):
        if linea <= 0:
            return

        inicio = f"{linea}.0"
        fin = f"{linea}.end"
        self.txtCodigo.tag_add("error", inicio, fin)

    def limpiar_resultados(self):
        for item in self.tablaTokens.get_children():
            self.tablaTokens.delete(item)

        self.txtSalida.delete("1.0", tk.END)
        self.txtCodigo.tag_remove("error", "1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = AppCompilador(root)
    root.mainloop()