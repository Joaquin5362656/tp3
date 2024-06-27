from librerias import funcionesGrafo
from librerias import auxiliares

class informe_delincuentes:
    def __init__(self, g):
        self.red_delincuentes = g
        self.mas_importantes = {}
        
    def minimos_seguimientos(self, origen, destino):
        return funcionesGrafo.camino_minimo(self.red_delincuentes, origen, destino)
    
    def delincuentes_mas_importantes(self, n):

        if len(self.mas_importantes) == 0:

            puntaje = funcionesGrafo.page_rank(self.red_delincuentes)
            arr_puntaje = auxiliares.diccionarioAArray(puntaje)
            
            digitos_a_ordenar = 5
            while digitos_a_ordenar > 0:
                def obtener_digito_n(puntaje):
                    return auxiliares.obtener_digito(puntaje, digitos_a_ordenar)
                arr_puntaje = auxiliares.counting_sort(arr_puntaje, obtener_digito_n)
                digitos_a_ordenar = digitos_a_ordenar-1
            

            for vertice, pj in reversed(arr_puntaje):
                puesto = len(self.mas_importantes) + 1
                self.mas_importantes[vertice] = (puesto, pj / len(arr_puntaje))


        mas_importantes = []

        for vertice in self.mas_importantes:
            if len(mas_importantes) >= n:
                return mas_importantes
            mas_importantes.append(vertice)

        return mas_importantes
 
    def persecucion_rapida(self, delincuentes_a_seguir, k):

        visitados = {}
        padres = {}
        orden = {}
        persecucion_mas_corta = []

        def encontrar_mas_buscados(raiz, adyacente):

            nonlocal persecucion_mas_corta
            if persecucion_mas_corta and len(persecucion_mas_corta) <= orden[raiz]+1:
                return False

            if adyacente in delincuentes_a_seguir and adyacente not in visitados:
                padres[adyacente] = None
                orden[adyacente] = 0
                funcionesGrafo.bfs(self.red_delincuentes, adyacente, encontrar_mas_buscados, visitados)

            if adyacente not in visitados or orden[raiz]+1 < orden[adyacente]:
                orden[adyacente] = orden[raiz] + 1
                padres[adyacente] = raiz
                if adyacente in visitados:
                    del(visitados[adyacente])

            if self.mas_importantes[adyacente][0] <= k:
                visitados[adyacente] = True
                camino = funcionesGrafo.reconstruir_camino(padres, adyacente)
                if not persecucion_mas_corta or auxiliares.se_encontro_mejor_camino(camino, persecucion_mas_corta, self.mas_importantes, adyacente):
                    persecucion_mas_corta = camino
                    return False    

            return True 

        for delincuente in delincuentes_a_seguir:
            if delincuente not in visitados:
                padres[delincuente] = None
                visitados[delincuente] = True
                orden[delincuente] = 0
                funcionesGrafo.bfs(self.red_delincuentes, delincuente, encontrar_mas_buscados, visitados)

        return persecucion_mas_corta
    

    def obtener_comunidades_n_integrantes(self, n):

        comunidades = funcionesGrafo.label_propagation(self.red_delincuentes)
        i = 0
        while i < len(comunidades):
            if len(comunidades[i]) < n:
                comunidades[i] = comunidades[-1]
                comunidades.pop()
            else:
                i = i+1
        
        return comunidades
        

    def divulgar_rumor(self, origen, amplitud):

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
    
        funcionesGrafo.bfs(self.red_delincuentes, origen, obtener_nodos_recorridos)
        return recorrido    
    
    def ciclo_mas_corto(self, delincuente):
        return funcionesGrafo.camino_minimo(self.red_delincuentes, delincuente, delincuente)
    

    def hallar_cfc(self):
        return funcionesGrafo.cfc(self.red_delincuentes)