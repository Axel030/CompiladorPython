import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from token_type import TokenType
from compiler_service import CompilerService
from themes import aplicar_tema_claro, aplicar_tema_oscuro


class AppCompilador:
    def __init__(self, root):
        self.root = root
        self.root.title("Mi Compilador")
        self.root.geometry("1200x750")

        self.tokens_visible = True
        self.modo_oscuro = False
        self.compiler_service = CompilerService()

        self.crear_interfaz()
        self.cargar_ejemplo()
        self.actualizar_numeros_linea()
        aplicar_tema_claro(self)

    def crear_interfaz(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.barra = tk.Frame(self.root)
        self.barra.pack(fill="x", padx=10, pady=8)

        self.btnAnalizar = tk.Button(
            self.barra,
            text="Compilar / Ejecutar",
            command=self.compilar_codigo,
            bg="#0D6EFD",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=18,
            pady=7,
            relief="flat",
            cursor="hand2"
        )
        self.btnAnalizar.pack(side="left", padx=5)

        self.btnToggleTokens = tk.Button(
            self.barra,
            text="Ocultar / Mostrar Tokens",
            command=self.toggle_tokens,
            font=("Arial", 10),
            padx=12,
            pady=7,
            relief="flat",
            cursor="hand2"
        )
        self.btnToggleTokens.pack(side="left", padx=5)

        self.btnTema = tk.Button(
            self.barra,
            text="Modo oscuro",
            command=self.cambiar_tema,
            font=("Arial", 10),
            padx=12,
            pady=7,
            relief="flat",
            cursor="hand2"
        )
        self.btnTema.pack(side="left", padx=5)

        self.paned_principal = tk.PanedWindow(
            self.root,
            orient=tk.HORIZONTAL,
            sashrelief=tk.RAISED,
            sashwidth=6
        )
        self.paned_principal.pack(fill="both", expand=True, padx=10, pady=5)

        self.frame_izquierdo = tk.Frame(self.paned_principal)
        self.frame_tokens = tk.Frame(self.paned_principal)

        self.paned_principal.add(self.frame_izquierdo, minsize=500)
        self.paned_principal.add(self.frame_tokens, minsize=300)

        self.paned_vertical = tk.PanedWindow(
            self.frame_izquierdo,
            orient=tk.VERTICAL,
            sashrelief=tk.RAISED,
            sashwidth=6
        )
        self.paned_vertical.pack(fill="both", expand=True)

        self.frame_codigo = tk.Frame(self.paned_vertical)
        self.frame_salida = tk.Frame(self.paned_vertical)

        self.paned_vertical.add(self.frame_codigo, minsize=250)
        self.paned_vertical.add(self.frame_salida, minsize=150)

        self.lbl_codigo = tk.Label(
            self.frame_codigo,
            text="Código fuente",
            font=("Arial", 10, "bold")
        )
        self.lbl_codigo.pack(anchor="w", pady=(0, 4))

        self.editor_frame = tk.Frame(self.frame_codigo)
        self.editor_frame.pack(fill="both", expand=True)

        self.txtLineas = tk.Text(
            self.editor_frame,
            width=5,
            padx=4,
            takefocus=0,
            border=0,
            state="disabled",
            font=("Consolas", 12)
        )
        self.txtLineas.pack(side="left", fill="y")

        self.txtCodigo = ScrolledText(
            self.editor_frame,
            font=("Consolas", 12),
            relief="flat",
            padx=8,
            pady=8,
            undo=True
        )
        self.txtCodigo.pack(side="left", fill="both", expand=True)

        self.txtCodigo.bind("<KeyRelease>", self.actualizar_numeros_linea)
        self.txtCodigo.bind("<MouseWheel>", self.sincronizar_scroll_lineas)
        self.txtCodigo.bind("<ButtonRelease-1>", self.actualizar_numeros_linea)

        self.txtCodigo.tag_config("error_lexico", background="#FECACA")
        self.txtCodigo.tag_config("error_sintactico", background="#FED7AA")
        self.txtCodigo.tag_config("error_semantico", background="#DDD6FE")

        self.lbl_salida = tk.Label(
            self.frame_salida,
            text="Errores / Resultado",
            font=("Arial", 10, "bold")
        )
        self.lbl_salida.pack(anchor="w", pady=(4, 4))

        self.txtSalida = ScrolledText(
            self.frame_salida,
            font=("Consolas", 11),
            relief="flat",
            padx=8,
            pady=8
        )
        self.txtSalida.pack(fill="both", expand=True)

        self.txtSalida.tag_config("lexico", foreground="#DC2626")
        self.txtSalida.tag_config("sintactico", foreground="#EA580C")
        self.txtSalida.tag_config("semantico", foreground="#9333EA")
        self.txtSalida.tag_config("correcto", foreground="#16A34A")
        self.txtSalida.tag_config("titulo", font=("Consolas", 11, "bold"))

        self.lbl_tokens = tk.Label(
            self.frame_tokens,
            text="Tabla de tokens",
            font=("Arial", 10, "bold")
        )
        self.lbl_tokens.pack(anchor="w", pady=(0, 4))

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
for (int i = 0;; i < 5;; i = i + 1) {
    print(i);;
}
'''
        self.txtCodigo.insert("1.0", codigo)

    def compilar_codigo(self):
        self.limpiar_resultados()

        codigo = self.txtCodigo.get("1.0", tk.END)

        tokens, errores, salida = self.compiler_service.compilar(codigo)

        self.mostrar_tokens(tokens)
        self.mostrar_errores_o_resultado(errores, salida)

    def mostrar_tokens(self, tokens):
        for token in tokens:
            if token.tipo != TokenType.EOF:
                self.tablaTokens.insert(
                    "",
                    "end",
                    values=(token.tipo.name, token.valor, token.linea, token.columna)
                )

    def mostrar_errores_o_resultado(self, errores, salida):
        errores_lexicos = errores["lexicos"]
        errores_sintacticos = errores["sintacticos"]
        errores_semanticos = errores["semanticos"]

        hay_errores = errores_lexicos or errores_sintacticos or errores_semanticos

        if hay_errores:
            self.txtSalida.insert(tk.END, "ERRORES ENCONTRADOS:\n\n", "titulo")

            if errores_lexicos:
                self.txtSalida.insert(tk.END, "Errores Lexicos:\n", "titulo")
                for error in errores_lexicos:
                    self.txtSalida.insert(tk.END, f"- {error}\n", "lexico")
                self.txtSalida.insert(tk.END, "\n")

            if errores_sintacticos:
                self.txtSalida.insert(tk.END, "Errores Sintacticos:\n", "titulo")
                for error in errores_sintacticos:
                    self.txtSalida.insert(tk.END, f"- {error}\n", "sintactico")
                    self.marcar_linea_error(error.linea, "sintactico")
                self.txtSalida.insert(tk.END, "\n")

            if errores_semanticos:
                self.txtSalida.insert(tk.END, "Errores Semanticos:\n", "titulo")
                for error in errores_semanticos:
                    self.txtSalida.insert(tk.END, f"- {error}\n", "semantico")
                    self.marcar_linea_error(error.linea, "semantico")
                self.txtSalida.insert(tk.END, "\n")

            return

        self.txtSalida.insert(tk.END, "EJECUCION CORRECTA:\n\n", "correcto")
        self.txtSalida.insert(
            tk.END,
            salida if salida.strip() else "El programa no imprimio ningún resultado."
        )

    def actualizar_numeros_linea(self, event=None):
        total_lineas = int(self.txtCodigo.index("end-1c").split(".")[0])
        numeros = "\n".join(str(i) for i in range(1, total_lineas + 1))

        self.txtLineas.config(state="normal")
        self.txtLineas.delete("1.0", tk.END)
        self.txtLineas.insert("1.0", numeros)
        self.txtLineas.config(state="disabled")

        self.sincronizar_scroll_lineas()

    def sincronizar_scroll_lineas(self, event=None):
        self.txtLineas.yview_moveto(self.txtCodigo.yview()[0])

    def cambiar_tema(self):
        self.modo_oscuro = not self.modo_oscuro

        if self.modo_oscuro:
            aplicar_tema_oscuro(self)
        else:
            aplicar_tema_claro(self)

    def toggle_tokens(self):
        if self.tokens_visible:
            self.paned_principal.forget(self.frame_tokens)
            self.tokens_visible = False
        else:
            self.paned_principal.add(self.frame_tokens, minsize=300)
            self.tokens_visible = True

    def marcar_linea_error(self, linea, tipo):
        if linea <= 0:
            return

        inicio = f"{linea}.0"
        fin = f"{linea}.end"

        if tipo == "lexico":
            self.txtCodigo.tag_add("error_lexico", inicio, fin)
        elif tipo == "sintactico":
            self.txtCodigo.tag_add("error_sintactico", inicio, fin)
        elif tipo == "semantico":
            self.txtCodigo.tag_add("error_semantico", inicio, fin)

    def limpiar_resultados(self):
        for item in self.tablaTokens.get_children():
            self.tablaTokens.delete(item)

        self.txtSalida.delete("1.0", tk.END)

        self.txtCodigo.tag_remove("error_lexico", "1.0", tk.END)
        self.txtCodigo.tag_remove("error_sintactico", "1.0", tk.END)
        self.txtCodigo.tag_remove("error_semantico", "1.0", tk.END)