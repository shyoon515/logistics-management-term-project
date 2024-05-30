import json

def get_cost_time(index1, index2, route_type, json_path, toll_include=True):
    """
    index1, index2와 route_type을 지정해주면 json 파일을 파싱하여 비용을 반환
    """
    # 출발지와 도착지가 같은 경우 0 반환
    if index1 == index2:
        return 0
    else:
        from_idx = min(index1, index2)
        to_idx = max(index1, index2)

        # 마지막에 /가 없으면 붙이기
        if json_path[-1] != '/':
            json_path += '/'
        json_path = json_path + f'route_{from_idx}_{to_idx}.json'
        
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
        except:
            print(f"{json_path} 파일을 읽을 수 없음")
            raise ValueError()
        
        try:
            tollFare = 0 if toll_include else data['route'][route_type][0]['summary']['tollFare']
            feulPrice = data['route'][route_type][0]['summary']['fuelPrice']
            time = data['route'][route_type][0]['summary']['duration']
            return tollFare+feulPrice, time
        except:
            print(f"{json_path} 파일의 tollFare와 fuelPrice 파싱 불가")
            raise ValueError()