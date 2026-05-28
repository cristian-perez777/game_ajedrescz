import pygame
import os


tablero_inicial = [
    ["TE1", "C1", "AL1", "RA1", "RY1", "AL1", "C1", "TE1"],
    ["PN1", "PN1", "PN1", "PN1", "PN1", "PN1", "PN1", "PN1"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    ["PN", "PN", "PN", "PN", "PN", "PN", "PN", "PN"],
    ["TE", "C", "AL", "RA", "RY", "AL", "C", "TE"],
]

imagenes_piezas = {}

def cargar_imagenes1(tamaño_celda):
    piezas = ["RA", "RY", "TE", "AL", "C", "PN", "TE1", "PN1", "C1", "AL1", "RY1", "RA1"]
    
    for pieza in piezas:
        ruta = os.path.join("imagenes1", f"{pieza}.png")
        imagen = pygame.image.load(ruta)
        imagen = pygame.transform.scale(imagen, (tamaño_celda, tamaño_celda))
        imagenes_piezas[pieza] = imagen


def dibujar_piezas(pantalla, tablero, tamaño_celda):
    for fila in range(8):
        for col in range(8):
            pieza = tablero[fila][col]
            if pieza != " ":
                x = col * tamaño_celda
                y = fila * tamaño_celda
                pantalla.blit(imagenes_piezas[pieza], (x, y))