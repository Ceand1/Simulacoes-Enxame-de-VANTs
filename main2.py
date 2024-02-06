from incendio import draw_burn, create_cell_map
from Cell import Cell
import cv2
import random
import math as mt
from Node import Node
from star import astar
from Drone import Drone

cont = 1
b = 0.111
x = 50
y = 50
c1 = 0.045
c2 = 0.131
U = 6


p_veg_grama = 0.4
p_veg_arbusto = 0.4

md_grama = 0.18
md_arbusto = 0.24

pden_espalhado = -0.4
pden_normal = 0
pden_denso = 0.3

vx1 = []
vy1 = []
vx2 = []
vy2 = []
cx = 0
cy = 0
x_atual = 0
y_atual = 0
x_prox = 0
y_prox = 0

PROB_PH = 0.6
PROB_UMI = 0.5
PROB_DEN = 0.33

cont_pixel = 0
cont_int = 0
cont_state = 0
cont_drone = 0

start_node = Node(8, 8)
targets = Node(765, 450)
target_node = Node(0,0)
drones = []

current_node = start_node

#Calcula pm
def prop_pm(mb):
    return mt.exp((-b)*mb)
    
#calcula pv
def prob_pw(theta):
    return mt.exp(c1*U)*mt.exp(U*c2*(mt.cos(theta)-1))

#calcula p_queima
def pburn(map, theta):
    return PROB_PH*(1+map.p_veg)*(1+map.p_den)*map.p_m*(prob_pw(theta))


#Causa o efeito do vento
def efWind(map,x,y):
    if(U >= 5 and map[x][y+1].value == 2):
        map[x][y+1].value = 3
        vx1.append(x)
        vy1.append(y+1)
    
    if(U >= 6 and map[x][y+2].value == 2):
        map[x][y+2].value = 3
        vx1.append(x)
        vy1.append(y+2)

    if(U >= 6 and map[x-1][y+1].value == 2):
        map[x-1][y+1].value = 3
        vx1.append(x-1)
        vy1.append(y+1)

    if(U >= 6 and map[x+1][y+1].value == 2):
        map[x+1][y+1].value = 3
        vx1.append(x+1)
        vy1.append(y+1)
        
map_data = create_cell_map()

#Para cada celula, colocar um valor de umidade, densidade e o tipo de vegetaçao 
for x1 in range(100):
    for y1 in range (100):
        map_data[x1][y1].p_veg = 0.4
        random.seed(random.randint(1,10000))
        if(random.random() <= PROB_UMI):
            map_data[x1][y1].p_m = prop_pm(md_grama)
        else:
            map_data[x1][y1].p_m = prop_pm(md_arbusto)

        rd = random.random()
        if(rd > PROB_DEN+0.33):
            map_data[x1][y1].p_den = pden_denso
        elif(rd > 0.33):
            map_data[x1][y1].p_den = pden_normal
        else:
            map_data[x1][y1].p_den = pden_espalhado


#Cria o foco de incêndio inicial
vx1.append(x)
vy1.append(y)
map_data[x][y].value = 3
draw_burn(map_data, drones)

#Espalha o incêndio pelo mapa de acordo com p_queima de cada celula e o 
#estado atual da mesmo, presente em cell.value
while True:
    random.seed(random.randint(1,1000))
    vx2 = vx1[:]
    vy2 = vy1[:]
    for i in range(len(vx2)):
        x = vx2[i]
        y = vy2[i]

        if(map_data[x+1][y].value == 2 and map_data[x][y].value == 3 and random.random() <= pburn(map_data[x+1][y], 4.71239)):
            map_data[x+1][y].value = 3
            vx1.append(x+1)
            vy1.append(y)
            efWind(map_data, x+1,y)
    
        if(map_data[x-1][y].value == 2 and map_data[x][y].value == 3 and random.random() <= pburn(map_data[x-1][y], 1.5708)): 
            map_data[x-1][y].value = 3
            vx1.append(x-1)
            vy1.append(y)
            efWind(map_data,x-1,y)

        if(map_data[x][y+1].value == 2 and map_data[x][y].value == 3 and random.random() <= pburn(map_data[x][y+1], 0)): 
            map_data[x][y+1].value = 3
            vx1.append(x)
            vy1.append(y+1)
            efWind(map_data,x,y+1)

        if(map_data[x][y-1].value == 2 and map_data[x][y].value == 3 and random.random() <= pburn(map_data[x][y-1], 3.14159)): 
            map_data[x][y-1].value = 3
            vx1.append(x)
            vy1.append(y-1)
            efWind(map_data,x,y-1)

        if(map_data[x+1][y+1].value == 2 and map_data[x][y].value == 3 and random.random() <= pburn(map_data[x+1][y+1], 5.49779)): 
            map_data[x+1][y+1].value = 3
            vx1.append(x+1)
            vy1.append(y+1)
            efWind(map_data,x+1,y+1)

        if(map_data[x+1][y-1].value == 2 and map_data[x][y].value == 3 and random.random() <= pburn(map_data[x+1][y-1], 3.92699)): 
            map_data[x+1][y-1].value = 3
            vx1.append(x+1)
            vy1.append(y-1)
            efWind(map_data,x+1,y-1)

        if(map_data[x-1][y+1].value == 2 and map_data[x][y].value == 3 and random.random() <= pburn(map_data[x-1][y+1], 0.785398)): 
            map_data[x-1][y+1].value = 3
            vx1.append(x-1)
            vy1.append(y+1)
            efWind(map_data,x-1,y+1)

        if(map_data[x-1][y-1].value == 2 and map_data[x][y].value == 3 and random.random() <= pburn(map_data[x-1][y-1], 2.35619)): 
            map_data[x-1][y-1].value = 3
            vx1.append(x-1)
            vy1.append(y-1)
            efWind(map_data,x-1,y-1)

        if(map_data[x][y].value == 3):
            map_data[x][y].value = 4


    #Escreve os dados do incendio em um arquivo .txt
    with open("wind9", 'a') as file:
        file.write(f"{cont}\t{len(vx1)}\n")
    cont+=1

    draw_burn(map_data, drones)

    #Atualiza o mapa a cada 60 segundos  
    if cv2.waitKey(60000) & 0xFF==ord('d'):
        break

    #Se o incêndio chegou a um tempo pré-determinado de iterações (cont_int), 
    #os drones são liberados para o combate
    cont_int+=1
    if cont_state == 0:
        if(cont_int == 2):
            
            #inicializa os drones
            for i in range(len(vx1)):
                x = vx1[i]
                y = vy1[i]

                if(map_data[x][y].value == 3):
                    cont_drone+=1
            
            drones += [Drone(Node(15, 15)) for _ in range(cont_drone)]

            draw_burn(map_data, drones)

            #Para cada drones, se o mesmo ainda não foi designado para uma nova celula
            # o mesmo recebe um alvo
            for drone in drones:
                if drone.state == 0:
                    for i in range(len(vx1)):
                        x = vx1[i]
                        y = vy1[i]
                        print(f"cell1: {map_data[x][y].value}, cell2: {map_data[x][y+1].value}")
                        #Testa se a celula designada como alvo esta queimando e se ainda não possui drone
                        if((map_data[x][y].value == 3 and map_data[x][y].value2 != 1)):
                            x1 = x * 8
                            y1 = y * 8
                            drone.cell_x = x
                            drone.cell_y = y
                            map_data[x][y].value2 = 1
                            cx = x1 + 8 // 2
                            cy = y1 + 8 // 2

                            print(f"x1: {x}, y1: {y}, cx: {cx}, cy: {cy}")

                            print(f"x1: {map_data[x][y].value}, y1: {map_data[x][y+1].value}, cx: {map_data[x][y+2].value}")
                            drone.state = 1
                            break
                    
                    #A cada iteração, testa se o movimento do drone não passa da distância max
                    #que ele consegue atingir em 1min
                    while cont_pixel < 1400:
                        drone.target_node = Node(cy,cx)
                        #Obtém o próximo passo de movimento
                        path = astar(drone.current_node, drone.target_node)

                        if path is None:
                            print("Erro.")
                            break

                        #Move o ponto atual para o próximo nó no caminho
                        drone.current_node = Node(path[1][0], path[1][1])
                        cont_pixel+=1

                        #Atualiza o mapa 
                        draw_burn(map_data, drones)

                        if drone.current_node == drone.target_node:
                            cont_state = 1
                            break
                
            for drone in drones:
                if drone.state == 0:
                    for i in range(len(vx1)):
                        x = vx1[i]
                        y = vy1[i]
                        print(f"cell1: {map_data[x][y].value}, cell2: {map_data[x][y+1].value}")
                        if((map_data[x][y].value == 3 and map_data[x-1][y].value == 4 and 
                            map_data[x][y].value2 != 1) or (map_data[x][y].value == 3 and map_data[x+1][y].value == 4 and map_data[x][y].value2 != 1)):
                            x1 = x * 8
                            y1 = y * 8
                            drone.cell_x = x
                            drone.cell_y = y
                            map_data[x][y].value2 = 1
                            cx = x1 + 8 // 2
                            cy = y1 + 8 // 2

                            print(f"x1: {x}, y1: {y}, cx: {cx}, cy: {cy}")

                            print(f"x1: {map_data[x][y].value}, y1: {map_data[x][y+1].value}, cx: {map_data[x][y+2].value}")
                            drone.state = 1
                            break

                    while cont_pixel < 1400:
                        drone.target_node = Node(cy,cx)
                        path = astar(drone.current_node, drone.target_node)

                        if path is None:
                            print("Erro.")
                            break

                        drone.current_node = Node(path[1][0], path[1][1])
                        cont_pixel+=1

                        draw_burn(map_data, drones)

                        if drone.current_node == drone.target_node:
                            cont_state = 1
                            break

            for drone in drones:
                if drone.state == 0:
                    for i in range(len(vx1)):
                        x = vx1[len(vx1)-1-i]
                        y = vy1[len(vx1)-1-i]
                        print(f"cell1: {map_data[x][y].value}, cell2: {map_data[x][y+1].value}")
                        if((map_data[x][y].value == 3 and map_data[x][y].value2 != 1)):
                            x1 = x * 8
                            y1 = y * 8
                            drone.cell_x = x
                            drone.cell_y = y
                            map_data[x][y].value2 = 1
                            cx = x1 + 8 // 2
                            cy = y1 + 8 // 2

                            print(f"x1: {x}, y1: {y}, cx: {cx}, cy: {cy}")

                            print(f"x1: {map_data[x][y].value}, y1: {map_data[x][y+1].value}, cx: {map_data[x][y+2].value}")
                            drone.state = 1
                            break

                        


                    while cont_pixel < 1400:
                        drone.target_node = Node(cy,cx)
                        path = astar(drone.current_node, drone.target_node)

                        if path is None:
                            print("Erro.")
                            break

                        drone.current_node = Node(path[1][0], path[1][1])
                        cont_pixel+=1

                        draw_burn(map_data, drones)

                        if drone.current_node == drone.target_node:
                            cont_state = 1
                            break

            for drone in drones:
                if drone.state == 0:
                    for i in range(len(vx1)):
                        x = vx1[len(vx1)-1-i]
                        y = vy1[len(vx1)-1-i]
                        print(f"cell1: {map_data[x][y].value}, cell2: {map_data[x][y+1].value}")
                        if((map_data[x][y-1].value == 4 and map_data[x][y].value == 3 and 
                            map_data[x][y+1].value == 3 and map_data[x][y+2].value == 2 and map_data[x][y].value2 != 1)):
                            x1 = x * 8
                            y1 = y * 8
                            drone.cell_x = x
                            drone.cell_y = y
                            map_data[x][y].value2 = 1
                            cx = x1 + 8 // 2
                            cy = y1 + 8 // 2

                            print(f"x1: {x}, y1: {y}, cx: {cx}, cy: {cy}")

                            print(f"x1: {map_data[x][y].value}, y1: {map_data[x][y+1].value}, cx: {map_data[x][y+2].value}")
                            drone.state = 1
                            break

                        


                    while cont_pixel < 1400:
                        drone.target_node = Node(cy,cx)
                        path = astar(drone.current_node, drone.target_node)

                        if path is None:
                            print("Erro.")
                            break

                        drone.current_node = Node(path[1][0], path[1][1])
                        cont_pixel+=1

                        draw_burn(map_data, drones)

                        if drone.current_node == drone.target_node:
                            cont_state = 1
                            break

        for drone in drones:
            drone.state = 0

        cont_pixel = 0


    #Define um novo alvo, ou celula, para cada drone
    if cont_state == 1:
        for drone in drones:
            #Testa todas as celulas vizinhas da atual
            for dx in [0, -1, 1]:
                for dy in [1, -1, 0]:
                    if((map_data[drone.cell_x+dx][drone.cell_y+dy].value == 3 or map_data[drone.cell_x+dx][drone.cell_y+dy].value == 4) 
                       and map_data[drone.cell_x+dx][drone.cell_y+dy].value != 1):
                        
                        x1 = drone.cell_x * 8
                        y1 = drone.cell_y * 8

                        cx = x1 + 8 // 2
                        cy = y1 + 8 // 2
                        drone.current_node = Node(cy,cx)
                        map_data[drone.cell_x][drone.cell_y].value = 1
                                    
                        x1 = (drone.cell_x+dx) * 8
                        y1 = (drone.cell_y+dy) * 8

                        x_prox = drone.cell_x+dx
                        y_prox = drone.cell_y+dy

                        map_data[x_prox][y_prox].value = 1

                        cx = x1 + 8 // 2
                        cy = y1 + 8 // 2
                        drone.target_node = Node(cy,cx)
                        drone.state = 1
                        break
                
                if drone.state == 1:
                    drone.state = 0
                    break


                    
            
            print(drone)
            print(f"x1: {x_prox}, y1: {y_prox}")
            #Executa, novamente, o A* para cada drone
            while drone.current_node != drone.target_node:
                    path = astar(drone.current_node, drone.target_node)

                    if path is None:
                        print("Erro.")
                        break

                    drone.current_node = Node(path[1][0], path[1][1])

                    map_data[x_atual][y_atual].value = 1
                    draw_burn(map_data, drones)

                    if drone.current_node == drone.target_node:
                        map_data[drone.cell_x][drone.cell_y].value = 1
                        drone.cell_x = x_prox
                        drone.cell_y = y_prox
                        break




    
#    cv2.waitKey(0)
