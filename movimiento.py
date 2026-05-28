import pygame


COLOR_SELECCION  = (0, 200, 100, 150)   
COLOR_MOVIMIENTO = (100, 180, 255, 150) 
COLOR_JAQUE      = (255, 50,  50,  180) 

pieza_seleccionada = None
movimientos_validos = []
turno   = "blancas"   
mensaje = ""          


PIEZAS_BLANCAS = ["TE", "C", "AL", "RA", "RY", "PN"]
PIEZAS_NEGRAS  = ["TE1",  "C1",  "AL1",  "RA1",  "RY1",  "PN1" ]

def equipo_de(pieza):
    if pieza in PIEZAS_BLANCAS: return "blancas"
    if pieza in PIEZAS_NEGRAS:  return "negras"
    return None

def misma_equipo(p1, p2):
    e = equipo_de(p1)
    return e is not None and e == equipo_de(p2)



def movimientos_peon(tablero, fila, col):
    movs = []
    pieza = tablero[fila][col]

    if equipo_de(pieza) == "blancas":
        direccion  = -1
        fila_inicio = 6
    else:
        direccion  = 1
        fila_inicio = 1

    nf = fila + direccion

    if 0 <= nf < 8 and tablero[nf][col] == " ":
        movs.append((nf, col))
        
        nf2 = fila + 2 * direccion
        if fila == fila_inicio and 0 <= nf2 < 8 and tablero[nf2][col] == " ":
            movs.append((nf2, col))


    for dc in [-1, 1]:
        nc = col + dc
        if 0 <= nf < 8 and 0 <= nc < 8:
            objetivo = tablero[nf][nc]
            if objetivo != " " and not misma_equipo(pieza, objetivo):
                movs.append((nf, nc))

    return movs


def movimientos_torre(tablero, fila, col):
    movs = []
    pieza = tablero[fila][col]
    for df, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nf, nc = fila+df, col+dc
        while 0 <= nf < 8 and 0 <= nc < 8:
            obj = tablero[nf][nc]
            if obj == " ":
                movs.append((nf, nc))
            elif not misma_equipo(pieza, obj):
                movs.append((nf, nc)); break
            else:
                break
            nf += df; nc += dc
    return movs


def movimientos_alfil(tablero, fila, col):
    movs = []
    pieza = tablero[fila][col]
    for df, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
        nf, nc = fila+df, col+dc
        while 0 <= nf < 8 and 0 <= nc < 8:
            obj = tablero[nf][nc]
            if obj == " ":
                movs.append((nf, nc))
            elif not misma_equipo(pieza, obj):
                movs.append((nf, nc)); break
            else:
                break
            nf += df; nc += dc
    return movs


def movimientos_reina(tablero, fila, col):
    return movimientos_torre(tablero, fila, col) + movimientos_alfil(tablero, fila, col)


def movimientos_rey(tablero, fila, col):
    movs = []
    pieza = tablero[fila][col]
    for df in [-1,0,1]:
        for dc in [-1,0,1]:
            if df == 0 and dc == 0: continue
            nf, nc = fila+df, col+dc
            if 0 <= nf < 8 and 0 <= nc < 8:
                obj = tablero[nf][nc]
                if obj == " " or not misma_equipo(pieza, obj):
                    movs.append((nf, nc))
    return movs


def movimientos_caballo(tablero, fila, col):
    movs = []
    pieza = tablero[fila][col]
    for df, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
        nf, nc = fila+df, col+dc
        if 0 <= nf < 8 and 0 <= nc < 8:
            obj = tablero[nf][nc]
            if obj == " " or not misma_equipo(pieza, obj):
                movs.append((nf, nc))
    return movs


def movimientos_crudos(tablero, fila, col):
    pieza = tablero[fila][col]
    if pieza in ["PN","PN1"]:  return movimientos_peon(tablero, fila, col)
    if pieza in ["TE","TE1"]:  return movimientos_torre(tablero, fila, col)
    if pieza in ["AL","AL1"]:  return movimientos_alfil(tablero, fila, col)
    if pieza in ["RA","RA1"]:  return movimientos_reina(tablero, fila, col)
    if pieza in ["RY","RY1"]:  return movimientos_rey(tablero, fila, col)
    if pieza in ["C","C1"]:  return movimientos_caballo(tablero, fila, col)
    return []

def copiar_tablero(tablero):
    return [fila[:] for fila in tablero]

def posicion_rey(tablero, equipo):
    rey = "RY" if equipo == "blancas" else "RY1"
    for f in range(8):
        for c in range(8):
            if tablero[f][c] == rey:
                return (f, c)
    return None

def rey_en_jaque(tablero, equipo):
    pos = posicion_rey(tablero, equipo)
    if pos is None:
        return False
    fila_rey, col_rey = pos
    rival = "negras" if equipo == "blancas" else "blancas"
    for f in range(8):
        for c in range(8):
            if equipo_de(tablero[f][c]) == rival:
                if (fila_rey, col_rey) in movimientos_crudos(tablero, f, c):
                    return True
    return False

def obtener_movimientos(tablero, fila, col):
    pieza  = tablero[fila][col]
    eq     = equipo_de(pieza)
    legales = []
    for (nf, nc) in movimientos_crudos(tablero, fila, col):
        copia = copiar_tablero(tablero)
        copia[nf][nc] = copia[fila][col]
        copia[fila][col] = " "
        if not rey_en_jaque(copia, eq):
            legales.append((nf, nc))
    return legales


def hay_movimientos_posibles(tablero, equipo):
    for f in range(8):
        for c in range(8):
            if equipo_de(tablero[f][c]) == equipo:
                if obtener_movimientos(tablero, f, c):
                    return True
    return False

def manejar_click(tablero, pos, tamaño_celda):
    global pieza_seleccionada, movimientos_validos, turno, mensaje

    
    if "mate" in mensaje:
        return tablero

    col  = pos[0] // tamaño_celda
    fila = pos[1] // tamaño_celda

    if not (0 <= fila < 8 and 0 <= col < 8):
        pieza_seleccionada = None
        movimientos_validos = []
        return tablero

    
    if pieza_seleccionada and (fila, col) in movimientos_validos:
        f_orig, c_orig = pieza_seleccionada
        tablero[fila][col]   = tablero[f_orig][c_orig]
        tablero[f_orig][c_orig] = " "
        pieza_seleccionada   = None
        movimientos_validos  = []

        
        turno = "negras" if turno == "blancas" else "blancas"

        
        if rey_en_jaque(tablero, turno):
            if not hay_movimientos_posibles(tablero, turno):
                ganador = "Blancas" if turno == "negras" else "Negras"
                mensaje = f"¡Jaque mate! Ganan {ganador}"
            else:
                mensaje = f"¡Jaque al rey {turno}!"
        else:
            if not hay_movimientos_posibles(tablero, turno):
                mensaje = "¡Tablas por ahogado!"
            else:
                mensaje = ""

        return tablero


    pieza = tablero[fila][col]
    if pieza != " " and equipo_de(pieza) == turno:
        pieza_seleccionada  = (fila, col)
        movimientos_validos = obtener_movimientos(tablero, fila, col)
    else:
        pieza_seleccionada  = None
        movimientos_validos = []

    return tablero


def dibujar_movimientos(pantalla, tamaño_celda):
    if pieza_seleccionada is None:
        return

    overlay = pygame.Surface((tamaño_celda, tamaño_celda), pygame.SRCALPHA)

    
    fila, col = pieza_seleccionada
    overlay.fill(COLOR_SELECCION)
    pantalla.blit(overlay, (col * tamaño_celda, fila * tamaño_celda))

    
    overlay.fill(COLOR_MOVIMIENTO)
    for (mf, mc) in movimientos_validos:
        pantalla.blit(overlay, (mc * tamaño_celda, mf * tamaño_celda))


def dibujar_info(pantalla, tamaño_celda, ancho):
    """Muestra turno y mensajes de jaque debajo del tablero."""
    pygame.font.init()
    fuente_msg  = pygame.font.SysFont("Arial", 26, bold=True)
    fuente_turno = pygame.font.SysFont("Arial", 22)

    # Turno
    texto_turno = fuente_turno.render(f"Turno: {turno.capitalize()}", True, (30, 30, 30))
    pantalla.blit(texto_turno, (10, 8 * tamaño_celda + 8))

    
    if mensaje:
        color_msg = (200, 0, 0) if "mate" in mensaje or "Jaque" in mensaje else (0, 120, 200)
        texto_msg = fuente_msg.render(mensaje, True, color_msg)
        rect = texto_msg.get_rect(center=(ancho // 2, 8 * tamaño_celda + 40))
        pantalla.blit(texto_msg, rect)