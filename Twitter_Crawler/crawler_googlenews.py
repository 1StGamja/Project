import requests
from bs4 import BeautifulSoup
import time

def get_news_articles():
    url = "https://search.naver.com/search.naver?where=news&query=%EC%86%8C%EB%A7%8C%EC%82%AC&sm=tab_opt&sort=1&photo=0&field=0&pd=4&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3A1d&is_sug_officeid=0"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_items = soup.select('ul.list_news > li')

    for item in news_items:
        press = item.select_one('a.info.press').text.strip()
        title = item.select_one('a.news_tit').text
        summary = item.select_one('div.news_dsc').text.strip()
        timestamp = item.select_one('span.info').text
        article_url = item.select_one('a.news_tit')['href']

        print("시간:", timestamp)
        print("언론사명:", press)
        print("기사 제목:", title)
        print("간략한 본문:", summary)
        print("해당 기사 URL:", article_url)
        print("-" * 80)

while True:
    get_news_articles()
    time.sleep(3600)  # 1시간마다 크롤링
