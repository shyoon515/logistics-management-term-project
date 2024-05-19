import requests
import pandas as pd
import json

# JSON 파일에서 API 키 불러오기
def load_api_keys(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config['client_id'], config['client_secret']

def get_coordinates(address, client_id, client_secret):
    """
    address에 주소지를 입력, naver map의 client_id와 client_secret을 넣으면 해당 주소지의 coordinate을 반환
    """
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }
    params = {"query": address}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['addresses']:
            latitude = float(data['addresses'][0]['y'])
            longitude = float(data['addresses'][0]['x'])
            return latitude, longitude
        else:
            return 0.0, 0.0
    else:
        print(f"오류 발생 - 상태 코드: {response.status_code}, 응답: {response.text}")
        return 0.0, 0.0

def process_address(df, client_id, client_secret):
    """
    'Address' column에 대하여 get_coordinates를 진행하여 새로운 column을 생성
    """
    df[['latitude', 'longitude']] = df.apply(lambda row: get_coordinates(row['Address'], client_id, client_secret), axis=1).apply(pd.Series)