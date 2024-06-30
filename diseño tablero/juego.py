import pygame
from ajustes import *



class Juego:
    def __init__(self):

        #GENERAL
        self.surface=pygame.Surface((ancho_juego,alto_juego))
        self.display_surface=pygame.display.get_surface()
        self.rect= self.surface.get_rect(topleft=(margen, margen))  #BORDE DEL TABLERO

        #lineas tablero
        self.lineas_surface = self.surface.copy() # copia los parametros del surface
        self.lineas_surface.set_alpha(40)  #  el set_alpha establece la opacidad de la superficie de las líneas


    def cuadriculas(self):   #DIBUJA LA MATRIZ
        self.lineas_surface.fill((0,0,0,0)) # Limpia la superficie de las líneas con un color transparente
        for colum in range(1,m):    #INICIAMOS EN 1 PARA QUE EL BORDE IZQUIERDO NO ESTE EN BLANCO
            x= colum*tam_celdas
            pygame.draw.line(self.lineas_surface, blanco, (x,0), (x,self.lineas_surface.get_height()),1)    #DIBUJA LAS LINEAS DE LAS COLUMNAS
        
        for fila in range(1,n):  #INICIAMOS EN 1 PARA QUE LA LINEA DEL TOPE NO ESTE EN BLANCO
            y= fila*tam_celdas
            pygame.draw.line(self.lineas_surface, blanco, (0,y), (self.lineas_surface.get_width(), y),1)  #DIBUJA LAS LINEAS DE LAS FILAS
        
        self.surface.blit(self.lineas_surface,(0,0)) #dibuja las líneas transparentes sobre la superficie principal


    def run(self):
        self.surface.fill(negro) #Color tablero

        self.cuadriculas() #DIBUJA LAS CUADRICULAS
        self.display_surface.blit(self.surface,(margen,margen))
        pygame.draw.rect(self.display_surface, blanco, self.rect, 2, 2)  #BORDE DEL TABLERO
                
       



