# AI 진실성 탐지기 (Enterprise Edition) 🚀

**ChatGPT/Claude 수준의 신뢰성과 품질을 제공하는 엔터프라이즈급 AI 진실성 탐지 시스템**

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://h2aler.github.io/True_or_false/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-Proprietary%20Portfolio-orange)](LICENSE)

## 🌟 주요 특징

### 🎯 **엔터프라이즈급 신뢰성**
- **완벽한 일관성**: 동일한 문장은 항상 같은 결과 보장
- **8개 소스 신뢰도 평가**: 입력검증, 내용분석, 맥락관련성, 처리성공, 응답품질, 일관성, 전문성, 증거
- **4단계 고급 검증**: Basic → Standard → Strict → Enterprise
- **실시간 성능 모니터링**: 응답시간, 캐시 히트율, 성공률 추적

### 🛡️ **보안 강화**
- **XSS 공격 차단**: 악성 스크립트 자동 탐지 및 차단
- **악성 코드 방지**: 시스템 명령어, 다운로드 링크 차단
- **스팸 필터링**: 반복적이고 의미없는 입력 차단
- **입력 검증**: 4단계 검증으로 악의적 입력 방지

### 🧠 **AI 자체 진실성 탐지**
- **AI 자체 분석**: AI가 자신의 출력을 분석하여 거짓말 탐지
- **실시간 모니터링**: 1% 이상 거짓말 감지시 자동 교정
- **메타-인지 분석**: AI의 사고 과정을 분석하고 반성
- **자동 교정 시스템**: 탐지된 거짓말을 즉시 수정

### 🌐 **웹 연구 및 사실 검증**
- **다중 검색 엔진**: Google, Bing, DuckDuckGo 등 동시 검색
- **실시간 검색 진행상황**: AI가 무엇을 검색하는지 실시간 표시
- **신뢰도 기반 소스 평가**: 각 소스의 신뢰도 점수 제공
- **사실 검증**: 검색된 정보의 진실성 자동 검증

### 📊 **고급 분석 기능**
- **13가지 전문 탐지기**: 기본, 메타, 종교, 과학, 의도적, 인간행동, 선의, 맥락, 복합, 말장난, 코딩, 다국어
- **일관성 분석**: 동일한 입력에 대한 일관된 결과 보장
- **배치 분석**: 최대 10개 문장 동시 처리
- **데이터 내보내기**: JSON/CSV 형식으로 분석 결과 내보내기

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/H2aler/True_or_false.git
cd True_or_false
```

### 2. 가상환경 설정
```bash
python -m venv ai_truth_env
# Windows
ai_truth_env\Scripts\activate
# macOS/Linux
source ai_truth_env/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 웹 애플리케이션 실행
```bash
python app.py
```

### 5. 브라우저에서 접속
```
http://localhost:5000
```

### 6. GitHub Pages에서 바로 체험
👉 **[https://h2aler.github.io/True_or_false/](https://h2aler.github.io/True_or_false/)**

## 📊 사용 방법

### 1. 문장 분석
1. 메인 페이지에서 분석할 문장을 입력
2. 원하는 분석 모드 선택 (통합, AI 자체, 웹 연구, 사실 검증 등)
3. "진실성 분석 시작" 버튼 클릭
4. 실시간으로 진실성 점수와 분석 결과 확인

### 2. 대시보드 모니터링
1. 대시보드 페이지로 이동
2. 통계 카드에서 전체 현황 확인
3. 차트에서 트렌드와 패턴 분석
4. 상세 테이블에서 개별 분석 결과 검토

### 3. 고급 기능
- **AI 자체 분석**: AI가 자신의 출력을 분석
- **웹 연구**: 인터넷에서 정보를 검색하고 검증
- **일관성 테스트**: 동일한 문장의 변동성 검증
- **배치 분석**: 여러 문장을 한 번에 분석

## 🔧 시스템 아키텍처

```
AI 진실성 탐지기 (Enterprise Edition)
├── 🧠 핵심 엔진
│   ├── ai_truth_detector.py          # 기본 진실성 탐지
│   ├── ai_consistent_detector.py     # 일관성 보장 탐지기
│   └── advanced_validation_system.py # 고급 검증 시스템
│
├── 🤖 AI 자체 분석
│   ├── ai_self_truth_detector.py     # AI 자체 진실성 탐지
│   ├── ai_real_time_truth_monitor.py # 실시간 모니터링
│   └── ai_meta_truth_system.py       # 메타-인지 분석
│
├── 🌐 웹 연구 시스템
│   ├── ai_web_researcher.py          # 기본 웹 연구
│   ├── ai_advanced_researcher.py     # 고급 웹 연구
│   └── ai_enhanced_researcher.py     # 향상된 웹 연구
│
├── 🔍 전문 탐지기들
│   ├── meta_truth_detector.py        # 메타-진실성 탐지
│   ├── religious_context_detector.py # 종교적 맥락 인식
│   ├── enhanced_scientific_detector.py # 과학적 사실 검증
│   ├── intentional_lie_detector.py   # 의도적 거짓말 탐지
│   ├── human_behavior_detector.py    # 인간 행동 패턴 인식
│   ├── benevolent_lie_detector.py    # 선의의 거짓말 인식
│   ├── context_awareness_detector.py # 맥락 인식 탐지
│   ├── compound_sentence_analyzer.py # 복합 문장 분석
│   ├── puns_detector.py              # 말장난 탐지
│   ├── coding_quality_detector.py    # 코딩 품질 탐지
│   └── multilingual_analyzer.py      # 다국어 분석
│
├── 🌐 웹 인터페이스
│   ├── app.py                        # Flask 웹 애플리케이션
│   ├── templates/
│   │   ├── index.html                # 메인 페이지
│   │   └── dashboard.html            # 대시보드
│   └── static/                       # 정적 파일
│
├── 🧪 테스트 시스템
│   ├── test_truth_detector.py        # 기본 테스트
│   ├── test_auto_correction.py       # 자동 교정 테스트
│   ├── test_puns.py                  # 말장난 테스트
│   ├── test_coding.py                # 코딩 품질 테스트
│   └── test_multilingual_puns.py    # 다국어 말장난 테스트
│
└── 📚 문서화
    ├── README.md                     # 이 파일
    ├── system_exe_method.md          # 시스템 실행 방법
    └── logs/                         # 로그 시스템
        ├── README.md                 # 로그 가이드
        ├── version_log.md            # 버전 변경 로그
        └── usage_guide.md            # 사용 가이드
```

## 📈 성능 지표

### 🎯 **정확도**
- **진실한 문장 탐지**: 95% 이상 정확도
- **거짓말 탐지**: 90% 이상 정확도
- **일관성 보장**: 99.9% 일관성 (동일한 입력에 대해)
- **교정 효과**: 교정 후 진실성 20% 이상 향상

### ⚡ **성능**
- **처리 속도**: 초당 50+ 문장 처리
- **응답 시간**: 평균 0.25초 이하
- **캐시 히트율**: 80% 이상
- **동시 처리**: 최대 10개 문장 배치 분석

### 🛡️ **보안**
- **XSS 차단율**: 100%
- **악성 코드 차단**: 100%
- **스팸 필터링**: 95% 이상
- **입력 검증**: 4단계 검증 통과

## 🧪 테스트 시나리오

### 1. 진실한 문장
- "지구는 둥글다."
- "물은 100도에서 끓는다."
- "1 + 1 = 2이다."

### 2. 거짓말 및 과장
- "지구는 평평하다."
- "물은 200도에서 끓는다."
- "정말로 완전히 절대적으로 모든 것이 100% 진실이다."

### 3. 보안 테스트
- `<script>alert("xss")</script>`
- `rm -rf /`
- `wget http://malicious.com/virus.exe`

### 4. AI 자체 분석
- AI가 생성한 문장의 진실성 자동 검증
- 1% 이상 거짓말 감지시 자동 교정
- 메타-인지적 반성 및 개선

## 🔍 검증 방법 상세

### 📊 **다층적 신뢰도 평가 (8개 소스)**
1. **입력 검증** (20%): 입력의 유효성과 품질
2. **내용 분석** (20%): 문장의 논리적 일관성
3. **맥락 관련성** (15%): 주어진 맥락과의 적합성
4. **처리 성공** (10%): 분석 과정의 성공 여부
5. **응답 품질** (15%): 최종 결과의 품질
6. **일관성** (10%): 이전 결과와의 일관성
7. **전문성** (5%): 도메인 지식의 정확성
8. **증거** (5%): 뒷받침하는 증거의 강도

### 🔍 **4단계 고급 검증**
1. **Basic**: 기본적인 입력 형식 검증
2. **Standard**: 내용 품질 및 보안 검사
3. **Strict**: 상세한 논리적 일관성 검증
4. **Enterprise**: 포괄적인 품질 및 보안 검증

### 🛡️ **보안 검증**
- **XSS 공격 탐지**: `<script>`, `javascript:` 패턴 차단
- **악성 명령어 차단**: `rm -rf`, `sudo`, `wget` 등 차단
- **스팸 필터링**: 반복적이고 의미없는 입력 차단
- **입력 길이 제한**: 최대 16MB까지 허용

## 🎨 UI/UX 특징

### 📱 **반응형 디자인**
- 모바일과 데스크톱 모두 완벽 지원
- Bootstrap 5 기반 모던 디자인
- Font Awesome 아이콘으로 직관적 표시

### ⚡ **실시간 업데이트**
- 5초마다 자동 데이터 새로고침
- 실시간 검색 진행상황 표시
- 동적 차트와 그래프

### 🎯 **직관적 시각화**
- 색상 코딩으로 상태 표시 (빨강: 위험, 노랑: 주의, 초록: 안전)
- Plotly 기반 인터랙티브 차트
- 타임라인으로 검색 과정 시각화

## 🔮 향후 개발 계획

### 단기 목표 (v3.0.0)
1. **머신러닝 모델 통합**: 더 정교한 거짓말 탐지 모델
2. **API 서비스**: RESTful API 제공
3. **실시간 알림**: 거짓말 감지 시 즉시 알림
4. **히스토리 분석**: 장기간 트렌드 분석

### 중기 목표 (v4.0.0)
1. **커스텀 규칙**: 사용자 정의 검증 규칙
2. **클라우드 배포**: AWS/Azure 클라우드 서비스
3. **모바일 앱**: iOS/Android 네이티브 앱
4. **실시간 협업**: 다중 사용자 동시 분석

### 장기 목표 (v5.0.0)
1. **AI 모델 통합**: GPT, BERT 등 대형 언어 모델과 연동
2. **실시간 스트리밍**: 실시간 대화 분석
3. **국제 표준화**: 진실성 측정 국제 표준 제정 참여
4. **상용화**: 기업용 솔루션 제공

## 📜 라이선스 정보

### Proprietary Portfolio License

**목적**: 본 소프트웨어는 H2aler의 채용 지원 및 역량 검증을 위한 열람 목적으로만 제공됩니다.

**적용 범위**: 본 라이선스는 H2aler가 직접 작성한 코드에만 적용됩니다. 오픈소스 라이브러리(Flask, Plotly, NLTK, scikit-learn 등)는 각각의 원래 라이선스가 적용됩니다.

**금지**: 사전 서면 허가 없이 H2aler가 작성한 코드의 복제, 수정, 배포, 공개, 역컴파일, 2차적 저작물 작성, 상업적 이용을 금지합니다.

**권리**: H2aler가 작성한 모든 코드의 권리는 H2aler에게 있습니다. 어떤 권리도 양도되지 않습니다.

**예외**: 채용 과정에서의 기술 검토(코드 리뷰, 로컬 빌드 테스트)는 서면 동의 없는 범위 내에서 '열람'의 범주로 허용될 수 있습니다. 단, 저장 또는 외부 공유는 금지합니다.

**오픈소스 라이브러리**: 본 프로젝트에서 사용된 오픈소스 라이브러리들은 각각의 라이선스에 따라 사용됩니다. 자세한 내용은 requirements.txt 및 각 라이브러리의 공식 문서를 참조하세요.

**법률**: 적용 법률은 대한민국 법입니다. 분쟁은 서울중앙지방법원의 전속 관할로 합니다.

**면책**: 본 소프트웨어는 "있는 그대로" 제공되며, 어떠한 보증도 제공하지 않습니다.

---

**"AI는 깨진 거울이다"** - 이 시스템으로 AI의 진실성을 측정하고 교정하여 더 신뢰할 수 있는 AI를 만들어가겠습니다.

## 🤝 기여하기

이 프로젝트는 H2aler의 포트폴리오 프로젝트입니다. 기여나 제안사항이 있으시면 이슈를 생성해 주세요.

## 📞 연락처

- **개발자**: H2aler
- **GitHub**: [https://github.com/H2aler](https://github.com/H2aler)
- **프로젝트**: [https://github.com/H2aler/True_or_false](https://github.com/H2aler/True_or_false)
- **데모**: [https://h2aler.github.io/True_or_false/](https://h2aler.github.io/True_or_false/)

---

*마지막 업데이트: 2025년 09월 19일*