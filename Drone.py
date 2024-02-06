class Drone:
    def __init__(self, start_node):
        self.current_node = start_node
        self.target_node = None
        self.cell_x = 0
        self.cell_y = 0
        self.state = 0