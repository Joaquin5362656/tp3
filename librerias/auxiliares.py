def diccionarioAArray(dicc):
    arr = []
    for clave, valor in dicc.items():
        arr.append((clave, valor))
    return arr

def obtener_digito(numero, n):
    num = numero * 10**(n-1)
    return int(num) % 10

def counting_sort(tuplas, obtener_valor_interes):

    frecuencias = []
    puntaje_ordenado = []
    while len(frecuencias) < 10:
        frecuencias.append(0)

    for _, valor in tuplas:
        puntaje_ordenado.append(0)
        posicion = obtener_valor_interes(valor)
        frecuencias[posicion] = frecuencias[posicion] + 1

    posiciones_iniciales = []
    posiciones_iniciales.append(0)

    for frecuencia in frecuencias[:len(frecuencias)-1]:
        posiciones_iniciales.append(frecuencia+posiciones_iniciales[-1])
    
    for clave, valor in tuplas:
        nueva_pos = posiciones_iniciales[obtener_valor_interes(valor)]
        puntaje_ordenado[nueva_pos] = (clave, valor)
        posiciones_iniciales[obtener_valor_interes(valor)] = nueva_pos + 1

    return puntaje_ordenado

def se_encontro_mejor_camino(camino, persecucion_mas_corta, mas_importantes, delincuente):
    if len(camino) < len(persecucion_mas_corta):
        return True
    
    puesto = mas_importantes[delincuente][0]
    if puesto < mas_importantes[persecucion_mas_corta[-1]][0]:
        return True
    
    return False