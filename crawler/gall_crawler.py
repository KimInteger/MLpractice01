from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# ChromeDriver 자동 설치 및 실행
ser = Service(ChromeDriverManager().install())
op = Options()
op.add_argument("--headless")  # 헤드리스 모드 추가
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=ser, options=op)

# 날짜 설정
start_date = datetime.strptime("2024.09.08", "%Y.%m.%d")
end_date = datetime.strptime("2024.09.01", "%Y.%m.%d")

# 수집한 정보를 저장하는 리스트
c_gall_no_list = []
title_list = []
contents_list = []
contents_date_list = []
gall_no_list = []
reply_id = []
reply_content = []
reply_date = []

# 기존에 저장된 데이터를 불러오는 함수
def load_existing_data(contents_file="contents.csv", reply_file="reply.csv"):
    try:
        contents_df = pd.read_csv(contents_file, encoding='utf8')
        reply_df = pd.read_csv(reply_file, encoding='utf8')
        return contents_df, reply_df
    except FileNotFoundError:
        return pd.DataFrame(), pd.DataFrame()

# 기존 데이터를 불러오기
contents_df, reply_df = load_existing_data()

# 기존 데이터에서 id 리스트를 가져옴
if not contents_df.empty:
    c_gall_no_list = contents_df['id'].tolist()
if not reply_df.empty:
    gall_no_list = reply_df['id'].tolist()

# 기본 URL
BASE = "http://gall.dcinside.com"
start_page = 200
Flag = True

while Flag:
    base_url = BASE + '/mgallery/board/lists/?id=bser&page=' + str(start_page)

    try:
        driver.get(base_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'tbody'))
        )
    except Exception as e:
        print(f"Error loading page {base_url}: {e}")
        start_page += 1
        continue

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    article_list = soup.find('tbody')
    if article_list is None:
        start_page += 1
        continue

    article_list = article_list.find_all('tr')
    if not article_list:
        start_page += 1
        continue

    for article in article_list:
        date_td = article.find("td", {"class": "gall_date"})
        if date_td:
            date_text = date_td.get_text(strip=True)
            print(f"Extracted date text: {date_text}")

            try:
                # 현재 연도를 자동으로 추가하여 날짜를 처리
                current_year = datetime.now().year
                if len(date_text) == 5:  # Format like '09.08'
                    date_text = f"{current_year}.{date_text}"
                contents_date = datetime.strptime(date_text, "%Y.%m.%d")
            except ValueError:
                print(f"Date format error: {date_text}")
                continue

            if start_date < contents_date:
                start_page += 1
                continue
            elif contents_date < end_date:
                print("수집을 종료합니다.")
                Flag = False
                break

            title_tag = article.find('a')
            title = title_tag.get_text(strip=True) if title_tag else "No Title"

            head_tag = article.find('td', {"class": "gall_subject"})
            head = head_tag.get_text(strip=True) if head_tag else "No Head"

            if head not in ['설문', 'AD', '공지']:
                gall_id_tag = article.find("td", {"class": "gall_num"})
                gall_id = gall_id_tag.get_text(strip=True) if gall_id_tag else "No ID"

                if gall_id in c_gall_no_list:
                    continue

                tag = article.find('a', href=True)
                content_url = BASE + tag['href']

                try:
                    driver.get(content_url)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.write_div'))
                    )
                    contents_soup = BeautifulSoup(driver.page_source, "html.parser")
                    contents_div = contents_soup.find('div', {"class": "write_div"})
                    contents = contents_div.get_text(strip=True) if contents_div else "No Content"
                except Exception as e:
                    print(f"Error loading content {content_url}: {e}")
                    continue

                c_date = "20" + date_text

                # 데이터를 리스트에 추가
                c_gall_no_list.append(gall_id)
                title_list.append(title)
                contents_list.append(contents)
                contents_date_list.append(c_date)

                # 댓글 처리
                reply_no = contents_soup.find_all("li", {"class": "ub-content"})
                if reply_no:
                    for r in reply_no:
                        try:
                            user_name = r.find("em").get_text(strip=True) if r.find("em") else "No User"
                            user_reply_date = r.find("span", {"class": "date_time"}).get_text(strip=True) if r.find("span", {"class": "date_time"}) else "No Date"
                            user_reply = r.find("p", {"class": "usertxt ub-word"}).get_text(strip=True) if r.find("p", {"class": "usertxt ub-word"}) else "No Reply"

                            gall_no_list.append(gall_id)
                            reply_id.append(user_name)
                            reply_date.append(user_reply_date)
                            reply_content.append(user_reply)
                        except Exception as e:
                            print(f"Error processing reply: {e}")
                            continue

    # 크롤링한 데이터를 주기적으로 저장
    contents_temp_df = pd.DataFrame({
        "id": c_gall_no_list,
        "title": title_list,
        "contents": contents_list,
        "date": contents_date_list
    })

    reply_temp_df = pd.DataFrame({
        "id": gall_no_list,
        "reply_id": reply_id,
        "reply_content": reply_content,
        "reply_date": reply_date
    })

    # 기존 데이터와 병합 후 저장
    contents_df = pd.concat([contents_df, contents_temp_df]).drop_duplicates(subset='id')
    reply_df = pd.concat([reply_df, reply_temp_df]).drop_duplicates(subset=['id', 'reply_id'])

    # CSV 파일로 저장
    contents_df.to_csv("contents.csv", encoding='utf8', index=False)
    reply_df.to_csv("reply.csv", encoding='utf8', index=False)

    # 다음 페이지로 넘어가기
    start_page += 1

print("Data collection completed and files saved.")
