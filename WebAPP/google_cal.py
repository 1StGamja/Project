import datetime
import pickle
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


# 구글 캘린더 API 사용을 위한 인증
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            '/home/heewonyu/client_secret_275638909238-kb77uk1u5jsr65rj7skq2fur32fdktkn.apps.googleusercontent.com.json', ['https://www.googleapis.com/auth/calendar.readonly'])
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

# 구글 캘린더 API 클라이언트 생성
service = build('calendar', 'v3', credentials=creds)

# 캘린더 이벤트 목록 가져오기
now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
events_result = service.events().list(calendarId='primary', timeMin=now,
                                      maxResults=10, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

# 이벤트 목록을 파일에 저장
with open('/tmp/google_cal.txt', 'w') as f:
    if not events:
        f.write('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        summary = event['summary']
        f.write(f"{start} / {end} / {summary}\n")
