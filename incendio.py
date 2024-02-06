import cv2
import numpy as np
from Cell import Cell
from Drone import Drone

map_width = 800
map_height = 800
cell_size = 8 
color_green = (0, 255, 0)
color_green2 = (200, 255, 0)
color_gray = (128, 128, 128)
color_blue = (255, 75, 75)
color_red = (0, 0, 255)

#Cria o mapa de célula usando o tamanho de uma célula e as dimensões do mapa de pixels
def create_cell_map():
    cells_x = map_width // cell_size
    cells_y = map_height // cell_size
    return [[Cell(x, y) for x in range(cells_x)] for y in range(cells_y)]


#Desenha o mapa
def draw_burn(map_data, drones):
    map_img = np.zeros((map_height, map_width, 3), dtype=np.uint8)
    map_img[:] = color_green

    #Pinta as células de acordo com o seu estado de AC
    for row in map_data:
        for cell in row:
            x1 = cell.x * cell_size
            y1 = cell.y * cell_size
            x2 = (cell.x + 1) * cell_size - 1
            y2 = (cell.y + 1) * cell_size - 1

            if cell.value == 1:
                cv2.rectangle(map_img, (x1, y1), (x2, y2), color_green2, -1)
            if cell.value == 3:
                cv2.rectangle(map_img, (x1, y1), (x2, y2), color_red, -1)
            if cell.value == 4:
                cv2.rectangle(map_img, (x1, y1), (x2, y2), color_gray, -1)

    
    #Faz o efeito de movimento do drone
    for drone in drones:
        cv2.circle(map_img, (drone.current_node.x, drone.current_node.y), 3, color_blue, -1)

    cv2.imshow("Map", map_img)
    cv2.waitKey(1)

