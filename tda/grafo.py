import random

class Grafo:
    def __init__(self, dirigido=False):
        self.vertices = {}
        self.dirigido = dirigido
    
    def eliminar_grafo(self):
        self.vertices.clear()

    def agregar_vertice(self, vertice):
        if vertice not in self.vertices:
            self.vertices[vertice] = {}

    def sacar_vertice(self, vertice):
        if vertice in self.vertices:
            for adyacentes in self.vertices.values():
                if vertice in adyacentes:
                    del adyacentes[vertice]
            del self.vertices[vertice]

    def agregar_arista(self, origen, destino, peso=1):
        if origen in self.vertices and destino in self.vertices:
            self.vertices[origen][destino] = peso
            if not self.dirigido:
                self.vertices[destino][origen] = peso

    def sacar_arista(self, origen, destino):
        if origen in self.vertices and destino in self.vertices[origen]:
            del self.vertices[origen][destino]
            if not self.dirigido and destino in self.vertices and origen in self.vertices[destino]:
                del self.vertices[destino][origen]

    def estan_unidos(self, origen, destino):
        if origen in self.vertices and destino in self.vertices[origen]:
            return True, self.vertices[origen][destino]
        return False, None

    def existe_vertice(self, vertice):
        return vertice in self.vertices

    def obtener_vertices(self):
        return list(self.vertices.keys())

    def obtener_adyacentes(self, vertice):
        if vertice in self.vertices:
            return list(self.vertices[vertice].keys())
        return []

    def iterar_vertices(self):
        for vertice in self.vertices:
            yield vertice

    def obtener_vertice_al_azar(self):
        if not self.vertices:
            return None
        return random.choice(list(self.vertices.keys()))

    def __str__(self):
        result = []
        for vertice, adyacentes in self.vertices.items():
            for destino, peso in adyacentes.items():
                result.append(f"{vertice} -> {destino} [peso: {peso}]")
        return "\n".join(result)

"""# chequeo de operaciones del grafo:
grafo = Grafo(dirigido=False)

# agregar vertices
for i in range(1, 5):
    grafo.agregar_vertice(i)

# agregar aristas
grafo.agregar_arista(1, 2, 5)
grafo.agregar_arista(1, 3, 10)
grafo.agregar_arista(2, 3, 3)
grafo.agregar_arista(3, 4, 2)

# verificar si dos vertices estan unidos
print(grafo.estan_unidos(1, 2))  # (True, 5)
print(grafo.estan_unidos(1, 4))  # (False, None)

# verificar si un vertice existe
print(grafo.existe_vertice(3))  # True
print(grafo.existe_vertice(5))  # False

# obtener todos los vertices
print(grafo.obtener_vertices())  # [1, 2, 3, 4]

# obtener los adyacentes a un vertice
print(grafo.obtener_adyacentes(1))  # [2, 3]
print(grafo.obtener_adyacentes(4))  # [3]

# iterar sobre los vertices
print("\nVetices del grafo:")
for vertice in grafo.iterar_vertices():
    print(vertice)

# Visualizar el grafo
print("\nRepresentacion del grafo:")
print(grafo)

# Eliminar aristas y vertices
grafo.sacar_arista(1, 2)
grafo.sacar_vertice(3)

print("\nGrafo despues de eliminar aristas y vertices:")
print(grafo)
"""