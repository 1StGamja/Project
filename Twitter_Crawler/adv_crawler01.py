import time
import psycopg2
import tweepy
from psycopg2 import sql
from datetime import datetime

# DB 접속 정보
host = "localhost"
port = 5432
database = "postgres"
user = "postgres"
password = "dlQmsdl00"

# Twitter API 인증 정보
consumer_key = "d6Olnocpg0mmlcDz2Rg8R7v2H"
consumer_secret = "FHZHPwRXyivlfSIwbuvzl1fG0N7HWzciWi1mL8HBxxsbwDeUEN"
access_token = "1000388956737888256-eWjWZcxpXBytTwd0j9to9XD7SC2xOG"
access_token_secret = "ncPcuI0zdl4d8zJSyNZFp6oUPviP4s7miig584SgHfPzf"

# OAuth 인증
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

# API 객체 생성
api = tweepy.API(auth)

# DB 연결
conn = psycopg2.connect(
    host=host, port=port, database=database, user=user, password=password
)
# autocommit 설정 추가
conn.autocommit = True
cur = conn.cursor()


# 테이블 이름
table_name = "tw_" + datetime.today().strftime("%Y%m%d")

# 테이블 생성 SQL 문
create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name.lower()} (
        id SERIAL PRIMARY KEY,
        author_name VARCHAR(255),
        author_screen_name VARCHAR(255),
        created_at TIMESTAMP,
        full_text TEXT
    );
"""

# 테이블 생성
try:
    cur.execute(create_table_query)
    conn.commit()
    print(f"Table {table_name} created successfully!")
except Exception as e:
    print(f"Error creating table {table_name}: {e}")
    cur.close()
    conn.close()
    exit()


# 크롤링할 키워드
keywords = ["(간단 OR 조건 OR ㅈㄱ OR ㄱㄷ) (양주 OR 의정 OR 부천 OR 청라 OR 인천 OR 김포 OR 일산 OR 고양 OR 파주 OR 목동 OR 양천 OR 강서 OR 영등) -filter:links"]

# 최신 트윗 1000건 크롤링 및 DB 저장
for keyword in keywords:
    print(f"Keyword: {keyword}")
    tweets = []
    try:
        current_time = datetime.now()  # 현재 시간
        for tweet in tweepy.Cursor(api.search_tweets, q=keyword, tweet_mode="extended", lang="ko").items(1000):
            if not tweet.retweeted and 'RT @' not in tweet.full_text:
                if 'withheld' in tweet.__dict__ and tweet.__dict__['withheld'] is True:
                    continue
                tweet_time = tweet.created_at  # 트윗 작성 시간
                time_diff = (current_time - tweet_time).total_seconds() / 60  # 시간 차이 (분 단위)
                if time_diff <= 30:  # 30분 이내의 트윗만 저장
                    tweets.append(tweet)
                    time.sleep(0.3)
                    print(f"({len(tweets)}) Author: {tweet.user.name} / Created at: {tweet.created_at} / Tweet: {tweet.full_text}")

    except tweepy.TweepError as e:
        print(f"Error: {e}")
        continue

    for tweet in tweets:
        author_name = tweet.user.name
        author_screen_name = tweet.user.screen_name
        created_at = tweet.created_at
        full_text = tweet.full_text

        # SQL 문 작성
        insert_query = sql.SQL(
            "INSERT INTO {} ({}, {}, {}, {}) VALUES (%s, %s, %s, %s)"
        ).format(
            sql.Identifier(table_name),
            sql.Identifier("author_name"),
            sql.Identifier("author_screen_name"),
            sql.Identifier("created_at"),
            sql.Identifier("full_text"),
        )

        # 크롤링 결과 DB 저장
        try:
            cur.execute(insert_query, (author_name, author_screen_name, created_at, full_text))
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            continue


# DB 연결 해제
cur.close()
conn.close()
