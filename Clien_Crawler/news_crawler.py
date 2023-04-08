import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime

# PostgreSQL 데이터베이스 연결 설정
db_host = 'localhost'
db_user = 'postgres'
db_password = 'dlQmsdl00'
db_port = '5432'
db_name = 'postgres'

# 현재 날짜 가져오기
now = datetime.now()
table_name = f"clien_{now.strftime('%Y%m%d')}"

# 데이터베이스 연결
conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password, port=db_port)
cursor = conn.cursor()

# 테이블 생성 (테이블이 없으면)
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    date TEXT NOT NULL,
    author TEXT NOT NULL,
    link TEXT NOT NULL
);
"""

cursor.execute(create_table_query)
conn.commit()

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
        date_elem = post_author.find_next('span', {'class': 'timestamp'})
        if date_elem:
            date_str = date_elem.text.strip()
            if ':' in date_str:  # 시:분 형식
                date = now.strftime('%Y-%m-%d') + ' ' + date_str
            else:  # 월-일 형식
                year = now.year
                month, day = map(int, date_str.split('-'))
                date = datetime(year, month, day).strftime('%Y-%m-%d')
        else:
            date = 'N/A'
    else:
        date = 'N/A'

    author = article_soup.find('span', {'class': 'nickname'}).text.strip()

    # 데이터베이스에 중복되는 제목이 없는 경우에만 저장
    select_query = f"SELECT title FROM {table_name} WHERE title = %s"
    cursor.execute(select_query, (title,))
    if cursor.fetchone() is None:
        print(f"title: {title}")
        print(f"content: {content}")
        print(f"date: {'작성일: ' if date != 'N/A' else ''}{date if date != 'N/A' else 'N/A'}")
        print(f"author: {author}")
        print(f"link: {link}\n")

        # 데이터베이스에 크롤링 결과 저장
        insert_query = f"""
        INSERT INTO {table_name} (title, content, date, author, link)
        VALUES (%s, %s, %s, %s, %s);
        """

        cursor.execute(insert_query, (title, content, date, author, link))
        conn.commit()
    else:
        print(f"Skipping duplicate article with title: {title}\n")

# 데이터베이스 연결 종료
cursor.close()
conn.close()

