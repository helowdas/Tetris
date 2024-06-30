from ajustes import *

class Datos_usuario:
    def __init__(self):
        self.display_surface=pygame.display.get_surface()
        self.surface=pygame.Surface((sidebar_ancho,alto_juego*datos_usuario-margen))
        self.rect=self.surface.get_rect(bottomright=(window_ancho-margen,window_alto-margen))   #PARA MOVERLO AL SIDEBAR        
        
    def run(self):
        self.display_surface.blit(self.surface,self.rect)