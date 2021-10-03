class Node:
    def __init__(self, position, parent):
        self.position = position
        self.parent = parent
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
         return self.f < other.f
