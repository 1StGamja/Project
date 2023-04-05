
# public.tw_20230405

import psycopg2
import tweepy
import time
from tweepy.errors import TweepError

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

# PostgreSQL 데이터베이스 연결
conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)

# Tweepy 인증 설정
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Tweepy API 객체 생성
api = tweepy.API(auth)

# DM을 발송할 계정의 스크린 네임 목록 가져오기
cur = conn.cursor()
cur.execute("SELECT DISTINCT author_screen_name FROM public.tw_20230405")
screen_names = cur.fetchall()
cur.close()

# 각 계정에게 DM 발송
for screen_name in screen_names:
    try:
        recipient_id = api.get_user(screen_name=screen_name[0]).id
        api.send_direct_message(recipient_id=recipient_id, text="나랑 ㅈㄱ이나 ㄱㄷ으로 빠르게 볼래요?")
        print(f"DM sent to {screen_name[0]}")
        time.sleep(0.5)
    except TweepError as e:
        print(f"Failed to send DM to {screen_name[0]}: {str(e)}")

# PostgreSQL 연결 종료
conn.close()
