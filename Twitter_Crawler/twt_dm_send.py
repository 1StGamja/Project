import configparser
import psycopg2
import tweepy
import time
import random
import datetime

# conn.conf 파일에서 API 정보와 DB 접속 정보를 가져옴
config = configparser.ConfigParser()
config.read('/home/heewonyu/Project/Project/Twitter_Crawler/conn.conf')

# Twitter API 인증 정보를 설정함
consumer_key = config.get('twitter_api', 'consumer_key')
consumer_secret = config.get('twitter_api', 'consumer_secret')
access_token = config.get('twitter_api', 'access_token')
access_token_secret = config.get('twitter_api', 'access_token_secret')

# Tweepy를 사용하여 Twitter API에 인증함
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# PostgreSQL DB에 접속함
db_host = config.get('postgres', 'host')
db_port = config.get('postgres', 'port')
db_name = config.get('postgres', 'dbname')
db_user = config.get('postgres', 'user')
db_password = config.get('postgres', 'password')
conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
cur = conn.cursor()

# public.twt_jg_20230409 테이블에서 author_screen_name 칼럼의 모든 사용자들을 가져옴
cur.execute("SELECT DISTINCT author_screen_name FROM public.twt_jg_20230409;")
users = cur.fetchall()

# 현재 시간을 가져옴
now = datetime.datetime.now()

# 각 사용자들에게 DM 메시지를 보냄
for user in users:
    try:
        recipient_id = api.get_user(screen_name=user[0]).id
        api.send_direct_message(recipient_id=recipient_id, text="안녕하세요. 반가워요. 혹시 가능하세요?")
        print("DM sent to {}".format(user[0]))
        sleep_time = random.uniform(0.5, 3.0)
        time.sleep(sleep_time)
        # DM 전송 결과를 PostgreSQL DB에 저장함
        cur.execute("INSERT INTO public.twt_dm_send_result (user_screen_name, sent_time, message, result) VALUES (%s, %s, %s, %s);",
                    (user[0], now, "안녕하세요. 반가워요. 혹시 가능하세요?", "Success"))
        conn.commit()
    except tweepy.TweepError as e:
        print("Failed to send DM to {}: {}".format(user[0], e))
        # DM 전송 결과를 PostgreSQL DB에 저장함
        cur.execute("INSERT INTO public.twt_dm_send_result (user_screen_name, sent_time, message, result) VALUES (%s, %s, %s, %s);",
                    (user[0], now, "안녕하세요. 반가워요. 혹시 가능하세요?", "Fail"))
        conn.commit()

# DB 연결을 닫음
cur.close()
conn.close()
