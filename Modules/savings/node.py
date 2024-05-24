class Node:
    def __init__(self, index, x, y, demand=None):
        self.index = index
        self.x = x
        self.y = y
        self.position = (x, y)
        self.demand = demand
    
    def set_demand(self, demand):
        self.demand = demand

    def __str__(self):
        return f'Node {self.index} ({self.x}, {self.y}) : Demand {self.demand}'
    
