from ajustes import * 
import sys
#COMPONENTES
from juego import Juego
from puntaje import Puntaje
from preview import Preview
from datos_usuario import Datos_usuario


class Main:
    def __init__(self):
        #GENERAL
        pygame.init()
        self.display_surface=pygame.display.set_mode((window_ancho,window_alto))
        self.clock=pygame.time.Clock()
        pygame.display.set_caption("TETRIS")

        #COMPONENTES
        self.juego=Juego()
        self.preview=Preview()
        self.puntaje=Puntaje()
        self.datos_usuario=Datos_usuario()
       
     

    def run(self):  #bucle juego
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #fondito
            self.display_surface.fill(azul)

            #COMPONENTS
            self.juego.run() 
            self.preview.run() 
            self.puntaje.run() 
            self.datos_usuario.run() 
          
           
            #ACTUALIZACIÓN DEL JUEGO
            pygame.display.update()
            self.clock.tick(100)  #FPS


if __name__=="__main__":
    main=Main()
    main.run()