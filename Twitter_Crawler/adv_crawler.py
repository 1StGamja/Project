import time
import psycopg2
import tweepy
from psycopg2 import sql

# DB 접속 정보
host = "localhost"
port = 5432
database = "postgres"
user = "postgres"
password = "dlQmsdl00"

# 테이블 레이아웃
# CREATE TABLE tweets (
#     id SERIAL PRIMARY KEY,
#     author_name VARCHAR(255),
#     author_screen_name VARCHAR(255),
#     created_at TIMESTAMP,
#     full_text TEXT
# );

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
cur = conn.cursor()

# 크롤링할 키워드
keywords = ["(간단 OR 조건 OR ㅈㄱ OR ㄱㄷ) (양주 OR 의정 OR 부천 OR 청라 OR 인천 OR 김포 OR 일산 OR 고양 OR 파주 OR 목동 OR 양천 OR 강서 OR 영등) -filter:links"]

# 최신 트윗 1000건 크롤링 및 DB 저장
for keyword in keywords:
    print(f"Keyword: {keyword}")
    tweets = []
    for tweet in tweepy.Cursor(api.search_tweets, q=keyword, tweet_mode="extended", lang="ko", exclude_replies=True).items(1000):
        if not tweet.retweeted and 'RT @' not in tweet.full_text:
            tweets.append(tweet)
            time.sleep(0.3)
            print(f"({len(tweets)}) Author: {tweet.user.name} / Created at: {tweet.created_at} / Tweet: {tweet.full_text}")

    for tweet in tweets:
        author_name = tweet.user.name
        author_screen_name = tweet.user.screen_name
        created_at = tweet.created_at
        full_text = tweet.full_text

        # SQL 문 작성
        insert_query = sql.SQL(
            "INSERT INTO {} ({}, {}, {}, {}) VALUES (%s, %s, %s, %s)"
        ).format(
            sql.Identifier("tweets"),
            sql.Identifier("author_name"),
            sql.Identifier("author_screen_name"),
            sql.Identifier("created_at"),
            sql.Identifier("full_text"),
        )

        # 크롤링 결과 DB 저장
        cur.execute(
            insert_query,
            (author_name, author_screen_name, created_at, full_text),
        )
        conn.commit()
