from itertools import combinations
from .route import Route
from .SavingsAlgorithm import Clarke_Wright_Savings

class SavingsModel:
    def __init__(self, graph, depot_index):
        self.graph = graph
        self.depot = graph.get_node(depot_index)
        self.savings = None
        self.routes = []
        self.demand = 0
        self.cost = 0
        #print('SavingsModel initialized')
    
    def calculate_savings(self):
        """
        self.savings에 savings를 자동으로 계산하여 저장
        """
        savings = dict()

        # depot node가 아닌 node들의 combination 조합에서 savings들을 계산
        non_depot_nodes = [n for n in self.graph.nodes if n != self.depot]
        node_combs = [comb for comb in combinations(non_depot_nodes, 2)]
        #print(f"Calculating savings for {len(self.graph.nodes)-1} nodes, \n[Depot node] {self.depot}")
        for n1, n2  in node_combs:
            savings[(n1.index, n2.index)] = self.graph.get_link(self.depot, n1).cost + self.graph.get_link(self.depot, n2).cost - self.graph.get_link(n1, n2).cost
        
        # 정렬 후 savings에 저장
        result= {}
        for i, j in sorted(savings.items(), key=lambda item: item[1], reverse=True):
            result[i] = j
        self.savings = result
        

    def apply_algorithm(self, capa, algorithm, verbose=True, stochastic_drop=0.0):
        """
        self.routes에 알고리즘을 통해 구해진 route 해를 저장
        """
        self.routes = [] # 초기화
        self.demand = 0
        self.cost = 0
        self.time = 0
        # savings가 계산이 안 된 경우
        if self.savings == None:
            raise ValueError("Savings uncalculated. Calculate savings first by 'self.calculate_savings()'.")
        
        all_routes = algorithm(self.savings, self.graph.nodes, capa, self.depot, verbose=verbose, stochastic_drop=stochastic_drop)
        for r in all_routes:
            self.routes.append(Route(self.graph, r))
        
        for r in self.routes:
            self.demand += r.demand
            self.cost += r.cost
            self.time += r.time
    
    def print_routes(self):
        for r in self.routes:
            print(r)
    
    def yearly_cost(self, yearly_days=365, fixed=0, verbose=False):
        fixed = int(fixed)
        total_cost = self.cost*yearly_days + len(self.routes)*fixed
        if verbose==False:
            print(f"연간 운송비: {self.cost*yearly_days:,}원")
            print(f"연간 인건비: {len(self.routes)*fixed:,}원")
            print(f"연간 총 비용: {total_cost:,}원")
        return total_cost
