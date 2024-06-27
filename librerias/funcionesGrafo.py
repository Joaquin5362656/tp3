from tdas import cola
from tdas import pila
import random

class NoSeEncontroCaminoError(Exception):
    pass

def grados_entrada(grafo):

    grados = {}
    vertices = grafo.obtener_vertices()

    for v in vertices:
        grados[v] = 0

    for v in vertices:
        for w in grafo.adyacentes(v):
            grados[w] = grados[w] + 1
    
    return grados

def grados_salida(grafo):

    grados = {}

    for v in grafo.obtener_vertices():
        grados[v] = 0

    for v in grafo.obtener_vertices():
        for _ in grafo.adyacentes(v):
            grados[v] = grados[v]+1

    return grados

def bfs_general(grafo, recorrer):

    visitados = {}
    q = cola.Cola() 
    seguir_recorriendo = True

    for v in grafo.obtener_vertices():
        if v in visitados:
            continue

        q.encolar(v)
        visitados[v] = True

        while not q.esta_vacia() and seguir_recorriendo:

            actual = q.desencolar()
            for w in grafo.adyacentes(actual):
                seguir_recorriendo = recorrer(actual, w)
                if not w in visitados and seguir_recorriendo:
                    q.encolar(w)
                    visitados[w] = True



def bfs(grafo, origen, recorrer, visitados = None):
    
    q = cola.Cola() 
    seguir_recorriendo = True
    q.encolar(origen)
    if visitados is None:
        visitados = {}
    visitados[origen] = True

    while not q.esta_vacia() and seguir_recorriendo:
        actual = q.desencolar()

        for w in grafo.adyacentes(actual):
            seguir_recorriendo = recorrer(actual, w)
            if not w in visitados and seguir_recorriendo:
                q.encolar(w)
                visitados[w] = True



def reconstruir_camino(padres, destino):

    if padres[destino] is None:
        return [destino]
    camino = reconstruir_camino(padres, padres[destino])
    camino.append(destino)
    return camino




def camino_minimo(grafo, origen, destino):

    padres = {}
    padres[origen] = None

    def actualizar_padres(raiz, adyacente):
        if adyacente not in padres or padres[adyacente] is None:
            padres[adyacente] = raiz    
        if adyacente == destino:
            return False
        else:
            return True

    bfs(grafo, origen, actualizar_padres)

    if destino not in padres or padres[destino] is None:
        raise NoSeEncontroCaminoError

    if origen == destino:
        predecesor_ciclo = padres[origen]
        padres[origen] = None
        camino = reconstruir_camino(padres, predecesor_ciclo)
        camino.append(origen)
        return camino
    else:
        return reconstruir_camino(padres, destino)


def divulgar_rumor(grafo, origen, amplitud):

    recorrido = []
    nivel = {}
    nivel[origen] = 0

    def obtener_nodos_recorridos(raiz, adyacente):
        if nivel[raiz] == amplitud:
            return False

        if adyacente not in nivel:
            nivel[adyacente] = nivel[raiz] + 1
            recorrido.append(adyacente)
        return True
    
    bfs(grafo, origen, obtener_nodos_recorridos)
    return recorrido



def cfc(grafo):

    visitados = {}
    orden = {}
    mas_bajo = {}
    fuertemente_conexas = []

    for vertice in grafo.obtener_vertices():
        if vertice not in visitados:
            orden[vertice] = len(visitados)
            dfs_cfc(grafo, vertice, visitados, orden, mas_bajo, pila.Pila(), {}, fuertemente_conexas)

    return fuertemente_conexas   



def dfs_cfc(grafo, raiz, visitados, orden, mas_bajo, nodos_conexos, recorrido, fuertemente_conexas):

    visitados[raiz] = True
    nodos_conexos.apilar(raiz)
    recorrido[raiz] = True
    mas_bajo[raiz] = orden[raiz]

    for adyacente in grafo.adyacentes(raiz):
        if adyacente not in visitados:
            orden[adyacente] = len(visitados)
            dfs_cfc(grafo, adyacente, visitados, orden, mas_bajo, nodos_conexos, recorrido, fuertemente_conexas)
            mas_bajo[raiz] = min(mas_bajo[raiz], mas_bajo[adyacente])
        elif adyacente in recorrido:
            mas_bajo[raiz] = orden[adyacente]
        

    if orden[raiz] == mas_bajo[raiz]:
        nueva_cfc = [nodos_conexos.ver_tope()]
        while nodos_conexos.desapilar() != raiz:
            nueva_cfc.append(nodos_conexos.ver_tope())

        fuertemente_conexas.append(nueva_cfc)


def persecucion_rapida(grafo, delincuentes_origen, buscados):

    visitados = {}
    padres = {}
    orden = {}
    persecucion_mas_corta = []

    def encontrar_mas_buscados(raiz, adyacente):

        nonlocal persecucion_mas_corta
        if persecucion_mas_corta and len(persecucion_mas_corta) <= orden[raiz]+1:
            return False

        if adyacente in delincuentes_origen and adyacente not in visitados:
            padres[adyacente] = None
            orden[adyacente] = 0
            bfs(grafo, adyacente, encontrar_mas_buscados, visitados)

        if adyacente not in visitados or orden[raiz]+1 < orden[adyacente]:
            orden[adyacente] = orden[raiz] + 1
            padres[adyacente] = raiz
            if adyacente in visitados:
                del(visitados[adyacente])

        if adyacente in buscados:
            visitados[adyacente] = True
            camino = reconstruir_camino(padres, adyacente)
            if not persecucion_mas_corta or len(camino) < len(persecucion_mas_corta):
                persecucion_mas_corta = camino
                return False    

        return True 

    for delincuente in delincuentes_origen:
        if delincuente not in visitados:
            padres[delincuente] = None
            visitados[delincuente] = True
            orden[delincuente] = 0
            bfs(grafo, delincuente, encontrar_mas_buscados, visitados)

    return persecucion_mas_corta


def page_rank(grafo):

    grado_salida = grados_salida(grafo)
    vertices = grafo.obtener_vertices()
    puntaje = {}
    puntaje_recorrido_actual = {}
    nodos_sin_relacion = []

    for v in vertices:
        if grado_salida[v] == 0:
            nodos_sin_relacion.append(v)
        puntaje[v] = 1

    def actualizar_ranking(raiz, adyacente):
        if adyacente not in puntaje_recorrido_actual:
            puntaje_recorrido_actual[adyacente] = puntaje[adyacente]
            puntaje[adyacente] = (puntaje_recorrido_actual[raiz] / grado_salida[raiz]) + aporte_nodos_sin_relacion(puntaje_recorrido_actual, puntaje, nodos_sin_relacion)
        else:
            puntaje[adyacente] = (puntaje[adyacente] + puntaje_recorrido_actual[raiz] / grado_salida[raiz])
        return True
    
    numero_recorridos = 0

    while numero_recorridos < 50:
        visitados = {}
        puntaje_recorrido_actual = {}
        for v in vertices:
            if v not in visitados:
                puntaje_recorrido_actual[v] = puntaje[v]
                puntaje[v] = aporte_nodos_sin_relacion(puntaje_recorrido_actual, puntaje, nodos_sin_relacion)
                bfs(grafo, v, actualizar_ranking, visitados)
        
        numero_recorridos = numero_recorridos + 1

    return puntaje


def aporte_nodos_sin_relacion(puntaje_recorrido_actual, puntaje, nodos_sin_relacion):

    aporte = 0
    for nodo in nodos_sin_relacion:
        if nodo in puntaje_recorrido_actual:
            aporte += puntaje_recorrido_actual[nodo]
        else:
            aporte += puntaje[nodo]
    
    return aporte / len(puntaje)


def label_propagation(grafo):

    label = {}
    padres = {}
    vertices = grafo.obtener_vertices()

    _inicializar_padres_y_etiquetas(grafo, padres, label)  
    
    numeros_recorridos = 0
    while numeros_recorridos < len(vertices) * 5:
        vertice = vertices[random.randint(0, len(vertices))-1]
        label[vertice] = _obtener_etiqueta_mas_frecuente(vertice, padres, label)
        numeros_recorridos = numeros_recorridos + 1

    return _buscar_comunidades(vertices, label)


def _obtener_etiqueta_mas_frecuente(adyacente, padres, label):

    frecuencias = {}
    mas_frecuente = label[padres[adyacente][0]]

    for padre in padres[adyacente]:

        if label[padre] not in frecuencias:
            frecuencias[label[padre]] = 1
        else:
            frecuencias[label[padre]] = frecuencias[label[padre]] + 1
    
        if frecuencias[label[padre]] > frecuencias[mas_frecuente]:
            mas_frecuente = label[padre]

    return mas_frecuente



def _inicializar_padres_y_etiquetas(grafo, padres, label):

    id_label = 0

    def actualizar_datos(raiz, adyacente):
        nonlocal id_label
        if raiz not in label:
            label[raiz] = id_label
            id_label = id_label + 1

        if adyacente not in label:
            label[adyacente] = id_label
            id_label = id_label + 1

        if adyacente not in padres:
            padres[adyacente] = []

        padres[adyacente].append(raiz)
        
        return True

    bfs_general(grafo, actualizar_datos)



def _buscar_comunidades(vertices, label):

    comunidades = {}
    arr_comunidades = []

    for v in vertices:
        if label[v] not in comunidades:
            nueva_comunidad = [v]
            arr_comunidades.append(nueva_comunidad)
            comunidades[label[v]] = nueva_comunidad
        else:
            comunidades[label[v]].append(v)

    return arr_comunidades   


