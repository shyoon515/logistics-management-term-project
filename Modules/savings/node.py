import numpy as np

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
    
    def generate_demand(self, demand_mu, upper_bound, cv=0):
        std = demand_mu * cv
        np.random.seed(42)
        demand = np.random.normal(demand_mu, std)
        if demand < 0:
            demand = 0
        if demand > upper_bound:
            demand = upper_bound
        self.set_demand(demand)

    
