
import tweepy

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

# 크롤링할 키워드
keywords = ["보안", "해킹", "유출", "개인정보", "해킹"]

# 최신 트윗 100건 크롤링
for keyword in keywords:
    print(f"Keyword: {keyword}")
    tweets = api.search_tweets(q=keyword, count=100, tweet_mode="extended")
    for tweet in tweets:
        print(
            f"{tweet.user.name}, {tweet.user.screen_name}, "
            f"{tweet.created_at}, {tweet.full_text}"
        )
