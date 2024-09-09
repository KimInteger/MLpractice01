import requests
from bs4 import BeautifulSoup
import re

# 특정 키워드와 도메인
keyword = "사이퍼즈"
base_url = "https://search.naver.com"
params = {
    'where': 'blog',
    'query': keyword,
}

def fetch_page(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    # 블로그 글의 링크를 찾는 CSS 선택자를 사용합니다.
    for a_tag in soup.select('.api_txt_lines.total_tit'):
        href = a_tag.get('href')
        if href:
            urls.append(href)
    return urls

def save_urls_to_file(urls, filename):
    with open(filename, 'w') as file:
        for url in urls:
            file.write(url + '\n')

def main():
    print("Fetching page...")
    html = fetch_page(base_url, params)
    if html:
        print("Parsing page...")
        urls = parse_page(html)
        print(f"Found {len(urls)} URLs.")
        print("Saving URLs to file...")
        save_urls_to_file(urls, 'urls.txt')
        print("Finished. URLs saved to 'urls.txt'.")

if __name__ == "__main__":
    main()
