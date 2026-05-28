import pygame
import sys
from pygame.locals import *

BOTON_REINICIO = pygame.Rect(480, 668, 140, 35)

def dibujar_boton_reinicio(pantalla):
    pygame.font.init()
    fuente = pygame.font.SysFont("Arial", 16, bold=True)
    mouse  = pygame.mouse.get_pos()

    color = (180, 0, 0) if BOTON_REINICIO.collidepoint(mouse) else (220, 50, 50)
    pygame.draw.rect(pantalla, color, BOTON_REINICIO, border_radius=8)

    texto = fuente.render("⟲  Rebobinar", True, (255, 255, 255))
    pantalla.blit(texto, texto.get_rect(center=BOTON_REINICIO.center))


def mostrar_menu(screen, ancho, alto):
    pygame.font.init()
    BLANCO   = (255, 255, 255)
    NEGRO    = (0,   0,   0  )
    AZUL     = (0,   80,  180)
    AZUL_HOV = (0,   120, 220)

    fuente_titulo = pygame.font.SysFont("Arial", 52, bold=True)
    fuente_boton  = pygame.font.SysFont("Arial", 30)
    boton_rect    = pygame.Rect(ancho // 2 - 110, alto // 2, 220, 55)

    while True:
        screen.fill(BLANCO)

        titulo = fuente_titulo.render("♟ Ajedrez", True, NEGRO)
        screen.blit(titulo, titulo.get_rect(center=(ancho // 2, alto // 2 - 80)))

        mouse = pygame.mouse.get_pos()
        color_boton = AZUL_HOV if boton_rect.collidepoint(mouse) else AZUL
        pygame.draw.rect(screen, color_boton, boton_rect, border_radius=10)

        texto_boton = fuente_boton.render("Jugar", True, BLANCO)
        screen.blit(texto_boton, texto_boton.get_rect(center=boton_rect.center))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(event.pos):
                    return

        pygame.display.flip()