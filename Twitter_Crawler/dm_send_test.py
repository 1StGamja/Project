
import tweepy

# Twitter API 인증 정보
consumer_key = "d6Olnocpg0mmlcDz2Rg8R7v2H"
consumer_secret = "FHZHPwRXyivlfSIwbuvzl1fG0N7HWzciWi1mL8HBxxsbwDeUEN"
access_token = "1000388956737888256-eWjWZcxpXBytTwd0j9to9XD7SC2xOG"
access_token_secret = "ncPcuI0zdl4d8zJSyNZFp6oUPviP4s7miig584SgHfPzf"

# Twitter API 인증
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret)

# DM 받을 사람 ID
recipient_id = "yunarsis"

# 발송할 DM 내용
text = "나랑 ㅈㄱ이나 ㄱㄷ으로 빠르게 볼래요?"

# DM 발송
api = tweepy.API(auth)
dm = api.send_direct_message(recipient_id, text)

# 결과 확인
if dm.id is not None:
    print("DM 발송 성공!")
else:
    print("DM 발송 실패 :(")
