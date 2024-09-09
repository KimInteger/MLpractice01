from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep

# ChromeDriver 자동 설치 및 실행
ser = Service(ChromeDriverManager().install())
op = Options()
op.add_argument("--headless")  # 헤드리스 모드 추가
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=ser, options=op)

# 날짜 설정
start_date = datetime.strptime("2024.9.8", "%Y.%m.%d")
end_date = datetime.strptime("2024.9.1", "%Y.%m.%d")

# 수집한 정보를 저장하는 리스트
c_gall_no_list = []
title_list = []
contents_list = []
contents_date_list = []
gall_no_list = []
reply_id = []
reply_content = []
reply_date = []

# 기본 URL
BASE = "http://gall.dcinside.com"
start_page = 151
Flag = True

while Flag:
    base_url = BASE + '/mgallery/board/lists/?id=bser&page=' + str(start_page)

    try:
        driver.get(base_url)
        sleep(3)  # WebDriverWait로 변경하는 것이 좋습니다.
    except Exception as e:
        print(f"Error loading page {base_url}: {e}")
        continue

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    article_list = soup.find('tbody')
    if article_list is None:
        continue

    article_list = article_list.find_all('tr')
    if not article_list:
        continue

    # 페이지 소스에서 날짜를 추출하고 로그에 출력
    date_text = article_list[-1].find("td", {"class": "gall_date"}).text
    print(f"Extracted date text: {date_text}")

    try:
        if len(date_text) == 7:  # Format like '2009.03'
            date_text = date_text + ".01"  # Assume the first day of the month
        print(f"Adjusted date text: {date_text}")  # Adjusted date text 출력
        contents_date = datetime.strptime(date_text, "%Y.%m.%d")
        print(f"Parsed contents_date: {contents_date}")  # Parsed 날짜 출력
    except ValueError as e:
        print(f"Date format error: {date_text}")
        print(f"Error details: {e}")  # 오류 세부사항 출력
        continue

    if start_date < contents_date:
        start_page += 1
        continue
    elif contents_date < end_date:
        print("수집을 종료합니다.")
        Flag = False
        continue

    for article in article_list:
        title_tag = article.find('a')
        title = title_tag.text if title_tag else "No Title"

        head_tag = article.find('td', {"class": "gall_subject"})
        head = head_tag.text if head_tag else "No Head"

        if head not in ['설문', 'AD', '공지']:
            gall_id_tag = article.find("td", {"class": "gall_num"})
            gall_id = gall_id_tag.text if gall_id_tag else "No ID"

            if gall_id in c_gall_no_list:
                continue

            tag = article.find('a', href=True)
            content_url = BASE + tag['href']

            try:
                driver.get(content_url)
                sleep(3)
                contents_soup = BeautifulSoup(driver.page_source, "html.parser")
                contents_div = contents_soup.find('div', {"class": "write_div"})
                contents = contents_div.text if contents_div else "No Content"
            except Exception as e:
                print(f"Error loading content {content_url}: {e}")
                continue

            c_date = "20" + article.find("td", {"class": "gall_date"}).text

            c_gall_no_list.append(gall_id)
            title_list.append(title)
            contents_list.append(contents)
            contents_date_list.append(c_date)

            reply_no = contents_soup.find_all("li", {"class": "ub-content"})
            if reply_no:
                for r in reply_no:
                    try:
                        user_name = r.find("em").text
                        user_reply_date = r.find("span", {"class": "date_time"}).text
                        user_reply = r.find("p", {"class": "usertxt ub-word"}).text

                        gall_no_list.append(gall_id)
                        reply_id.append(user_name)
                        reply_date.append(user_reply_date)
                        reply_content.append(user_reply)
                    except Exception as e:
                        print(f"Error processing reply: {e}")
                        continue

    start_page += 1

contents_df = pd.DataFrame({
    "id": c_gall_no_list,
    "title": title_list,
    "contents": contents_list,
    "date": contents_date_list
})

reply_df = pd.DataFrame({
    "id": gall_no_list,
    "reply_id": reply_id,
    "reply_content": reply_content,
    "reply_date": reply_date
})

contents_df.to_csv("contents.csv", encoding='utf8', index=False)
reply_df.to_csv("reply.csv", encoding='utf8', index=False)

print("Data collection completed and files saved.")
