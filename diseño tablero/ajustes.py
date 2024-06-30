import pygame


n=15  #FILAS
m=9   #COLUMNAS


#tamaño
tam_celdas=40
ancho_juego=m*tam_celdas
alto_juego=n*tam_celdas


#barra lateral
sidebar_ancho=300
preview_alto=0.25
score_alto=0.4
rest_alto=0.3
datos_usuario=0.2

#window
margen=15
window_ancho=ancho_juego+sidebar_ancho+margen*3
window_alto=alto_juego+margen*2


#COLORES
azul='#3399FF'
azul_2='#6EC4EC'
azul_3='#2980B9'
negro_2='#1C2833'
negro='#101010'
blanco='#FCFCFA'

#COLORES PIEZAS
rojo='#CB4335'
amarillo='#F1C40F'
verde='#ABEBC6'
morado='#8E44AD'
naranja='#F39C12'
rosado='#F472EA'
aqua='#66CCCD'
verde_2='#439C71'
marron='#9C6F43'

#FORMA PIEZAS DICCIONARIO
PIEZAS={
    'T':{'forma': [(0,0), (-1,0), (1,0),(0,-1),(0,-2)], 'color': rojo},
    'O':{'forma': [(0,0), (0,-1), (1,0),(1,-1)], 'color': amarillo},
    'J':{'forma': [(0,0), (0,-1), (0,1),(-1,1)], 'color': verde},
    'L':{'forma': [(0,0), (0,-1), (0,1),(1,1)], 'color': morado},
    'I':{'forma': [(0,0), (0,-1), (0,-2)], 'color': naranja},
    'p':{'forma': [(0,0), (-1,0), (1,0)], 'color': rosado},
    'z':{'forma': [(0,0), (-1,0), (0,1), (1,1)], 'color': aqua},
}



#COMPONENTES DEL JUEGO
pieza_out = pygame.Vector2(m//2,-2)  #PARA QUE LA PIEZA SE ENCUENTRE DENTRO DEL TABLERO
refresh_tiempo_incio = 500
tiempo_espera = 140
tiempo_rotacion = 150
