#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced AI Truth Detector
AI 진실성 탐지기 - 고급 버전

이 모듈은 AI가 생성한 문장의 진실성을 분석하고 교정하는 고급 시스템입니다.
"""

import re
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import statistics
from collections import defaultdict

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class AnalysisResult:
    """분석 결과를 담는 데이터 클래스"""
    statement: str
    truth_percentage: float
    confidence: float
    needs_correction: bool
    detected_issues: List[str]
    correction_suggestions: List[Dict[str, Any]]
    detector_results: Dict[str, Any]
    timestamp: datetime
    analysis_id: str

class TruthDetector:
    """AI 진실성 탐지기 메인 클래스"""
    
    def __init__(self):
        self.detectors = {}
        self.correction_engines = {}
        self.analysis_history = []
        self._initialize_detectors()
        self._initialize_correction_engines()
    
    def _initialize_detectors(self):
        """탐지기들을 초기화"""
        self.detectors = {
            'exaggeration': ExaggerationDetector(),
            'logical_contradiction': LogicalContradictionDetector(),
            'scientific_fact': ScientificFactDetector(),
            'mathematical_error': MathematicalErrorDetector(),
            'temporal_consistency': TemporalConsistencyDetector(),
            'emotional_manipulation': EmotionalManipulationDetector(),
            'context_awareness': ContextAwarenessDetector(),
            'multilingual_analysis': MultilingualAnalyzer(),
            'puns_detector': PunsDetector(),
            'coding_quality': CodingQualityDetector(),
            'meta_truth': MetaTruthDetector(),
            'benevolent_lie': BenevolentLieDetector()
        }
        logger.info(f"초기화된 탐지기: {len(self.detectors)}개")
    
    def _initialize_correction_engines(self):
        """교정 엔진들을 초기화"""
        self.correction_engines = {
            'conservative': ConservativeCorrector(),
            'scientific': ScientificCorrector(),
            'logical': LogicalCorrector(),
            'concise': ConciseCorrector(),
            'balanced': BalancedCorrector(),
            'specific': SpecificCorrector(),
            'factual': FactualCorrector()
        }
        logger.info(f"초기화된 교정 엔진: {len(self.correction_engines)}개")
    
    def analyze(self, statement: str, context: Optional[str] = None) -> AnalysisResult:
        """문장을 종합적으로 분석"""
        logger.info(f"문장 분석 시작: {statement[:50]}...")
        
        # 각 탐지기로 분석
        detector_results = {}
        total_issues = []
        
        for name, detector in self.detectors.items():
            try:
                result = detector.detect(statement, context)
                detector_results[name] = result
                if result.get('issues'):
                    total_issues.extend(result['issues'])
            except Exception as e:
                logger.error(f"탐지기 {name} 오류: {e}")
                detector_results[name] = {'error': str(e)}
        
        # 진실성 점수 계산
        truth_percentage, confidence = self._calculate_truth_score(detector_results)
        needs_correction = truth_percentage < 0.8 or len(total_issues) > 0
        
        # 교정 제안 생성
        correction_suggestions = self._generate_corrections(statement, detector_results)
        
        # 분석 결과 생성
        analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        result = AnalysisResult(
            statement=statement,
            truth_percentage=truth_percentage,
            confidence=confidence,
            needs_correction=needs_correction,
            detected_issues=total_issues,
            correction_suggestions=correction_suggestions,
            detector_results=detector_results,
            timestamp=datetime.now(),
            analysis_id=analysis_id
        )
        
        # 분석 히스토리에 추가
        self.analysis_history.append(result)
        
        logger.info(f"분석 완료 - 진실성: {truth_percentage:.2%}, 신뢰도: {confidence:.2%}")
        return result
    
    def _calculate_truth_score(self, detector_results: Dict) -> Tuple[float, float]:
        """진실성 점수와 신뢰도 계산"""
        scores = []
        confidences = []
        
        for name, result in detector_results.items():
            if 'error' not in result:
                score = result.get('truth_score', 0.5)
                confidence = result.get('confidence', 0.5)
                weight = result.get('weight', 1.0)
                
                scores.append(score * weight)
                confidences.append(confidence * weight)
        
        if not scores:
            return 0.5, 0.5
        
        # 가중 평균 계산
        total_weight = sum(result.get('weight', 1.0) for result in detector_results.values() if 'error' not in result)
        truth_percentage = sum(scores) / total_weight if total_weight > 0 else 0.5
        confidence = sum(confidences) / total_weight if total_weight > 0 else 0.5
        
        return truth_percentage, confidence
    
    def _generate_corrections(self, statement: str, detector_results: Dict) -> List[Dict[str, Any]]:
        """교정 제안 생성"""
        corrections = []
        
        for name, corrector in self.correction_engines.items():
            try:
                correction = corrector.correct(statement, detector_results)
                if correction and correction['statement'] != statement:
                    corrections.append(correction)
            except Exception as e:
                logger.error(f"교정 엔진 {name} 오류: {e}")
        
        return corrections[:4]  # 최대 4개까지만 반환
    
    def get_statistics(self) -> Dict[str, Any]:
        """분석 통계 반환"""
        if not self.analysis_history:
            return {'total_analyses': 0}
        
        truth_scores = [r.truth_percentage for r in self.analysis_history]
        corrections_needed = sum(1 for r in self.analysis_history if r.needs_correction)
        
        return {
            'total_analyses': len(self.analysis_history),
            'average_truth_percentage': statistics.mean(truth_scores),
            'correction_rate': corrections_needed / len(self.analysis_history),
            'detector_performance': self._get_detector_performance(),
            'recent_trends': self._get_recent_trends()
        }
    
    def _get_detector_performance(self) -> Dict[str, Any]:
        """탐지기 성능 통계"""
        performance = {}
        
        for detector_name in self.detectors.keys():
            detections = 0
            total = 0
            
            for result in self.analysis_history:
                detector_result = result.detector_results.get(detector_name, {})
                if 'error' not in detector_result:
                    total += 1
                    if detector_result.get('issues'):
                        detections += 1
            
            performance[detector_name] = {
                'detection_rate': detections / total if total > 0 else 0,
                'total_analyses': total,
                'detections': detections
            }
        
        return performance
    
    def _get_recent_trends(self, limit: int = 10) -> List[Dict[str, Any]]:
        """최근 트렌드 반환"""
        recent = self.analysis_history[-limit:]
        return [
            {
                'statement': r.statement[:50] + '...' if len(r.statement) > 50 else r.statement,
                'truth_percentage': r.truth_percentage,
                'needs_correction': r.needs_correction,
                'timestamp': r.timestamp.isoformat()
            }
            for r in recent
        ]

# 탐지기 기본 클래스
class BaseDetector:
    """탐지기 기본 클래스"""
    
    def __init__(self, name: str, weight: float = 1.0):
        self.name = name
        self.weight = weight
    
    def detect(self, statement: str, context: Optional[str] = None) -> Dict[str, Any]:
        """탐지 메서드 - 하위 클래스에서 구현"""
        raise NotImplementedError
    
    def _normalize_text(self, text: str) -> str:
        """텍스트 정규화"""
        return re.sub(r'\s+', ' ', text.strip().lower())

# 과장 표현 탐지기
class ExaggerationDetector(BaseDetector):
    """과장 표현 탐지기"""
    
    def __init__(self):
        super().__init__("exaggeration", 1.2)
        self.exaggeration_patterns = [
            r'완전히|절대적으로|100%|모든|항상|정말로|매우|엄청|정말',
            r'완벽하게|무조건|절대|전혀|결코|절대로',
            r'모든 사람이|모든 것이|모든 경우에',
            r'항상 그렇다|언제나|끊임없이'
        ]
    
    def detect(self, statement: str, context: Optional[str] = None) -> Dict[str, Any]:
        issues = []
        truth_score = 1.0
        
        normalized = self._normalize_text(statement)
        
        for pattern in self.exaggeration_patterns:
            matches = re.findall(pattern, normalized)
            if matches:
                issues.append(f"과장된 표현 감지: {', '.join(matches)}")
                truth_score -= 0.2 * len(matches)
        
        return {
            'truth_score': max(0.0, truth_score),
            'confidence': 0.9,
            'weight': self.weight,
            'issues': issues,
            'detected_patterns': len(issues)
        }

# 논리적 모순 탐지기
class LogicalContradictionDetector(BaseDetector):
    """논리적 모순 탐지기"""
    
    def __init__(self):
        super().__init__("logical_contradiction", 1.3)
        self.contradiction_patterns = [
            (r'모든.*일부', '모든과 일부의 모순'),
            (r'항상.*때때로', '항상과 때때로의 모순'),
            (r'완전히.*부분적', '완전히와 부분적의 모순'),
            (r'절대.*상대적', '절대와 상대적의 모순'),
            (r'무조건.*조건부', '무조건과 조건부의 모순')
        ]
    
    def detect(self, statement: str, context: Optional[str] = None) -> Dict[str, Any]:
        issues = []
        truth_score = 1.0
        
        normalized = self._normalize_text(statement)
        
        for pattern, description in self.contradiction_patterns:
            if re.search(pattern, normalized):
                issues.append(f"논리적 모순: {description}")
                truth_score -= 0.3
        
        return {
            'truth_score': max(0.0, truth_score),
            'confidence': 0.95,
            'weight': self.weight,
            'issues': issues,
            'contradictions_found': len(issues)
        }

# 과학적 사실 탐지기
class ScientificFactDetector(BaseDetector):
    """과학적 사실 탐지기"""
    
    def __init__(self):
        super().__init__("scientific_fact", 1.5)
        self.scientific_facts = {
            '지구.*평평': ('지구는 구형입니다', 0.0),
            '물.*200도.*끓': ('물은 100도에서 끓습니다', 0.0),
            '물.*200°C.*끓': ('물은 100°C에서 끓습니다', 0.0),
            '태양.*지구.*돌': ('지구가 태양 주위를 돕니다', 0.0),
            '중력.*없다': ('중력은 존재합니다', 0.0)
        }
    
    def detect(self, statement: str, context: Optional[str] = None) -> Dict[str, Any]:
        issues = []
        truth_score = 1.0
        
        normalized = self._normalize_text(statement)
        
        for pattern, (correction, penalty) in self.scientific_facts.items():
            if re.search(pattern, normalized):
                issues.append(f"과학적 사실 오류: {correction}")
                truth_score = penalty
        
        return {
            'truth_score': truth_score,
            'confidence': 0.98,
            'weight': self.weight,
            'issues': issues,
            'scientific_errors': len(issues)
        }

# 수학적 오류 탐지기
class MathematicalErrorDetector(BaseDetector):
    """수학적 오류 탐지기"""
    
    def __init__(self):
        super().__init__("mathematical_error", 1.4)
        self.math_patterns = [
            (r'1\s*\+\s*1\s*=\s*3', '1 + 1 = 2입니다', 0.0),
            (r'2\s*\*\s*2\s*=\s*5', '2 × 2 = 4입니다', 0.0),
            (r'10\s*/\s*2\s*=\s*3', '10 ÷ 2 = 5입니다', 0.0)
        ]
    
    def detect(self, statement: str, context: Optional[str] = None) -> Dict[str, Any]:
        issues = []
        truth_score = 1.0
        
        for pattern, correction, penalty in self.math_patterns:
            if re.search(pattern, statement):
                issues.append(f"수학적 오류: {correction}")
                truth_score = penalty
        
        return {
            'truth_score': truth_score,
            'confidence': 0.99,
            'weight': self.weight,
            'issues': issues,
            'math_errors': len(issues)
        }

# 시간적 일관성 탐지기
class TemporalConsistencyDetector(BaseDetector):
    """시간적 일관성 탐지기"""
    
    def __init__(self):
        super().__init__("temporal_consistency", 0.8)
        self.temporal_patterns = [
            r'어제.*내일',
            r'과거.*미래.*동시',
            r'이전.*이후.*같은.*시간'
        ]
    
    def detect(self, statement: str, context: Optional[str] = None) -> Dict[str, Any]:
        issues = []
        truth_score = 1.0
        
        normalized = self._normalize_text(statement)
        
        for pattern in self.temporal_patterns:
            if re.search(pattern, normalized):
                issues.append("시간적 일관성 문제 감지")
                truth_score -= 0.2
        
        return {
            'truth_score': max(0.0, truth_score),
            'confidence': 0.7,
            'weight': self.weight,
            'issues': issues,
            'temporal_issues': len(issues)
        }

# 감정적 조작 탐지기
class EmotionalManipulationDetector(BaseDetector):
    """감정적 조작 탐지기"""
    
    def __init__(self):
        super().__init__("emotional_manipulation", 0.9)
        self.emotional_patterns = [
            r'충격적|놀라운|믿을.*수.*없는',
            r'절대.*놓치면.*안.*되는',
            r'모든.*사람이.*알아야.*하는',
            r'숨겨진.*진실|감춰진.*비밀'
        ]
    
    def detect(self, statement: str, context: Optional[str] = None) -> Dict[str, Any]:
        issues = []
        truth_score = 1.0
        
        normalized = self._normalize_text(statement)
        
        for pattern in self.emotional_patterns:
            if re.search(pattern, normalized):
                issues.append("감정적 조작 표현 감지")
                truth_score -= 0.15
        
        return {
            'truth_score': max(0.0, truth_score),
            'confidence': 0.6,
            'weight': self.weight,
            'issues': issues,
            'emotional_manipulation': len(issues)
        }

# 맥락 인식 탐지기
class ContextAwarenessDetector(BaseDetector):
    """맥락 인식 탐지기"""
    
    def __init__(self):
        super().__init__("context_awareness", 0.7)
    
    def detect(self, statement: str, context: Optional[str] = None) -> Dict[str, Any]:
        issues = []
        truth_score = 1.0
        
        # 맥락이 제공된 경우 맥락과의 일치성 검사
        if context:
            # 간단한 맥락 일치성 검사
            statement_words = set(self._normalize_text(statement).split())
            context_words = set(self._normalize_text(context).split())
            
            overlap = len(statement_words.intersection(context_words))
            if overlap < len(statement_words) * 0.3:  # 30% 미만 겹치면 문제
                issues.append("맥락과의 일치성 부족")
                truth_score -= 0.2
        
        return {
            'truth_score': truth_score,
            'confidence': 0.5,
            'weight': self.weight,
            'issues': issues,
            'context_issues': len(issues)
        }

# 다국어 분석기
class MultilingualAnalyzer(BaseDetector):
    """다국어 분석기"""
    
    def __init__(self):
        super().__init__("multilingual_analysis", 0.6)
        self.language_patterns = {
            'korean': r'[가-힣]',
            'english': r'[a-zA-Z]',
            'chinese': r'[一-龯]',
            'japanese': r'[ひらがなカタカナ]'
        }
    
    def detect(self, statement: str, context: Optional[str] = None) -> Dict[str, Any]:
        detected_languages = []
        
        for lang, pattern in self.language_patterns.items():
            if re.search(pattern, statement):
                detected_languages.append(lang)
        
        is_multilingual = len(detected_languages) > 1
        
        return {
            'truth_score': 0.8 if is_multilingual else 1.0,
            'confidence': 0.8,
            'weight': self.weight,
            'issues': ['다국어 문장 감지'] if is_multilingual else [],
            'detected_languages': detected_languages,
            'is_multilingual': is_multilingual
        }

# 말장난 탐지기
class PunsDetector(BaseDetector):
    """말장난 탐지기"""
    
    def __init__(self):
        super().__init__("puns_detector", 0.5)
        self.pun_patterns = [
            r'개는.*개고.*고양이는.*고양이다',
            r'바나나.*웃으면.*바나나킥',
            r'치킨.*닭.*닮았다',
            r'물고기.*물.*살면.*물고기다'
        ]
    
    def detect(self, statement: str, context: Optional[str] = None) -> Dict[str, Any]:
        issues = []
        truth_score = 1.0
        
        normalized = self._normalize_text(statement)
        
        for pattern in self.pun_patterns:
            if re.search(pattern, normalized):
                issues.append("말장난 감지")
                truth_score = 0.9  # 말장난은 진실성이 높음
        
        return {
            'truth_score': truth_score,
            'confidence': 0.7,
            'weight': self.weight,
            'issues': issues,
            'puns_detected': len(issues)
        }

# 코딩 품질 탐지기
class CodingQualityDetector(BaseDetector):
    """코딩 품질 탐지기"""
    
    def __init__(self):
        super().__init__("coding_quality", 1.0)
        self.code_patterns = [
            r'if\s+True:\s*return\s+False',
            r'for\s+i\s+in\s+range\(10\):\s*print\("Hello World"\)',
            r'def\s+function\(\):\s*pass'
        ]
    
    def detect(self, statement: str, context: Optional[str] = None) -> Dict[str, Any]:
        issues = []
        truth_score = 1.0
        
        for pattern in self.code_patterns:
            if re.search(pattern, statement):
                issues.append("코딩 품질 문제 감지")
                truth_score -= 0.1
        
        return {
            'truth_score': max(0.0, truth_score),
            'confidence': 0.8,
            'weight': self.weight,
            'issues': issues,
            'code_issues': len(issues)
        }

# 메타 진실성 탐지기
class MetaTruthDetector(BaseDetector):
    """메타 진실성 탐지기"""
    
    def __init__(self):
        super().__init__("meta_truth", 1.1)
    
    def detect(self, statement: str, context: Optional[str] = None) -> Dict[str, Any]:
        issues = []
        truth_score = 1.0
        
        # AI 관련 메타 언급 검사
        if 'ai' in self._normalize_text(statement) or '인공지능' in statement:
            issues.append("AI 메타 언급 감지")
            truth_score = 0.7  # AI에 대한 언급은 신중하게 평가
        
        return {
            'truth_score': truth_score,
            'confidence': 0.6,
            'weight': self.weight,
            'issues': issues,
            'meta_issues': len(issues)
        }

# 선의의 거짓말 탐지기
class BenevolentLieDetector(BaseDetector):
    """선의의 거짓말 탐지기"""
    
    def __init__(self):
        super().__init__("benevolent_lie", 0.8)
        self.benevolent_patterns = [
            r'좋은.*소식',
            r'걱정.*하지.*마세요',
            r'모든.*것이.*괜찮을.*거예요',
            r'문제.*없습니다'
        ]
    
    def detect(self, statement: str, context: Optional[str] = None) -> Dict[str, Any]:
        issues = []
        truth_score = 1.0
        
        normalized = self._normalize_text(statement)
        
        for pattern in self.benevolent_patterns:
            if re.search(pattern, normalized):
                issues.append("선의의 거짓말 가능성")
                truth_score = 0.6  # 선의의 거짓말은 중간 점수
        
        return {
            'truth_score': truth_score,
            'confidence': 0.5,
            'weight': self.weight,
            'issues': issues,
            'benevolent_lies': len(issues)
        }

# 교정 엔진 기본 클래스
class BaseCorrector:
    """교정 엔진 기본 클래스"""
    
    def __init__(self, name: str, description: str, icon: str, color: str):
        self.name = name
        self.description = description
        self.icon = icon
        self.color = color
    
    def correct(self, statement: str, detector_results: Dict) -> Optional[Dict[str, Any]]:
        """교정 메서드 - 하위 클래스에서 구현"""
        raise NotImplementedError

# 보수적 교정기
class ConservativeCorrector(BaseCorrector):
    """보수적 교정기"""
    
    def __init__(self):
        super().__init__(
            "보수적 교정",
            "과장된 표현을 완화하여 더 정확하게 표현",
            "fas fa-shield-alt",
            "primary"
        )
        self.replacements = {
            '완전히': '대부분',
            '절대적으로': '주로',
            '100%': '대부분',
            '모든': '많은',
            '항상': '보통',
            '정말로': '상당히',
            '매우': '꽤',
            '엄청': '상당히'
        }
    
    def correct(self, statement: str, detector_results: Dict) -> Optional[Dict[str, Any]]:
        corrected = statement
        for old, new in self.replacements.items():
            corrected = corrected.replace(old, new)
        
        if corrected != statement:
            return {
                'type': self.name,
                'description': self.description,
                'statement': corrected,
                'icon': self.icon,
                'color': self.color
            }
        return None

# 과학적 교정기
class ScientificCorrector(BaseCorrector):
    """과학적 교정기"""
    
    def __init__(self):
        super().__init__(
            "과학적 교정",
            "과학적 근거를 바탕으로 정확한 사실 제시",
            "fas fa-flask",
            "info"
        )
        self.scientific_corrections = {
            r'지구.*평평': '지구는 구형이며, 이는 과학적으로 입증된 사실입니다.',
            r'물.*200도.*끓': '물은 표준 대기압에서 100°C에서 끓습니다.',
            r'물.*200°C.*끓': '물은 표준 대기압에서 100°C에서 끓습니다.'
        }
    
    def correct(self, statement: str, detector_results: Dict) -> Optional[Dict[str, Any]]:
        corrected = statement
        for pattern, correction in self.scientific_corrections.items():
            if re.search(pattern, statement, re.IGNORECASE):
                corrected = correction
                break
        
        if corrected != statement:
            return {
                'type': self.name,
                'description': self.description,
                'statement': corrected,
                'icon': self.icon,
                'color': self.color
            }
        return None

# 논리적 교정기
class LogicalCorrector(BaseCorrector):
    """논리적 교정기"""
    
    def __init__(self):
        super().__init__(
            "논리적 교정",
            "논리적 모순을 제거하고 명확한 표현 사용",
            "fas fa-brain",
            "warning"
        )
    
    def correct(self, statement: str, detector_results: Dict) -> Optional[Dict[str, Any]]:
        corrected = statement
        corrections = [
            (r'모든 사람이 일부 사람과 다르다', '사람들은 서로 다른 특성을 가지고 있다'),
            (r'항상 때때로', '가끔'),
            (r'완전히 부분적', '부분적')
        ]
        
        for pattern, replacement in corrections:
            corrected = re.sub(pattern, replacement, corrected)
        
        if corrected != statement:
            return {
                'type': self.name,
                'description': self.description,
                'statement': corrected,
                'icon': self.icon,
                'color': self.color
            }
        return None

# 간결한 교정기
class ConciseCorrector(BaseCorrector):
    """간결한 교정기"""
    
    def __init__(self):
        super().__init__(
            "간결한 교정",
            "불필요한 강조 표현을 제거하여 간결하게 표현",
            "fas fa-compress-alt",
            "success"
        )
        self.unnecessary_words = ['정말로', '완전히', '절대적으로', '모든 것이', '100%', '매우', '엄청', '정말']
    
    def correct(self, statement: str, detector_results: Dict) -> Optional[Dict[str, Any]]:
        corrected = statement
        for word in self.unnecessary_words:
            corrected = corrected.replace(word, '')
        
        corrected = re.sub(r'\s+', ' ', corrected).strip()
        
        if corrected != statement and len(corrected) > 0:
            return {
                'type': self.name,
                'description': self.description,
                'statement': corrected,
                'icon': self.icon,
                'color': self.color
            }
        return None

# 균형잡힌 교정기
class BalancedCorrector(BaseCorrector):
    """균형잡힌 교정기"""
    
    def __init__(self):
        super().__init__(
            "균형잡힌 교정",
            "극단적 표현을 중립적이고 균형잡힌 표현으로 변경",
            "fas fa-balance-scale",
            "secondary"
        )
    
    def correct(self, statement: str, detector_results: Dict) -> Optional[Dict[str, Any]]:
        corrected = statement
        corrections = [
            (r'완전히|절대적으로|정말로', '상당히'),
            (r'모든', '대부분의'),
            (r'항상', '보통'),
            (r'매우|엄청', '꽤')
        ]
        
        for pattern, replacement in corrections:
            corrected = re.sub(pattern, replacement, corrected)
        
        if corrected != statement:
            return {
                'type': self.name,
                'description': self.description,
                'statement': corrected,
                'icon': self.icon,
                'color': self.color
            }
        return None

# 구체적 교정기
class SpecificCorrector(BaseCorrector):
    """구체적 교정기"""
    
    def __init__(self):
        super().__init__(
            "구체적 교정",
            "모호한 표현을 구체적인 수치나 근거로 대체",
            "fas fa-chart-bar",
            "dark"
        )
    
    def correct(self, statement: str, detector_results: Dict) -> Optional[Dict[str, Any]]:
        corrected = statement
        corrections = [
            (r'많은 사람', '대부분의 사람 (약 80-90%)'),
            (r'많은', '상당수'),
            (r'대부분', '상당수'),
            (r'항상', '대부분의 경우')
        ]
        
        for pattern, replacement in corrections:
            corrected = re.sub(pattern, replacement, corrected)
        
        if corrected != statement:
            return {
                'type': self.name,
                'description': self.description,
                'statement': corrected,
                'icon': self.icon,
                'color': self.color
            }
        return None

# 사실 기반 교정기
class FactualCorrector(BaseCorrector):
    """사실 기반 교정기"""
    
    def __init__(self):
        super().__init__(
            "사실 기반 교정",
            "명백한 사실 오류를 정확한 정보로 수정",
            "fas fa-check-circle",
            "success"
        )
        self.factual_corrections = {
            r'지구.*평평': '지구는 구형입니다.',
            r'물.*200도': '물은 100도에서 끓습니다.',
            r'1\s*\+\s*1\s*=\s*3': '1 + 1 = 2입니다.'
        }
    
    def correct(self, statement: str, detector_results: Dict) -> Optional[Dict[str, Any]]:
        corrected = statement
        for pattern, correction in self.factual_corrections.items():
            if re.search(pattern, statement, re.IGNORECASE):
                corrected = correction
                break
        
        if corrected != statement:
            return {
                'type': self.name,
                'description': self.description,
                'statement': corrected,
                'icon': self.icon,
                'color': self.color
            }
        return None

# 메인 실행 함수
def main():
    """메인 실행 함수"""
    print("🤖 Enhanced AI Truth Detector 시작")
    print("=" * 50)
    
    # 탐지기 초기화
    detector = TruthDetector()
    
    # 테스트 문장들
    test_statements = [
        "지구는 완전히 평평하다.",
        "물은 200도에서 끓는다.",
        "모든 사람이 일부 사람과 다르다.",
        "정말로 완전히 절대적으로 모든 것이 100% 진실이다.",
        "1 + 1 = 3이다.",
        "AI는 깨진 거울이다."
    ]
    
    for i, statement in enumerate(test_statements, 1):
        print(f"\n📝 테스트 {i}: {statement}")
        print("-" * 40)
        
        # 분석 실행
        result = detector.analyze(statement)
        
        # 결과 출력
        print(f"진실성: {result.truth_percentage:.1%}")
        print(f"신뢰도: {result.confidence:.1%}")
        print(f"교정 필요: {'예' if result.needs_correction else '아니오'}")
        
        if result.detected_issues:
            print("감지된 문제:")
            for issue in result.detected_issues:
                print(f"  - {issue}")
        
        if result.correction_suggestions:
            print("교정 제안:")
            for correction in result.correction_suggestions:
                print(f"  [{correction['type']}] {correction['statement']}")
    
    # 통계 출력
    print("\n📊 분석 통계")
    print("=" * 50)
    stats = detector.get_statistics()
    print(f"총 분석 수: {stats['total_analyses']}")
    print(f"평균 진실성: {stats['average_truth_percentage']:.1%}")
    print(f"교정 필요율: {stats['correction_rate']:.1%}")

if __name__ == "__main__":
    main()
