import cv2
from Node import Node
from star import astar
from map import draw_map



def main():
    #Cria os pontos de partida e destino
    start_node = Node(18, 20)
    targets = [Node(765, 20),
               Node(373, 372)]
    target_index = 0

    #Inicializa o ponto atual como o ponto de partida
    current_node = start_node

    #Cria o mapa
    draw_map(start_node, targets, current_node)

    #Executa o loop de movimento até chegar no destino final
    while target_index < len(targets):
        target_node = targets[target_index]

        #Obtém o próximo passo de movimento
        path = astar(current_node, target_node)

        if path is None:
            print("Erro.")
            break

        #Move o ponto atual para o próximo nó no caminho
        current_node = Node(path[1][0], path[1][1])

        #Atualiza o mapa 
        draw_map(start_node, targets, current_node)

        #Verifica se chegou no destino
        if current_node == target_node:
            target_index += 1


    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

