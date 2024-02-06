import cv2
import numpy as np


map_width = 800
map_height = 800
color_green = (0, 255, 0)
color_blue = (255, 0, 0)

map_img = np.zeros((map_height, map_width, 3), dtype=np.uint8)
map_img[:] = color_green


def draw_map(start, targets, current):
    #map_img = np.zeros((map_height, map_width, 3), dtype=np.uint8)
    #map_img[:] = color_green

    #Desenha o ponto de partida
    cv2.circle(map_img, (start.x, start.y), 7, color_blue, -1)

    #Desenha os pontos de destino
    #for target in targets:
    cv2.circle(map_img, (targets.x, targets.y), 7, color_blue, -1)

    #Desenha o ponto atual
    cv2.circle(map_img, (current.x, current.y), 3, color_blue, -1)

    cv2.imshow("Map", map_img)
    cv2.waitKey(1)