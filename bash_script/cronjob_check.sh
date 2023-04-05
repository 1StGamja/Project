#!/bin/bash

# cron 작업에 대한 로그 파일 디렉토리 설정
LOG_DIR=/var/log/cron

# 로그 디렉토리가 없으면 생성
if [ ! -d $LOG_DIR ]; then
  mkdir -p $LOG_DIR
fi

# 로그 파일 경로 설정
LOG_FILE=$LOG_DIR/cron_check.log

# 현재 시간을 로그에 기록
echo "=============================" >> $LOG_FILE
echo "Cron 작업 확인 - $(date)" >> $LOG_FILE

# 각각의 cron 작업에 대한 로그 확인 및 결과 출력
if grep -q "cronjob1" /var/log/syslog; then
  echo "cronjob1: 성공" >> $LOG_FILE
else
  echo "cronjob1: 실패" >> $LOG_FILE
fi

if grep -q "cronjob2" /var/log/syslog; then
  echo "cronjob2: 성공" >> $LOG_FILE
else
  echo "cronjob2: 실패" >> $LOG_FILE
fi

# 로그 파일 출력
cat $LOG_FILE
