import requests
from bs4 import BeautifulSoup
import json
import datetime

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = "gurunaru"
filename = f"{folder_path}/menugurunaru_{current_date}.json"

# 웹 페이지로부터 데이터 요청 및 수신
response = requests.get("https://www.coffine.co.kr/front/menu/coffee_list.php#contents")
soup = BeautifulSoup(response.text, "lxml")

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
