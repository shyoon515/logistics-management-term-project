from itertools import combinations
import more_itertools
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

        self.merged_routes = []
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
        

    def apply_algorithm(self, capa, algorithm, max_time, service_time, stochastic_drop=0.0):
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
        
        # node to node time list of list 만들기
        n2n_time = []
        for n1 in self.graph.nodes:
            temp = []
            for n2 in self.graph.nodes:
                if n1 == n2:
                    temp.append(0)
                    continue
                temp.append(self.graph.get_link(n1, n2).time)
            n2n_time.append(temp)

        all_routes = algorithm(self.savings, self.graph.nodes, capa, self.depot, max_time, n2n_time, service_time, stochastic_drop=stochastic_drop)
        
        for r in all_routes:
            self.routes.append(Route(self.graph, r))
        
        for r in self.routes:
            self.demand += r.demand
            self.cost += r.cost
            self.time += r.time
    
    def print_routes(self):
        for r in self.routes:
            print(r)
    
    # truck의 시간 capa도 merge 해준 비용 계산
    def yearly_cost(self, max_time, yearly_days=365, fixed=0, verbose=False):

        truck_num = len(self.routes)
        all_merged_routes = list(more_itertools.set_partitions(self.routes))
        best_merged_routes = all_merged_routes[-1]
        for merged_routes in all_merged_routes:
            cur_truck_num = len(merged_routes)
            ismergeable = True
            for merged_route in merged_routes:
                cur_merged_route_time = sum([r.time for r in merged_route])
                if cur_merged_route_time > max_time:
                    ismergeable=False
                    break
            
            if ismergeable: # mergeable인 경우, truck_num을 비교하여 작은 것을 선택
                if cur_truck_num < truck_num:
                    truck_num = cur_truck_num
                    best_merged_routes = merged_routes
        self.merged_routes = best_merged_routes

        fixed = int(fixed)
        total_cost = self.cost*yearly_days + len(self.merged_routes)*fixed
        if verbose==False:
            print(f"연간 운송비: {self.cost*yearly_days:,}원")
            print(f"연간 인건비: {len(self.merged_routes)*fixed:,}원")
            print(f"연간 총 비용: {total_cost:,}원")
        return total_cost
