import pygame
import sys
import time
# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Menú de Juego')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fuentes
font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    click  = False

    while True:
        screen.fill(WHITE)
        draw_text('Menú de Juego', font, BLACK, screen, 300, 100)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(300, 200, 200, 50)
        button_2 = pygame.Rect(300, 300, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click != False:
                time_menu()
        if button_2.collidepoint((mx, my)):
            if click != False:
                move_menu()

        pygame.draw.rect(screen, GRAY, button_1)
        pygame.draw.rect(screen, GRAY, button_2)

        draw_text('Jugar por Tiempo', font, BLACK, screen, 320, 210)
        draw_text('Jugar por Movimientos', font, BLACK, screen, 305, 310)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def time_menu():
    input_active = False
    user_text = ''
    input_box = pygame.Rect(300, 200, 200, 50)
    clock = pygame.time.Clock()
    game_started = False
    start_time = 0
    duration = 0

    while True:
        screen.fill(WHITE)
        draw_text('Ingrese el tiempo de juego en segundos', font, BLACK, screen, 150, 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        try:
                            duration = int(user_text)
                            start_time = time.time()
                            game_started = True
                            user_text = ''
                        except ValueError:
                            print("Por favor ingrese un número válido.")
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        if game_started:
            elapsed_time = time.time() - start_time
            remaining_time = duration - elapsed_time
            if remaining_time <= 0:
                draw_text('Juego terminado', font, BLACK, screen, 300, 300)
                game_started = False
            else:
                draw_text(f'Tiempo restante: {int(remaining_time)} segundos', font, BLACK, screen, 300, 300)

        color = BLACK if input_active else GRAY
        pygame.draw.rect(screen, color, input_box, 2)

        txt_surface = font.render(user_text, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 10))

        input_box.w = max(200, txt_surface.get_width() + 10)

        pygame.display.flip()
        clock.tick(30)

def move_menu():
    input_active = False
    user_text = ''
    input_box = pygame.Rect(300, 200, 200, 50)
    clock = pygame.time.Clock()
    game_started = False
    moves_count = 0
    target_moves = 0

    while True:
        screen.fill(WHITE)
        draw_text('Ingrese la cantidad de movimientos', font, BLACK, screen, 200, 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        try:
                            target_moves = int(user_text)
                            game_started = True
                            moves_count = 0
                            user_text = ''
                        except ValueError:
                            print("Por favor ingrese un número válido.")
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
                elif game_started:
                    moves_count += 1
                    print(f"Movimiento {moves_count} de {target_moves}")
                    if moves_count >= target_moves:
                        game_started = False
                        draw_text('Juego terminado', font, BLACK, screen, 300, 300)

        if game_started:
            draw_text(f'Movimientos restantes: {target_moves - moves_count}', font, BLACK, screen, 300, 300)

        color = BLACK if input_active else GRAY
        pygame.draw.rect(screen, color, input_box, 2)

        txt_surface = font.render(user_text, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 10))

        input_box.w = max(200, txt_surface.get_width() + 10)

        pygame.display.flip()
        clock.tick(30)

main_menu()
