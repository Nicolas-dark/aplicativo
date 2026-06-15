import copy


LABERINTO_ORIGINAL = [
    ['F',  1,  1,  1,  0,  1,  1,  1,  1],
    [ -2,  0,  0, -1,  0,  1,  0,  1,  0],
    [  1,  1,  0,  1,  1,  1,  0,  1,  0],
    [  0,  1,  0, -1,  0,  0, -1,  0,  0],
    [  1,  1,  1,  1,  1,  1,  1,  1,  0],
    [ -1,  0,  0,  0,  0,  0,  0,  0, -1],
    [  1,  1,  1, -1,  1,  1,  1,  1,  0],
    [  1,  0,  0,  1,  0,  1,  0,  1,  0],
    [ 'I',  1, -1,  1,  1,  1,  0,  1,  1],
]

FILAS   = 9
COLUMNAS = 9
VIDAS_INICIALES = 3

MOVIMIENTOS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
NOMBRES_MOV = ['Abajo', 'Derecha', 'Arriba', 'Izquierda']

def valor_celda(laberinto, fila, col):
    """Devuelve el valor numérico de una celda (F e I valen 1)."""
    v = laberinto[fila][col]
    if v in ('F', 'I'):
        return 1
    return v


def es_transitable(laberinto, fila, col):
    """Una celda es transitable si su valor NO es 0."""
    return laberinto[fila][col] != 0


def dentro_del_laberinto(fila, col):
    return 0 <= fila < FILAS and 0 <= col < COLUMNAS


def mostrar_laberinto(laberinto, titulo="Laberinto"):
    """Imprime el laberinto con formato de tabla."""
    print(f"\n{'─'*40}")
    print(f"  {titulo}")
    print(f"{'─'*40}")

    print("      " + "  ".join(f"{c:2}" for c in range(COLUMNAS)))
    print("      " + "──" * COLUMNAS)
    for i, fila in enumerate(laberinto):
        fila_str = "  ".join(f"{str(v):>2}" for v in fila)
        print(f"  f{i} | {fila_str}")
    print(f"{'─'*40}\n")


def mostrar_laberinto_con_camino(laberinto, camino):
    """Imprime el laberinto marcando el camino con '*'."""
    grid = copy.deepcopy(laberinto)
    for (f, c) in camino:
        if grid[f][c] not in ('F', 'I'):
            grid[f][c] = '*'
    mostrar_laberinto(grid, titulo="Laberinto con camino solución")


def backtracking(laberinto, fila, col, vidas, visitadas, camino, pasos):
    """
    Busca recursivamente un camino desde (fila, col) hasta (0, 0).
    Devuelve True si encontró solución, False si no.
    """
    if fila == 0 and col == 0:
        pasos.append(f"  ✔ ¡Llegamos a la meta! Vidas restantes: {vidas}")
        return True

    for idx, (df, dc) in enumerate(MOVIMIENTOS):
        nf, nc = fila + df, col + dc

        if not dentro_del_laberinto(nf, nc):
            continue
        if not es_transitable(laberinto, nf, nc):
            continue
        if (nf, nc) in visitadas:
            continue

        nueva_vida = vidas + valor_celda(laberinto, nf, nc)

        pasos.append(
            f"  → Mov {NOMBRES_MOV[idx]:10s} ({fila},{col})→({nf},{nc})  "
            f"val={valor_celda(laberinto,nf,nc):+d}  vidas={nueva_vida}"
        )

        if nueva_vida <= 0:
            pasos.append(f"      ✘ Vidas agotadas en ({nf},{nc}), se descarta.")
            continue

        visitadas.add((nf, nc))
        camino.append((nf, nc))

        if backtracking(laberinto, nf, nc, nueva_vida, visitadas, camino, pasos):
            return True
        camino.pop()
        visitadas.discard((nf, nc))
        pasos.append(f"      ↩ Retroceso desde ({nf},{nc})")

    return False
def main():
    print("\n" + "═"*50)
    print("   LABERINTO DEL RATÓN – BACKTRACKING")
    print("═"*50)

   
    mostrar_laberinto(LABERINTO_ORIGINAL, "Laberinto Original")
    fila_inicio, col_inicio = 8, 0
    vidas_iniciales = VIDAS_INICIALES
    
    vidas_en_inicio = vidas_iniciales + valor_celda(LABERINTO_ORIGINAL, fila_inicio, col_inicio)

    visitadas = {(fila_inicio, col_inicio)}
    camino    = [(fila_inicio, col_inicio)]
    pasos     = []

    pasos.append(f"\n[Inicio] Posición ({fila_inicio},{col_inicio})  Vidas={vidas_en_inicio}")

    
    encontrado = backtracking(
        LABERINTO_ORIGINAL,
        fila_inicio, col_inicio,
        vidas_en_inicio,
        visitadas,
        camino,
        pasos
    )
    print("    Registro de pasos ")
    for p in pasos:
        print(p)

    print("\n" + "═"*50)
    if encontrado:
        print("  ✔ SE ENCONTRÓ UN CAMINO VIABLE")
        print("  Camino (fila, columna):")
        for i, (f, c) in enumerate(camino):
            celda = LABERINTO_ORIGINAL[f][c]
            print(f"    Paso {i+1:2d}: ({f},{c})  valor={celda}")
        mostrar_laberinto_con_camino(LABERINTO_ORIGINAL, camino)
    else:
        print("  ✘ NO SE ENCONTRÓ UN CAMINO VIABLE")
        print("  El ratón no puede salir del laberinto con las vidas disponibles.")
        mostrar_laberinto(LABERINTO_ORIGINAL, "Laberinto – Sin solución")
    print("═"*50 + "\n")


if __name__ == "__main__":
    main()