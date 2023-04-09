import tweepy

# Twitter API authentication information
consumer_key = "h5NqBorp4shgZDEw1zs2ByNcQ"
consumer_secret = "lCUa3VfRGT0pb0fV76sXiuPYzpMfyHkJK6Z7Q0XnJJroiwyks9"
access_token = "1000388956737888256-cOk32BQ2UQN2tilwVYbo4vslQciEMy"
access_token_secret = "YDkPvLixL85MiLCPxv4ZjTBZfjSoVRUC7WciTqJMOY8AF"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create a Tweepy API object
api = tweepy.API(auth)

# Define the keywords
keywords = ["해킹", "보안", "정보보호", "정보보안", "개인정보", "유출"]

# Define a search query that ORs the keywords
search_query = " OR ".join(keywords)

# Perform the search
tweets = api.search(q=search_query, count=100, lang="ko", tweet_mode="extended")

# Print the crawled tweets
for tweet in tweets:
    print(f"작성자명 : {tweet.user.name}")
    print(f"작성자 계정 : {tweet.user.screen_name}")
    print(f"작성일시 : {tweet.created_at}")
    print(f"본문내용 : {tweet.full_text}\n")
