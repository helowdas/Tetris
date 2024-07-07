import sys
import tkinter as tk
from tkinter import ttk, messagebox
from login_usuario_graficos.Utilerias import funciones_dimensiones as fd

#clase para el login de usuario

class login_user:

    def registrar_usuario(self):
        self.ventana.destroy()
        from login_usuario_graficos.formularios.formulario_registrase import registrar_usuario
        registrar_usuario()


    def finalizar(self):
        self.ventana.destroy()
        sys.exit()

    def verificar(self):
        usuario = self.usuario.get()
        password = self.password.get()
        if(usuario == "root" and password == "1234"):
            self.ventana.destroy()
            from menu.menu import pygame_menu
            pygame_menu()
        else:
            messagebox.showerror(message="la contraseña o el usuarios son incorrectos", title="MENSAJE")

    def __init__(self):
        # clase
        self.ventana = tk.Tk()
        self.ventana.title("Inicio de sesion")
        self.ventana.geometry("800x650")
        self.ventana.config(bg = "#3a7ff6")
        self.ventana.resizable(width=0, height=0)
        fd.centrar_ventana(self.ventana, 800, 650)
        

        logo = fd.leer_imagen("login_usuario_graficos/utilerias/imagenes/logo_tetris.png", (200, 200))

        #espacio del logo
        espacio_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=0, pady=0, bg="#1c2833" )
        espacio_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        etiqueta = tk.Label(espacio_logo, image=logo, bg= "#000000")
        etiqueta.place(x=0, y=0, relwidth=1, relheight=1)
        
        #espacio del formulario
        espacio_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg= "#3a7ff6")
        espacio_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        #espacio del formulario Titulo
        formulario_titulo = tk.Frame(espacio_form, height=50, bd=0, relief=tk.SOLID, bg = "black")
        formulario_titulo.pack(side="top", fill=tk.X)
        titulo = tk.Label(formulario_titulo, text="INICIO DE SESION", font=("helvetica", 37, "bold"), fg="#fcfcfc", bg="#3a7ff6", pady=50)
        titulo.pack(expand=tk.YES, fill=tk.BOTH)
        
        #espacio de los rellenados de informacion
        espacio_archivos = tk.Frame(espacio_form, height=50, bd=0, relief=tk.SOLID, bg="#3a7ff6")
        espacio_archivos.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        #rellenado de codigo de usuario
        etiqueta_usuario = tk.Label(espacio_archivos, text="CODIGO DE USUARIO", font=("courier", 14), fg= "#000000", bg= "#fcfcfc", anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=5)
        self.usuario = ttk.Entry(espacio_archivos, font=("times", 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=10)

        #rellenado de contraseña
        etiqueta_password = tk.Label(espacio_archivos, text="CONTRASEÑA", font=("courier", 14), fg= "#000000", bg="#fcfcfc", anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(espacio_archivos, font=("times", 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)

        #boton de Iniciar Sesion
        boton_login = tk.Button(espacio_archivos, text="INICIAR SESION", font=("courier", 15, "bold"), bg="#000000", bd=0, fg= "#fff", command=self.verificar)
        boton_login.pack(fill=tk.X, padx=20, pady=20)
        boton_login.bind("<Return>", (lambda event: self.verificar()))

        #boton de Registrase
        boton_login = tk.Button(espacio_archivos, text="REGISTRARSE", font=("courier", 15, "bold"), bg="#000000", bd=0, fg= "#fff", command=self.registrar_usuario)
        boton_login.pack(fill=tk.X, padx=20, pady=20)
        boton_login.bind("<Return>", (lambda event: self.registrar_usuario()))

        #boton de salir
        boton_login = tk.Button(espacio_archivos, text="SALIR", font=("courier", 15, "bold"), bg="#000000", bd=0, fg= "#fff", command=self.finalizar)
        boton_login.pack(fill=tk.X, padx=20, pady=20)
        boton_login.bind("<Return>", (lambda event: self.finalizar()))

        
        #bucle de la ventana
        self.ventana.mainloop()




