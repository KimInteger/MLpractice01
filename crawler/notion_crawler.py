import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

NOTION_API_KEY = os.getenv("NOTION_SECREAT_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")


# API 요청을 위한 헤더 설정
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"  # 최신 버전
}

# 데이터베이스 쿼리 요청을 위한 엔드포인트 URL
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

# API 요청 실행
response = requests.post(url, headers=headers)

# 요청이 성공했는지 확인
if response.status_code == 200:
    data = response.json()  # 응답을 JSON으로 파싱

    # 데이터를 JSON 파일로 저장
    with open("notion_tool_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("데이터베이스 데이터가 notion_database_data.json으로 저장되었습니다.")
else:
    print(f"데이터를 가져오지 못했습니다: {response.status_code}, {response.text}")
