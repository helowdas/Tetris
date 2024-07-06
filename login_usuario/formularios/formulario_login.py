import tkinter as tk
from tkinter import ttk, messagebox
from login_usuario.Utilerias import funciones_dimensiones as fd
from login_usuario.formularios.formulario_master import panel_master


#clase para el login de usuario

class login_user:

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Inicio de sesion")
        self.ventana.geometry("900x750")
        self.ventana.config(bg = "#1c2833")
        self.ventana.resizable(width=0, height=0)
        fd.centrar_ventana(self.ventana, 900, 750)
        self.ventana.mainloop()
