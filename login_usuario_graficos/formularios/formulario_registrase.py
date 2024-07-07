import tkinter as tk
from tkinter import ttk, messagebox
from login_usuario_graficos.Utilerias import funciones_dimensiones as fd


class registrar_usuario:

    def volver_login(self):
        self.ventana.destroy()
        from formularios.formulario_login import login_user
        login_user()

    
    def guardar_datos(self):
        messagebox.showerror(message="No esta en funcionamiento", title="MENSAJE")


    def __init__(self):
        # clase
        self.ventana = tk.Tk()
        self.ventana.title("registro de Usuario")
        self.ventana.geometry("900x800")
        self.ventana.config(bg = "#d8dee3")
        self.ventana.resizable(width=0, height=0)
        fd.centrar_ventana(self.ventana, 900, 800)

        logo = fd.leer_imagen("login_usuario_graficos/utilerias/imagenes/logo_tetris.png", (200, 250))

        #espacio del logo
        espacio_logo = tk.Frame(self.ventana, bd=0, width=250, relief=tk.SOLID, padx=0, pady=0, bg="#1c2833" )
        espacio_logo.pack(side="right", expand=tk.NO, fill=tk.BOTH)
        etiqueta = tk.Label(espacio_logo, image=logo, bg= "#000000")
        etiqueta.place(x=0, y=0, relwidth=1, relheight=1)

        #espacio del formulario
        espacio_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg= "#d8dee3")
        espacio_form.pack(side="left", expand=tk.YES, fill=tk.BOTH)

        #espacio del formulario Titulo
        formulario_titulo = tk.Frame(espacio_form, height=40, bd=0, relief=tk.SOLID, bg = "black")
        formulario_titulo.pack(side="top", fill=tk.X)
        titulo = tk.Label(formulario_titulo, text="REGISTRO", font=("helvetica", 40, "bold"), fg="black", bg="#d8dee3", pady=40)
        titulo.pack(expand=tk.YES, fill=tk.BOTH)

        #espacio de los rellenados de informacion
        espacio_archivos = tk.Frame(espacio_form, height=60, bd=0, relief=tk.SOLID, bg="#d8dee3")
        espacio_archivos.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        #rellenado de Nombre
        etiqueta_usuario = tk.Label(espacio_archivos, text="NOMBRES", font=("courier", 14), fg= "#000000", bg= "#fcfcfc", anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=5)
        self.usuario = ttk.Entry(espacio_archivos, font=("times", 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=10)

        #rellenado de Apellidos
        etiqueta_password = tk.Label(espacio_archivos, text="APELLIDOS", font=("courier", 14), fg= "#000000", bg="#fcfcfc", anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(espacio_archivos, font=("times", 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)

        #rellenado de correo electronico
        etiqueta_usuario = tk.Label(espacio_archivos, text="CORREO ELECTRONICO", font=("courier", 14), fg= "#000000", bg= "#fcfcfc", anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=5)
        self.usuario = ttk.Entry(espacio_archivos, font=("times", 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=10)

        #rellenado de Estado de procedencia
        etiqueta_password = tk.Label(espacio_archivos, text="ESTADO DE PROCEDENCIA", font=("courier", 14), fg= "#000000", bg="#fcfcfc", anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(espacio_archivos, font=("times", 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)

        #rellenado de codido de usuario
        etiqueta_usuario = tk.Label(espacio_archivos, text="CODIGO DE USUARIO", font=("courier", 14), fg= "#000000", bg= "#fcfcfc", anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=5)
        self.usuario = ttk.Entry(espacio_archivos, font=("times", 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=10)

        #rellenado de Estado de procedencia
        etiqueta_password = tk.Label(espacio_archivos, text="CONTRASEÑA", font=("courier", 14), fg= "#000000", bg="#fcfcfc", anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(espacio_archivos, font=("times", 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)

        #boton de Registrase
        boton_login = tk.Button(espacio_archivos, text="REGISTRARSE", font=("courier", 15, "bold"), bg="#000000", bd=0, fg= "#fff", command=self.guardar_datos)
        boton_login.pack(fill=tk.X, padx=20, pady=20)
        boton_login.bind("<Return>", (lambda event: self.guardar_datos()))

        #boton de volver
        boton_login = tk.Button(espacio_archivos, text="VOLVER", font=("courier", 15, "bold"), bg="#000000", bd=0, fg= "#fff", command=self.volver_login)
        boton_login.pack(fill=tk.X, padx=20, pady=20)
        boton_login.bind("<Return>", (lambda event: self.volver_login()))

        #bucle de la ventana
        self.ventana.mainloop()
