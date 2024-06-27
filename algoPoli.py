from librerias import informeDelincuentes
from tdas import grafo

g = grafo.Grafo(True)

g.agregar_vertice("Pablo")
g.agregar_vertice("Rosita")
g.agregar_vertice("Dato")

g.agregar_vertice("Dato")
g.agregar_vertice("Fede")
g.agregar_vertice("Jorge")
g.agregar_vertice("Martin")
g.agregar_vertice("Mati")
g.agregar_vertice("Nacho")
g.agregar_vertice("Cami")
g.agregar_vertice("Jas")
g.agregar_vertice("Eze")

g.agregar_arista("Dato", "Mati")
g.agregar_arista("Nacho", "Jorge")
g.agregar_arista("Cami", "Nacho")
g.agregar_arista("Mati", "Nacho")
g.agregar_arista("Jorge", "Dato")
g.agregar_arista("Jorge", "Cami")
g.agregar_arista("Jorge", "Jas")
g.agregar_arista("Jas", "Eze")
g.agregar_arista("Eze", "Jas")
g.agregar_arista("Eze", "Rosita")
g.agregar_arista("Jorge", "Martin")
g.agregar_arista("Fede", "Martin")
g.agregar_arista("Martin", "Pablo")
g.agregar_arista("Pablo", "Fede")
g.agregar_arista("Fede", "Pablo")

informe = informeDelincuentes.informe_delincuentes(g)

mas_importantes = informe.delincuentes_mas_importantes(5)

persecucion = informe.persecucion_rapida(["Nacho", "Jas"], 6)

comunidades = informe.obtener_comunidades_n_integrantes(4)

informados = informe.divulgar_rumor("Nacho", 2)

ciclo = informe.ciclo_mas_corto("Nacho")

cfc = informe.hallar_cfc()