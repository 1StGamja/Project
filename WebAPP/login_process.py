import requests
from bs4 import BeautifulSoup

# 로그인할 URL
login_url = 'https://goldmine.somansa.com/login/'

# 로그인 정보
payload = {
    'username': 'yuheewon',
    'password': 'ehtjrhks00!',
}

# 세션 생성
with requests.Session() as session:
    # 로그인 페이지 가져오기
    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.content, 'html.parser')
    csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'})

    # CSRF 토큰이 존재하는지 확인
    if csrf is not None:
        csrf_value = csrf.get('value')

        # 로그인 정보에 CSRF 토큰 추가
        payload['csrfmiddlewaretoken'] = csrf_value

        # 로그인 요청
        response = session.post(login_url, data=payload)

        # 로그인 결과 확인
        print(response.content)
    else:
        print('CSRF 토큰을 찾을 수 없습니다.')
