# python -m venv mi_entorno
# .\mi_entorno\Scripts\Activate.ps1
# pip install pygame
# python .\trabajo.py

import pygame,sys
from pygame.locals import *
from figuras import *
from tablero import *
from dibujar_piezas import *
from movimiento import *  
from menu import mostrar_menu, dibujar_boton_reinicio, BOTON_REINICIO
from temporizador import Temporizador        



def main():
    pygame.init()
    ANCHO = 800
    ALTO  = 880                    
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ajedrez.Fig")
    clock = pygame.time.Clock()
    #TODO
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    estado_juego = tablero_inicial

    cargar_imagenes1(100)
    
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:                   
                estado_juego = manejar_click(estado_juego, event.pos, 100)

        screen.fill(BLANCO)
        #font = pygame.font.SysFont("Arial", 30)
        #text = font.render("Hola Mundo!", True, BLANCO)

        #text_rect = text.get_rect()
        #text_rect.center =  (ANCHO // 2, ALTO // 2)

        tablero(screen,100)
        #dibujar_circulo(screen, NEGRO, 45, 45, 40)
        #screen.blit(text, text_rect)

        dibujar_movimientos(screen, 100)                        
        dibujar_piezas(screen, estado_juego, 100)
        dibujar_info(screen, 100, ANCHO)                        

        pygame.display.flip()
        clock.tick(60)
    
if __name__ == "__main__":
    main()