import json
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import time

class Route:
    def __init__(self, graph, nodes):
        """
        nodes는 index일수도, node 객체일수도 있는 list 객체. graph 상에서 움직일 수 있어야 하므로 graph도 input으로 받음
        """
        self.graph = graph
        self.nodes = []
        self.links = []
        self.demand = 0
        self.cost = 0
        self.time = 0
        for n in nodes:
            if isinstance(n, int):
                n = graph.get_node(n)
            self.nodes.append(n)
            self.demand += + n.demand
        for idx in range(len(self.nodes)):
            if idx != len(self.nodes)-1:
                l = self.graph.get_link(self.nodes[idx], self.nodes[idx+1])
                self.links.append(l)
                self.cost += l.cost
                self.time += l.time
    
    def visualize(self, ax, json_path, route_option='trafast', update_sec = 1, color='black'):
        for link in self.links:
            start_idx = link.start.index
            goal_idx = link.end.index
            if start_idx > goal_idx:
                temp = start_idx
                start_idx = goal_idx
                goal_idx = temp
            
            if json_path[-1] != '/':
                json_path += '/'
            
            file_path = json_path + f"route_{start_idx}_{goal_idx}.json"

            with open(file_path, 'r') as file:
                data = json.load(file)
            route = data['route'][route_option][0]['path']

            # x, y좌표 생성
            x_coords = [point[0] for point in route]
            y_coords = [point[1] for point in route]

            ax.plot(x_coords, y_coords, linewidth=0.7, c=color)
            display(plt.gcf())  # 현재 플롯을 표시
            clear_output(wait=True)  # 이전 플롯을 지움
            time.sleep(update_sec)  # 1초 대기 (업데이트 속도 조절)    
    
    def __str__(self):
        txt = "Route :"
        for idx in range(len(self.nodes)):
            if idx == len(self.nodes)-1:
                txt = txt + f' {self.nodes[idx].index}\n'
            else:
                txt = txt + f' {self.nodes[idx].index} -'
        
        seconds = self.time//1000
        minutes = seconds//60
        hours = minutes//60
        remaining_minutes = minutes % 60

        txt = txt + f'Demand met : {self.demand}, Cost : {self.cost}, Time {hours}H {remaining_minutes}M'
        return txt