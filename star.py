import heapq
from Node import Node

#Dimensões do mapa
map_width = 800
map_height = 800

#calculo por distância Manhattan do nó atual até o nó de destino (h)
def heuristic(node, target):
    return abs(node.x - target.x) + abs(node.y - target.y)


#Valida que um ponto está dentro do mapa
def is_valid_point(x, y):
    return 0 <= x < map_width and 0 <= y < map_height


#A*
def astar(start, target):
    open_list = []      #lista de nós abertos
    closed_list = []    #lista de nós fechados

    #Inicializa o nó inicial
    start.g = 0
    start.h = heuristic(start, target)
    start.f = start.h
    heapq.heappush(open_list, start)


    #procura o melhor caminho enquanto existir algo na lista de abertos
    while len(open_list) > 0:
        #retorna o nó com menor valor de f e coloca o nó atual na lista de fechados
        current_node = heapq.heappop(open_list) 
        closed_list.append(current_node)

        #Verifica se chegou no ponto de destino
        if current_node == target:
            path = []
            while current_node is not None:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]

        #Gera os vizinhos do nó atual
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x = current_node.x + dx
                new_y = current_node.y + dy
                if is_valid_point(new_x, new_y):

                    #calcula o custo para o novo nó
                    neighbor = Node(new_x, new_y)
                    neighbor.g = current_node.g + 1
                    neighbor.h = heuristic(neighbor, target)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current_node

                    #Verifica se o vizinho já está na lista aberta ou fechada
                    #Verifica se o vizinho já foi considerado anteriormente
                    if neighbor in closed_list:
                        continue
                    if neighbor in open_list:
                        existing_neighbor = open_list[open_list.index(neighbor)]

                        #verifica se os valores atuais (f,g) do vizinho são menores que
                        #os anteriores
                        if neighbor.g < existing_neighbor.g:
                            existing_neighbor.g = neighbor.g
                            existing_neighbor.f = neighbor.f
                            existing_neighbor.parent = neighbor.parent
                    else:
                        neighbors.append(neighbor)

        #Adiciona os vizinhos na lista aberta
        for neighbor in neighbors:
            heapq.heappush(open_list, neighbor)

    
    return None