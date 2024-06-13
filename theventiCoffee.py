from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = "theventi"
filename = f"{folder_path}/menutheventi_{current_date}.json"

# 웹드라이브 설치
options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.get("https://www.theventi.co.kr/new2022/menu/all.html?mode=2")

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 데이터 추출
coffee_data = []
tracks = soup.select("#contents > div > div > .menu_list > ul > li")

for track in tracks:
    # 각 커피 항목의 링크(Anchor 태그)를 찾습니다.
    coffee_link_element = track.select_one("a")
    if coffee_link_element:
        coffee_link = coffee_link_element.get('href')
    
        # 상세 페이지로 이동하여 추가 데이터를 가져옵니다.
        browser.get(f"https://www.theventi.co.kr/new2022/menu/{coffee_link}")
            
        # 페이지가 완전히 로드될 때까지 대기
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "menu_desc_wrap"))
        )

        # 상세 페이지의 소스를 변수에 저장
        detail_page_source = browser.page_source
        detail_soup = BeautifulSoup(detail_page_source, 'html.parser')

        title = detail_soup.select_one(".txt_bx > p > span:nth-child(3)").text.strip()
        titleeng = detail_soup.select_one(".img_bx > img").text.strip()
        image_url = detail_soup.select_one(".img_bx > img").get('src')
        descrition = detail_soup.select_one(".txt_bx > .txt.scroll-con-y").text.strip()


        # 영양 정보 표를 가져옵니다.
        nutrition_table = detail_soup.select_one(".txt_bx > .menu-ingredient > table")
        # print("Nutrition Table:", nutrition_table)  # nutrition_table이 제대로 선택되었는지 확인
        if nutrition_table:
            nutrition_info = {}
            rows = nutrition_table.select("tr")
            # print("Rows:", rows)  # 행이 제대로 선택되었는지 확인
            
            # 첫 번째 행은 키로 사용하고, 나머지 행은 값으로 사용합니다.
            keys_row = rows[0]
            values_row = rows[1]
            keys = keys_row.select("th")
            values = values_row.select("td")

            for key_elem, value_elem in zip(keys, values):
                key = key_elem.text.strip()
                value = value_elem.text.strip()
                # print("Key:", key, "Value:", value)  # key와 value가 제대로 가져와지는지 확인
                nutrition_info[key] = value

        coffee_data.append({
            "brand": "더벤티",
            "title": title,
            "titleE": titleeng,
            "imageURL": image_url,
            "desction": descrition,
            "information": nutrition_info,
            "address": "https://mmthcoffee.com/"
        })

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(theventi_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()
