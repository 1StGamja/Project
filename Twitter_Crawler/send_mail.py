import psycopg2
import time
import smtplib
from email.mime.text import MIMEText

# PostgreSQL DB 접속 정보
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = 'dlQmsdl00'

# 이메일 설정
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_USER = 'narsis.yu@gmail.com'
EMAIL_PASS = 'uwgditzevmbnnbvo'
EMAIL_FROM = 'narsis.yu@gmail.com'
EMAIL_TO = 'visionperformer@kakao.com'

# 데이터베이스 연결
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)

# SELECT 쿼리문
query = 'SELECT * FROM public."TW_%s"'

# 마지막으로 검색된 레코드 ID
last_record_id = None

while True:
    # 현재 시간 기록
    current_time = time.time()
    
    # 현재 시간에서 10초 이전 시간 계산
    past_time = current_time - 10
    
    # SELECT 쿼리 실행
    year_month_day = time.strftime('%Y%m%d', time.localtime(current_time))
    cur = conn.cursor()
    cur.execute(query % year_month_day)
    
    # 결과 레코드 확인
    new_record = False
    for record in cur.fetchall():
        record_id = record[0]
        if last_record_id is None or record_id > last_record_id:
            new_record = True
            last_record_id = record_id
    
    # 새 레코드가 생성된 경우 이메일 발송
    if new_record:
        # 현재 날짜와 시간을 메일 제목에 포함
        subject = '[{}] 새로운 트윗 알림!'.format(time.strftime('%Y-%m-%d %H:%M'))
        # 메일 내용에 새 레코드 추가
        message_body = ''
        for record in cur.fetchall():
            record_id = record[0]
            if last_record_id is None or record_id > last_record_id:
                message_body += str(record) + '\n'
                last_record_id = record_id
        
        # 새 레코드가 없는 경우 빈 문자열로 메일 본문 전송
        if message_body:
            message = MIMEText(message_body)
            message['Subject'] = subject
            message['From'] = EMAIL_FROM
            message['To'] = EMAIL_TO
            
            try:
                # 메일 발송
                smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                smtp.set_debuglevel(1)
                smtp.starttls()
                smtp.login(EMAIL_USER, EMAIL_PASS)
                smtp.sendmail(EMAIL_FROM, [EMAIL_TO], message.as_string())
                smtp.quit()
                print('메일이 성공적으로 발송되었습니다.')
            except smtplib.SMTPException as e:
                print('메일 발송 실패: {}'.format(e))

    
    # 10초 대기
    time.sleep(max(0, past_time + 10 - time.time()))
