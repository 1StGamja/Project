import tweepy

# 개인 정보를 불러옵니다. 
consumer_key = 'h5NqBorp4shgZDEw1zs2ByNcQ'
consumer_secret = 'lCUa3VfRGT0pb0fV76sXiuPYzpMfyHkJK6Z7Q0XnJJroiwyks9'
access_token = '1000388956737888256-cOk32BQ2UQN2tilwVYbo4vslQciEMy'
access_token_secret = 'YDkPvLixL85MiLCPxv4ZjTBZfjSoVRUC7WciTqJMOY8AF'

# OAuth 인증 처리 
auth = tweepy.OAuthHandler(
    consumer_key, consumer_secret
)
auth.set_access_token(
    access_token, access_token_secret
)

# API 객체 생성 
api = tweepy.API(auth)

# 현재 차단한 사용자 리스트 출력 
blocked_users = api.get_blocked()
blocked_users_info = [api.get_user(user.id) for user in blocked_users]

for user in blocked_users_info:
    print(f"{user.name} (@{user.screen_name})")
