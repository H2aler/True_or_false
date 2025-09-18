# AI 진실성 탐지기 시스템 실행 방법 🚀

## 📋 시스템 개요

**AI 진실성 탐지기 (Enterprise Edition)**는 ChatGPT/Claude 수준의 신뢰성과 품질을 제공하는 엔터프라이즈급 AI 진실성 탐지 시스템입니다.

### 🌟 주요 특징
- **완벽한 일관성**: 동일한 문장은 항상 같은 결과 보장
- **8개 소스 신뢰도 평가**: 다층적 신뢰도 분석
- **4단계 고급 검증**: Basic → Standard → Strict → Enterprise
- **AI 자체 진실성 탐지**: AI가 자신의 출력을 분석하고 교정
- **웹 연구 및 사실 검증**: 실시간 인터넷 검색 및 검증
- **보안 강화**: XSS, 악성 코드, 스팸 차단

## 🛠️ 시스템 요구사항

### 필수 요구사항
- **Python**: 3.8 이상
- **메모리**: 최소 4GB RAM (권장 8GB)
- **디스크**: 최소 1GB 여유 공간
- **네트워크**: 인터넷 연결 (웹 연구 기능용)

### 권장 사양
- **Python**: 3.9 이상
- **메모리**: 8GB RAM 이상
- **CPU**: 멀티코어 프로세서
- **디스크**: SSD (성능 향상)

## 📦 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/H2aler/True_or_false.git
cd True_or_false
```

### 2. 가상환경 생성 및 활성화

#### Windows
```bash
python -m venv ai_truth_env
ai_truth_env\Scripts\activate
```

#### macOS/Linux
```bash
python -m venv ai_truth_env
source ai_truth_env/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 설치 확인
```bash
python -c "import flask; print('Flask 설치 완료')"
python -c "import plotly; print('Plotly 설치 완료')"
```

## 🚀 실행 방법

### 1. 기본 실행
```bash
python app.py
```

### 2. 백그라운드 실행 (Linux/macOS)
```bash
nohup python app.py > app.log 2>&1 &
```

### 3. Windows 서비스로 실행
```bash
# 관리자 권한으로 실행
python -m pip install pywin32
python -c "import win32serviceutil; win32serviceutil.InstallService('AITruthDetector', 'AI Truth Detector', 'python app.py')"
```

### 4. Docker로 실행 (선택사항)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

```bash
docker build -t ai-truth-detector .
docker run -p 5000:5000 ai-truth-detector
```

## 🌐 접속 방법

### 로컬 접속
- **메인 페이지**: http://localhost:5000
- **대시보드**: http://localhost:5000/dashboard
- **API 문서**: http://localhost:5000/api/health

### GitHub Pages 접속
- **라이브 데모**: https://h2aler.github.io/True_or_false/

## 🔧 설정 및 구성

### 1. 환경 변수 설정
```bash
# .env 파일 생성
echo "FLASK_ENV=production" > .env
echo "SECRET_KEY=your_secret_key_here" >> .env
echo "DEBUG=False" >> .env
```

### 2. 로그 설정
```python
# app.py에서 로그 레벨 조정
logging.basicConfig(level=logging.INFO)  # INFO, DEBUG, WARNING, ERROR
```

### 3. 성능 튜닝
```python
# app.py에서 성능 설정 조정
app.config.update(
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24)
)
```

## 🧪 테스트 실행

### 1. 기본 테스트
```bash
python test_truth_detector.py
```

### 2. 자동 교정 테스트
```bash
python test_auto_correction.py
```

### 3. 말장난 테스트
```bash
python test_puns.py
```

### 4. 코딩 품질 테스트
```bash
python test_coding.py
```

### 5. 다국어 테스트
```bash
python test_multilingual_puns.py
```

### 6. 통합 테스트
```bash
python -m pytest tests/ -v
```

## 📊 모니터링 및 관리

### 1. 시스템 상태 확인
```bash
curl http://localhost:5000/api/health
```

### 2. 성능 메트릭 조회
```bash
curl http://localhost:5000/api/metrics
```

### 3. 로그 확인
```bash
# 실시간 로그 모니터링
tail -f app.log

# 에러 로그만 확인
grep "ERROR" app.log
```

### 4. 캐시 관리
```bash
# 캐시 초기화
curl -X POST http://localhost:5000/api/clear-cache
```

## 🔍 문제 해결

### 1. 포트 충돌
```bash
# 포트 5000이 사용 중인 경우
lsof -i :5000
kill -9 <PID>

# 다른 포트로 실행
python app.py --port 5001
```

### 2. 모듈 import 오류
```bash
# 가상환경 재활성화
deactivate
source ai_truth_env/bin/activate  # Linux/macOS
ai_truth_env\Scripts\activate     # Windows

# 의존성 재설치
pip install -r requirements.txt --force-reinstall
```

### 3. 메모리 부족
```bash
# 메모리 사용량 확인
ps aux | grep python

# 가상환경에서 메모리 제한 설정
export PYTHONHASHSEED=0
python -O app.py
```

### 4. 네트워크 오류
```bash
# 방화벽 설정 확인
sudo ufw status
sudo ufw allow 5000

# 방화벽 비활성화 (개발 환경만)
sudo ufw disable
```

## 🚀 고급 사용법

### 1. API 사용
```python
import requests

# 문장 분석
response = requests.post('http://localhost:5000/api/analyze', json={
    'statement': '지구는 둥글다.',
    'context': '과학적 사실',
    'analysis_mode': 'all'
})

print(response.json())
```

### 2. 배치 분석
```python
# 여러 문장 동시 분석
statements = [
    '지구는 둥글다.',
    '물은 100도에서 끓는다.',
    '1 + 1 = 2이다.'
]

response = requests.post('http://localhost:5000/api/batch-analyze', json={
    'statements': statements,
    'context': '배치 분석 테스트'
})
```

### 3. 웹 연구 기능
```python
# 질문 연구
response = requests.post('http://localhost:5000/api/research-question', json={
    'question': '인공지능의 미래는?',
    'type': 'enhanced'
})
```

### 4. 일관성 테스트
```python
# 일관성 테스트
response = requests.post('http://localhost:5000/api/consistency-test', json={
    'statement': '지구는 둥글다.',
    'test_count': 5
})
```

## 📈 성능 최적화

### 1. 캐싱 활성화
```python
# app.py에서 캐시 TTL 조정
@cache_response(ttl=600)  # 10분 캐시
```

### 2. 비동기 처리
```python
# 비동기 라우트 사용
@app.route('/api/analyze', methods=['POST'])
@async_route
async def api_analyze():
    # 비동기 처리 로직
```

### 3. 데이터베이스 연동
```python
# SQLite 데이터베이스 사용
import sqlite3

def init_db():
    conn = sqlite3.connect('analysis.db')
    # 테이블 생성 로직
```

## 🔒 보안 설정

### 1. HTTPS 설정
```python
# SSL 인증서 설정
app.run(ssl_context='adhoc', host='0.0.0.0', port=5000)
```

### 2. CORS 설정
```python
# CORS 정책 설정
CORS(app, origins=['https://yourdomain.com'])
```

### 3. 세션 보안
```python
# 세션 보안 설정
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
```

## 📱 모바일 최적화

### 1. 반응형 디자인
- Bootstrap 5 사용으로 자동 모바일 최적화
- 터치 친화적 인터페이스
- 모바일 전용 네비게이션

### 2. PWA 설정
```javascript
// service-worker.js
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('ai-truth-detector-v1').then(cache => {
            return cache.addAll([
                '/',
                '/static/css/style.css',
                '/static/js/app.js'
            ]);
        })
    );
});
```

## 🌍 다국어 지원

### 1. 언어 설정
```python
# 다국어 분석 활성화
multilingual_analysis = multilingual_analyzer.analyze_multilingual_statement(statement, context)
```

### 2. 번역 기능
```python
# 자동 번역 지원
if multilingual_analysis['needs_translation']:
    translated = translate_statement(statement)
```

## 📊 로그 및 모니터링

### 1. 로그 레벨 설정
```python
# 개발 환경
logging.basicConfig(level=logging.DEBUG)

# 프로덕션 환경
logging.basicConfig(level=logging.INFO)
```

### 2. 로그 파일 관리
```bash
# 로그 로테이션 설정
logrotate -f /etc/logrotate.d/ai-truth-detector
```

### 3. 모니터링 도구 연동
```python
# Prometheus 메트릭 수집
from prometheus_client import Counter, Histogram

request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')
```

## 🔄 업데이트 및 유지보수

### 1. 시스템 업데이트
```bash
# 최신 버전으로 업데이트
git pull origin main
pip install -r requirements.txt --upgrade
```

### 2. 데이터 백업
```bash
# 분석 히스토리 백업
cp analysis_history.json backup/analysis_history_$(date +%Y%m%d).json
```

### 3. 성능 모니터링
```bash
# 시스템 리소스 모니터링
htop
iostat -x 1
```

## 🆘 지원 및 문의

### 1. 문제 신고
- GitHub Issues: https://github.com/H2aler/True_or_false/issues
- 이메일: h2aler@example.com

### 2. 문서 참조
- API 문서: http://localhost:5000/api/health
- 사용 가이드: logs/usage_guide.md
- 버전 로그: logs/version_log.md

### 3. 커뮤니티
- GitHub Discussions: https://github.com/H2aler/True_or_false/discussions
- 위키: https://github.com/H2aler/True_or_false/wiki

---

**마지막 업데이트**: 2025년 09월 19일  
**버전**: 2.0.0-enterprise  
**개발자**: H2aler