# 로그 시스템 가이드 📊

## 📋 개요

AI 진실성 탐지기 (Enterprise Edition)의 로그 시스템은 시스템의 모든 활동을 추적하고 모니터링하기 위한 포괄적인 로깅 솔루션입니다.

## 🗂️ 로그 파일 구조

```
logs/
├── README.md              # 이 파일 (로그 시스템 가이드)
├── version_log.md         # 버전 변경 로그
├── usage_guide.md         # 사용 가이드
├── change_tracker.py      # 변경사항 추적 도구
├── app.log               # 애플리케이션 로그 (자동 생성)
├── error.log             # 에러 로그 (자동 생성)
├── access.log            # 접근 로그 (자동 생성)
└── performance.log       # 성능 로그 (자동 생성)
```

## 📊 로그 레벨

### 1. DEBUG (10)
- 상세한 디버깅 정보
- 개발 환경에서만 사용
- 모든 함수 호출과 변수 상태 추적

### 2. INFO (20)
- 일반적인 정보 메시지
- 시스템 상태 및 진행 상황
- 사용자 활동 기록

### 3. WARNING (30)
- 잠재적인 문제 상황
- 시스템이 계속 작동하지만 주의 필요
- 성능 저하나 예상치 못한 동작

### 4. ERROR (40)
- 오류 발생
- 기능이 제대로 작동하지 않음
- 사용자 요청 처리 실패

### 5. CRITICAL (50)
- 심각한 오류
- 시스템이 중단될 수 있는 상황
- 즉시 조치가 필요한 문제

## 🔍 로그 분석 도구

### 1. 실시간 로그 모니터링
```bash
# 실시간 로그 확인
tail -f logs/app.log

# 에러만 실시간 확인
tail -f logs/error.log | grep ERROR

# 특정 사용자 활동 추적
tail -f logs/access.log | grep "user_id:123"
```

### 2. 로그 검색 및 필터링
```bash
# 특정 시간대 로그 확인
grep "2024-12-19 14:" logs/app.log

# 에러 로그만 추출
grep "ERROR" logs/app.log > logs/error_summary.log

# 특정 기능 관련 로그
grep "analyze_statement" logs/app.log
```

### 3. 로그 통계 분석
```bash
# 로그 레벨별 통계
grep -c "DEBUG" logs/app.log
grep -c "INFO" logs/app.log
grep -c "WARNING" logs/app.log
grep -c "ERROR" logs/app.log
grep -c "CRITICAL" logs/app.log

# 시간대별 요청 수
grep "분석 요청 시작" logs/app.log | cut -d' ' -f1-2 | sort | uniq -c
```

## 📈 성능 모니터링

### 1. 응답 시간 분석
```bash
# 평균 응답 시간 계산
grep "분석 완료" logs/app.log | grep -o "처리 시간: [0-9.]*" | cut -d' ' -f3 | awk '{sum+=$1; count++} END {print "평균 응답 시간:", sum/count, "초"}'

# 가장 느린 요청 찾기
grep "분석 완료" logs/app.log | sort -k10 -nr | head -10
```

### 2. 에러율 분석
```bash
# 에러율 계산
total_requests=$(grep -c "분석 요청 시작" logs/app.log)
error_requests=$(grep -c "ERROR" logs/app.log)
error_rate=$(echo "scale=2; $error_requests * 100 / $total_requests" | bc)
echo "에러율: $error_rate%"
```

### 3. 사용량 통계
```bash
# 일일 사용량
grep "$(date +%Y-%m-%d)" logs/app.log | grep "분석 요청 시작" | wc -l

# 시간대별 사용량
grep "$(date +%Y-%m-%d)" logs/app.log | grep "분석 요청 시작" | cut -d' ' -f2 | cut -d':' -f1 | sort | uniq -c
```

## 🔧 로그 설정

### 1. 로그 레벨 설정
```python
# app.py에서 로그 레벨 조정
import logging

# 개발 환경
logging.basicConfig(level=logging.DEBUG)

# 프로덕션 환경
logging.basicConfig(level=logging.INFO)

# 디버깅 모드
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
```

### 2. 로그 파일 설정
```python
# 파일별 로그 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.FileHandler('logs/error.log', level=logging.ERROR),
        logging.StreamHandler()
    ]
)
```

### 3. 로그 로테이션 설정
```bash
# logrotate 설정 파일 생성
sudo nano /etc/logrotate.d/ai-truth-detector

# 설정 내용
/path/to/True_or_false/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        systemctl reload ai-truth-detector
    endscript
}
```

## 📊 로그 분석 스크립트

### 1. 기본 통계 스크립트
```python
#!/usr/bin/env python3
# log_analyzer.py

import re
from collections import Counter
from datetime import datetime

def analyze_logs(log_file):
    """로그 파일 분석"""
    with open(log_file, 'r', encoding='utf-8') as f:
        logs = f.readlines()
    
    # 로그 레벨별 통계
    levels = Counter()
    for log in logs:
        if 'DEBUG' in log:
            levels['DEBUG'] += 1
        elif 'INFO' in log:
            levels['INFO'] += 1
        elif 'WARNING' in log:
            levels['WARNING'] += 1
        elif 'ERROR' in log:
            levels['ERROR'] += 1
        elif 'CRITICAL' in log:
            levels['CRITICAL'] += 1
    
    print("=== 로그 레벨별 통계 ===")
    for level, count in levels.items():
        print(f"{level}: {count}")
    
    # 에러 분석
    errors = [log for log in logs if 'ERROR' in log]
    print(f"\n=== 에러 분석 ===")
    print(f"총 에러 수: {len(errors)}")
    
    if errors:
        print("\n최근 에러들:")
        for error in errors[-5:]:
            print(f"  {error.strip()}")

if __name__ == "__main__":
    analyze_logs('logs/app.log')
```

### 2. 성능 분석 스크립트
```python
#!/usr/bin/env python3
# performance_analyzer.py

import re
import statistics
from datetime import datetime

def analyze_performance(log_file):
    """성능 분석"""
    with open(log_file, 'r', encoding='utf-8') as f:
        logs = f.readlines()
    
    # 응답 시간 추출
    response_times = []
    for log in logs:
        match = re.search(r'처리 시간: ([\d.]+)초', log)
        if match:
            response_times.append(float(match.group(1)))
    
    if response_times:
        print("=== 성능 분석 ===")
        print(f"총 요청 수: {len(response_times)}")
        print(f"평균 응답 시간: {statistics.mean(response_times):.3f}초")
        print(f"중간값 응답 시간: {statistics.median(response_times):.3f}초")
        print(f"최소 응답 시간: {min(response_times):.3f}초")
        print(f"최대 응답 시간: {max(response_times):.3f}초")
        print(f"표준편차: {statistics.stdev(response_times):.3f}초")

if __name__ == "__main__":
    analyze_performance('logs/app.log')
```

## 🚨 알림 설정

### 1. 에러 알림
```bash
# 에러 발생시 이메일 알림
#!/bin/bash
# error_monitor.sh

tail -f logs/error.log | while read line; do
    if echo "$line" | grep -q "ERROR"; then
        echo "에러 발생: $line" | mail -s "AI Truth Detector Error" admin@example.com
    fi
done
```

### 2. 성능 모니터링
```bash
# 응답 시간이 5초를 초과하면 알림
#!/bin/bash
# performance_monitor.sh

tail -f logs/app.log | while read line; do
    if echo "$line" | grep -q "분석 완료"; then
        response_time=$(echo "$line" | grep -o "처리 시간: [0-9.]*" | cut -d' ' -f3)
        if (( $(echo "$response_time > 5.0" | bc -l) )); then
            echo "응답 시간 초과: $response_time초" | mail -s "Performance Alert" admin@example.com
        fi
    fi
done
```

## 📱 대시보드 연동

### 1. Grafana 대시보드
```json
{
  "dashboard": {
    "title": "AI Truth Detector Logs",
    "panels": [
      {
        "title": "Log Levels",
        "type": "pie",
        "targets": [
          {
            "expr": "sum by (level) (rate(log_entries_total[5m]))"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(response_time_seconds_bucket[5m]))"
          }
        ]
      }
    ]
  }
}
```

### 2. ELK Stack 연동
```yaml
# logstash.conf
input {
  file {
    path => "/path/to/True_or_false/logs/*.log"
    type => "ai-truth-detector"
  }
}

filter {
  grok {
    match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} - %{WORD:logger} - %{LOGLEVEL:level} - %{GREEDYDATA:message}" }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "ai-truth-detector-%{+YYYY.MM.dd}"
  }
}
```

## 🔒 보안 및 개인정보 보호

### 1. 민감한 정보 마스킹
```python
# 로그에서 민감한 정보 제거
import re

def mask_sensitive_data(log_message):
    # 이메일 주소 마스킹
    log_message = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***@***.***', log_message)
    
    # 전화번호 마스킹
    log_message = re.sub(r'\b\d{3}-\d{4}-\d{4}\b', '***-****-****', log_message)
    
    # IP 주소 마스킹
    log_message = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '***.***.***.***', log_message)
    
    return log_message
```

### 2. 로그 접근 권한
```bash
# 로그 파일 권한 설정
chmod 640 logs/*.log
chown root:ai-truth-detector logs/*.log

# 로그 디렉토리 권한 설정
chmod 750 logs/
chown root:ai-truth-detector logs/
```

## 📋 로그 정리 및 유지보수

### 1. 자동 로그 정리
```bash
# 30일 이상 된 로그 파일 삭제
find logs/ -name "*.log" -mtime +30 -delete

# 압축된 로그 파일은 90일 후 삭제
find logs/ -name "*.log.gz" -mtime +90 -delete
```

### 2. 로그 아카이브
```bash
# 월별 로그 아카이브
tar -czf logs/archive_$(date +%Y%m).tar.gz logs/*.log
```

### 3. 디스크 사용량 모니터링
```bash
# 로그 디렉토리 크기 확인
du -sh logs/

# 가장 큰 로그 파일 찾기
ls -lah logs/*.log | sort -k5 -hr | head -10
```

## 🆘 문제 해결

### 1. 로그 파일이 생성되지 않는 경우
```bash
# 로그 디렉토리 권한 확인
ls -la logs/

# 애플리케이션 권한 확인
ps aux | grep python

# 디스크 공간 확인
df -h
```

### 2. 로그 파일이 너무 큰 경우
```bash
# 로그 파일 크기 확인
ls -lah logs/*.log

# 로그 파일 압축
gzip logs/app.log

# 로그 파일 분할
split -b 100M logs/app.log logs/app.log.part
```

### 3. 로그 파싱 오류
```bash
# 로그 파일 인코딩 확인
file logs/app.log

# 로그 파일 형식 확인
head -5 logs/app.log
```

---

**마지막 업데이트**: 2025년 09월 20일  
**버전**: 2.0.0-enterprise  
**관리자**: H2aler