import numpy as np

def calcular_u_v(costes, solucion):
    n_filas, n_columnas = costes.shape
    u = [None] * n_filas
    v = [None] * n_columnas
    u[0] = 0

    print("\nCalculando u y v usando Z_ij = u_i + v_j:")
    cambios = True
    while cambios:
        cambios = False
        for i in range(n_filas):
            for j in range(n_columnas):
                if solucion[i][j] != 0:
                    if u[i] is not None and v[j] is None:
                        v[j] = costes[i][j] - u[i]
                        cambios = True
                        print(f"Z_{i}{j} = {costes[i][j]} -> v_{j} = {v[j]}")
                    elif v[j] is not None and u[i] is None:
                        u[i] = costes[i][j] - v[j]
                        cambios = True
                        print(f"Z_{i}{j} = {costes[i][j]} -> u_{i} = {u[i]}")

    return u, v

def calcular_diferencias(costes, u, v):
    diferencias = np.zeros(costes.shape)
    print("\nCalculando las diferencias C_ij - Z_ij para todas las celdas:")
    for i in range(costes.shape[0]):
        for j in range(costes.shape[1]):
            diferencias[i][j] = (
                costes[i][j] - (u[i] + v[j]) 
                if u[i] is not None and v[j] is not None 
                else float('inf')
            )
            print(f"C_{i}{j} - Z_{i}{j} = {diferencias[i][j]}" if diferencias[i][j] != float('inf') else f"C_{i}{j} - Z_{i}{j} no calculable (falta u o v)")

    return diferencias

def encontrar_ciclo(solucion, i_inicial, j_inicial):
    ruta = [(i_inicial, j_inicial)]
    horizontal = True
    i, j = i_inicial, j_inicial

    while True:
        siguiente = buscar_ruta_horizontal if horizontal else buscar_ruta_vertical
        siguiente_index = siguiente(i, j, solucion) if horizontal else siguiente(j, i, solucion)
        
        if siguiente_index is None:
            break
        ruta.append(siguiente_index)
        i, j = siguiente_index
        horizontal = not horizontal

    ciclo = {(i, j): ('+' if k % 2 == 0 else '-') for k, (i, j) in enumerate(ruta)}
    return ciclo

def buscar_ruta_horizontal(fila, excluye_columna, solucion):
    return next((j for j in range(solucion.shape[1]) if j != excluye_columna and solucion[fila][j] != 0), None)

def buscar_ruta_vertical(columna, excluye_fila, solucion):
    return next((i for i in range(solucion.shape[0]) if i != excluye_fila and solucion[i][columna] != 0), None)

def metodo_modi(costes, solucion_inicial):
    solucion = np.array(solucion_inicial)
    print("Matriz inicial de solución:")
    print(solucion)

    while True:
        u, v = calcular_u_v(costes, solucion)
        print("\nValores de u y v obtenidos:")
        print("u =", u)
        print("v =", v)

        diferencias = calcular_diferencias(costes, u, v)

        if np.all(diferencias >= 0):
            print("\nLa solución es óptima.")
            print("Solución final (matriz de transporte):")
            print(solucion)
            coste_total = np.sum(costes * solucion)
            print(f"Coste total óptimo: {coste_total}")
            return solucion

        i_min, j_min = np.unravel_index(np.argmin(diferencias), diferencias.shape)
        ciclo = encontrar_ciclo(solucion, i_min, j_min)
        theta = min(solucion[i, j] for (i, j) in ciclo if ciclo[(i, j)] == '-')

        print("\nActualizando la solución con el ciclo encontrado:")
        for (i, j), signo in ciclo.items():
            solucion[i][j] += theta if signo == '+' else -theta
            print(f"Celda ({i}, {j}) -> signo {signo}, valor {solucion[i][j]}")

        print("\nSolución actualizada:")
        print(solucion)

costes = np.array([[500, 300, 0, 0], 
                   [0, 20, 310, 0], 
                   [0, 0, 140, 210]])

solucion_inicial = [[15, 19, 10, 27], 
                    [13, 16, 24, 23], 
                    [27, 15, 12, 17]]

solucion_optima = metodo_modi(costes, solucion_inicial)
