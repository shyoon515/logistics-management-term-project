from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

import pandas as pd
import random

XPATHS = {
    'search' : '//*[@id="__next"]/div/div/div/div[2]/div/svg/path',
    'magnify' : '//*[@id="__next"]/div/div/div/div/div[2]/div[1]',
    'search_input' : '//input[@placeholder="기기명, 주소, 지역 등 검색"]'
}
URL = 'https://www.superbin.co.kr'

def crawl_superbin(search_area_keywords):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # 맵 사이트 접속 및 
    driver.get(URL)
    time.sleep(random.uniform(0.5, 2))
    driver.find_element(By.XPATH, value='//*[@id="__next"]/header/div/div[2]').click()
    time.sleep(random.uniform(0.5, 2))
    driver.find_element(By.XPATH, value='//*[@id="modal"]/div/div[2]/ul/li[2]').click()
    time.sleep(random.uniform(0.5, 2))

    # 창 최대화
    driver.maximize_window()

    driver.refresh()
    time.sleep(random.uniform(3, 4))

    while(1):
        try:
            # 입력 필드 찾기 (placeholder 속성 사용)
            search_box = driver.find_element(By.XPATH, XPATHS['search_input'])
            break
        except:
            driver.refresh()
            time.sleep(random.uniform(3, 4))

    # 입력 필드가 비활성화되어 있다면 활성화하는 코드 필요
    # 비활성화된 요소를 활성화하는 방식은 페이지마다 다를 수 있음 (여기서는 간단히 JavaScript 사용 예시)
    driver.execute_script("arguments[0].disabled = false;", search_box)

    addresses = []
    capacities = []

    for search_text in search_area_keywords:
        # 입력필드 제거 후 검색어 입력
        search_box.clear()
        search_box.send_keys(search_text)
        search_box.send_keys(Keys.RETURN)

        time.sleep(random.uniform(0.5, 2))

        # 모든 리스트 요소 찾기
        list_items = driver.find_elements(By.CSS_SELECTOR, 'ul.list li')

        # 각 리스트를 클릭 후 상세 정보 표시
        for item in list_items:
            # 리스트 요소 클릭
            item.click()
            time.sleep(random.uniform(0.5, 0.7))
            # BeautifulSoup을 사용하여 HTML 파싱
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 필요한 정보 추출
            elements_containing_text = soup.find_all(text=lambda text: "1인 1일" in text)
            try:
                item_limit = elements_containing_text[0]
            except:
                item_limit = "Unspecified"
            capacities.append(item_limit)

            time.sleep(random.uniform(0.5, 2))

        # 파싱
        soup = BeautifulSoup(html, 'html.parser')
        address_list = []
        address_elements = soup.select('ul.list li div.container p.address')

        for address_element in address_elements:
            address_list.append(address_element.text)
        addresses.extend(address_list)

    driver.quit()
    return pd.DataFrame({"Address": addresses, "Capacity": capacities})