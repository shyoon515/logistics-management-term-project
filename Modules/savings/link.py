class Link:
    def __init__(self, node1, node2, cost = None):
        self.start = node1
        self.end = node2
        self.nodes = {node1, node2}
        self.cost = cost
    
    def set_cost(cost):
        self.cost = cost
    
    def __str__(self):
        return f"Link ({self.start.index} - {self.end.index}) : Cost {self.cost}"


        