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

ESTADOS_DE_VENEZUELA=  ["AMAZONAS", "ANZOÁTEGUI", "APURE", "ARAGUA", "BARINAS", "BOLÍVAR", "CARABOBO", "COJEDES", "DELTA AMACURO", "DISTRITO CAPITAL", "FALCÓN", "GUÁRICO", "LARA", "MÉRIDA", "MIRANDA", "MONAGAS", "NUEVA ESPARTA", "PORTUGUESA", "SUCRE", "TÁCHIRA", "TRUJILLO", "VARGAS", "YARACUY", "ZULIA"]


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
LISTA_COLORES_TETROMINOS=[CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE] #EL COLOR DEL TETROMINO Nro t ES EL COLOR INDICADO EN LA POSICION t DE LA LISTA 

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


def cargarSistema():

    #devuelve 1 si todo ok, 0 si hubo problema de memorias o abriendo archivos
    return 1


########################################################################################
#CADA UNA DE LOS SIGTES MENU Y DIALOGOS, CREAN SU VENTANA Y LA CIERRAN ANTES DEL MENU
########################################################################################


def menuIni():
    #CREA LA VENTANA CON EL MENU: 1)REGISTRAR USUARIO 2)INICIAR SESION 3)OLVIDASTE TU NOMBRE DE USUARIO? 4)OLVIDASTE TU CONTRASEñA 5)SALIR Y RETORNA LA OPCION SELECCIONADA
    
    #DEVUELVE LA OPCION DEL MENU INICIAL SELECCIONADA. SI CIERRAN
    return 2

#lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario]
def dialogoRegistrarUsuario(lista_objetos):

    #SI LOGRA REGISTRAR EL USUARIO EXITOSAMENTE, MANDA EL MENSAJE Y RETURN 1, SINO, SI ALT+F4 O CERRARON VENTANA RETURN 0
    lista_objetos[8]="charbel_k_18"
    return 1

def dialogoInicioSesion(lista_objetos):

    #PINTA EL CUADRO DE DIALOGO Y SI EL USUARIO O LA CLAVE SON INAVLIDOS, MANDA EL MENSAJE, Y VUELVE A PEDIR LOS DATOS.
    #SI EL PROCESO FUE BIEN RETORNA 1, SI EL USUARIO CERRO LA VENTANA RETORNA 0
    lista_objetos[8]="charbel_k_18"
    return 1

#lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario]
def dialogoConfigJuego(lista_objetos):
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

#lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario]
def tetris(etapa=0,lista_objetos=""):
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
        tetromino_sig_color=lista_objetos[28]
        position_panel2=lista_objetos[29]
        font=lista_objetos[30]
        nombre=lista_objetos[31]
        estado=lista_objetos[32]
        xp=lista_objetos[33]
        cont_jugadas=lista_objetos[34]
        start_time=lista_objetos[35]
        position=lista_objetos[36]
        tetromino=lista_objetos[37]

    if etapa==0:
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
        DESFACE_Y=DESFACE_CASILLAS_Y*GRID_SIZE_Y
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


        #INICIALIZA CON EL GRID VACIO
        tetromino_sig=random.choice(TETROMINOS_ESCOGIDOS)
        tetromino_sig_color = obtener_tetromino_color(tetromino_sig,LISTA_COLORES_TETROMINOS) #random.choice([CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE])
        position_panel2=[DESFACE_X+SCREEN_WIDTH+100,120]
        screen.fill(BLACK)
        draw_grid(x_ini,y_ini,screen,SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y)
        font = pygame.font.Font(None, 36)   # ("Arial",36) es bonita tambien
        #INFO PANEL DERECHO
        draw_tetromino_coord_pixel(tetromino_sig,position_panel2,screen,GRID_SIZE_X,GRID_SIZE_Y,font)
        next_text = font.render("NEXT:", True, WHITE)
        screen.blit(next_text, (DESFACE_X + SCREEN_WIDTH +((DISPLAY_WIDTH-(DESFACE_X+SCREEN_WIDTH))//2) - (next_text.get_width()//2), 70))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (DESFACE_X + SCREEN_WIDTH +((DISPLAY_WIDTH-(DESFACE_X+SCREEN_WIDTH))//2) - (score_text.get_width()//2), 250))
        #INFO PANEL IZQUIERDO
        user_text=font.render(f"@{usuario}", True, WHITE)
        screen.blit(user_text, (40, 70))
        nombre=obtenerNombreUsuario(listaJugadores,usuario)
        estado=obtenerEdoProcedUsuario(listaJugadores,usuario)
        nombre_edo_text=font.render(f"{nombre} - {estado}", True, WHITE)
        screen.blit(nombre_edo_text, (40, 100))
        font = pygame.font.Font(None, 50)   # ("Arial",36) es bonita tambien
        xp=obtenerXpUsuario(listaJugadas,usuario)
        if xp>10000:
            xp_text=font.render(f"{xp}XP", True, CYAN)
        else:
            xp_text=font.render(f"{xp}PUNTOS", True, CYAN)
        screen.blit(xp_text, (40, 130))
        #INFO TIEMPO RESTANTE O NRO DE JUGADAS RESTANTES
        if modalidad==MODALIDAD_POR_TIEMPO:
            modalidad_texto=font.render(f"{tiempo_asignado}", True, CYAN)
        else:
            modalidad_texto=font.render(f"Te restan {jugadas_asignada} jugadas", True, CYAN)
        screen.blit(modalidad_texto, (DISPLAY_WIDTH//2-modalidad_texto.get_width()//2, 10))
        #FIN MENSAJES CON FUENTE 50
        font = pygame.font.Font(None, 36)   # ("Arial",36) es bonita tambien
        cont_jugadas=0
        pygame.display.flip()
        pygame.time.wait(750)

        #clock.tick(FPS)   #Aqui fijamos el nivel de velocidad, limitando la rapidez de las llamadas recursivas a la funcion 
                            #principal del juego para que no se llame recursivamente a mas de 2 fotogramas por segundo fps  

        # APENAS SE PINTA EL TETROMINIO EN EL GRID COMIENZA EL TIEMPO
        tetromino = tetromino_sig   #ESCOGE UNA FIGURA DE LA LISTA DE LOS 5 ESCOGIDOS POR EL JUGADOR. A SU VEZ CADA FIGURA ES UNA LISTA DE LISTAS.  
        tetromino_color = obtener_tetromino_color(tetromino,LISTA_COLORES_TETROMINOS) #random.choice([CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE])
        position = list(INITIAL_POSITION)   #[15,0] por enlistar los elementos de la tupla (15,0)
        tetromino_sig=random.choice(TETROMINOS_ESCOGIDOS)
        tetromino_sig_color = obtener_tetromino_color(tetromino_sig,LISTA_COLORES_TETROMINOS) #random.choice([CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE])
        position_panel2=[DESFACE_X+SCREEN_WIDTH+100,120]
        screen.fill(BLACK)
        draw_grid(x_ini,y_ini,screen,SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y)
        font = pygame.font.Font(None, 36)   # ("Arial",36) es bonita tambien
        draw_tetromino_casillas_grid(tetromino, position,screen,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y,font) #usa font para escribir dentro de las casillas del tetromino
        #INFO PANEL DERECHO
        draw_tetromino_coord_pixel(tetromino_sig,position_panel2,screen,GRID_SIZE_X,GRID_SIZE_Y,font)
        next_text = font.render("NEXT:", True, WHITE)
        screen.blit(next_text, (DESFACE_X + SCREEN_WIDTH +((DISPLAY_WIDTH-(DESFACE_X+SCREEN_WIDTH))//2) - (next_text.get_width()//2), 70))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (DESFACE_X + SCREEN_WIDTH +((DISPLAY_WIDTH-(DESFACE_X+SCREEN_WIDTH))//2) - (score_text.get_width()//2), 250))
        #INFO PANEL IZQUIERDO
        user_text=font.render(f"@{usuario}", True, WHITE)
        screen.blit(user_text, (40, 70))
        nombre_edo_text=font.render(f"{nombre} - {estado}", True, WHITE)
        screen.blit(nombre_edo_text, (40, 100))
        font = pygame.font.Font(None, 50)   # ("Arial",36) es bonita tambien
        #INFO PUNTAJE ACUMULADO
        if xp>10000:
            xp_text=font.render(f"{xp}XP", True, CYAN)
        else:
            xp_text=font.render(f"{xp}PUNTOS", True, CYAN)
        screen.blit(xp_text, (40, 130))
        #INFO TIEMPO RESTANTE O NRO DE JUGADAS RESTANTES
        if modalidad==MODALIDAD_POR_TIEMPO:
            modalidad_texto=font.render(f"{tiempo_asignado}", True, CYAN)
        else:
            modalidad_texto=font.render(f"Te restan {jugadas_asignada} jugadas", True, CYAN)
        screen.blit(modalidad_texto, (DISPLAY_WIDTH//2-modalidad_texto.get_width()//2, 10))
        #FIN MENSAJES CON FUENTE 50
        font = pygame.font.Font(None, 36)   # ("Arial",36) es bonita tambien
        cont_jugadas=0
        pygame.display.flip()
        pygame.time.wait(750)
        clock.tick(FPS)   #Aqui fijamos el nivel de velocidad, limitando la rapidez de las llamadas recursivas a la funcion 
                            #principal del juego para que no se llame recursivamente a mas de 2 fotogramas por segundo fps  
        start_time = pygame.time.get_ticks()

        #AGREGAMOS lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario]
        #LO SIGUIENTE [SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,GRID_WIDTH,GRID_HEIGHT,DESFACE_CASILLAS_Y,DESFACE_CASILLAS_X,DESFACE_Y,DESFACE_X,INITIAL_POSITION,x_ini,y_ini,screen,grid,score,clock,game_over,tetromino_sig,tetromino_sig_color,position_panel2,font,nombre,estado,xp,cont_jugadas,start_time,position,tetromino]
        lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario,SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,GRID_WIDTH,GRID_HEIGHT,DESFACE_CASILLAS_Y,DESFACE_CASILLAS_X,DESFACE_Y,DESFACE_X,INITIAL_POSITION,x_ini,y_ini,screen,grid,score,clock,game_over,tetromino_sig,tetromino_sig_color,position_panel2,font,nombre,estado,xp,cont_jugadas,start_time,position,tetromino]
        # lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario,SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,GRID_WIDTH,GRID_HEIGHT,DESFACE_CASILLAS_Y,DESFACE_CASILLAS_X,DESFACE_Y,DESFACE_X,INITIAL_POSITION,x_ini,y_ini,screen,grid,score,clock,game_over,tetromino_sig,tetromino_sig_color,position_panel2,font,nombre,estado,xp,cont_jugadas,start_time,position,tetromino]
        tetris(1,lista_objetos)
    if etapa==1:
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
                #tetromino_color=tetromino_sig_color
                position = list(INITIAL_POSITION)
                tetromino_sig = random.choice(TETROMINOS_ESCOGIDOS)
                tetromino_sig_color = obtener_tetromino_color(tetromino_sig,LISTA_COLORES_TETROMINOS) #random.choice([CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE])
                if check_collision(tetromino, position, grid,GRID_WIDTH,GRID_HEIGHT):
                    game_over = True
            screen.fill(BLACK)
            draw_grid(x_ini,y_ini,screen,SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y)
            if not game_over:
                draw_tetromino_casillas_grid(tetromino, position,screen,GRID_SIZE_X,GRID_SIZE_Y,DESFACE_X,DESFACE_Y,font)
            #INFO PANEL DERECHO
            draw_tetromino_coord_pixel(tetromino_sig, position_panel2,screen,GRID_SIZE_X,GRID_SIZE_Y,font)
            next_text = font.render("NEXT:", True, WHITE)
            screen.blit(next_text, (DESFACE_X + SCREEN_WIDTH +((DISPLAY_WIDTH-(DESFACE_X+SCREEN_WIDTH))//2) - (next_text.get_width()//2), 70))
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (DESFACE_X + SCREEN_WIDTH +((DISPLAY_WIDTH-(DESFACE_X+SCREEN_WIDTH))//2) - (score_text.get_width()//2), 250))
            #INFO PANEL IZQUIERDO
            user_text=font.render(f"@{usuario}", True, WHITE)
            screen.blit(user_text, (40, 70))
            nombre_edo_text=font.render(f"{nombre} - {estado}", True, WHITE)
            screen.blit(nombre_edo_text, (40, 100))
            font = pygame.font.Font(None, 50)   # ("Arial",36) es bonita tambien
            xp_text=font.render(f"{xp}XP", True, CYAN)
            screen.blit(xp_text, (40, 130))
            font = pygame.font.Font(None, 36)   # ("Arial",36) es bonita tambien
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

            
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if grid[y][x] > 0:
                        COLOR_CASILLA=LISTA_COLORES_TETROMINOS[grid[y][x]-1]
                        pygame.draw.rect(screen, COLOR_CASILLA, (x * GRID_SIZE_X+DESFACE_X, y * GRID_SIZE_Y+DESFACE_Y, GRID_SIZE_X, GRID_SIZE_Y))
                        valor_casilla_text=font.render(f"{grid[y][x]}", True, BLACK)
                        screen.blit(valor_casilla_text, ((((x * GRID_SIZE_X)+(GRID_SIZE_X//2)+DESFACE_X) - (valor_casilla_text.get_width()//2)), (((y * GRID_SIZE_Y)+(GRID_SIZE_Y//2)+DESFACE_Y) - (valor_casilla_text.get_height()//2))))

            pygame.display.flip()
            clock.tick(FPS)   #Aqui fijamos el nivel de velocidad, limitando la rapidez de las llamadas recursivas a la funcion 
                            #principal del juego para que no se llame recursivamente a mas de 2 fotogramas por segundo fps  
            """############### SPRITE#####################
            nombre_archivo="ods13-14-15.jpg"
            mi_sprite=pygame.image.load(nombre_archivo)
            class MiSprite(pygame.sprite.Sprite):
                def __init__(self, x,y):
                    super().__init__()
                    self.image=mi_sprite
                    self.rect=self.image.get_rect()
                    self.rect.topleft=(x,y) #establezco el sprite en funcion del pto topleft del sprite que yo indique 
            sprites=pygame.sprite.Group()
            sprites.add(MiSprite(0,n*GRID_SIZE_Y))
            sprites.draw(screen)
            ############################################"""
        lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario,SCREEN_WIDTH,SCREEN_HEIGHT,GRID_SIZE_X,GRID_SIZE_Y,GRID_WIDTH,GRID_HEIGHT,DESFACE_CASILLAS_Y,DESFACE_CASILLAS_X,DESFACE_Y,DESFACE_X,INITIAL_POSITION,x_ini,y_ini,screen,grid,score,clock,game_over,tetromino_sig,tetromino_sig_color,position_panel2,font,nombre,estado,xp,cont_jugadas,start_time,position,tetromino]
        if not game_over:
            tetris(1,lista_objetos)
        else:
            tetris(2,lista_objetos)
    if etapa==2:    
        #AL SALIR POR FINALIZAR O QUEDAR GAMEOVER
        #SE MUESTRA EL GRID COMO QUEDO Y EN TUS ULTIMAS JUGADAS MOSTRADAS EN PANEL 2 SE INCLUYE ESTA ULTIMA.
        # EN VEZ DE TIEMPO RESTANTE O NRO JUGADAS RESTANTES SE MUESTRA EN PANEL 2 EL TIEMPO USADO O EL NRO DE JUGADAS HECHAS
        # Y EN PANEL 2 LA OPCION DE INICIAR NUEVA RONDA DE JUEGO O CERRAR SESION
        # Y LOS SPRITES SI SE SIGUEN CAMBIANDO

        end_time=pygame.time.get_ticks()
        elapsed_time = (end_time - start_time) / 1000 #redondeamos el cronometro a 3 decimales
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)   # ("Arial",36) es bonita tambien

        tmp_text = font.render(f"Ancho del Monitor: {DISPLAY_WIDTH} Alto del Monitor: {DISPLAY_HEIGHT}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        time_text = font.render(f"Time: {elapsed_time} seconds", True, WHITE)

        screen.blit(tmp_text, (SCREEN_WIDTH // 2 - tmp_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(1000)
        #si en la pantalla final evaluar las opciones
        return 1

    if etapa==3:
        return 1
    
    return 1




#lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario]
def main(etapa=0,opcion=0,lista_objetos=""):
    if etapa==0:
        if opcion==0:
            if not cargarSistema():
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
                if not dialogoConfigJuego(lista_objetos): #SI EL USUARIO CERRO LA VENTANA DE CONFIGURACION DEL JUEGO 
                    main(1,2,lista_objetos)   #REPITE EL INICIO DE SESION 
                else:
                    if not tetris(0,lista_objetos):    #SI EL USUARIO CERRO LA VENTANA DEL JUEGO TETRIS, SE VUELVE AL DIALOGO PARA CONFIGURAR EL JUEGO
                        main(1,2,lista_objetos)
        elif opcion==3:
            return
    

listaJugadas=[]
listaJugadores=[]
#cargar sistema de main las llena
usuario=""
n=15
m=12
TETROMINOS_ESCOGIDOS=[]
modalidad=MODALIDAD_POR_TIEMPO
tiempo_asignado=300.0
jugadas_asignada=100
#configurar jugada de main le pone los valores

#jugador=("charbel_k_18","charbel180806@gmail.com","Charbel","KHALIL",5,"Tetris*123")
#usuario="charbel_k_18"
#nombre="Charbel"
#estado="Bolivar"
#xp="38940"





pygame.init()
display_info=pygame.display.Info()
DISPLAY_WIDTH,DISPLAY_HEIGHT=display_info.current_w-10,display_info.current_h-80
lista_objetos=[listaJugadas,listaJugadores,TETROMINOS_ESCOGIDOS,n,m,modalidad,tiempo_asignado,jugadas_asignada,usuario]
main(0,0,lista_objetos)
pygame.quit()   












