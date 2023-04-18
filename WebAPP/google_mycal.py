import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, time, timedelta

def get_credentials():
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
    return creds

def main():
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    today_start = datetime.combine(datetime.today(), time.min).isoformat() + 'Z'
    today_end = datetime.combine(datetime.today(), time.max).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=today_start, timeMax=today_end,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('오늘 일정이 없습니다.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_time = datetime.fromisoformat(start).strftime("%m월 %d일 %H:%M")
        print(f"{start_time} - {event['summary']}")

if __name__ == '__main__':
    main()

