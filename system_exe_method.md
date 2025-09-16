# AI 진실성 탐지기 시스템 실행 방법

## 📄 저작권 안내

**Copyright © 2025 H2aler. 모든 권리 보유.**

### 사용 제한
본 저장소는 채용 평가 및 포트폴리오 열람 목적에 한해 공개되었습니다.
사전 서면 동의 없이 코드의 복제, 수정, 배포, 상업적 이용을 금지합니다.

---

## 📋 목차
1. [시스템 요구사항](#시스템-요구사항)
2. [설치 및 설정](#설치-및-설정)
3. [실행 방법](#실행-방법)
4. [사용 방법](#사용-방법)
5. [문제 해결](#문제-해결)
6. [고급 설정](#고급-설정)

---

## 🖥️ 시스템 요구사항

### 최소 요구사항
- **운영체제**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 이상
- **메모리**: 4GB RAM 이상
- **저장공간**: 2GB 이상 여유 공간
- **네트워크**: 인터넷 연결 (패키지 설치용)

### 권장 요구사항
- **Python**: 3.9 이상
- **메모리**: 8GB RAM 이상
- **저장공간**: 5GB 이상 여유 공간
- **브라우저**: Chrome, Firefox, Safari, Edge 최신 버전

---

## 🔧 설치 및 설정

### 1단계: Python 설치 확인
```bash
# Python 버전 확인
python --version
# 또는
python3 --version

# pip 버전 확인
pip --version
```

### 2단계: 프로젝트 다운로드
```bash
# 프로젝트 디렉토리로 이동
cd C:\Users\H2aler\Documents\true_or_false

# 현재 파일 구조 확인
dir
# 또는
ls
```

### 3단계: 의존성 패키지 설치
```bash
# 가상환경 생성 (권장)
python -m venv ai_truth_env

# 가상환경 활성화
# Windows:
ai_truth_env\Scripts\activate
# macOS/Linux:
source ai_truth_env/bin/activate

# 의존성 패키지 설치
pip install -r requirements.txt
```

### 4단계: 설치 확인
```bash
# 빠른 테스트 실행
python quick_test.py
```

---

## 🚀 실행 방법

### 방법 1: 자동 실행 스크립트 사용 (권장)
```bash
# 종합 실행 스크립트
python run.py
```

이 스크립트는 다음을 자동으로 수행합니다:
- 의존성 패키지 확인
- 가상환경 활성화
- 테스트 실행 (선택사항)
- 웹 애플리케이션 시작
- 모든 탐지기 시스템 초기화

### 방법 2: 직접 실행
```bash
# 웹 애플리케이션 직접 실행
python app.py
```

### 방법 3: 개발 모드 실행
```bash
# 디버그 모드로 실행
python app.py --debug
```

---

## 🌐 사용 방법

### 1. 웹 애플리케이션 접속
1. 터미널에서 `python app.py` 실행
2. 브라우저에서 `http://localhost:5000` 접속
3. 메인 페이지에서 AI 진실성 탐지기 사용

### 2. 문장 분석하기
1. **메인 페이지**에서 분석할 문장 입력
2. **"진실성 분석 시작"** 버튼 클릭
3. **실시간 결과** 확인:
   - 기본 진실성 퍼센테이지
   - 신뢰도 점수
   - 거짓말 감지 여부
   - 교정 제안 (필요시)
   - 고급 탐지기 결과:
     - 메타-진실성 탐지 결과
     - 종교적 맥락 인식 결과
     - 과학적 사실 검증 결과
     - 의도적 거짓말 탐지 결과
     - 인간 행동 패턴 분석 결과
     - 선의의 거짓말 인식 결과
     - 맥락 인식 탐지 결과
     - 복합 문장 분석 결과
     - 코딩 품질 탐지 결과
     - 다국어 분석 결과
     - 말장난 탐지 결과

### 3. 대시보드 모니터링
1. **대시보드** 페이지로 이동
2. **통계 카드**에서 전체 현황 확인
3. **차트**에서 트렌드 분석
4. **상세 테이블**에서 개별 결과 검토

### 4. API 사용 (고급 사용자)
```bash
# 문장 분석 API 호출 예시
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"statement": "지구는 완전히 평평하다."}'
```

---

## 🔍 테스트 및 검증

### 1. 기본 테스트
```bash
# 빠른 기능 테스트
python quick_test.py
```

### 2. 종합 테스트
```bash
# 전체 테스트 스위트 실행
python test_truth_detector.py

# 자동 교정 테스트
python test_auto_correction.py

# 코딩 품질 테스트
python test_coding.py

# 다국어 및 말장난 테스트
python test_multilingual_puns.py

# 말장난 테스트
python test_puns.py
```

### 3. 성능 테스트
```bash
# 벤치마크 실행
python -c "from test_truth_detector import TruthDetectorBenchmark; TruthDetectorBenchmark().run_performance_test(100)"

# 검증 방법 데모
python verification_methods_demo.py
```

---

## 🛠️ 문제 해결

### 일반적인 문제들

#### 1. 모듈 Import 오류
```bash
# 오류: ModuleNotFoundError
# 해결책: 의존성 재설치
pip install -r requirements.txt --force-reinstall
```

#### 2. 포트 충돌 오류
```bash
# 오류: Address already in use
# 해결책: 다른 포트 사용
python app.py --port 5001
```

#### 3. 메모리 부족 오류
```bash
# 오류: MemoryError
# 해결책: 가상환경에서 실행하거나 메모리 정리
```

#### 4. 브라우저 접속 불가
- 방화벽 설정 확인
- `localhost` 대신 `127.0.0.1:5000` 사용
- 다른 브라우저로 시도

### 로그 확인
```bash
# 애플리케이션 로그 확인
tail -f app.log
```

---

## ⚙️ 고급 설정

### 1. 환경 변수 설정
```bash
# Windows
set FLASK_ENV=development
set FLASK_DEBUG=1

# macOS/Linux
export FLASK_ENV=development
export FLASK_DEBUG=1
```

### 2. 설정 파일 수정
```python
# app.py에서 설정 변경
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### 3. 탐지기 설정
```python
# 개별 탐지기 초기화
from meta_truth_detector import MetaTruthDetector
from religious_context_detector import ReligiousContextDetector
from enhanced_scientific_detector import EnhancedScientificDetector
from intentional_lie_detector import IntentionalLieDetector
from human_behavior_detector import HumanBehaviorDetector
from benevolent_lie_detector import BenevolentLieDetector
from context_awareness_detector import ContextAwarenessDetector
from compound_sentence_analyzer import CompoundSentenceAnalyzer
from coding_quality_detector import CodingQualityDetector
from multilingual_analyzer import MultilingualAnalyzer
from puns_detector import PunsDetector
from correction_capability_enhancer import CorrectionCapabilityEnhancer

# 탐지기 인스턴스 생성
meta_detector = MetaTruthDetector()
religious_detector = ReligiousContextDetector()
scientific_detector = EnhancedScientificDetector()
# ... 기타 탐지기들
```

### 4. 데이터베이스 설정 (향후 확장)
```python
# SQLite 데이터베이스 사용
import sqlite3
conn = sqlite3.connect('truth_analysis.db')
```

### 5. 로깅 설정
```python
# 로그 레벨 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

---

## 📊 성능 최적화

### 1. 메모리 사용량 최적화
```bash
# 가상환경 사용
python -m venv ai_truth_env
ai_truth_env\Scripts\activate
```

### 2. 처리 속도 향상
```python
# 배치 처리 설정
BATCH_SIZE = 10
MAX_WORKERS = 4
```

### 3. 캐싱 설정
```python
# 결과 캐싱
from functools import lru_cache

@lru_cache(maxsize=128)
def analyze_statement_cached(statement):
    return detector.analyze_statement(statement)
```

---

## 🔒 보안 설정

### 1. HTTPS 설정 (프로덕션)
```python
# SSL 인증서 설정
app.run(ssl_context='adhoc')
```

### 2. 접근 제한
```python
# IP 화이트리스트
ALLOWED_IPS = ['127.0.0.1', '192.168.1.0/24']
```

### 3. API 키 인증 (향후)
```python
# API 키 검증
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != 'your-api-key':
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function
```

---

## 📈 모니터링 및 유지보수

### 1. 시스템 모니터링
```bash
# CPU/메모리 사용량 확인
# Windows:
tasklist /fi "imagename eq python.exe"
# macOS/Linux:
ps aux | grep python
```

### 2. 로그 분석
```bash
# 에러 로그 확인
grep "ERROR" app.log
```

### 3. 정기 업데이트
```bash
# 패키지 업데이트 확인
pip list --outdated
pip install --upgrade package_name

# 로그 시스템 업데이트 확인
python logs/change_tracker.py check

# 버전 히스토리 확인
python logs/change_tracker.py history
```

---

## 🆘 지원 및 문의

### 문제 발생 시
1. **로그 파일** 확인: `app.log`
2. **에러 메시지** 복사
3. **시스템 정보** 수집:
   ```bash
   python --version
   pip list
   ```

### 추가 도움
- GitHub Issues: 프로젝트 저장소
- 문서: README.md 참조
- 테스트: test_truth_detector.py 실행

---

## 📝 실행 체크리스트

### 설치 전 확인사항
- [ ] Python 3.8+ 설치됨
- [ ] pip 최신 버전
- [ ] 인터넷 연결 확인
- [ ] 충분한 저장공간 (2GB+)

### 설치 과정
- [ ] 프로젝트 디렉토리로 이동
- [ ] 가상환경 생성 (권장)
- [ ] requirements.txt 설치
- [ ] quick_test.py 실행

### 실행 확인
- [ ] python app.py 실행
- [ ] 브라우저에서 localhost:5000 접속
- [ ] 테스트 문장 입력 및 분석
- [ ] 기본 진실성 분석 결과 확인
- [ ] 고급 탐지기 결과 확인
- [ ] 대시보드 확인
- [ ] 자동 교정 기능 확인

### 문제 해결
- [ ] 로그 파일 확인
- [ ] 의존성 재설치
- [ ] 포트 변경 시도
- [ ] 브라우저 캐시 삭제

---

**🎉 축하합니다! AI 진실성 탐지기가 성공적으로 실행되었습니다.**

이제 AI의 거짓말을 탐지하고 교정하는 고도화된 시스템을 사용할 수 있습니다. 
- **12개의 고급 탐지기**로 다각도 분석
- **자동 교정 시스템**으로 실시간 개선
- **웹 기반 대시보드**로 직관적 모니터링
- **종합적인 진실성 평가**로 신뢰할 수 있는 결과

"AI는 깨진 거울이다"라는 철학을 바탕으로 더 신뢰할 수 있는 AI를 만들어가세요!

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

### 저장소 구성
- **README**: 프로젝트 요약, 기술 스택, 담당 역할, 성과 지표, 스크린샷/데모 링크, 위 '사용 제한' 문구
- **LICENSE**: 전용 라이선스 텍스트
- **NOTICE**: 제3자 라이브러리 사용 시 해당 라이선스 고지

### 코드 주석
핵심 파일 상단에 저작권/사용 제한 주석 반복 표기

### 데모
기능 데모 링크(예: 배포된 웹앱), 혹은 화면 녹화 영상
실행용 시드 데이터는 최소화, 비밀키/환경변수는 절대 푸시 금지

### 자동화
저장소 설명(Description)에 "For portfolio review only. No permission to use." 간단 표기
