from PIL import ImageTk, Image

#definicion de funciones


def centrar_ventana(ventana, aplicacion_ancho, aplicacion_largo):
    # lee el ancho y largo de la pantalla en la que se esta reproduciendo la ventana del Tkinter
    screen_ancho = ventana.winfo_screenwidth()
    screen_largo = ventana.winfo_screenheight()

    #centra la ventana en la pantalla dada
    x = int((screen_ancho/2) - (aplicacion_ancho/2))
    y = int((screen_largo/2) - (aplicacion_largo/2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")


def leer_imagen (ruta, size):
    return ImageTk.PhotoImage(Image.open(ruta).resize(size, Image.LANCZOS))