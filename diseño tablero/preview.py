from ajustes import *

class Preview:
    def __init__(self):
        self.display_surface=pygame.display.get_surface()
        self.surface=pygame.Surface((sidebar_ancho,alto_juego*preview_alto-margen))
        self.rect=self.surface.get_rect(topright=(window_ancho-margen,margen))   #PARA MOVERLO AL SIDEBAR
        

    def run(self):
        self.display_surface.blit(self.surface,self.rect)