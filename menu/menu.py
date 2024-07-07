import pygame
from menu import botones

pygame.init()

# Crear ventana de juego
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TetroBreak")

# Variables del juego
menu_state = "main"

# Definir fuentes
font = pygame.font.SysFont("arialblack", 40)

# Definir colores
TEXT_COL = (255, 255, 255)

# Cargar imágenes de los botones
jugar_img = pygame.image.load("menu/jugar.png").convert_alpha()
informes_img = pygame.image.load("menu/informe.png").convert_alpha()
cerrar_sesion_img = pygame.image.load("menu/salir.png").convert_alpha()
informes_top10_img = pygame.image.load("menu/top10.png").convert_alpha()
atras_img = pygame.image.load("menu/atras.png").convert_alpha()

# Crear los botones
jugar_boton = botones.Button((SCREEN_WIDTH - 250) // 2, (SCREEN_HEIGHT - 100) //2 , jugar_img, 0.8)
informes_boton = botones.Button((SCREEN_WIDTH - 250)//2, (SCREEN_HEIGHT + 75) // 2, informes_img, 0.8)
cerrar_sesion = botones.Button((SCREEN_WIDTH - 250)//2, 450, cerrar_sesion_img, 0.8)
informes_top10_img = botones.Button((SCREEN_WIDTH - 250)//2,(SCREEN_HEIGHT - 50)//2,informes_top10_img,0.8)
atras_img = botones.Button((SCREEN_WIDTH - 250)//2,(SCREEN_HEIGHT + 400)//2,atras_img,0.8)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))



# Bucle principal del juego
def pygame_menu():
    menu_state = "main"
    run = True
    while run:

        screen.fill((51, 153, 255))
        draw_text("Tetris Break", font, TEXT_COL, (SCREEN_HEIGHT - 110) //2, (SCREEN_WIDTH - 600)//2)    
    # Comprobar si el juego está pausado
    #if game_paused:
        # Comprobar el estado del menú
        if menu_state == "main":
            # Dibujar los botones del menú de pausa
            if jugar_boton.draw(screen):
                menu_state = "Jugar"
                if menu_state == "jugar":
                    print("SELECCIONE MODO DE JUEGO")
            if informes_boton.draw(screen):
                menu_state = "Informe"
            if cerrar_sesion.draw(screen):
                run = False
        # Comprobar si el menú de opciones está abierto
        if menu_state == "Informe":
            # Dibujar los botones de las diferentes opciones
            if atras_img.draw(screen):
                menu_state = "main"
            if informes_top10_img.draw(screen):
                print("TOP 10 DE VENEZUELA")

                if atras_img.draw(screen):
                    menu_state = "main"
    #else:
        #draw_text("Presiona ESPACIO para pausar", font, TEXT_COL, 160, 250)

    # Manejador de eventos
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = True
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


