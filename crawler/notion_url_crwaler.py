from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from convert_json_to_python import json_to_python
import json
import time

# WebDriver 설정
def setup_driver():
    ser = Service(ChromeDriverManager().install())
    op = Options()
    op.add_argument("--headless")  # 헤드리스 모드
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=ser, options=op)

# URL에서 데이터 크롤링
def crawl_url(url, driver):
    driver.get(url)
    time.sleep(3)  # 페이지 로드 대기
    try:
        # 'notion-page-content' 클래스의 내용을 가져옴
        page_content = driver.find_element(By.CLASS_NAME, 'notion-page-content').text
        return page_content
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        return None

# JSON 데이터를 순회하며 'url'이 있는 객체에 대해 크롤링 수행
def process_data_and_crawl(data):
    driver = setup_driver()
    with open('./crawlerData/작업일지.md', 'w', encoding='utf-8') as file:
        # 'results' 필드에 있는 리스트 안의 객체 순회
        results = data.get('results', [])
        for item in results:
            if 'url' in item:
                url = item['url']
                try:
                    print(f"크롤링 중: {url}")
                    content = crawl_url(url, driver)
                    if content:
                        file.write(f"URL: {url}\n")
                        file.write(content + '\n\n')
                except Exception as e:
                    print(f"크롤링 중 오류 발생: {e}")
            else:
                print("해당 객체에는 'url' 키가 없습니다.")
    driver.quit()

# 메인 실행
if __name__ == "__main__":
    data = json_to_python("notion_tool_data.json")
    if data:
        process_data_and_crawl(data)
