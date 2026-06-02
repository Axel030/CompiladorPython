def aplicar_tema_claro(app):
    app.btnTema.config(text="Modo oscuro")

    fondo = "#F5F7FA"
    panel = "#FFFFFF"
    texto = "#1F2937"
    editor_fondo = "#FFFFFF"
    editor_texto = "#111827"
    salida_fondo = "#F9FAFB"
    lineas_fondo = "#E5E7EB"
    lineas_texto = "#4B5563"

    app.root.config(bg=fondo)
    app.barra.config(bg=fondo)

    for frame in [
        app.frame_izquierdo,
        app.frame_tokens,
        app.frame_codigo,
        app.frame_salida,
        app.editor_frame
    ]:
        frame.config(bg=panel)

    for label in [
        app.lbl_codigo,
        app.lbl_salida,
        app.lbl_tokens
    ]:
        label.config(bg=panel, fg=texto)

    app.btnToggleTokens.config(bg="#E5E7EB", fg="#111827")
    app.btnTema.config(bg="#E5E7EB", fg="#111827")

    app.txtLineas.config(bg=lineas_fondo, fg=lineas_texto)

    app.txtCodigo.config(
        bg=editor_fondo,
        fg=editor_texto,
        insertbackground=editor_texto
    )

    app.txtSalida.config(
        bg=salida_fondo,
        fg=editor_texto,
        insertbackground=editor_texto
    )

    app.txtCodigo.tag_config("error_lexico", background="#FECACA", foreground="#000000")
    app.txtCodigo.tag_config("error_sintactico", background="#FED7AA", foreground="#000000")
    app.txtCodigo.tag_config("error_semantico", background="#DDD6FE", foreground="#000000")

    app.style.configure(
        "Treeview",
        background="#FFFFFF",
        foreground="#111827",
        fieldbackground="#FFFFFF",
        rowheight=25
    )

    app.style.configure(
        "Treeview.Heading",
        background="#E5E7EB",
        foreground="#111827",
        font=("Arial", 10, "bold")
    )


def aplicar_tema_oscuro(app):
    app.btnTema.config(text="Modo claro")

    fondo = "#111827"
    panel = "#1F2937"
    texto = "#F9FAFB"
    editor_fondo = "#0F172A"
    editor_texto = "#E5E7EB"
    salida_fondo = "#111827"
    lineas_fondo = "#1E293B"
    lineas_texto = "#94A3B8"

    app.root.config(bg=fondo)
    app.barra.config(bg=fondo)

    for frame in [
        app.frame_izquierdo,
        app.frame_tokens,
        app.frame_codigo,
        app.frame_salida,
        app.editor_frame
    ]:
        frame.config(bg=panel)

    for label in [
        app.lbl_codigo,
        app.lbl_salida,
        app.lbl_tokens
    ]:
        label.config(bg=panel, fg=texto)

    app.btnToggleTokens.config(bg="#374151", fg="#F9FAFB")
    app.btnTema.config(bg="#374151", fg="#F9FAFB")

    app.txtLineas.config(bg=lineas_fondo, fg=lineas_texto)

    app.txtCodigo.config(
        bg=editor_fondo,
        fg=editor_texto,
        insertbackground=editor_texto
    )

    app.txtSalida.config(
        bg=salida_fondo,
        fg=editor_texto,
        insertbackground=editor_texto
    )

    app.txtCodigo.tag_config("error_lexico", background="#7F1D1D", foreground="#FFFFFF")
    app.txtCodigo.tag_config("error_sintactico", background="#9A3412", foreground="#FFFFFF")
    app.txtCodigo.tag_config("error_semantico", background="#581C87", foreground="#FFFFFF")

    app.style.configure(
        "Treeview",
        background="#111827",
        foreground="#F9FAFB",
        fieldbackground="#111827",
        rowheight=25
    )

    app.style.configure(
        "Treeview.Heading",
        background="#374151",
        foreground="#F9FAFB",
        font=("Arial", 10, "bold")
    )