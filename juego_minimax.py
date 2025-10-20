import random

gato = 'G'
raton = 'R'
queso = 'Q'

filas = 10
columnas = 10
tablero_actual = [[0 for _ in range(columnas)] for _ in range(filas)]

# Posiciones iniciales
tablero_actual[0][0] = raton
tablero_actual[9][9] = gato
tablero_actual[4][4] = queso

# -------- FUNCIONES --------
def imprimir_tablero(tablero):
    for fila in tablero:
        for elemento in fila:
            simbolo = elemento if elemento != 0 else "."
            print(simbolo, end=" ")
        print()
    print()
#Busca y devuelve la posición de un simbolo encontrado en el tablero.
def encontrar_posicion(tablero, simbolo):
    for f in range(filas):
        for c in range(columnas):
            if tablero[f][c] == simbolo:
                return f, c
    return None

def evaluar(tablero):
    f_g, c_g = encontrar_posicion(tablero, gato)
    f_r, c_r = encontrar_posicion(tablero, raton)
    return abs(f_g - f_r) + abs(c_g - c_r)

def movimientos_validos(tablero, simbolo):
    f, c = encontrar_posicion(tablero, simbolo)
    candidatos = [(f-1,c), (f+1,c), (f,c-1), (f,c+1)]
    return [(nf,nc) for nf,nc in candidatos if 0 <= nf < filas and 0 <= nc < columnas]

import copy

def copiar_y_mover(tablero, simbolo, mov):
    nuevo = copy.deepcopy(tablero)
    f, c = encontrar_posicion(nuevo, simbolo)
    nf, nc = mov
    nuevo[f][c] = 0
    nuevo[nf][nc] = simbolo
    return nuevo


def minimax(tablero, profundidad, turno_gato):
    # Caso base: profundidad agotada o juego terminado
    if profundidad == 0:
        return evaluar(tablero), None

    if turno_gato:

        movimientos = movimientos_validos(tablero, gato)
        if not movimientos:   # <- no hay jugadas
            return evaluar(tablero), None
        
        mejor_valor = float("inf")
        mejor_mov = None

        for mov in movimientos_validos(tablero, gato):
            tablero_copia = copiar_y_mover(tablero, gato, mov)
            valor, _ = minimax(tablero_copia, profundidad-1, False)
            if valor < mejor_valor:
                mejor_valor, mejor_mov = valor, mov
        return mejor_valor, mejor_mov
    
    else:  # turno del ratón
        
        movimientos = movimientos_validos(tablero, gato)
        if not movimientos:   # <- no hay jugadas
            return evaluar(tablero), None
        
        mejor_valor = float("-inf")
        mejor_mov = None

        for mov in movimientos_validos(tablero, raton):
            tablero_copia = copiar_y_mover(tablero, raton, mov)
            valor, _ = minimax(tablero_copia, profundidad-1, True)
            if valor > mejor_valor:
                mejor_valor, mejor_mov = valor, mov
        return mejor_valor, mejor_mov

 
def mover_raton_jugador(tablero):
    fila_actual, col_actual = encontrar_posicion(tablero, raton)
    movimiento = input("Mover ratón (w=arriba, s=abajo, a=izquierda, d=derecha): ")

    if movimiento == "w":
        nueva_fila, nueva_col = fila_actual - 1, col_actual
    elif movimiento == "s":
        nueva_fila, nueva_col = fila_actual + 1, col_actual
    elif movimiento == "a":
        nueva_fila, nueva_col = fila_actual, col_actual - 1
    elif movimiento == "d":
        nueva_fila, nueva_col = fila_actual, col_actual + 1
    else:
        print("Movimiento inválido, el ratón no se mueve.")
        return

    if 0 <= nueva_fila < filas and 0 <= nueva_col < columnas:
        tablero[fila_actual][col_actual] = 0
        tablero[nueva_fila][nueva_col] = raton
    else:
        print("¡No puedes salir del tablero!")

# def mover_gato_random(tablero):
#     fila_actual, col_actual = encontrar_posicion(tablero, gato)
#     movimientos_posibles = [
#         (fila_actual - 1, col_actual),     # arriba
#         (fila_actual + 1, col_actual),     # abajo
#         (fila_actual, col_actual - 1),     # izquierda
#         (fila_actual, col_actual + 1)      # derecha
#     ]
#     # Filtrar solo los movimientos válidos
#     movimientos_validos = [
#         (f, c) for f, c in movimientos_posibles
#         if 0 <= f < filas and 0 <= c < columnas
#     ]

#     if movimientos_validos:
#         nueva_fila, nueva_col = random.choice(movimientos_validos)
#         tablero[fila_actual][col_actual] = 0
#         tablero[nueva_fila][nueva_col] = gato

# -------- BUCLE PRINCIPAL --------
while True:
    imprimir_tablero(tablero_actual)

    # 1. Movimiento del ratón (jugador con input)
    mover_raton_jugador(tablero_actual)

    # 2. Turno del gato (con minimax)
    _, mejor_mov = minimax(tablero_actual, profundidad=2, turno_gato=True)
    if mejor_mov:
        f, c = encontrar_posicion(tablero_actual, gato)
        nf, nc = mejor_mov
        tablero_actual[f][c] = 0
        tablero_actual[nf][nc] = gato

    # 3. Revisar condiciones de finalización
    pos_raton = encontrar_posicion(tablero_actual, raton)
    pos_gato = encontrar_posicion(tablero_actual, gato)

    if pos_gato == pos_raton:
        print("¡El gato atrapó al ratón!")
        break
    if pos_raton == (4, 4):
        print("¡El ratón llegó al queso!")
        break




