import tkinter as tk
from login_usuario_graficos.Utilerias import funciones_dimensiones as fd

# colores

NEGRO = "#1c2833"

# deficion de clase 

class panel_master:

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Panel Maestro")
        ancho, largo = self.ventana.winfo_screenwidth(), self.ventana.winfo_screenheight()
        self.ventana.geometry("%dx%d+0+0" % (ancho, largo))
        self.ventana.config(bg= NEGRO)
        self.ventana.resizable(width=0, height=0)

        logo = fd.leer_imagen("login_usuario_graficos/utilerias/imagenes/logo_tetris.png", (200, 200))

        etiqueta = tk.Label (self.ventana, image=logo, bg="#3a7ff6")
        etiqueta.place (x=0, y=0, relheight=1, relwidth=1)
        self.ventana.mainloop()