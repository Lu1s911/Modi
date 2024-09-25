import numpy as np

def calcular_u_v(costes, solucion):
    n_filas, n_columnas = costes.shape
    u = [None] * n_filas
    v = [None] * n_columnas
    u[0] = 0

    print("\nCalculando u y v usando Z_ij = u_i + v_j:")
    iteraciones = 0  # Contador de iteraciones
    max_iteraciones = 100  # Límite de iteraciones para evitar bucles infinitos
    while True:
        cambios = False
        for i in range(n_filas):
            for j in range(n_columnas):
                if solucion[i][j] != 0:
                    if u[i] is not None and v[j] is None:
                        v[j] = costes[i][j] - u[i]
                        cambios = True
                        print(f"Z_{i}{j} = {costes[i][j]} -> v_{j} = {costes[i][j]} - u_{i} = {v[j]}")
                    elif v[j] is not None and u[i] is None:
                        u[i] = costes[i][j] - v[j]
                        cambios = True
                        print(f"Z_{i}{j} = {costes[i][j]} -> u_{i} = {costes[i][j]} - v_{j} = {u[i]}")

        iteraciones += 1
        if not cambios or iteraciones >= max_iteraciones:
            if iteraciones >= max_iteraciones:
                print("Límite máximo de iteraciones alcanzado, revisa la solución inicial.")
            break

    return u, v

def calcular_diferencias(costes, u, v):
    n_filas, n_columnas = costes.shape
    diferencias = np.zeros((n_filas, n_columnas))

    print("\nCalculando las diferencias C_ij - Z_ij para todas las celdas:")
    for i in range(n_filas):
        for j in range(n_columnas):
            if u[i] is not None and v[j] is not None:
                diferencias[i][j] = costes[i][j] - (u[i] + v[j])
                print(f"C_{i}{j} - Z_{i}{j} = {costes[i][j]} - ({u[i]} + {v[j]}) = {diferencias[i][j]}")
            else:
                diferencias[i][j] = float('inf')
                print(f"C_{i}{j} - Z_{i}{j} no calculable (falta u o v)")

    return diferencias

def encontrar_ciclo(solucion, i_inicial, j_inicial):
    n_filas, n_columnas = solucion.shape

    def buscar_ruta_horizontal(fila, excluye_columna):
        for j in range(n_columnas):
            if j != excluye_columna and solucion[fila][j] != 0:
                return j
        return None

    def buscar_ruta_vertical(columna, excluye_fila):
        for i in range(n_filas):
            if i != excluye_fila and solucion[i][columna] != 0:
                return i
        return None

    ruta = [(i_inicial, j_inicial)]
    horizontal = True

    i, j = i_inicial, j_inicial
    while True:
        if horizontal:
            j_siguiente = buscar_ruta_horizontal(i, j)
            if j_siguiente is None:
                break
            j = j_siguiente
        else:
            i_siguiente = buscar_ruta_vertical(j, i)
            if i_siguiente is None:
                break
            i = i_siguiente

        ruta.append((i, j))

        if (i, j) == (i_inicial, j_inicial):
            break

        horizontal = not horizontal

    ciclo = {}
    for k, (i, j) in enumerate(ruta):
        signo = '+' if k % 2 == 0 else '-'
        ciclo[(i, j)] = signo

    return ciclo

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
            coste_total = np.sum(np.multiply(costes, solucion))
            print(f"Coste total óptimo: {coste_total}")
            return solucion
        
        i_min, j_min = np.unravel_index(np.argmin(diferencias), diferencias.shape)

        ciclo = encontrar_ciclo(solucion, i_min, j_min)
        theta = min(solucion[i, j] for (i, j) in ciclo if ciclo[(i, j)] == '-')

        print("\nActualizando la solución con el ciclo encontrado:")
        for (i, j), signo in ciclo.items():
            print(f"Celda ({i}, {j}) -> signo {signo}, valor {solucion[i][j]}")
            if signo == '+':
                solucion[i][j] += theta
            else:
                solucion[i][j] -= theta

        print("\nSolución actualizada:")
        print(solucion)

costes = np.array([[50, 20, 13, 12], 
                   [15, 40, 50, 25], 
                   [15, 14, 20, 95]])

solucion_inicial = [[17, 20, 0, 0], 
                    [0, 21, 26, 0], 
                    [15, 14, 15, 17]]

solucion_optima = metodo_modi(costes, solucion_inicial)
