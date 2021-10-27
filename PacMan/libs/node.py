class Node:
    def __init__(self, position=None, parent=None, children=[], value=0, state=None):
        self.position = position
        self.parent = parent
        self.children = children
        self.value = value
        self.state = state
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
         return self.f < other.f

