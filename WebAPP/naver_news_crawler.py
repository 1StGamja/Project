import requests
from bs4 import BeautifulSoup

url = 'https://search.naver.com/search.naver?where=news&query=chatgpt&sm=tab_opt&sort=1&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall&is_sug_officeid=0'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

articles = soup.select('.list_news > li')

for i in range(0, 100, 10):
    print(f"{'='*50} {i//10+1}페이지 {'='*50}")
    for article in articles[i:i+10]:
        press = article.select_one('.info_group > a').text.strip()
        date = article.select_one('.info_group > span').text.strip()
        title = article.select_one('a.news_tit').text.strip()
        content_url = article.select_one('a.news_tit')['href']
        content_response = requests.get(content_url)
        content_soup = BeautifulSoup(content_response.text, 'html.parser')
        content_element = content_soup.select('#articleBodyContents')
        if content_element:
            content = content_element[0].text.replace('\n', '').replace('\t', '').strip()
        else:
            content = ''
        print(f"언론사: {press}")
        print(f"생성시간: {date}")
        print(f"뉴스 제목: {title}")
        print(f"뉴스 내용: {content}")
        print()
