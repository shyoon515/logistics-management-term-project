import numpy as np

def Clarke_Wright_Savings(saving_dict, node_list, capa, depot_node, time_constraint, n2n_time, service_time, stochastic_drop=0.0):
    """
    saving_dict: 정렬된 saving의 dictionary 객체
    demand_list: 각 node들의 demand list를 나열 -> depot을 제외한 demand list 만들기
    capa: 트럭의 capacity
    depot_node.index: depot의 index -> 오로지 마지막에 depot index를 붙여줄 때에만 쓰임
    """

    # demand_list 만들기
    demand_list = []
    for node in node_list:
        if node.index == depot_node.index:
            continue
        else:
            demand_list.append(node.demand)

    # time_constraint 설정 -> 추후, function parameter로 넣어주면 됨!
    # time은 계산하기 편하게 우선 min으로 해 줌, 나머지 시간들도 min 기준이라 생각하면 될 듯

    # node-node 이동 시간 : 2차원 리스트
    # 디폿(물류창고)+노드(네프론)의 개수가 54이라고 가정 -> elem이 모두 0인 54x54 2차원 리스트 생성

    # node의 service time : 1차원 리스트
    # 노드(네프론)의 개수가 53이라고 가정 -> elem이 모두 0인 리스트 생성
    service_time = [service_time for i in range(len(demand_list))]

    route_list = []
    node_state_list = [[0, 0, 0] for i in range(len(demand_list))]
    for link in saving_dict:
        if (np.random.binomial(n=1, p=stochastic_drop, size=1)[0] == 1):
           continue
        if saving_dict[link] < 0:
           continue # saving이 음수인 경우 건너뜀

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
              # time <= time_constraint 확인
              time = n2n_time[0][i_idx] + n2n_time[i_idx][j_idx] + n2n_time[j_idx][0] + service_time[i_idx] + service_time[j_idx]
              if (time <= time_constraint):
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
                  # time <= time_constraint 확인
                  time = n2n_time[0][i_idx] + n2n_time[i_idx][j_idx] + n2n_time[j_idx][0] + service_time[i_idx-1] + service_time[j_idx-1]
                  if (time <= time_constraint):
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

                    # depot -> i_route -> j_route -> depot의 소요 time + 노드의 service time <= time_constraint인 경우
                    time = 0
                    # service time 모두 합하기
                    # 노드 간 이동 시간은 각 branch 별로 merge_route 생성 후, merge_route 통해서 한 번에 구하는게 편할 것 같아서 밑에서 해줄게
                    for i in route_list[i_route_idx]:
                      time += service_time[i-1]
                    for j in route_list[j_route_idx]:
                      time += service_time[j-1]

                    if (demand <= capa):
                        # i, j 모두 route의 첫 번째인 경우
                        if (i_node_idx == 0 and j_node_idx == 0):

                            # merge route
                            merge_route = []
                            for i in route_list[i_route_idx]:
                                merge_route.append(i)
                            for j in route_list[j_route_idx]:
                                merge_route.insert(0, j)

                            # node 간 이동 시간 모두 합하기
                            for i in range(len(merge_route)-1):
                              # merge_route의 i번째 node -> i+1번째 node 이동 시간
                              time += n2n_time[merge_route[i]][merge_route[i+1]]
                              # depot -> 0번째 노드 + 마지막 노드 -> depot 시간 합하기
                              time += n2n_time[0][merge_route[0]]
                              time += n2n_time[merge_route[-1]][0]

                            # time constraint 만족하는지 확인
                            if (time <= time_constraint):
                              # merge_route 추가
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

                            # node 간 이동 시간 모두 합하기
                            for i in range(len(merge_route)-1):
                              # merge_route의 i번째 node -> i+1번째 node 이동 시간
                              time += n2n_time[merge_route[i]][merge_route[i+1]]
                              # depot -> 0번째 노드 + 마지막 노드 -> depot 시간 합하기
                              time += n2n_time[0][merge_route[0]]
                              time += n2n_time[merge_route[-1]][0]

                            # time constraint 만족하는지 확인
                            if (time <= time_constraint):
                              # merge_route 추가
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

                            # node 간 이동 시간 모두 합하기
                            for i in range(len(merge_route)-1):
                              # merge_route의 i번째 node -> i+1번째 node 이동 시간
                              time += n2n_time[merge_route[i]][merge_route[i+1]]
                              # depot -> 0번째 노드 + 마지막 노드 -> depot 시간 합하기
                              time += n2n_time[0][merge_route[0]]
                              time += n2n_time[merge_route[-1]][0]

                            # time constraint 만족하는지 확인
                            if (time <= time_constraint):
                              # merge_route 추가
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

                            # node 간 이동 시간 모두 합하기
                            for i in range(len(merge_route)-1):
                              # merge_route의 i번째 node -> i+1번째 node 이동 시간
                              time += n2n_time[merge_route[i]][merge_route[i+1]]
                              # depot -> 0번째 노드 + 마지막 노드 -> depot 시간 합하기
                              time += n2n_time[0][merge_route[0]]
                              time += n2n_time[merge_route[-1]][0]

                            # time constraint 만족하는지 확인
                            if (time <= time_constraint):
                              # merge_route 추가
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

                    # depot -> i_route -> j_route -> depot의 소요 time + 노드의 service time <= time_constraint인 경우
                    time = 0
                    # service time 모두 합하기
                    for i in route_list[i_route_idx]:
                      time += service_time[i-1]
                    time += service_time[j_idx-1]

                    if (demand <= capa):
                        # i가 route의 첫 번째인 경우
                        if (i_node_idx == 0):
                          # route_list[i_route_idx] 복사
                          list = []
                          for i in route_list[i_route_idx]:
                            list.append(i)
                          list.insert(0, j_idx)
                          # node 간 이동 시간 모두 합하기
                          for i in range(len(list)-1):
                            time += n2n_time[list[i]][list[i+1]]
                          time += n2n_time[0][list[0]]
                          time += n2n_time[list[-1]][0]

                          # time constraint 만족하는지 확인
                          if (time <= time_constraint):
                            route_list[i_route_idx].insert(0, j_idx)


                        # i가 route의 마지막인 경우
                        else :
                          # route_list[i_route_idx] 복사
                          list = []
                          for i in route_list[i_route_idx]:
                            list.append(i)
                          list.append(j_idx)
                          # node 간 이동 시간 모두 합하기
                          for i in range(len(list)-1):
                            time += n2n_time[list[i]][list[i+1]]
                          time += n2n_time[0][list[0]]
                          time += n2n_time[list[-1]][0]

                          # time constraint 만족하는지 확인
                          if (time <= time_constraint):
                            route_list[i_route_idx].append(j_idx)
                
                # j_in == 1 & j가 route의 exterior인 경우
                elif (j_in == 1 and (j_node_idx == 0 or j_node_idx == len(route_list[j_route_idx])-1)):
                    # j_route와 i의 demand의 합 <= capa인 경우
                    demand = 0
                    for j in route_list[j_route_idx]:
                        demand += demand_list[j-1]
                    demand += i_demand

                    # depot -> i_route -> j_route -> depot의 소요 time + 노드의 service time <= time_constraint인 경우
                    time = 0
                    # service time 모두 합하기
                    for j in route_list[j_route_idx]:
                      time += service_time[j-1]
                    time += service_time[i_idx-1]

                    if (demand <= capa):
                        # j가 route의 첫 번째인 경우
                        if (j_node_idx == 0):
                          # route_list[i_route_idx] 복사
                          list = []
                          for i in route_list[j_route_idx]:
                            list.append(i)
                          list.insert(0, i_idx)
                          # node 간 이동 시간 모두 합하기
                          for i in range(len(list)-1):
                            time += n2n_time[list[i]][list[i+1]]
                          time += n2n_time[0][list[0]]
                          time += n2n_time[list[-1]][0]

                          # time constraint 만족하는지 확인
                          if (time <= time_constraint):
                            route_list[j_route_idx].insert(0, i_idx)



                        # j가 route의 마지막인 경우
                        else :
                          # route_list[j_route_idx] 복사
                          list = []
                          for i in route_list[j_route_idx]:
                            list.append(i)
                          list.append(i_idx)
                          # node 간 이동 시간 모두 합하기
                          for i in range(len(list)-1):
                            time += n2n_time[list[i]][list[i+1]]
                          time += n2n_time[0][list[0]]
                          time += n2n_time[list[-1]][0]

                          # time constraint 만족하는지 확인
                          if (time <= time_constraint):
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