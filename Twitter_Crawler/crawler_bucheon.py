import tweepy
import pytz
import psycopg2
from datetime import datetime, timedelta
import configparser

# Read the configuration file
config = configparser.ConfigParser()
config.read('/home/heewonyu/Project/Project/Twitter_Crawler/conn.conf')

# Twitter API authentication information
consumer_key = config.get('twitter_api', 'consumer_key')
consumer_secret = config.get('twitter_api', 'consumer_secret')
access_token = config.get('twitter_api', 'access_token')
access_token_secret = config.get('twitter_api', 'access_token_secret')

# PostgreSQL DB connection information
DB_HOST = config.get('postgres', 'host')
DB_PORT = config.getint('postgres', 'port')  # Use getint() to read an integer value
DB_NAME = config.get('postgres', 'dbname')
DB_USER = config.get('postgres', 'user')
DB_PASS = config.get('postgres', 'password')

# Twitter 인증
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Tweepy API 객체 생성
api = tweepy.API(auth)

# 검색할 키워드 정의
keywords1 = ["간단", "조건", "ㅈㄱ", "ㄱㄷ", "미자", "가출"]
keywords2 = ["부천", "부평", "시흥", "광명", "안산", "시화"]


# 키워드를 OR로 연결한 검색 쿼리 정의
search_query = "(" + " OR ".join(keywords1) + ") AND (" + " OR ".join(keywords2) + ") -filter:retweets -filter:mentions -filter:links -filter:남자 -filter:출장 -filter:여성분 -filter:남고딩"


# 현재 시간에서 1시간 전 시간 계산동
now = datetime.utcnow()
one_hour_ago = now - timedelta(hours=1)

# 최근 1시간 이내 트윗 검색
tweets = api.search(q=search_query, count=100, lang="ko", tweet_mode="extended", since_id=one_hour_ago.strftime("%Y-%m-%dT%H:%M:%SZ"))

# 대한민국 시간대 객체 생성
south_korea_tz = pytz.timezone("Asia/Seoul")

# PostgreSQL에 연결
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = conn.cursor()  # 이 줄을 추가합니다.

# PostgreSQL 쿼리를 실행하는 함수
def execute_query(query, data=None):
    global cur  # 이 줄을 추가합니다.
    if data:
        cur.execute(query, data)
    else:
        cur.execute(query)
    conn.commit()


# 테이블 생성 (존재하지 않는 경우에만)
table_name = f"twt_jogeon_{datetime.now().strftime('%Y%m%d')}"
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id SERIAL PRIMARY KEY,
    author_name VARCHAR(255),
    author_screen_name VARCHAR(255),
    created_at TIMESTAMP,
    full_text TEXT,
    keyword VARCHAR(255)
);
"""


execute_query(create_table_query)

# 크롤링한 트윗을 PostgreSQL에 저장하는 함수
def save_tweet_to_db(tweet):
    korean_created_at = tweet.created_at.replace(tzinfo=pytz.utc).astimezone(south_korea_tz)

    check_query = f"""
    SELECT COUNT(*) FROM {table_name}
    WHERE author_screen_name = %s AND full_text = %s
    """
    execute_query(check_query, (tweet.user.screen_name, tweet.full_text))
    count = cur.fetchone()[0]

    if count == 0:
        insert_query = f"""
        INSERT INTO {table_name} (author_name, author_screen_name, created_at, full_text, keyword)
        VALUES (%s, %s, %s, %s, %s)
        """
        execute_query(insert_query, (tweet.user.name, tweet.user.screen_name, korean_created_at, tweet.full_text, keywords2[0]))


# 크롤링한 트윗 출력 및 저장
for tweet in tweets:
    # 트윗의 타임스탬프를 대한민국 현지 시간으로 변환
    korean_created_at = tweet.created_at.replace(tzinfo=pytz.utc).astimezone(south_korea_tz)

    # 트윗이 최근 1시간 이내에 작성된 경우 출력
    if tweet.created_at >= one_hour_ago:
        print(f"작성자명: {tweet.user.name}")
        print(f"작성자 계정: @{tweet.user.screen_name}")
        print(f"작성일시: {korean_created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"본문내용: {tweet.full_text}\n")

        # 트윗을 PostgreSQL에 저장
        save_tweet_to_db(tweet)

# 연결 종료
conn.close()



