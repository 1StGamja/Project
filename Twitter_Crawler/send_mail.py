import psycopg2
import time
import smtplib
from email.mime.text import MIMEText
import configparser

config = configparser.ConfigParser()
config.read('/home/heewonyu/Project/Project/Twitter_Crawler/conn.conf')

# PostgreSQL DB 접속 정보
DB_HOST = config.get('postgres', 'host')
DB_PORT = config.getint('postgres', 'port')
DB_NAME = config.get('postgres', 'dbname')
DB_USER = config.get('postgres', 'user')
DB_PASS = config.get('postgres', 'password')

# 이메일 설정
SMTP_SERVER = config.get('GMAIL', 'SMTP_SERVER')
SMTP_PORT = config.getint('GMAIL', 'SMTP_PORT')
EMAIL_USER = config.get('GMAIL', 'EMAIL_USER')
EMAIL_PASS = config.get('GMAIL', 'EMAIL_PASS')
EMAIL_FROM = config.get('GMAIL', 'EMAIL_FROM')
EMAIL_TO = config.get('GMAIL', 'EMAIL_TO')

# 데이터베이스 연결
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)

# SELECT 쿼리문
query = 'SELECT * FROM public."twt_jg_%s" WHERE created_at >= now() - interval \'10 minutes\''

# 마지막으로 검색된 레코드 ID
last_record_id = None

while True:
    # SELECT 쿼리 실행
    year_month_day = time.strftime('%Y%m%d', time.localtime())
    cur = conn.cursor()
    cur.execute(query % year_month_day)
    
    # 결과 레코드 확인
    new_record = False
    message_body = ''
    for record in cur.fetchall():
        record_id = record[0]
        if last_record_id is None or record_id > last_record_id:
            new_record = True
            last_record_id = record_id
            # 작성자명, 작성자 계정, 작성 시간, 작성 내용을 이메일 본문에 추가
            message_body += '작성자: {}\n'.format(record[1])
            message_body += '작성자 계정: {}\n'.format(record[2])
            message_body += '작성 시간: {}\n'.format(record[3])
            message_body += '작성 내용: {}\n\n'.format(record[4])
    
    # 새 레코드가 생성된 경우 이메일 발송
    if new_record:
        # 현재 날짜와 시간을 메일 제목에 포함
        subject = '[{}]새로운 트윗 알림!'.format(time.strftime('%Y-%m-%d %H:%M'))
        
        message = MIMEText(message_body)
        message['Subject'] = subject
        message['From'] = EMAIL_FROM
        message['To'] = EMAIL_TO
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.sendmail(EMAIL_FROM, [EMAIL_TO], message.as_string())
        smtp.quit()
    
    # 10초 대기
    time.sleep(10)
