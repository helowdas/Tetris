import pygame
import random

FPS=2
MODALIDAD_POR_TIEMPO=0
MODALIDAD_POR_NRO_JUGADAS=1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

COLOR_BOTON=(240,240,240)
COLOR_BOTON_CLICK=(150,150,150)

MENSAJES_ODS=["ods1.jpg","ods2.jpg","ods3.jpg","ods4.jpg","ods5.jpg","ods6.jpg","ods7.jpg","ods1.jpg","ods2.jpg","ods3.jpg","ods4.jpg","ods5.jpg","ods6.jpg","ods7.jpg","ods1.jpg","ods2.jpg","ods3.jpg"]

ESTADOS_DE_VENEZUELA=  ["AMAZONAS", "ANZOÁTEGUI", "APURE", "ARAGUA", "BARINAS", "BOLÍVAR", "CARABOBO", "COJEDES", "DELTA AMACURO", "DISTRITO CAPITAL", "FALCÓN", "GUÁRICO", "LARA", "MÉRIDA", "MIRANDA", "MONAGAS", "NUEVA ESPARTA", "PORTUGUESA", "SUCRE", "TÁCHIRA", "TRUJILLO", "VARGAS", "YARACUY", "ZULIA"]

LISTA_COLORES_TETROMINOS=[CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE] #EL COLOR DEL TETROMINO Nro t ES EL COLOR INDICADO EN LA POSICION t DE LA LISTA 

# REPRESENTAMOS LAS PIEZAS(TETROMINOS) COMO MATRICES (LISTAS DE LISTAS) CON LA PARTICULARIDAD DE QUE PARA 
# UNA MATRIZ de nxm, LA PRIMERA SUB-LISTA DE LA LISTA es la n-esima fila de la matriz, escogido asi para que 
# sea la base de la figura tetrominio de manera que las subsiguientes filas van sobre la anterior. 
# ASI, LA ULTIMA ULTIMA SUBLISTA DE LA LISTA es la primera fila de la matriz.  
TETROMINOS = [
    [[1, 1, 1, 1]],     #matriz de 1x4 (vector fila de 4 columnas) ****
    [[6, 6], [6, 6]],   #matriz de 2x2 **
    [[4, 4, 0], [0, 4, 4]],  #matriz de 2*3 con las casillas (1,4) y  
    [[0, 5, 5], [5, 5, 0]],  
    [[7, 7, 7], [0, 7, 0]],  
    [[2, 2, 2], [0, 0, 2]],  
    [[3, 3, 3], [3, 0, 0]]  
]

def draw_grid(x_ini,y_ini,screen,SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y):
    for x in range(x_ini, SCREEN_WIDTH+GRID_SIZE_X+DESFACE_X, GRID_SIZE_X):
        pygame.draw.line(screen, WHITE, (x, 0+DESFACE_Y), (x, SCREEN_HEIGHT+DESFACE_Y))
    for y in range(y_ini, SCREEN_HEIGHT+GRID_SIZE_Y+DESFACE_Y, GRID_SIZE_Y):
        pygame.draw.line(screen, WHITE, (0+DESFACE_X, y), (SCREEN_WIDTH+DESFACE_X, y))

def draw_tetromino_casillas_grid(tetromino, position,screen,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y,font):
    tetromino_color=obtener_tetromino_color(tetromino,LISTA_COLORES_TETROMINOS)
    for y in range(len(tetromino)):         # y recorre las filas del tetromino
        for x in range(len(tetromino[y])):  # x recorre las columnas de cada fila del tetromino
            if tetromino[y][x] > 0:
                pygame.draw.rect(screen, tetromino_color, (position[0] * GRID_SIZE_X+DESFACE_X + x * GRID_SIZE_X,  position[1] * GRID_SIZE_Y+DESFACE_Y + y * GRID_SIZE_Y, GRID_SIZE_X, GRID_SIZE_Y))
                nro_tetromino_text=font.render(f"{tetromino[y][x]}", True, BLACK)
                screen.blit(nro_tetromino_text, ((((position[0] * GRID_SIZE_X+DESFACE_X + x * GRID_SIZE_X)+(GRID_SIZE_X//2)) - (nro_tetromino_text.get_width()//2)), (((position[1] * GRID_SIZE_Y+DESFACE_Y + y * GRID_SIZE_Y)+(GRID_SIZE_Y//2)) - (nro_tetromino_text.get_height()//2))))

def draw_tetromino_coord_pixel(tetromino, position,screen,GRID_SIZE_X,GRID_SIZE_Y,font):
    tetromino_color=obtener_tetromino_color(tetromino,LISTA_COLORES_TETROMINOS)
    for y in range(len(tetromino)):         # y recorre las filas del tetromino
        for x in range(len(tetromino[y])):  # x recorre las columnas de cada fila del tetromino
            if tetromino[y][x] > 0:
                pygame.draw.rect(screen, tetromino_color, (position[0] + x * GRID_SIZE_X,  position[1] + y * GRID_SIZE_Y, GRID_SIZE_X, GRID_SIZE_Y))
                nro_tetromino_text=font.render(f"{tetromino[y][x]}", True, BLACK)
                screen.blit(nro_tetromino_text, ((((position[0] + x * GRID_SIZE_X)+(GRID_SIZE_X//2)) - (nro_tetromino_text.get_width()//2)), (((position[1] + y * GRID_SIZE_Y)+(GRID_SIZE_Y//2)) - (nro_tetromino_text.get_height()//2))))

def borrarTetrominioSgte(position,screen,GRID_SIZE_X,GRID_SIZE_Y):
    tetrominoCompleto=[[1,1,1,1],[1,1,1,1]]
    tetromino_color=BLACK
    for y in range(len(tetrominoCompleto)):         # y recorre las filas del tetromino
        for x in range(len(tetrominoCompleto[y])):  # x recorre las columnas de cada fila del tetromino
            pygame.draw.rect(screen, tetromino_color, (position[0] + x * GRID_SIZE_X,  position[1] + y * GRID_SIZE_Y, GRID_SIZE_X, GRID_SIZE_Y))

def drawLocatedTetrominos(GRID_HEIGHT,GRID_WIDTH,grid,screen,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y,font):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] > 0:
                COLOR_CASILLA=LISTA_COLORES_TETROMINOS[grid[y][x]-1]
                pygame.draw.rect(screen, COLOR_CASILLA, (x * GRID_SIZE_X+DESFACE_X, y * GRID_SIZE_Y+DESFACE_Y, GRID_SIZE_X, GRID_SIZE_Y))
                valor_casilla_text=font.render(f"{grid[y][x]}", True, BLACK)
                screen.blit(valor_casilla_text, ((((x * GRID_SIZE_X)+(GRID_SIZE_X//2)+DESFACE_X) - (valor_casilla_text.get_width()//2)), (((y * GRID_SIZE_Y)+(GRID_SIZE_Y//2)+DESFACE_Y) - (valor_casilla_text.get_height()//2))))


def obtener_tetromino_color(tetromino,lista_colores_tetrominos):
    for y in range(len(tetromino)):         # y recorre las filas del tetromino
        for x in range(len(tetromino[y])):  # x recorre las columnas de cada fila del tetromino
            if tetromino[y][x] > 0:
                return LISTA_COLORES_TETROMINOS[tetromino[y][x]-1] #El color del tetromino 1 es lista_colores[0], y asi sucesivamente

def check_collision(tetromino, position, grid,GRID_WIDTH,GRID_HEIGHT):
    for y in range(len(tetromino)):
        for x in range(len(tetromino[y])):
            if tetromino[y][x] > 0:
                if position[0] + x < 0 or position[0] + x >= GRID_WIDTH or \
                        position[1] + y >= GRID_HEIGHT or grid[position[1] + y][position[0] + x]:
                    return True
    return False

def merge_tetromino(tetromino, position, grid): #posicion[0] es la columna del grid donde se empieza a dibujar el tetromino y posicion[1] es la fila
    for y in range(len(tetromino)): # y recorre las filas del tetromino dado por el numero de listas que forman el tetromino
        for x in range(len(tetromino[y])):  #x recorre las columnas de cada fila del tetrominio
            if tetromino[y][x] > 0:
                grid[position[1] + y][position[0] + x] = tetromino[y][x]

def remove_completed_rows(grid,GRID_WIDTH,GRID_HEIGHT):
    completed_rows = []
    completed_rows_value=0
    for y in range(GRID_HEIGHT):
        if all(grid[y]):
            completed_rows.append(y)
            for valor in grid[y]:
                completed_rows_value+=valor
    for row in completed_rows:
        del grid[row]
        grid.insert(0, [0] * GRID_WIDTH)
    return completed_rows_value #antes devolvia len(completed_rows)

def rotate_tetromino(tetromino):
    nro_filas_tetromino=len(tetromino)
    if nro_filas_tetromino > 0:
        colum_por_filas_tetromino=len(tetromino[0])
        if colum_por_filas_tetromino>0:
            revertido=list(reversed(tetromino))
            rotated=[[] for _ in range(colum_por_filas_tetromino)]
            for i in range(colum_por_filas_tetromino):
                for fila in revertido: 
                    rotated[i].append(fila[i])
            return rotated
    return tetromino


def cargarSistema(lista_objetos):

    #devuelve 1 si todo ok, 0 si hubo problema de memorias o abriendo archivos
    return 1


def respaldarSistema(lista_objetos):

    return 1

########################################################################################
#CADA UNA DE LOS SIGTES MENU Y DIALOGOS, CREAN SU VENTANA Y LA CIERRAN ANTES DEL RETURN
########################################################################################


def menuIni():
    #1)REGISTRAR USUARIO
    #2)INICIAR SESION
    #3)SALIR
    #CREA LA VENTANA CON EL MENU: 1)REGISTRAR USUARIO 2)INICIAR SESION 3)OLVIDASTE TU NOMBRE DE USUARIO? 4)OLVIDASTE TU CONTRASEñA 5)SALIR Y RETORNA LA OPCION SELECCIONADA
    #SI EL USUARIO CANCELA ESTA VENTANA , SE HACE LO QUE SE HARIA SI LE DA A SALIRreturn 0, PARA SABER 
    #DEVUELVE LA OPCION DEL MENU INICIAL SELECCIONADA. SI CIERRAN
    pygame.init()
    display_info=pygame.display.Info()
    DISPLAY_WIDTH,DISPLAY_HEIGHT=display_info.current_w-10,display_info.current_h-80

    pygame.quit()
    return 2

def menuJuego():
    #1)INICIAR UN JUEGO
    #2)MOSTRAR JUGADA DE MAYOR PUNTUACION DE UN JUGADOR
    #3)MOSTRAR JUGADA DE MAYOR PUNTUACION DE UN ESTADO
    #4)REPORTE DE JUGADAS DE UN JUGADOR
    #5)TOP 10 JUGADORES DEL PAIS
    #6)TOP 10 JUGADORES DE UN ESTADO
    #CREA LA VENTANA CON EL MENU Y RETORNA LA OPCION SELECCIONADA
    #SI EL USUARIO CANCELA ESTA VENTANA , SE HACE LO QUE SE HARIA SI LE DA A SALIR, CON return 0, PARA SABER 
    pygame.init()
    display_info=pygame.display.Info()
    DISPLAY_WIDTH,DISPLAY_HEIGHT=display_info.current_w-10,display_info.current_h-80

    pygame.quit()
    return 1

def jugada_max_puntuacion_jugador(lista_objetos):

    return

def jugada_max_puntuacion_estado(lista_objetos):

    return

def reporte_Jugador(lista_objetos):

    return

def top10_pais(lista_objetos):
    
    return

def top10_estado(lista_objetos):
    
    return

#lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario]
def dialogoRegistrarUsuario(lista_objetos):
    pygame.init()
    display_info=pygame.display.Info()
    DISPLAY_WIDTH,DISPLAY_HEIGHT=display_info.current_w-10,display_info.current_h-80

    pygame.quit()

    #SI LOGRA REGISTRAR EL USUARIO EXITOSAMENTE, MANDA EL MENSAJE Y RETURN 1, SINO, SI ALT+F4 O CERRARON VENTANA RETURN 0
    lista_objetos[8]="charbel_k_18"
    return 1

def dialogoInicioSesion(lista_objetos):
    pygame.init()
    display_info=pygame.display.Info()
    DISPLAY_WIDTH,DISPLAY_HEIGHT=display_info.current_w-10,display_info.current_h-80

    pygame.quit()

    #PINTA EL CUADRO DE DIALOGO Y SI EL USUARIO O LA CLAVE SON INAVLIDOS, MANDA EL MENSAJE, Y VUELVE A PEDIR LOS DATOS.
    #SI EL PROCESO FUE BIEN RETORNA 1, SI EL USUARIO CERRO LA VENTANA RETORNA 0
    lista_objetos[8]="charbel_k_18"
    return 1

#lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario]
def dialogoConfigJuego(lista_objetos):
    pygame.init()
    display_info=pygame.display.Info()
    DISPLAY_WIDTH,DISPLAY_HEIGHT=display_info.current_w-10,display_info.current_h-80

    pygame.quit()

    #PINTA LA VENTANA CON LOS 7 TETRIS, PARA QUE SELECCIONEN 5, PIDE N,M, MODALIDAD DE JUGADA Y TIEMPO O NRO DE MOVIMIENTOS. 
    # SI EL USUARIO CIERRA LA VENTANA RETORNA 0

    lista_objetos[2]+=[
        [[1, 1, 1, 1]],     #matriz de 1x4 (vector fila de 4 columnas) ****
        [[6, 6], [6, 6]],   #matriz de 2x2 **
        [[4, 4, 0], [0, 4, 4]],  #matriz de 2*3 con las casillas (1,4) y  
        [[0, 5, 5], [5, 5, 0]],  
        [[7, 7, 7], [0, 7, 0]],  
        [[2, 2, 2], [0, 0, 2]],  
        [[3, 3, 3], [3, 0, 0]]  
    ]
    lista_objetos[3]=15
    lista_objetos[4]=12
    lista_objetos[5]=MODALIDAD_POR_TIEMPO
    lista_objetos[6]=300.0
    lista_objetos[7]=100

    return 1

def obtenerNombreUsuario(listaJugadores,usuario):
    
    return "charbel"

def obtenerEdoProcedUsuario(listaJugadores,usuario):
    
    return "Bolívar"
def obtenerXpUsuario(listaJugadas,usuario):
    
    return 38940

#INICIALMENTE lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario,i]
#A PARTIR DE ETAPA 1: lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario,i,SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,GRID_WIDTH,GRID_HEIGHT,DESFACE_CASILLAS_Y,DESFACE_CASILLAS_X,DESFACE_Y,DESFACE_X,INITIAL_POSITION,x_ini,y_ini,screen,grid,score,clock,game_over,tetromino_sig,position_panel2,font,nombre,estado,xp,cont_jugadas,start_time,position,tetromino] 
def tetris(etapa=0,lista_objetos="",opcion=0):
    pygame.init()
    display_info=pygame.display.Info()
    DISPLAY_WIDTH,DISPLAY_HEIGHT=display_info.current_w-10,display_info.current_h-80

    #DESEMPAQUETAMOS LA LISTA DE OBJETOS
    if etapa==0:
        listaJugadas=lista_objetos[0]
        listaJugadores=lista_objetos[1]
        TETROMINOS_ESCOGIDOS=lista_objetos[2]
        n=lista_objetos[3]
        m=lista_objetos[4]
        modalidad=lista_objetos[5]
        tiempo_asignado=lista_objetos[6]
        jugadas_asignada=lista_objetos[7]
        usuario=lista_objetos[8]
    else: #PARA LAS DEMAS ETAPAS, LA LISTA DE OBJETO PASA TODAS ESTAS VARIABLES
        listaJugadas=lista_objetos[0]
        listaJugadores=lista_objetos[1]
        TETROMINOS_ESCOGIDOS=lista_objetos[2]
        n=lista_objetos[3]
        m=lista_objetos[4]
        modalidad=lista_objetos[5]
        tiempo_asignado=lista_objetos[6]
        jugadas_asignada=lista_objetos[7]
        usuario=lista_objetos[8]
        SCREEN_WIDTH=lista_objetos[9]
        SCREEN_HEIGHT=lista_objetos[10]
        GRID_SIZE_X=lista_objetos[11]
        GRID_SIZE_Y=lista_objetos[12]
        GRID_WIDTH=lista_objetos[13]
        GRID_HEIGHT=lista_objetos[14]
        DESFACE_CASILLAS_Y=lista_objetos[15]
        DESFACE_CASILLAS_X=lista_objetos[16]
        DESFACE_Y=lista_objetos[17]
        DESFACE_X=lista_objetos[18]
        INITIAL_POSITION=lista_objetos[19]
        x_ini=lista_objetos[20]
        y_ini=lista_objetos[21]
        screen=lista_objetos[22]
        grid=lista_objetos[23]
        score=lista_objetos[24]
        clock=lista_objetos[25]
        game_over=lista_objetos[26]
        tetromino_sig=lista_objetos[27]
        position_panel2=lista_objetos[28]
        font=lista_objetos[29]
        nombre=lista_objetos[30]
        estado=lista_objetos[31]
        xp=lista_objetos[32]
        cont_jugadas=lista_objetos[33]
        start_time=lista_objetos[34]
        position=lista_objetos[35]
        tetromino=lista_objetos[36]
        cont_frames=lista_objetos[37]
        i=lista_objetos[38]

    if etapa==0:    #ETAPA DE INICIO QUE SE REPITE UNA SOLA VEZ, CREA LA VENTANA Y SUS ELEMENTOS
        SCREEN_WIDTH = 50*DISPLAY_WIDTH//100//m*m   #Dejamos el 25% del ancho A CADA LADO DE LA PANTALLA para panel de control e informacion y
                                                    #el resto lo convertimos en una cantidad multiplo de m
        SCREEN_HEIGHT = (DISPLAY_HEIGHT-60)//(n+1)*n   #Le dejamos los ultimos 120px verticales, para la publicidad y 
                                                    #el resto lo convertimos en una cantidad multiplo de n
        GRID_SIZE_X = SCREEN_WIDTH//m    #nro de pixel de la base de la casilla
        GRID_SIZE_Y = SCREEN_HEIGHT//n    #nro de pixel de la altura de la casilla

        GRID_WIDTH = m #SCREEN_WIDTH // GRID_SIZE_X      #Nro de columnas del grid
        GRID_HEIGHT = n #SCREEN_HEIGHT // GRID_SIZE_Y    #Nro de filas del grid

        DESFACE_CASILLAS_Y=1  #DESFAZAR 1 CASILLA HACIA ABAJO EL GRID
        DESFACE_CASILLAS_X=(DISPLAY_WIDTH-SCREEN_WIDTH)//2//GRID_SIZE_X
        DESFACE_Y=DESFACE_CASILLAS_Y*GRID_SIZE_Y    #DESFACES EXPRESADOS EN PIXELES
        DESFACE_X=DESFACE_CASILLAS_X*GRID_SIZE_X

        INITIAL_POSITION = (GRID_WIDTH // 2, 0)
        x_ini=0+DESFACE_X
        y_ini=0+DESFACE_Y
        #CREAMOS LA VENTANA CON LAS DIMENSIONES ESPECIFICADAS
        screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("TETRIS BY UCAB SOFTWARE       APORTE PARA LOGRAR OBJETIVOS DEL DESARROLLO SOSTENIBLE(ODS)")
        #CREAMOS E INICIALIZAMOS LA MATRIZ QUE REPRESENTA LA MALLA DE JUEGO  grid_height filas por grid_width columnas
        grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        score = 0
        clock = pygame.time.Clock()     # el reloj del sistema
        game_over = False


        #JUEGO INICIA PINTANDO EL GRID VACIO
        screen.fill(BLACK)
        draw_grid(x_ini,y_ini,screen,SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y)
        tetromino_sig=random.choice(TETROMINOS_ESCOGIDOS)
        position_panel2=[DESFACE_X+SCREEN_WIDTH+100,120]
        font = pygame.font.Font(None, 36)   # ("Arial",36) es bonita tambien

        #INFO PANEL DERECHO
        next_text = font.render("NEXT:", True, WHITE)
        screen.blit(next_text, (DESFACE_X + SCREEN_WIDTH +((DISPLAY_WIDTH-(DESFACE_X+SCREEN_WIDTH))//2) - (next_text.get_width()//2), 70))
        draw_tetromino_coord_pixel(tetromino_sig,position_panel2,screen,GRID_SIZE_X,GRID_SIZE_Y,font)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (DESFACE_X + SCREEN_WIDTH +((DISPLAY_WIDTH-(DESFACE_X+SCREEN_WIDTH))//2) - (score_text.get_width()//2), 250))

        #INFO PANEL IZQUIERDO
        nombre=obtenerNombreUsuario(listaJugadores,usuario)
        estado=obtenerEdoProcedUsuario(listaJugadores,usuario)
        xp=obtenerXpUsuario(listaJugadas,usuario)
        userInfo_text=font.render(f"@{usuario}  {nombre} - {estado}     {xp}XP", True, WHITE)
        screen.blit(userInfo_text, (10, 13))

        # EN FUENTE 50: INFO TIEMPO RESTANTE O NRO DE JUGADAS RESTANTES
        if modalidad==MODALIDAD_POR_TIEMPO:
            modalidad_texto=font.render(f"{tiempo_asignado}", True, CYAN)
        else:
            modalidad_texto=font.render(f"Te restan {jugadas_asignada} jugadas", True, CYAN)
        screen.blit(modalidad_texto, (DISPLAY_WIDTH//2-modalidad_texto.get_width()//2, 10))
        font = pygame.font.Font(None, 36)   # ("Arial",36) es bonita tambien
        ############### SPRITES DEL PANEL IZQUIERDO #####################
        i=0
        cont_frames=1
        nombre_archivo1=MENSAJES_ODS[i] 
        nombre_archivo2=MENSAJES_ODS[i+1]
        mi_sprite1=pygame.image.load(nombre_archivo1)
        mi_sprite2=pygame.image.load(nombre_archivo2)
        class MiSprite1(pygame.sprite.Sprite):
            def __init__(self, x,y):
                super().__init__()
                self.image=mi_sprite1
                self.rect=self.image.get_rect()
                self.rect.topleft=(x,y) #establezco el sprite en funcion del pto topleft del sprite que yo indique 
        class MiSprite2(pygame.sprite.Sprite):
            def __init__(self, x,y):
                super().__init__()
                self.image=mi_sprite2
                self.rect=self.image.get_rect()
                self.rect.topleft=(x,y) #establezco el sprite en funcion del pto topleft del sprite que yo indique 
        sprites=pygame.sprite.Group()
        sprites.add(MiSprite1(10,55)) #coordenada en pixel
        sprites.add(MiSprite2(10,490)) #coordenada en pixel
        sprites.draw(screen)
        ############################################
        pygame.display.flip()
        pygame.time.wait(750)

        # APENAS SE PINTA EL TETROMINIO EN EL GRID COMIENZA EL TIEMPO
        tetromino = tetromino_sig     
        position = list(INITIAL_POSITION)   #[15,0] por enlistar los elementos de la tupla (15,0)
        tetromino_sig=random.choice(TETROMINOS_ESCOGIDOS)
        position_panel2=[DESFACE_X+SCREEN_WIDTH+100,120]
        draw_tetromino_casillas_grid(tetromino, position,screen,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y,font) #usa font para escribir dentro de las casillas del tetromino
        borrarTetrominioSgte(position_panel2,screen,GRID_SIZE_X,GRID_SIZE_Y)
        draw_tetromino_coord_pixel(tetromino_sig,position_panel2,screen,GRID_SIZE_X,GRID_SIZE_Y,font)
        cont_jugadas=0
        pygame.display.flip()
        start_time = pygame.time.get_ticks()
        pygame.time.wait(750)
        clock.tick(FPS)   #Aqui fijamos el nivel de velocidad, limitando la rapidez de las llamadas recursivas a la funcion 
                            #principal del juego para que no se llame recursivamente a mas de 2 fotogramas por segundo fps  

        #AGREGAMOS lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario]
        #LO SIGUIENTE [SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,GRID_WIDTH,GRID_HEIGHT,DESFACE_CASILLAS_Y,DESFACE_CASILLAS_X,DESFACE_Y,DESFACE_X,INITIAL_POSITION,x_ini,y_ini,screen,grid,score,clock,game_over,tetromino_sig,position_panel2,font,nombre,estado,xp,cont_jugadas,start_time,position,tetromino,cont_frames,i]
        lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario,SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,GRID_WIDTH,GRID_HEIGHT,DESFACE_CASILLAS_Y,DESFACE_CASILLAS_X,DESFACE_Y,DESFACE_X,INITIAL_POSITION,x_ini,y_ini,screen,grid,score,clock,game_over,tetromino_sig,position_panel2,font,nombre,estado,xp,cont_jugadas,start_time,position,tetromino,cont_frames,i]
        tetris(1,lista_objetos) #SE LLAMA RECURSIVAMENTE PERO YA ENTRA EN LA ETAPA 1
    
    if etapa==1:    #ETAPA QUE SE REPITE CONTINUAMENTE ACTUALIZANDO LA PANTALLA DEL JUEGO HASTA QUE FINALICE LA MODALIDAD DE JUEGO, HASTA QUEDAR GAMEOVER O HASTA QUE EL USUARIO ABANDONE EL JUEGO 
        if not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        position[0] -= 1
                        if check_collision(tetromino, position, grid,GRID_WIDTH,GRID_HEIGHT):
                            position[0] += 1
                            cont_jugadas+=1
                    elif event.key == pygame.K_RIGHT:
                        position[0] += 1
                        if check_collision(tetromino, position, grid,GRID_WIDTH,GRID_HEIGHT):
                            position[0] -= 1
                            cont_jugadas+=1
                    elif event.key == pygame.K_DOWN:
                        position[1] += 1
                        if check_collision(tetromino, position, grid,GRID_WIDTH,GRID_HEIGHT):
                            position[1] -= 1
                            cont_jugadas+=1
                    elif event.key == pygame.K_UP:
                        rotated_tetromino=rotate_tetromino(tetromino)
                        if not check_collision(rotated_tetromino, position, grid,GRID_WIDTH,GRID_HEIGHT):
                            tetromino = rotated_tetromino
                            cont_jugadas+=1
            position[1] += 1    #cae una fila el elem
            if check_collision(tetromino, position, grid,GRID_WIDTH,GRID_HEIGHT):
                position[1] -= 1
                merge_tetromino(tetromino, position, grid) #marca en la matriz (grid) las casillas ocupadas por el tetromino
                completed_rows_value = remove_completed_rows(grid,GRID_WIDTH,GRID_HEIGHT)
                score += completed_rows_value*100 
                
                tetromino=tetromino_sig
                position = list(INITIAL_POSITION)
                tetromino_sig = random.choice(TETROMINOS_ESCOGIDOS)
                if check_collision(tetromino, position, grid,GRID_WIDTH,GRID_HEIGHT):
                    game_over = True
            screen.fill(BLACK)
            draw_grid(x_ini,y_ini,screen,SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y)
            if not game_over: #SI GAMEOVER NO PINTO EL TETROMINI ACTUAL PARA QUE NO SE MONTE SOBRE LOS OTROS POR NO HABER ESPACIO
                draw_tetromino_casillas_grid(tetromino, position,screen,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y,font)
            #INFO PANEL DERECHO
            draw_tetromino_coord_pixel(tetromino_sig, position_panel2,screen,GRID_SIZE_X,GRID_SIZE_Y,font)
            next_text = font.render("NEXT:", True, WHITE)
            screen.blit(next_text, (DESFACE_X + SCREEN_WIDTH +((DISPLAY_WIDTH-(DESFACE_X+SCREEN_WIDTH))//2) - (next_text.get_width()//2), 70))
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (DESFACE_X + SCREEN_WIDTH +((DISPLAY_WIDTH-(DESFACE_X+SCREEN_WIDTH))//2) - (score_text.get_width()//2), 250))
            #INFO PANEL IZQUIERDO
            userInfo_text=font.render(f"@{usuario}  {nombre} - {estado}     {xp}XP", True, WHITE)
            screen.blit(userInfo_text, (10, 13))
            #INFO TIEMPO RESTANTE O NRO DE JUGADAS RESTANTES
            actual_time=pygame.time.get_ticks()
            elapsed_time = (actual_time - start_time)/1000 #convertimos a segundos los milisegundos
            font = pygame.font.Font(None, 50)   # ("Arial",36) es bonita tambien
            if modalidad==MODALIDAD_POR_TIEMPO:
                modalidad_texto=font.render(f"{int(tiempo_asignado-elapsed_time)}", True, CYAN)
                if tiempo_asignado-elapsed_time<=0.0:
                    game_over=True
            else:
                modalidad_texto=font.render(f"Te restan {jugadas_asignada-cont_jugadas} jugadas", True, CYAN)
                if jugadas_asignada-cont_jugadas<=0:
                    game_over=True
            screen.blit(modalidad_texto, (DISPLAY_WIDTH//2-modalidad_texto.get_width()//2, 10))
            font = pygame.font.Font(None, 36)   # ("Arial",36) es bonita tambien

            
            drawLocatedTetrominos(GRID_HEIGHT,GRID_WIDTH,grid,screen,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y,font)

            ############### SPRITES DEL PANEL IZQUIERDO #####################
            cont_frames+=1 
            if cont_frames%6==0:
                if i==15:i=0 
                else:i+=1
            nombre_archivo1=MENSAJES_ODS[i] 
            nombre_archivo2=MENSAJES_ODS[i+1]
            mi_sprite1=pygame.image.load(nombre_archivo1)
            mi_sprite2=pygame.image.load(nombre_archivo2)
            class MiSprite1(pygame.sprite.Sprite):
                def __init__(self, x,y):
                    super().__init__()
                    self.image=mi_sprite1
                    self.rect=self.image.get_rect()
                    self.rect.topleft=(x,y) #establezco el sprite en funcion del pto topleft del sprite que yo indique 
            class MiSprite2(pygame.sprite.Sprite):
                def __init__(self, x,y):
                    super().__init__()
                    self.image=mi_sprite2
                    self.rect=self.image.get_rect()
                    self.rect.topleft=(x,y) #establezco el sprite en funcion del pto topleft del sprite que yo indique
            sprites=pygame.sprite.Group()
            sprites.add(MiSprite1(10,55)) #coordenada en pixel
            sprites.add(MiSprite2(10,490)) #coordenada en pixel
            sprites.draw(screen)
            ############################################

            pygame.display.flip()
            clock.tick(FPS)   #Aqui fijamos el nivel de velocidad, limitando la rapidez de las llamadas recursivas a la funcion 
                            #principal del juego para que no se llame recursivamente a mas de 2 fotogramas por segundo fps  
        lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario,SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,GRID_WIDTH,GRID_HEIGHT,DESFACE_CASILLAS_Y,DESFACE_CASILLAS_X,DESFACE_Y,DESFACE_X,INITIAL_POSITION,x_ini,y_ini,screen,grid,score,clock,game_over,tetromino_sig,position_panel2,font,nombre,estado,xp,cont_jugadas,start_time,position,tetromino,cont_frames,i]
        if not game_over:
            tetris(1,lista_objetos) ##LLAMADA RECURSIVA EN EL CASO QUE NO OCURRIO: LA FINALIZACION LA MODALIDAD DE JUEGO(TIEMPO O NRO JUGADAS), QUEDAR GAMEOVER NI ABANDONO DEL JUEGO POR PARTE DEL USUARIO
        else:
            tetris(2,lista_objetos) #LLAMADA RECURSIVA PARA FINALIZAR POR: AGOTADA LA MODALIDAD DE JUEGO(TIEMPO O NRO JUGADAS), QUEDAR GAMEOVER O POR ABANDONO DEL JUEGO POR PARTE DEL USUARIO


    #AL SALIR POR FINALIZAR MODALIDAD DE JUEGO,POR ABANDONO DEL USUARIO O POR QUEDAR GAMEOVER
    if etapa==2:
        if opcion==0:    
            end_time=pygame.time.get_ticks()
        else:
            end_time=lista_objetos[39]
        elapsed_time = int((end_time - start_time) / 1000) #redondeamos el cronometro a 3 decimales

        #AGREGAR ESTA JUGADA A LISTA_JUGADAS

        screen.fill(BLACK)
        draw_grid(x_ini,y_ini,screen,SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y)
        #INFO PANEL DERECHO
        draw_tetromino_coord_pixel(tetromino_sig, position_panel2,screen,GRID_SIZE_X,GRID_SIZE_Y,font)
        next_text = font.render("NEXT:", True, WHITE)
        screen.blit(next_text, (DESFACE_X + SCREEN_WIDTH +((DISPLAY_WIDTH-(DESFACE_X+SCREEN_WIDTH))//2) - (next_text.get_width()//2), 70))
        
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (DESFACE_X + SCREEN_WIDTH +((DISPLAY_WIDTH-(DESFACE_X+SCREEN_WIDTH))//2) - (score_text.get_width()//2), 250))
        time_text = font.render(f"Time: {elapsed_time} seconds", True, WHITE)
        screen.blit(time_text, (DESFACE_X + SCREEN_WIDTH +((DISPLAY_WIDTH-(DESFACE_X+SCREEN_WIDTH))//2) - (time_text.get_width()//2), 300))
        
        #EN TUS ULTIMAS JUGADAS MOSTRADAS EN PANEL DERECHO SE INCLUYE ESTA ULTIMA.

        anchoBoton=180
        altoBoton=40
        botonNuevaRonda=pygame.draw.rect(screen,COLOR_BOTON,(DESFACE_X + SCREEN_WIDTH+10,500,anchoBoton,altoBoton))
        botonCerrarSesion=pygame.draw.rect(screen,COLOR_BOTON,(DESFACE_X + SCREEN_WIDTH+200,500,anchoBoton,altoBoton))
        nuevaRonda_caption=font.render("Nueva ronda", True, BLACK)
        screen.blit(nuevaRonda_caption,(DESFACE_X + SCREEN_WIDTH+10+((anchoBoton-nuevaRonda_caption.get_width())//2),500+((altoBoton-nuevaRonda_caption.get_height())//2)))
        cerrarSesion_caption=font.render("Cerrar sesion", True, BLACK)
        screen.blit(cerrarSesion_caption,(DESFACE_X + SCREEN_WIDTH+200+((anchoBoton-cerrarSesion_caption.get_width())//2),500+((altoBoton-cerrarSesion_caption.get_height())//2)))


        #INFO PANEL IZQUIERDO
        userInfo_text=font.render(f"@{usuario}  {nombre} - {estado}     {xp}XP", True, WHITE)
        screen.blit(userInfo_text, (10, 13))
        
        #INFO TIEMPO RESTANTE O NRO DE JUGADAS RESTANTES
        #actual_time=pygame.time.get_ticks()
        #elapsed_time = (actual_time - start_time)/1000 #convertimos a segundos los milisegundos
        font = pygame.font.Font(None, 50)   # ("Arial",36) es bonita tambien
        if modalidad==MODALIDAD_POR_TIEMPO:
            modalidad_texto=font.render("0", True, CYAN)
        else:
            modalidad_texto=font.render("Te restan 0 jugadas", True, CYAN)
        screen.blit(modalidad_texto, (DISPLAY_WIDTH//2-modalidad_texto.get_width()//2, 10))
        font = pygame.font.Font(None, 36)   # ("Arial",36) es bonita tambien
        
        drawLocatedTetrominos(GRID_HEIGHT,GRID_WIDTH,grid,screen,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y,font)

        ############### SPRITES DEL PANEL IZQUIERDO #####################
        cont_frames+=1 
        if cont_frames%6==0:
            if i==15:i=0 
            else:i+=1
        nombre_archivo1=MENSAJES_ODS[i] 
        nombre_archivo2=MENSAJES_ODS[i+1]
        mi_sprite1=pygame.image.load(nombre_archivo1)
        mi_sprite2=pygame.image.load(nombre_archivo2)
        class MiSprite1(pygame.sprite.Sprite):
            def __init__(self, x,y):
                super().__init__()
                self.image=mi_sprite1
                self.rect=self.image.get_rect()
                self.rect.topleft=(x,y) #establezco el sprite en funcion del pto topleft del sprite que yo indique 
        class MiSprite2(pygame.sprite.Sprite):
            def __init__(self, x,y):
                super().__init__()
                self.image=mi_sprite2
                self.rect=self.image.get_rect()
                self.rect.topleft=(x,y) #establezco el sprite en funcion del pto topleft del sprite que yo indique
        sprites=pygame.sprite.Group()
        sprites.add(MiSprite1(10,55)) #coordenada en pixel
        sprites.add(MiSprite2(10,490)) #coordenada en pixel
        sprites.draw(screen)
        ############################################

        pygame.display.flip()
        clock.tick(FPS)   #Aqui fijamos el nivel de velocidad, limitando la rapidez de las llamadas recursivas a la funcion 
                        #principal del juego para que no se llame recursivamente a mas de 2 fotogramas por segundo fps  
        for event in pygame.event.get():
            lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario]
            if event.type == pygame.QUIT:
                pygame.quit()
                main(3,0,lista_objetos) #RESPALDAR SISTEMA
                return            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botonNuevaRonda.collidepoint(event.pos):
                    pygame.quit()   #CERRAMOS LA VENTANA DE JUEGO
                    # SE CREA NUEVA VENTANA PARA CONFIGURAR JUGADA 
                    if not dialogoConfigJuego(lista_objetos): #SI EL USUARIO CERRO LA VENTANA DE CONFIGURACION DEL JUEGO 
                        main(1,2,lista_objetos)   #REPITE EL INICIO DE SESION 
                    else:
                        if not tetris(0,lista_objetos):    #SI EL USUARIO CERRO LA VENTANA DEL JUEGO TETRIS ESTANDO FINALIZADO, ES EQUIVALENTE A CERRAR SESION
                            main(3,0,lista_objetos)
                    return
                if botonCerrarSesion.collidepoint(event.pos):
                    pygame.quit()
                    main(3,0,lista_objetos)
                    return
        lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario,SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,GRID_WIDTH,GRID_HEIGHT,DESFACE_CASILLAS_Y,DESFACE_CASILLAS_X,DESFACE_Y,DESFACE_X,INITIAL_POSITION,x_ini,y_ini,screen,grid,score,clock,game_over,tetromino_sig,position_panel2,font,nombre,estado,xp,cont_jugadas,start_time,position,tetromino,cont_frames,i,end_time]
        tetris(2,lista_objetos,1) #LLAMADA RECURSIVA PARA FINALIZAR POR: AGOTADA LA MODALIDAD DE JUEGO(TIEMPO O NRO JUGADAS), QUEDAR GAMEOVER O POR ABANDONO DEL JUEGO POR PARTE DEL USUARIO





#ETAPA QUE SE REPITE CONTINUAMENTE ACTUALIZANDO LA PANTALLA DE FINAL DEL JUEGO HASTA QUE SELECCIONEN: INICIAR NUEVA RONDA DE JUEGO O CERRAR SESION 
    if etapa==3:
        if not respaldarSistema(lista_objetos):
            #IMPRIMIR MENSAJE DE ERROR
            return
        return 1
    
    return 1




#lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario]
def main(etapa=0,opcion=0,lista_objetos=""):
    if etapa==0:
        if opcion==0:
            if not cargarSistema(lista_objetos):
                #IMPRIMIR MENSAJE DE ERROR
                return
        opcionMenuIni=menuIni() #SIEMPRE QUE SE MANDE A ETAPA 0 ES PINTAR EL MENU INICIAL
        if opcionMenuIni==1:
            main(1,1,lista_objetos)    
        elif opcionMenuIni==2:
            main(1,2,lista_objetos)
        elif opcionMenuIni==3:  #OPCION salir de menu ini
            return
    elif etapa==1:
        if opcion==1:
            dialogoRegistrarUsuario(lista_objetos)
            main(0,1,lista_objetos)
        elif opcion==2:
            if not dialogoInicioSesion(lista_objetos):  #SI EL USUARIO CERRO LA VENTANA DE LOGIN
                main(0,1,lista_objetos)  #SE VUELVE AL MENU INICIAL PERO CON OPC=1 PARA NO CARGAR SISTEMA NUEVAMENTE
            else:
                opcionMenuJuego=menuJuego() 
                if opcionMenuJuego==1:
                    if not dialogoConfigJuego(lista_objetos): #SI EL USUARIO CERRO LA VENTANA DE CONFIGURACION DEL JUEGO 
                        main(1,2,lista_objetos)   #REPITE EL INICIO DE SESION 
                    else:
                        tetris(0,lista_objetos)
                elif opcionMenuJuego==2:
                    jugada_max_puntuacion_jugador(lista_objetos)
                elif opcionMenuJuego==3:
                    jugada_max_puntuacion_estado(lista_objetos)
                elif opcionMenuJuego==4:
                    reporte_Jugador(lista_objetos)
                elif opcionMenuJuego==5:
                    top10_pais(lista_objetos)
                elif opcionMenuJuego==6:
                    top10_estado(lista_objetos)
                elif opcionMenuIni==7:  #OPCION SALIR MENU JUEGO
                    return







        elif opcion==3: # SALIR
            if not respaldarSistema(lista_objetos):
                #IMPRIMIR MENSAJE DE ERROR
                return
            return
    

listaJugadas=[]
listaJugadores=[]
usuario=""
n=15
m=12
TETROMINOS_ESCOGIDOS=[]
modalidad=MODALIDAD_POR_TIEMPO
tiempo_asignado=300.0
jugadas_asignada=100
lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario]
main(0,0,lista_objetos)
