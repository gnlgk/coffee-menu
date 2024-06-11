from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = "mammoth"
filename = f"{folder_path}/menumammoth_{current_date}.json"

# 웹드라이브 설치
options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.get("https://mmthcoffee.com/sub/menu/list_sub.php?menuType=C")

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 데이터 추출
coffee_data = []
tracks = soup.select("#sub .sub_con .con02 .clear > li")

for track in tracks:
    # 각 커피 항목의 링크(Anchor 태그)를 찾습니다.
    coffee_link_element = track.select_one("a")
    if coffee_link_element:
        coffee_link = coffee_link_element.get('href')
        if coffee_link and "javascript:goViewB" in coffee_link:
                
                # JavaScript 함수에서 ID를 추출합니다.
                coffee_id = re.search(r'goViewB\((\d+)\)', coffee_link).group(1)
                
                # 상세 페이지로 이동하여 추가 데이터를 가져옵니다.
                browser.get(f"https://mmthcoffee.com/sub/menu/list_coffee_view.php?menuSeq={coffee_id}")
                
                # 페이지가 완전히 로드될 때까지 대기
                WebDriverWait(browser, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "box.clear"))
                )

                # 상세 페이지의 소스를 변수에 저장
                detail_page_source = browser.page_source
                detail_soup = BeautifulSoup(detail_page_source, 'html.parser')

                title = detail_soup.select_one(".info_wrap > div > .i_tit > strong").text.strip()
                titleeng = detail_soup.select_one(".info_wrap > div > .i_tit > ul > li").text.strip()
                image_url = detail_soup.select_one(".img_wrap > img").get('src').replace('/files', 'https://mmthcoffee.com/files')
                descrition = detail_soup.select_one(".info_wrap > div > .txt_area > p:nth-child(2)").text.strip()
                # nutrition_info = detail_soup.select_one(".info_wrap > div > div.i_table > dl > dt").text.strip()

                # 영양 정보 표를 가져옵니다.
                nutrition_table = detail_soup.select_one(".info_wrap > div > .i_table > table")

                # 영양 정보 표의 각 행을 추출합니다.
                nutrition_info = {}
                if nutrition_table:
                    rows = nutrition_table.select("tbody tr")
                    for row in rows:
                        cells = row.find_all("td")
                        if len(cells) >= 2:
                            key = cells[0].text.strip()
                            value = cells[1].text.strip()
                            nutrition_info[key] = value

                coffee_data.append({
                    "brand": "메머드커피",
                    "title": title,
                    "titleE": titleeng,
                    "imageURL": image_url,
                    "desction": descrition,
                    "information": nutrition_info,
                    "address": "https://mmthcoffee.com/"
                })

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(coffee_data, f, ensure_ascii=False, indent=4)

# # 브라우저 종료
# browser.quit()
