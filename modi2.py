import numpy as np

# Función para calcular u y v según la ecuación z_ij = u_i + v_j, y mostrar el proceso
def calcular_u_v(costes, solucion):
    n_filas, n_columnas = costes.shape
    u = [None] * n_filas
    v = [None] * n_columnas
    u[0] = 0  # Asignar 0 arbitrariamente al primer u

    print("\nCalculando u y v usando Z_ij = u_i + v_j:")
    cambios = True
    while cambios:
        cambios = False
        for i in range(n_filas):
            for j in range(n_columnas):
                if solucion[i][j] != 0:  # Si es una solución básica
                    if u[i] is not None and v[j] is None:
                        v[j] = costes[i][j] - u[i]
                        cambios = True
                        print(f"Z_{i}{j} = {costes[i][j]} -> v_{j} = {costes[i][j]} - u_{i} = {v[j]}")
                    elif v[j] is not None and u[i] is None:
                        u[i] = costes[i][j] - v[j]
                        cambios = True
                        print(f"Z_{i}{j} = {costes[i][j]} -> u_{i} = {costes[i][j]} - v_{j} = {u[i]}")

    return u, v

# Función para calcular las diferencias c_ij - z_ij y mostrar los cálculos
def calcular_diferencias(costes, u, v):
    diferencias = np.zeros(costes.shape)

    print("\nCalculando las diferencias C_ij - Z_ij para todas las celdas:")
    for i in range(diferencias.shape[0]):
        for j in range(diferencias.shape[1]):
            if u[i] is not None and v[j] is not None:  # Verificar que u[i] y v[j] no sean None
                diferencias[i][j] = costes[i][j] - (u[i] + v[j])
                print(f"C_{i}{j} - Z_{i}{j} = {costes[i][j]} - ({u[i]} + {v[j]}) = {diferencias[i][j]}")
            else:
                diferencias[i][j] = float('inf')  # Marcar como infinito si no es posible calcular
                print(f"C_{i}{j} - Z_{i}{j} no calculable (falta u o v)")

    return diferencias

# Función auxiliar para encontrar el ciclo de una variable no básica
def encontrar_ciclo(solucion, i_inicial, j_inicial):
    ciclo = {(i_inicial, j_inicial): '+'}
    # Implementa la lógica para encontrar el ciclo completo aquí.
    # Este es solo un esqueleto de la función.
    return ciclo

# Función principal del Método MODI
def metodo_modi(costes, solucion_inicial):
    # Paso 1: Iniciar con la solución inicial
    solucion = np.array(solucion_inicial)
    print("Matriz inicial de solución:")
    print(solucion)
    
    while True:
        # Paso 2: Calcular u y v
        u, v = calcular_u_v(costes, solucion)

        # Mostrar los valores de u y v obtenidos
        print("\nValores de u y v obtenidos:")
        print("u =", u)
        print("v =", v)

        # Paso 3: Calcular c_ij - z_ij
        diferencias = calcular_diferencias(costes, u, v)

        # Verificar optimalidad
        if np.all(diferencias >= 0):
            print("\nLa solución es óptima.")
            print("Solución final (matriz de transporte):")
            print(solucion)
            # Calcular el coste total
            coste_total = np.sum(costes * solucion)
            print(f"Coste total óptimo: {coste_total}")
            return solucion, coste_total
        
        # Seleccionar la celda con el valor más negativo de c_ij - z_ij
        i_min, j_min = np.unravel_index(np.argmin(diferencias), diferencias.shape)

        # Iniciar la trayectoria +/- para ajustar las celdas
        ciclo = encontrar_ciclo(solucion, i_min, j_min)
        theta = min(solucion[i, j] for (i, j) in ciclo if ciclo[(i, j)] == '-')

        # Actualizar la solución siguiendo el ciclo
        for (i, j), signo in ciclo.items():
            solucion[i][j] += theta if signo == '+' else -theta

        print("\nSolución actualizada:")
        print(solucion)

# Ejemplo de uso
costes = np.array([[5, 1, 8, 0], 
                   [2, 4, 0, 0], 
                   [3, 6, 7, 0]])  # Matriz de costes
solucion_inicial = [[0, 3, 0, 0], 
                    [1, 0, 7, 0], 
                    [0, 0, 0, 0]]  # Solución inicial (Esquina Noroeste, por ejemplo)

solucion_optima, coste_total = metodo_modi(costes, solucion_inicial)
print(f"\nLa solución óptima es:\n{solucion_optima}\nCon un costo total de: {coste_total}")
