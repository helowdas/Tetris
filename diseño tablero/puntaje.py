from ajustes import *

class Puntaje:
    def __init__(self):
        self.display_surface=pygame.display.get_surface()
        self.surface=pygame.Surface((sidebar_ancho,alto_juego*score_alto-margen))
        self.rect=self.surface.get_rect(midright=(window_ancho-margen,window_alto//2-45))   #PARA MOVERLO AL SIDEBAR
        
    def run(self):
        self.display_surface.blit(self.surface,self.rect)
        pygame.draw.rect(self.display_surface, blanco, self.rect, 2, 2)  #BORDE DEL TABLERO



#self.rect=self.surface.get_rect(midright=(1130,310))   #PARA MOVERLO AL SIDEBAR