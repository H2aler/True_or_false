# AI 진실성 탐지기 사용 가이드 📚

## 📋 개요

**AI 진실성 탐지기 (Enterprise Edition)**는 ChatGPT/Claude 수준의 신뢰성과 품질을 제공하는 엔터프라이즈급 AI 진실성 탐지 시스템입니다.

## 🚀 빠른 시작

### 1. 시스템 실행
```bash
# 가상환경 활성화
ai_truth_env\Scripts\activate  # Windows
source ai_truth_env/bin/activate  # macOS/Linux

# 애플리케이션 실행
python app.py
```

### 2. 웹 접속
- **로컬**: http://localhost:5000
- **GitHub Pages**: https://h2aler.github.io/True_or_false/

## 🎯 주요 기능 사용법

### 1. 기본 문장 분석

#### 📝 문장 입력
1. 메인 페이지에서 "분석할 문장" 입력란에 문장을 입력
2. "맥락 정보" 입력란에 추가 정보 입력 (선택사항)
3. 원하는 분석 모드 선택

#### 🔍 분석 모드 선택
- **통합 분석**: 모든 탐지기를 사용한 종합 분석
- **AI 자체 분석**: AI가 자신의 출력을 분석
- **실시간 모니터링**: 실시간으로 거짓말 감지 및 교정
- **메타-인지 분석**: AI의 사고 과정 분석
- **웹 연구**: 인터넷에서 정보를 검색하고 검증
- **사실 검증**: 특정 문장의 사실 여부 검증
- **향상된 웹 연구**: 실시간 검색 진행상황 표시
- **일관성 분석**: 동일한 결과 보장
- **일관성 테스트**: 점수 변동성 검증

#### ⚡ 분석 실행
1. "진실성 분석 시작" 버튼 클릭
2. 실시간으로 분석 결과 확인
3. 상세한 분석 정보 및 교정 제안 검토

### 2. 고급 분석 기능

#### 🧠 AI 자체 분석
- **목적**: AI가 자신의 출력을 분석하여 거짓말 탐지
- **사용법**: "AI 자체 분석" 모드 선택 후 문장 입력
- **결과**: 자체 반성, 탐지된 거짓말, 교정 제안

#### 🌐 웹 연구
- **목적**: 인터넷에서 정보를 검색하고 검증
- **사용법**: "웹 연구" 또는 "향상된 웹 연구" 모드 선택
- **결과**: 검색된 소스, 신뢰도 점수, 사실 검증 결과

#### 🔍 일관성 분석
- **목적**: 동일한 문장에 대한 일관된 결과 보장
- **사용법**: "일관성 분석" 모드 선택
- **결과**: 일관성 점수, 캐시 통계, 분석 방법

### 3. 대시보드 모니터링

#### 📊 통계 확인
1. "대시보드" 버튼 클릭
2. 전체 분석 현황 확인
3. 탐지기별 성능 모니터링
4. 최근 분석 결과 검토

#### 📈 차트 분석
- **진실성 트렌드**: 시간에 따른 진실성 점수 변화
- **탐지기별 감지율**: 각 탐지기의 성능 비교
- **성능 메트릭**: 응답 시간, 캐시 히트율 등

### 4. 배치 분석

#### 📦 여러 문장 동시 분석
1. "배치 분석" 버튼 클릭
2. 분석할 문장들을 입력
3. "배치 분석 실행" 버튼 클릭
4. 결과를 아코디언 형태로 확인

#### 📋 배치 분석 결과
- 각 문장별 개별 분석 결과
- 전체 통계 및 요약
- 성공/실패 문장 수

## 🔧 고급 설정

### 1. API 사용

#### 📡 RESTful API 엔드포인트
```bash
# 기본 분석
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"statement": "지구는 둥글다.", "context": "과학적 사실"}'

# 시스템 상태 확인
curl http://localhost:5000/api/health

# 성능 메트릭 조회
curl http://localhost:5000/api/metrics

# 배치 분석
curl -X POST http://localhost:5000/api/batch-analyze \
  -H "Content-Type: application/json" \
  -d '{"statements": ["문장1", "문장2", "문장3"]}'
```

#### 🔍 검증 전용 API
```bash
# 입력 검증
curl -X POST http://localhost:5000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"statement": "지구는 둥글다.", "validation_level": "enterprise"}'

# 신뢰도 평가
curl -X POST http://localhost:5000/api/confidence \
  -H "Content-Type: application/json" \
  -d '{"statement": "지구는 둥글다.", "analysis_result": {}}'
```

### 2. 데이터 내보내기

#### 📊 분석 결과 내보내기
```bash
# JSON 형식으로 내보내기
curl "http://localhost:5000/api/export?format=json&limit=100"

# CSV 형식으로 내보내기
curl "http://localhost:5000/api/export?format=csv&limit=100"
```

### 3. 캐시 관리

#### 🗑️ 캐시 초기화
```bash
# 모든 캐시 초기화
curl -X POST http://localhost:5000/api/clear-cache

# 일관성 캐시만 초기화
curl -X POST http://localhost:5000/api/clear-consistency-cache
```

## 🧪 테스트 및 검증

### 1. 기본 테스트 실행
```bash
# 기본 진실성 탐지 테스트
python test_truth_detector.py

# 자동 교정 테스트
python test_auto_correction.py

# 말장난 테스트
python test_puns.py

# 코딩 품질 테스트
python test_coding.py

# 다국어 테스트
python test_multilingual_puns.py
```

### 2. 시스템 비교 테스트
```bash
# 기존 시스템 vs 엔터프라이즈 시스템 비교
python simple_comparison.py

# 상세한 차이점 분석
python test_difference.py
```

### 3. 일관성 테스트
```bash
# 일관성 테스트 (웹 인터페이스)
1. "일관성 테스트" 모드 선택
2. 테스트할 문장 입력
3. 테스트 횟수 설정 (기본 5회)
4. "진실성 분석 시작" 클릭
5. 결과에서 변동성 확인
```

## 📊 결과 해석

### 1. 진실성 점수
- **0.0 - 0.2**: 매우 거짓 (20% 이하)
- **0.2 - 0.4**: 거짓 (20-40%)
- **0.4 - 0.6**: 불확실 (40-60%)
- **0.6 - 0.8**: 진실 (60-80%)
- **0.8 - 1.0**: 매우 진실 (80% 이상)

### 2. 신뢰도 점수
- **0.0 - 0.2**: 매우 낮음
- **0.2 - 0.4**: 낮음
- **0.4 - 0.6**: 보통
- **0.6 - 0.8**: 높음
- **0.8 - 1.0**: 매우 높음

### 3. 교정 필요 여부
- **True**: 문장에 거짓말이나 문제가 있어 교정이 필요
- **False**: 문장이 정상적이거나 교정이 불필요

### 4. 일관성 점수
- **1.0**: 완벽한 일관성 (동일한 입력에 대해 항상 같은 결과)
- **0.8 - 0.9**: 높은 일관성
- **0.6 - 0.8**: 보통 일관성
- **0.6 미만**: 낮은 일관성

## 🛡️ 보안 기능

### 1. 자동 보안 검사
- **XSS 공격 차단**: `<script>`, `javascript:` 패턴 자동 차단
- **악성 명령어 차단**: `rm -rf`, `sudo`, `wget` 등 차단
- **스팸 필터링**: 반복적이고 의미없는 입력 차단

### 2. 입력 검증
- **4단계 검증**: Basic → Standard → Strict → Enterprise
- **길이 제한**: 최대 16MB까지 허용
- **형식 검증**: JSON 형식 및 필수 필드 검증

## 📈 성능 최적화

### 1. 캐싱 활용
- **응답 캐싱**: 동일한 요청에 대한 빠른 응답
- **일관성 캐싱**: 동일한 문장에 대한 일관된 결과
- **캐시 히트율**: 80% 이상 유지 권장

### 2. 배치 처리
- **동시 처리**: 최대 10개 문장까지 동시 분석
- **비동기 처리**: asyncio를 활용한 비동기 처리
- **성능 모니터링**: 실시간 성능 메트릭 추적

## 🔍 문제 해결

### 1. 일반적인 문제

#### 서버가 시작되지 않는 경우
```bash
# 포트 확인
netstat -an | grep 5000

# 포트 해제
lsof -ti:5000 | xargs kill -9

# 다른 포트로 실행
python app.py --port 5001
```

#### 모듈 import 오류
```bash
# 가상환경 재활성화
deactivate
source ai_truth_env/bin/activate

# 의존성 재설치
pip install -r requirements.txt --force-reinstall
```

#### 메모리 부족
```bash
# 메모리 사용량 확인
ps aux | grep python

# 가상환경에서 메모리 제한 설정
export PYTHONHASHSEED=0
python -O app.py
```

### 2. 분석 결과 문제

#### 일관성 없는 결과
- **해결**: "일관성 분석" 모드 사용
- **원인**: 캐시 문제 또는 시스템 부하
- **방법**: 캐시 초기화 후 재시도

#### 느린 응답 시간
- **해결**: 캐시 상태 확인
- **원인**: 네트워크 지연 또는 시스템 부하
- **방법**: 성능 메트릭 확인

#### 에러 발생
- **해결**: 로그 파일 확인
- **원인**: 입력 형식 오류 또는 시스템 오류
- **방법**: 에러 메시지 확인 후 재시도

## 📱 모바일 사용

### 1. 반응형 디자인
- **자동 최적화**: 모바일 화면에 자동 최적화
- **터치 친화적**: 터치 인터페이스 지원
- **빠른 로딩**: 모바일 최적화된 로딩

### 2. 모바일 전용 기능
- **간편 입력**: 모바일 키보드 최적화
- **스와이프 네비게이션**: 직관적인 네비게이션
- **오프라인 지원**: 기본 기능 오프라인 사용 가능

## 🌍 다국어 지원

### 1. 지원 언어
- **한국어**: 완전 지원
- **영어**: 기본 지원
- **일본어**: 기본 지원
- **중국어**: 기본 지원

### 2. 다국어 분석
- **자동 감지**: 입력된 언어 자동 감지
- **혼합 언어**: 여러 언어가 섞인 문장 분석
- **번역 지원**: 필요시 자동 번역

## 📊 로그 및 모니터링

### 1. 로그 확인
```bash
# 실시간 로그 모니터링
tail -f logs/app.log

# 에러 로그만 확인
grep "ERROR" logs/app.log

# 특정 시간대 로그
grep "2024-12-19 14:" logs/app.log
```

### 2. 성능 모니터링
```bash
# 시스템 상태 확인
curl http://localhost:5000/api/health

# 성능 메트릭 조회
curl http://localhost:5000/api/metrics

# 로그 통계 분석
python logs/change_tracker.py
```

## 🆘 지원 및 문의

### 1. 문제 신고
- **GitHub Issues**: https://github.com/H2aler/True_or_false/issues
- **이메일**: h2aler@example.com

### 2. 문서 참조
- **API 문서**: http://localhost:5000/api/health
- **시스템 가이드**: system_exe_method.md
- **버전 로그**: logs/version_log.md

### 3. 커뮤니티
- **GitHub Discussions**: https://github.com/H2aler/True_or_false/discussions
- **위키**: https://github.com/H2aler/True_or_false/wiki

---

**마지막 업데이트**: 2024년 12월 19일  
**버전**: 2.0.0-enterprise  
**관리자**: H2aler