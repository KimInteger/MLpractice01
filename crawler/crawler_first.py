import requests
import json
from bs4 import BeautifulSoup

url = "https://www.naver.com"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

keyword = "news"

data = []
for elemnets in soup.find_all(text=True):
    if keyword.lower() in elemnets.lower():
        data.append({"content" : elemnets})
        
links = soup.find_all('a', href=True)
for link in links:
    if keyword.lower() in link.get_text().lower():
        data.append({"content" : link["href"]})
        
with open('output.json','w') as f:
    json.dump(data, f, indent=4)
    
