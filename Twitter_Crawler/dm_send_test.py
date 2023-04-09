import tweepy
import pytz
import time
from datetime import datetime, timedelta

# Twitter API 인증 정보
consumer_key = "h5NqBorp4shgZDEw1zs2ByNcQ"
consumer_secret = "lCUa3VfRGT0pb0fV76sXiuPYzpMfyHkJK6Z7Q0XnJJroiwyks9"
access_token = "1000388956737888256-cOk32BQ2UQN2tilwVYbo4vslQciEMy"
access_token_secret = "YDkPvLixL85MiLCPxv4ZjTBZfjSoVRUC7WciTqJMOY8AF"

# Twitter 인증
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Tweepy API 객체 생성
api = tweepy.API(auth)

# 검색할 키워드 정의
keywords = ["해킹", "보안", "정보보호", "정보보안", "개인정보", "유출"]

# 키워드를 OR로 연결한 검색 쿼리 정의
search_query = " OR ".join(keywords)

# 현재 시간에서 1시간 전 시간 계산
now = datetime.utcnow()
one_hour_ago = now - timedelta(hours=1)

# 최근 1시간 이내 트윗 검색
tweets = api.search(q=search_query, count=100, lang="ko", tweet_mode="extended", since_id=one_hour_ago.strftime("%Y-%m-%dT%H:%M:%SZ"))

# 대한민국 시간대 객체 생성
south_korea_tz = pytz.timezone("Asia/Seoul")

def send_direct_message(api, user_id, message):
    try:
#        api.send_direct_message(user_id, message)
        print(f"DM sent to {user_id}")
        time.sleep(0.5)  # DM 전송 후 0.5초 대기
    except tweepy.TweepError as e:
        print(f"Failed to send DM to {user_id}: {e}")

# DM 내용
dm_message = "안녕하세요. 좋은 정보 고맙습니다. 감사합니다."

# 크롤링한 트윗 출력
for tweet in tweets:
    # 트윗의 타임스탬프를 대한민국 현지 시간으로 변환
    local_timestamp = tweet.created_at.replace(tzinfo=pytz.UTC).astimezone(south_korea_tz)

    # 트윗이 최근 1시간 이내에 작성된 경우 출력
    if tweet.created_at >= one_hour_ago:
        print(f"작성자명 : {tweet.user.name}")
        print(f"작성자 계정 : {tweet.user.screen_name}")
        print(f"작성일시 : {local_timestamp}")
        print(f"본문내용 : {tweet.full_text}\n")

