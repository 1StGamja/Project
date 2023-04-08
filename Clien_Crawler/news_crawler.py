import requests
from bs4 import BeautifulSoup

url = 'https://www.clien.net/service/board/news'

# Send an HTTP request to the URL
response = requests.get(url)
content = response.content

# Parse the HTML content
soup = BeautifulSoup(content, 'html.parser')

# Extract the article list
article_list = soup.find('div', {'class': 'list_content'})

# Extract article information
for article in article_list.find_all('div', {'class': 'list_item'}):
    title = article.find('span', {'class': 'subject_fixed'}).text.strip()
    link = 'https://www.clien.net' + article.find('a', {'class': 'list_subject'}).get('href')
    
    article_response = requests.get(link)
    article_content = article_response.content
    article_soup = BeautifulSoup(article_content, 'html.parser')
    
    content = article_soup.find('div', {'class': 'post_content'}).text.strip()
    date = article_soup.find('span', {'class': 'post_author'}).find_next('span', {'class': 'timestamp'}).text.strip()
    author = article_soup.find('span', {'class': 'nickname'}).text.strip()

    print('제목:', title)
    print('내용:', content)
    print('작성일:', date)
    print('작성자:', author)
    print('링크:', link)
    print('-------------------')
