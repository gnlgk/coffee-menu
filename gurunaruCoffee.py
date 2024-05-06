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
folder_path = "gurunaru"
filename = f"{folder_path}/menugurunaru_{current_date}.json"

# Chrome 서비스 설정
service = ChromeService(ChromeDriverManager().install())

# Chrome 옵션 설정
options = ChromeOptions()
options.add_argument('--headless')

# Chrome 시작
browser = webdriver.Chrome(service=service, options=options)
browser.get("https://www.coffine.co.kr/front/menu/coffee_list.php#contents")

WebDriverWait(browser, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "component_wrap"))
)

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 데이터 추출
coffee_data = []
tracks = soup.select("#contents > div > div > .pro_list > li")

for track in tracks:
    title = track.select_one("li > a > strong").text.strip()    
    image_url = track.select_one("li > a > img.img").get('src').replace('/uploads', 'https://www.coffine.co.kr/uploads')
    coffee_data.append({
        "title": title,
        "imageURL": image_url,
    })

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(coffee_data, f, ensure_ascii=False, indent=4)

# # 브라우저 종료
# browser.quit()
