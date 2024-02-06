
#Classe dos nós
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    