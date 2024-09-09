import requests
from bs4 import BeautifulSoup
import schedule
import time
import logging
from urllib.parse import urljoin

# 로그 설정
logging.basicConfig(filename='crawler.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def crawl_and_save(start_page, end_page, output_file, keyword):
    base_url = 'https://cyphers.nexon.com/article/tip?page='
    base_article_url = 'https://cyphers.nexon.com/'  # 상대 URL을 절대 URL로 변환하기 위한 기본 URL
    
    with open(output_file, 'a', encoding='utf-8') as file:  # 'a' 모드로 파일 열기 (추가 모드)
        for page_number in range(start_page, end_page + 1):
            url = base_url + str(page_number)
            print(f'크롤링 중인 페이지: {url}')  # 페이지 크롤링 시작 출력
            logging.info(f'Crawling page: {url}')  # 로그에 페이지 번호 기록
            try:
                response = requests.get(url)
                response.raise_for_status()  # HTTP 요청 오류 체크
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')

                # 데이터 추출
                articles = soup.find_all('a', href=True, title=True)  # 'a' 태그에 'title' 속성 포함된 경우
                found_links = False
                print(f'페이지 {page_number}에서 링크 추출 중...')  # 링크 추출 중 출력
                for article in articles:
                    title = article.get('title', '').strip().lower()  # title 속성값을 소문자로 변환
                    if keyword in title:  # '탱커' 키워드가 title에 포함된 경우
                        link = article['href']
                        # 상대 URL을 절대 URL로 변환
                        if link.startswith('/'):
                            link = urljoin(base_article_url, link)
                        if link.startswith('https'):
                            file.write(f'Found URL: {link}\n')
                            found_links = True
                            print(f'찾은 URL: {link}')  # URL 찾은 경우 출력
                            logging.info(f'Found URL: {link}')  # 로그에 URL 기록

                if not found_links:
                    print(f'페이지 {page_number}에서 "{keyword}" 키워드를 포함한 링크를 찾지 못했습니다.')
                    logging.info(f'No links found with the keyword "{keyword}" in title on page {page_number}.')
                    
            except requests.RequestException as e:
                print(f'페이지 {url} 요청 중 오류 발생: {e}')
                logging.error(f'Error fetching page {url}: {e}')
            except Exception as e:
                print(f'예상치 못한 오류 발생: {e}')
                logging.error(f'An unexpected error occurred: {e}')

def main():
    # 페이지 범위와 출력 파일 설정
    keyword = input("어느것을 가져올래요 ? :")
    start_page = 1
    end_page = 200  # 예를 들어 5페이지까지 크롤링
    output_file = f'crawlerData/{keyword}.txt'
    print('크롤링 작업 시작')
    crawl_and_save(start_page, end_page, output_file, keyword)
    print('크롤링 작업 완료')

# 주기적으로 크롤링을 수행합니다.
schedule.every(2).minutes.do(main)  # 2분마다 크롤링

print('크롤러가 실행됩니다.')

while True:
    schedule.run_pending()
    time.sleep(1)
