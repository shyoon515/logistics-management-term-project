class Link:
    def __init__(self, node1, node2, cost = None, time=None):
        self.start = node1
        self.end = node2
        self.nodes = {node1, node2}
        self.cost = cost
        self.time = time
    
    def set_cost(cost):
        self.cost = cost

    def set_time(time):
        self.time = time
    
    def __str__(self):
        seconds = self.time//1000
        minutes = seconds//60
        hours = minutes//60
        remaining_minutes = minutes % 60
        return f"Link ({self.start.index} - {self.end.index}) : Cost {self.cost}, Time {hours}H {remaining_minutes}M"


        