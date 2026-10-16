"""
Definicao da classe Point, que guarda informacoes sobre um ponto
Um ponto pode ser a origem de um abrigo ou de uma pessoa
Essa classe eh a responsavel por calcular a distancia entre dois pontos,
usando a formula de distancia Euclideana
"""
class Point:
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)

	def dist(self, other):
		deltax = (self.x - other.x) ** 2
		deltay = (self.y - other.y) ** 2
		return (deltax + deltay) ** 0.5
	
	def __repr__(self):
		return str((self.x, self.y))

"""
Definicao da classe Shelter, que guarda informacoes sobre os abrigos
O objetivo principal dessa classe eh o metodo is_connected, que
retorna um booleano indicando se um abrigo esta ou nao conectado a
qualquer outro recebido por parametro (abrigo A esta conectado a abrigo B
sse a distancia entre seus centros eh menor ou igual a soma de seus raios)
"""
class Shelter:
	def __init__(self, r, cx, cy):
		self.radius = int(r)
		self.center = Point(cx, cy)

	def __repr__(self):
		return str((self.radius, self.center.x, self.center.y))

	def is_connected(self, other):
		dist = self.center.dist(other.center)
		return dist <= (self.radius + other.radius)

"""
Definicao da classe Person, responsavel por modelar Ana e Bernardo
Ambos sao pessoas, com um ponto no plano cartesiano como local de origem
Essa classe possui o metodo find_sheltering, que retorna o indice (no vetor
de abrigos) do abrigo que a pessoa pertence
"""
class Person:
	def __init__(self, x, y):
		self.coord = Point(x, y)

	def __repr__(self):
		return self.coord.__repr__()

	def find_sheltering(self, shelters):
		for i in range(len(shelters)):
			shelter = shelters[i]
			dist_to_shelter_center = self.coord.dist(shelter.center)
			is_in_shelter =  dist_to_shelter_center <= shelter.radius
			if is_in_shelter: return i

"""
Funcao para a construcao do grafo. O grafo, nesse trabalho,
foi modelado utilizando uma lista de adjacencia - para garantir que
a complexidade temporal dos algoritmos permanecesse linear.
Dessa forma, essa funcao pega como parametro o vetor de abrigos e retorna
a lista de adjacencias que representa o grafo
"""
def build_graph(shelters):
	graph = []
	n = len(shelters)

	for i in range(n):
		graph.append([])
		shelteri = shelters[i]
		for j in range(n):
			shelterj = shelters[j]
			has_edge_ij = shelteri.is_connected(shelterj)
			if has_edge_ij:
				graph[i].append(j)
	
	return graph

"""
Funcao para a execucao da busca em largura (BFS). Pega como parametro
opcional um vetor de vertices descobertos - essa versatilidade permite 
que a funcao seja usada tambem para encontrar componentes conexos,
e nao somente caminhos entre vertices.
"""
def bfs(graph, s, discovered=None):
	if discovered == None:
		discovered = [False] * len(graph)

	discovered[s] = True
	layers = [[s]]
	i = 0

	while layers[i]:
		layers.append([])
		for node in layers[i]:
			edges = graph[node]
			for vertex in edges:
				if not discovered[vertex]:
					discovered[vertex] = True
					layers[i+1].append(vertex)

		i += 1
	
	layers.pop()
	return layers

"""
Funcao para a execucao da busca em profundidade (DFS), ja embutida com
o algoritmo de Tarjan, para encontrar pontos de articulacao (abrigos criticos)
em tempo linear.
"""
def dfs(graph, s, visited, discovered, low, time, parent, articulation_points):
	visited[s] = True
	time += 1
	discovered[s] = time
	low[s] = time
	children = 0

	edges = graph[s]
	for vertex in edges:
		if not visited[vertex]:
			children += 1
			time = dfs(graph, vertex, visited, discovered, low, time, s, articulation_points)
			low[s] = min(low[s], low[vertex])
			if parent != -1 and low[vertex] >= discovered[s]:
				articulation_points[s] = True
		elif vertex != parent:
			low[s] = min(low[s], discovered[vertex])

	if parent == -1 and children > 1:
		articulation_points[s] = True

	return time

"""
Funcao para encontrar componentes conexos. Utiliza
a BFS definida acima.
"""
def get_components(graph):
	discovered = [False] * len(graph)
	components = []

	while False in discovered:
		i = discovered.index(False)
		bfs_path = bfs(graph, i, discovered)
		components.append(bfs_path)

	return components

"""
Funcao para encontrar pontos de articulacao (aka vertices
de corte). Utiliza a DFS definida acima.
"""
def get_articulation_points(graph):
	n = len(graph)
	visited = [False] * n
	discovered = [0] * n
	low = [0] * n
	articulation_points = [False] * n

	while False in visited:
		i = visited.index(False)
		dfs(graph, i, visited, discovered, low, 0, -1, articulation_points)

	return [ idx for idx, ap in enumerate(articulation_points) if ap ]

"""
Funcao principal do programa.
"""
def main():
	shelters = []
	ana = input()
	if len(ana) == 0: ana = input()
	bernardo = input()
	n = input()
	ana = Person(*ana.split(' '))
	bernardo = Person(*bernardo.split(' '))
	n = int(n)

	for i in range(n):
		shelter = input()
		ri, xi, yi = shelter.split(' ')
		shelter = Shelter(ri, xi, yi)
		shelters.append(shelter)

	graph = build_graph(shelters)
	shelter_ana = ana.find_sheltering(shelters)
	shelter_bernardo = bernardo.find_sheltering(shelters)
	bfs_path = bfs(graph, shelter_ana)
	components = get_components(graph)
	components_layer_amounts = [ len(bfs(graph, component[-1][-1])) for component in components ]
	critical_shelters = get_articulation_points(graph)

	parte_1 = -1
	parte_2 = max(components_layer_amounts) - 1
	parte_3_1 = len(critical_shelters)
	parte_3_2 = ' '.join([ str(cs + 1) for cs in critical_shelters ])

	for i in range(len(bfs_path)):
		if shelter_bernardo in bfs_path[i]:
			parte_1 = i
			break

	print(f'Parte 1: {parte_1}')
	print(f'Parte 2: {parte_2}')
	print(f'Parte 3: {parte_3_1} {parte_3_2}')

if __name__ == '__main__':
	main()