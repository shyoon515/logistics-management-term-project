from tqdm import tqdm

def Clarke_Wright_Savings(saving_dict, node_list, capa, depot_node):
    """
    saving_dict: 정렬된 saving의 dictionary 객체
    demand_list: 각 node들의 demand list를 나열 -> depot을 제외한 demand list 만들기
    capa: 트럭의 capacity
    depot_node.index: depot의 index -> 오로지 마지막에 depot index를 붙여줄 때에만 쓰임
    """
    print("Iterating through the savings info ...")

    # demand_list 만들기
    demand_list = []
    for node in node_list:
        if node.index == depot_node.index:
            continue
        else:
            demand_list.append(node.demand)

    route_list = []
    node_state_list = [[0, 0, 0] for i in range(len(demand_list))]
    for link in tqdm(saving_dict):

        # 각 node의 idx
        i_idx = link[0]
        j_idx = link[1]

        # 각 node의 demand
        i_demand = demand_list[i_idx-1]
        j_demand = demand_list[j_idx-1]

        # route_list가 비어있는 경우 -> 새 route 생성
        if (len(route_list) == 0):
            # demand <= capa 확인
            demand = i_demand + j_demand
            if (demand <= capa):
                route_list.append([i_idx, j_idx])


        # route_list가 비어있지 않은 경우 -> node_state update
        else :
            for i in range(len(route_list)):
                for j in range(len(route_list[i])):
                    node_state_list[route_list[i][j]-1][0] = 1
                    node_state_list[route_list[i][j]-1][1] = i
                    node_state_list[route_list[i][j]-1][2] = j


            # node_state 가져오기
            i_in = node_state_list[i_idx-1][0]
            i_route_idx = node_state_list[i_idx-1][1]
            i_node_idx = node_state_list[i_idx-1][2]
            j_in = node_state_list[j_idx-1][0]
            j_route_idx = node_state_list[j_idx-1][1]
            j_node_idx = node_state_list[j_idx-1][2]


            # 기존 route들에 i, j 둘 다 없는 경우 -> 새 route 생성
            if (i_in == 0 and j_in == 0):
                # demand <= capa 확인
                demand = i_demand + j_demand
                if (demand <= capa):
                    route_list.append([i_idx, j_idx])


            # 기존 route들에 i, j 둘 다 있는 경우
            elif (i_in == 1 and j_in == 1):
                # i, j 모두 다른 route에 있는 경우
                if (i_route_idx != j_route_idx): 
                    # i_route와 j_route의 demand의 합 <= capa인 경우
                    demand = 0
                    for i in route_list[i_route_idx]:
                        demand += demand_list[i-1]
                    for j in route_list[j_route_idx]:
                        demand += demand_list[j-1]
                    
                    if (demand <= capa):
                        # i, j 모두 route의 첫 번째인 경우
                        if (i_node_idx == 0 and j_node_idx == 0):

                            # merge route
                            merge_route = []
                            for i in route_list[i_route_idx]:
                                merge_route.append(i)
                            for j in route_list[j_route_idx]:
                                merge_route.insert(0, j)
                            route_list.append(merge_route)

                            # delete route
                            if (i_route_idx > j_route_idx):
                                del route_list[i_route_idx]
                                del route_list[j_route_idx]
                            else :
                                del route_list[j_route_idx]
                                del route_list[i_route_idx]

                        # i, j 모두 route의 마지막인 경우
                        elif (i_node_idx == len(route_list[i_route_idx])-1 and j_node_idx == len(route_list[j_route_idx])-1):
                            # merge route
                            merge_route = []
                            for i in route_list[i_route_idx]:
                                merge_route.append(i)
                            for j in route_list[j_route_idx]:
                                merge_route.insert(len(route_list[i_route_idx]), j)
                            route_list.append(merge_route)

                            # delete route
                            if (i_route_idx > j_route_idx):
                                del route_list[i_route_idx]
                                del route_list[j_route_idx]
                            else :
                                del route_list[j_route_idx]
                                del route_list[i_route_idx]


                        # i는 route의 첫 번째, j는 route의 마지막인 경우
                        elif (i_node_idx == 0 and j_node_idx == len(route_list[j_route_idx])-1):
                            # merge route
                            merge_route = []
                            for j in route_list[j_route_idx]:
                                merge_route.append(j)
                            for i in route_list[i_route_idx]:
                                merge_route.append(i)
                            route_list.append(merge_route)

                            # delete route
                            if (i_route_idx > j_route_idx):
                                del route_list[i_route_idx]
                                del route_list[j_route_idx]
                            else :
                                del route_list[j_route_idx]
                                del route_list[i_route_idx]


                        # j는 route의 첫 번째, i는 route의 마지막인 경우
                        elif (j_node_idx == 0 and i_node_idx == len(route_list[i_route_idx])-1):
                            # merge route
                            merge_route = []
                            for i in route_list[i_route_idx]:
                                merge_route.append(i)
                            for j in route_list[j_route_idx]:
                                merge_route.append(j)
                            route_list.append(merge_route)

                            # delete route
                            if (i_route_idx > j_route_idx):
                                del route_list[i_route_idx]
                                del route_list[j_route_idx]
                            else :
                                del route_list[j_route_idx]
                                del route_list[i_route_idx]


            # 기존 route 들에 i, j 중 하나만 있는 경우
            else :
                # i_in == 1 & i가 route의 exterior인 경우
                if (i_in == 1 and (i_node_idx == 0 or i_node_idx == len(route_list[i_route_idx])-1)):
                    # i_route와 j의 demand의 합 <= capa인 경우
                    demand = 0
                    for i in route_list[i_route_idx]:
                        demand += demand_list[i-1]
                    demand += j_demand

                    if (demand <= capa):
                        # i가 route의 첫 번째인 경우
                        if (i_node_idx == 0):
                            route_list[i_route_idx].insert(0, j_idx)
                        # i가 route의 마지막인 경우
                        else :
                            route_list[i_route_idx].append(j_idx)
                
                # j_in == 1 & j가 route의 exterior인 경우
                elif (j_in == 1 and (j_node_idx == 0 or j_node_idx == len(route_list[j_route_idx])-1)):
                    # j_route와 i의 demand의 합 <= capa인 경우
                    demand = 0
                    for j in route_list[j_route_idx]:
                        demand += demand_list[j-1]
                    demand += i_demand

                    if (demand <= capa):
                        # j가 route의 첫 번째인 경우
                        if (j_node_idx == 0):
                            route_list[j_route_idx].insert(0, i_idx)
                        # j가 route의 마지막인 경우
                        else :
                            route_list[j_route_idx].append(i_idx)


    # 각 route의 양 쪽에 depot 연결해주기
    for i in route_list:
        i.insert(0, depot_node.index)
        i.append(depot_node.index)

    # route 어디에도 포함 안 된 point 새로운 route로 만들기
    for i in range(len(node_state_list)):
        if (node_state_list[i][0] == 0):
            route_list.append([depot_node.index, i+1, depot_node.index])
    
    return route_list
