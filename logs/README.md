# 📋 AI 진실성 탐지기 로그 시스템

## 📄 저작권 안내

**Copyright © 2025 H2aler. 모든 권리 보유.**

### 사용 제한
본 저장소는 채용 평가 및 포트폴리오 열람 목적에 한해 공개되었습니다.
사전 서면 동의 없이 코드의 복제, 수정, 배포, 상업적 이용을 금지합니다.

---

## 📁 디렉토리 구조
```
logs/
├── README.md              # 이 파일 (로그 시스템 설명)
├── version_log.md         # 버전별 변경사항 상세 로그
├── change_history.json    # JSON 형태의 변경 히스토리
└── change_tracker.py      # 변경사항 추적 도구
```

## 🔧 사용 방법

### 1. 변경사항 확인
```bash
python logs/change_tracker.py check
```
- 현재 추적 중인 파일들의 변경사항을 확인합니다
- Git 상태와 파일 해시를 비교하여 변경된 파일을 감지합니다

### 2. 변경사항 로그 기록
```bash
python logs/change_tracker.py log <버전> <설명> [이유]
```
예시:
```bash
python logs/change_tracker.py log v2.1.0 "로그 시스템 구축" "변경사항 추적 시스템 추가"
```

### 3. 버전 히스토리 확인
```bash
python logs/change_tracker.py history
```
- 모든 버전의 변경사항을 간단히 확인할 수 있습니다

## 📊 추적 대상 파일

### 핵심 시스템 파일
- `ai_truth_detector.py` - 핵심 탐지 엔진
- `app.py` - Flask 웹 애플리케이션
- `run.py` - 자동 실행 스크립트

### 고급 탐지기 파일
- `meta_truth_detector.py` - 메타-진실성 탐지기
- `religious_context_detector.py` - 종교적 맥락 인식
- `enhanced_scientific_detector.py` - 강화된 과학적 사실 검증
- `intentional_lie_detector.py` - 의도적 거짓말 탐지
- `human_behavior_detector.py` - 인간 행동 패턴 인식
- `benevolent_lie_detector.py` - 선의의 거짓말 인식
- `context_awareness_detector.py` - 맥락 인식 탐지
- `compound_sentence_analyzer.py` - 복합 문장 분석
- `coding_quality_detector.py` - 코딩 품질 탐지
- `multilingual_analyzer.py` - 다국어 분석
- `puns_detector.py` - 말장난 탐지
- `correction_capability_enhancer.py` - 교정 능력 강화

### 웹 인터페이스 파일
- `templates/base.html` - 기본 HTML 템플릿
- `templates/index.html` - 메인 페이지
- `templates/dashboard.html` - 대시보드

### 테스트 및 설정 파일
- `test_truth_detector.py` - 테스트 시스템
- `quick_test.py` - 빠른 테스트
- `test_auto_correction.py` - 자동 교정 테스트
- `test_coding.py` - 코딩 품질 테스트
- `test_multilingual_puns.py` - 다국어 및 말장난 테스트
- `test_puns.py` - 말장난 테스트
- `verification_methods_demo.py` - 검증 방법 데모
- `requirements.txt` - 의존성 패키지

## 📝 로그 파일 설명

### version_log.md
- **목적**: 사람이 읽기 쉬운 형태의 상세한 변경사항 로그
- **내용**: 
  - 버전별 변경사항
  - 수정된 파일과 라인 번호
  - 변경 전/후 코드 비교
  - 변경 이유와 테스트 결과

### change_history.json
- **목적**: 프로그램이 읽기 쉬운 형태의 구조화된 데이터
- **내용**:
  - 버전 정보
  - 파일 해시값
  - 변경 타임스탬프
  - Git 상태 정보

### change_tracker.py
- **목적**: 변경사항을 자동으로 감지하고 로그를 생성하는 도구
- **기능**:
  - 파일 해시 비교
  - Git 상태 확인
  - 자동 로그 생성
  - 변경사항 리포트 생성

## 🔄 버전 관리 규칙

### 버전 번호 체계
- **Major (v3.0.0)**: 대규모 기능 변경, 알고리즘 개선, 새로운 탐지기 추가
- **Minor (v2.15.0)**: 새로운 기능 추가, UI 개선, 탐지기 개선
- **Patch (v2.14.1)**: 버그 수정, 작은 개선, 성능 최적화

### 현재 버전 상태
- **최신 버전**: v2.14.0
- **다음 예정**: v2.15.0 (사용자 피드백 반영)
- **장기 목표**: v3.0.0 (머신러닝 모델 통합)

### 로그 작성 가이드
1. **명확한 설명**: 변경사항을 명확하게 설명
2. **구체적인 이유**: 왜 변경했는지 이유 명시
3. **테스트 결과**: 변경 후 테스트 결과 포함
4. **코드 비교**: 중요한 변경사항은 전/후 비교

## 🚀 자동화 기능

### Git 연동
- Git 상태를 자동으로 확인하여 변경된 파일 감지
- 커밋되지 않은 변경사항도 추적

### 해시 기반 감지
- 파일 내용의 MD5 해시를 계산하여 변경사항 감지
- 바이트 단위의 정확한 변경 감지

### 자동 로그 생성
- 변경사항을 자동으로 감지하고 로그에 기록
- Markdown과 JSON 형태로 동시 저장

## 📈 활용 방법

### 개발 과정 추적
```bash
# 개발 시작 전
python logs/change_tracker.py check

# 개발 완료 후
python logs/change_tracker.py log v2.15.0 "새로운 탐지기 추가" "사용자 요청 반영"
```

### 팀 협업
- 모든 변경사항이 체계적으로 기록됨
- 누가, 언제, 무엇을, 왜 변경했는지 추적 가능
- 롤백이나 문제 해결 시 이전 버전 참조 용이

### 프로젝트 관리
- 버전별 기능 추가/수정 내역 관리
- 테스트 결과와 성능 개선 추적
- 사용자 피드백 반영 과정 기록

## 🔍 문제 해결

### 로그 파일이 생성되지 않는 경우
1. `logs/` 디렉토리 권한 확인
2. Python 실행 권한 확인
3. 파일 경로 확인

### 변경사항이 감지되지 않는 경우
1. Git 저장소 초기화 확인
2. 추적 대상 파일 경로 확인
3. 파일 권한 확인

### 로그 형식이 깨지는 경우
1. UTF-8 인코딩 확인
2. Markdown 문법 확인
3. JSON 형식 확인

---

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

**💡 팁**: 개발 중에는 자주 `check` 명령어를 사용하여 변경사항을 확인하고, 중요한 변경이 있을 때마다 `log` 명령어로 기록하는 것을 권장합니다.
