import requests
from bs4 import BeautifulSoup

url = 'https://www.clien.net/service/board/news'

response = requests.get(url)
content = response.content

soup = BeautifulSoup(content, 'html.parser')
article_list = soup.find('div', {'class': 'list_content'})

for article in article_list.find_all('div', {'class': 'list_item'}):
    title = article.find('span', {'class': 'subject_fixed'}).text.strip()
    link = 'https://www.clien.net' + article.find('a', {'class': 'list_subject'}).get('href')
    
    article_response = requests.get(link)
    article_content = article_response.content
    article_soup = BeautifulSoup(article_content, 'html.parser')
    
    content = article_soup.find('div', {'class': 'post_content'}).text.strip()
    
    post_author = article_soup.find('span', {'class': 'post_author'})
    if post_author:
        date = post_author.find_next('span', {'class': 'timestamp'}).text.strip() if post_author.find_next('span', {'class': 'timestamp'}) else 'N/A'
    else:
        date = 'N/A'
    
    author = article_soup.find('span', {'class': 'nickname'}).text.strip()

    print('제목:', title)
    print('내용:', content)
    print('작성일:', date)
    print('작성자:', author)
    print('링크:', link)
    print('-------------------')
