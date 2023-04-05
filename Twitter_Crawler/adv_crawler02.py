import time
import psycopg2
import tweepy
from psycopg2 import sql
from datetime import datetime, timedelta
import pytz

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

kst = pytz.timezone('Asia/Seoul')  # 대한민국 시간대

# 오늘 날짜를 기준으로 'TW_년월일' 형식의 테이블 이름 생성
today = datetime.now(kst)
table_name = f"TW_{today.strftime('%Y%m%d')}"

# 테이블 존재 여부 확인 및 없으면 생성
table_check_query = f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}')"
cur.execute(table_check_query)
table_exists = cur.fetchone()[0]

if not table_exists:
    table_create_query = sql.SQL(
        """
        CREATE TABLE {} (
            id SERIAL PRIMARY KEY,
            author_name VARCHAR(255),
            author_screen_name VARCHAR(255),
            created_at TIMESTAMP,
            full_text TEXT
        );
        """
    ).format(sql.Identifier(table_name))
    cur.execute(table_create_query)
    conn.commit()

# 최신 트윗 1000건 크롤링 및 DB 저장
for keyword in keywords:
    print(f"Keyword: {keyword}")
    tweets = []
    try:
        for tweet in tweepy.Cursor(api.search_tweets, q=keyword, tweet_mode="extended", lang="ko").items(1000):
            # 현재 시간 기준 10분 이내의 트윗인지 확인
            current_time = datetime.now(pytz.utc)
            tweet_age = current_time - tweet.created_at
            if tweet_age <= timedelta(minutes=10):
                if not tweet.retweeted and 'RT @' not in tweet.full_text:
                    # 대한민국 시간대로 변환
                    created_at_kst = tweet.created_at.astimezone(kst)
                    tweets.append(tweet)
                    time.sleep(0.3)
                    print(f"({len(tweets)}) Author: {tweet.user.name} / Created at: {created_at_kst} / Tweet: {tweet.full_text}")
            else:
                break
    except tweepy.error.TweepError as e:
        print(f"Error: {e}")
        continue


# 데이터베이스에 저장하는 부분
for tweet in tweets:
    author_name = tweet.user.name
    author_screen_name = tweet.user.screen_name
    created_at = tweet.created_at.astimezone(kst)  # 대한민국 시간대로 변환
    full_text = tweet.full_text

    # SQL 문 작성
    insert_query = sql.SQL(
        "INSERT INTO {} ({}, {}, {}, {}) VALUES (%s, %s, %s, %s)"
    ).format(
        sql.Identifier(table_name),  # 수정된 부분
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
