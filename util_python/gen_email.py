import random
import string

def generate_email():
    # 랜덤한 길이의 문자열을 생성합니다.
    username_length = random.randint(5, 10)
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(username_length))
    
    # 도메인을 "somansa.com"으로 고정합니다.
    domain = "somansa.com"
    
    # E-mail 주소를 생성합니다.
    email = username + '@' + domain
    
    return email

num_emails = 100000
emails = []
for i in range(num_emails):
    email = generate_email()
    emails.append(email)

# 생성된 E-mail 주소와 함께 순번을 출력합니다.
for i, email in enumerate(emails):
    print(f"{i+1}. {email}")
