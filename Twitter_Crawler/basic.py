import tweepy
import psycopg2
import configparser
from datetime import datetime

# db.conn 파일에서 DB 접속 정보 읽기
config = configparser.ConfigParser()
config.read('db.conn')

# DB 접속 정보 가져오기
host = config['DATABASE']['host']
port = config['DATABASE']['port']
database = config['DATABASE']['database']
user = config['DATABASE']['user']
password = config['DATABASE']['password']

# Twitter API 인증 정보
consumer_key = "d6Olnocpg0mmlcDz2Rg8R7v2H"
consumer_secret = "FHZHPwRXyivlfSIwbuvzl1fG0N7HWzciWi1mL8HBxxsbwDeUEN"
access_token = "1000388956737888256-eWjWZcxpXBytTwd0j9to9XD7SC2xOG"
access_token_secret = "ncPcuI0zdl4d8zJSyNZFp6oUPviP4s7miig584SgHfPzf"

# 키워드 설정
keywords = ["보안", "해킹", "유출", "개인정보"]

# Twitter API 인증
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# DB 연결
conn = psycopg2.connect(
    host=host,
    port=port,
    dbname=database,
    user=user,
    password=password,
)

# 커서 생성
cur = conn.cursor()

# 키워드별로 최신 트윗 100개 크롤링
for keyword in keywords:
    print(f"Keyword: {keyword}")
    tweets = api.search_tweets(q=keyword, count=100)

    for tweet in tweets:
        # 트윗 정보 추출
        username = tweet.user.name
        screen_name = tweet.user.screen_name
        created_at = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
        full_text = tweet.full_text

        # DB에 저장
        sql = f"INSERT INTO tweets (username, screen_name, created_at, full_text) VALUES ('{username}', '{screen_name}', '{created_at}', '{full_text}')"
        cur.execute(sql)

# DB에 저장
conn.commit()

# DB 연결 종료
conn.close()
