import pygame

TIEMPO_INICIAL = 10 * 60  # 10 minutos en segundos

class Temporizador:
    def __init__(self):
        self.tiempos = {"blancas": TIEMPO_INICIAL, "negras": TIEMPO_INICIAL}
        self.ultimo_tick = pygame.time.get_ticks()
        self.activo = True

    def actualizar(self, turno):
        if not self.activo:
            return None  # None = nadie ganó aún

        ahora = pygame.time.get_ticks()
        delta = (ahora - self.ultimo_tick) / 1000  # segundos transcurridos
        self.ultimo_tick = ahora

        self.tiempos[turno] -= delta

        if self.tiempos[turno] <= 0:
            self.tiempos[turno] = 0
            self.activo = False
            ganador = "Negras" if turno == "blancas" else "Blancas"
            return f"¡Tiempo agotado! Ganan {ganador}"

        return None

    def cambiar_turno(self):
        self.ultimo_tick = pygame.time.get_ticks()

    def reiniciar(self):
        self.tiempos = {"blancas": TIEMPO_INICIAL, "negras": TIEMPO_INICIAL}
        self.ultimo_tick = pygame.time.get_ticks()
        self.activo = True

    def formato(self, turno):
        segundos = int(self.tiempos[turno])
        m = segundos // 60
        s = segundos % 60
        return f"{m:02}:{s:02}"

    def dibujar(self, pantalla, ancho, tamaño_celda):
        pygame.font.init()
        fuente = pygame.font.SysFont("Arial", 22, bold=True)
        y = 8 * tamaño_celda + 8

        # Temporizador negras — izquierda
        color_n = (200, 0, 0) if self.tiempos["negras"] < 30 else (30, 30, 30)
        texto_n = fuente.render(f"Negras: {self.formato('negras')}", True, color_n)
        pantalla.blit(texto_n, (10, y + 30))

        # Temporizador blancas — centro
        color_b = (200, 0, 0) if self.tiempos["blancas"] < 30 else (30, 30, 30)
        texto_b = fuente.render(f"Blancas: {self.formato('blancas')}", True, color_b)
        pantalla.blit(texto_b, (ancho // 2 - 60, y + 30))