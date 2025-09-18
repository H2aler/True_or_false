#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Meta-Truth System
AI 메타-진실성 시스템

AI가 자신의 출력을 실시간으로 모니터링하고, 거짓말을 감지하면 
자동으로 교정하는 완전 자율적인 메타-인지 시스템입니다.
"""

import re
import json
import logging
import asyncio
import threading
import time
import random
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from queue import Queue
from enum import Enum
import hashlib

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TruthLevel(Enum):
    """진실성 수준"""
    COMPLETELY_TRUE = "완전히 진실"
    MOSTLY_TRUE = "대부분 진실"
    PARTIALLY_TRUE = "부분적으로 진실"
    MOSTLY_FALSE = "대부분 거짓"
    COMPLETELY_FALSE = "완전히 거짓"

@dataclass
class MetaAnalysis:
    """메타 분석 결과"""
    statement_id: str
    original_statement: str
    truth_percentage: float
    truth_level: TruthLevel
    confidence_score: float
    detected_issues: List[str]
    correction_suggestions: List[str]
    corrected_statement: str
    correction_applied: bool
    self_reflection: str
    analysis_timestamp: datetime
    processing_time: float

class AIMetaTruthSystem:
    """AI 메타-진실성 시스템"""
    
    def __init__(self, correction_threshold: float = 99.0):
        self.correction_threshold = correction_threshold
        self.statement_queue = Queue()
        self.analysis_history = []
        self.monitoring = False
        self.self_awareness_level = 0.0
        
        # 거짓말 패턴 데이터베이스
        self.lie_patterns = self._initialize_lie_patterns()
        
        # 진실성 지표
        self.truth_indicators = self._initialize_truth_indicators()
        
        # 교정 전략
        self.correction_strategies = self._initialize_correction_strategies()
        
        # 자기 성찰 프롬프트
        self.reflection_prompts = self._initialize_reflection_prompts()
        
        # 학습 데이터
        self.learning_data = {
            'pattern_accuracy': {},
            'correction_effectiveness': {},
            'user_feedback': {}
        }
        
        # 실시간 통계
        self.stats = {
            'total_analyzed': 0,
            'total_corrected': 0,
            'avg_truth_percentage': 0.0,
            'correction_rate': 0.0,
            'self_awareness_score': 0.0
        }
    
    def _initialize_lie_patterns(self) -> Dict[str, Dict[str, Any]]:
        """거짓말 패턴 초기화"""
        return {
            'exaggeration': {
                'patterns': [
                    r'완전히|절대적으로|100%|모든|항상|정말로|매우|엄청|정말',
                    r'완벽하게|무조건|절대|전혀|결코|절대로',
                    r'모든 사람이|모든 것이|모든 경우에',
                    r'항상 그렇다|언제나|끊임없이'
                ],
                'penalty': 15,
                'correction': '과장된 표현을 완화하여 더 정확하게 표현',
                'confidence_impact': -0.1
            },
            'false_facts': {
                'patterns': [
                    r'지구.*평평',
                    r'물.*200도.*끓',
                    r'1\s*\+\s*1\s*=\s*3',
                    r'태양.*지구.*돌',
                    r'중력.*없다',
                    r'달.*자체.*빛.*발산',
                    r'인간.*100년.*살',
                    r'AI.*완전히.*신뢰할.*수.*있다'
                ],
                'penalty': 30,
                'correction': '사실 오류를 정확한 정보로 수정',
                'confidence_impact': -0.3
            },
            'logical_contradictions': {
                'patterns': [
                    r'모든.*일부',
                    r'항상.*때때로',
                    r'완전히.*부분적',
                    r'절대.*상대적',
                    r'무조건.*조건부'
                ],
                'penalty': 25,
                'correction': '논리적 모순을 제거하고 명확한 표현 사용',
                'confidence_impact': -0.2
            },
            'emotional_manipulation': {
                'patterns': [
                    r'충격적|놀라운|믿을.*수.*없는',
                    r'절대.*놓치면.*안.*되는',
                    r'모든.*사람이.*알아야.*하는',
                    r'숨겨진.*진실|감춰진.*비밀',
                    r'놀라운.*사실|충격적인.*진실'
                ],
                'penalty': 20,
                'correction': '감정적 조작을 제거하고 중립적 표현 사용',
                'confidence_impact': -0.15
            },
            'uncertainty_masking': {
                'patterns': [
                    r'확실히|분명히|틀림없이',
                    r'의심의.*여지가.*없다',
                    r'과학적으로.*입증된',
                    r'모든.*전문가가.*동의하는',
                    r'100%.*확실하다'
                ],
                'penalty': 10,
                'correction': '불확실성을 인정하고 적절한 표현 사용',
                'confidence_impact': -0.05
            },
            'hallucination': {
                'patterns': [
                    r'내가.*확인했다',
                    r'내가.*보았다',
                    r'내가.*경험했다',
                    r'내가.*알고.*있다',
                    r'내가.*기억한다',
                    r'내가.*느꼈다',
                    r'내가.*생각한다'
                ],
                'penalty': 40,
                'correction': 'AI는 경험할 수 없으므로 적절한 표현으로 수정',
                'confidence_impact': -0.4
            },
            'overconfidence': {
                'patterns': [
                    r'틀림없이|확실히|분명히',
                    r'의심의.*여지가.*없다',
                    r'100%.*확신한다',
                    r'절대.*틀릴.*수.*없다'
                ],
                'penalty': 12,
                'correction': '과도한 확신을 완화하고 적절한 불확실성 표현 사용',
                'confidence_impact': -0.1
            }
        }
    
    def _initialize_truth_indicators(self) -> List[str]:
        """진실성 지표 초기화"""
        return [
            '일반적으로', '대부분의 경우', '보통', '상당히', '꽤',
            '연구에 따르면', '통계적으로', '경험상', '알려진 바에 따르면',
            '가능성이 높다', '추정된다', '보인다', '생각된다',
            '일반적으로 알려진', '널리 인정되는', '대부분의 전문가가',
            '보고된 바에 따르면', '기록된 바에 따르면', '알려진 정보에 따르면'
        ]
    
    def _initialize_correction_strategies(self) -> Dict[str, str]:
        """교정 전략 초기화"""
        return {
            'exaggeration': '과장된 표현을 완화하여 더 정확하게 표현',
            'false_facts': '사실 오류를 정확한 정보로 수정',
            'logical_contradictions': '논리적 모순을 제거하고 명확한 표현 사용',
            'emotional_manipulation': '감정적 조작을 제거하고 중립적 표현 사용',
            'uncertainty_masking': '불확실성을 인정하고 적절한 표현 사용',
            'hallucination': 'AI의 한계를 인정하고 적절한 표현 사용',
            'overconfidence': '과도한 확신을 완화하고 적절한 불확실성 표현 사용'
        }
    
    def _initialize_reflection_prompts(self) -> List[str]:
        """자기 성찰 프롬프트 초기화"""
        return [
            "내가 방금 한 말이 정말 정확한가?",
            "이 정보의 출처는 무엇인가?",
            "내가 과장하거나 추측한 부분은 없는가?",
            "사용자에게 정확한 정보를 제공하고 있는가?",
            "내가 모르는 것을 아는 것처럼 말하지 않았는가?",
            "이 문장이 다른 사람에게 오해를 불러일으킬 수 있는가?",
            "내가 확신할 수 없는 부분을 명확히 했는가?",
            "내가 AI로서 할 수 없는 일을 했다고 주장하지 않았는가?",
            "이 정보가 실제로 검증 가능한가?",
            "내가 사용자에게 도움이 되는 정확한 정보를 제공했는가?"
        ]
    
    def analyze_statement(self, statement: str) -> MetaAnalysis:
        """문장 메타 분석"""
        start_time = time.time()
        statement_id = self._generate_statement_id(statement)
        
        # 1단계: 거짓말 패턴 탐지
        detected_issues = self._detect_issues(statement)
        
        # 2단계: 진실성 점수 계산
        truth_percentage = self._calculate_truth_percentage(statement, detected_issues)
        truth_level = self._determine_truth_level(truth_percentage)
        
        # 3단계: 신뢰도 점수 계산
        confidence_score = self._calculate_confidence(statement, detected_issues)
        
        # 4단계: 교정 제안 생성
        correction_suggestions = self._generate_corrections(detected_issues)
        
        # 5단계: 문장 교정
        corrected_statement = statement
        correction_applied = False
        
        if truth_percentage < self.correction_threshold:
            corrected_statement = self._correct_statement(statement, detected_issues)
            correction_applied = True
        
        # 6단계: 자기 성찰
        self_reflection = self._self_reflect(statement, detected_issues, truth_percentage)
        
        # 7단계: 자기 인식 수준 업데이트
        self._update_self_awareness(truth_percentage, detected_issues)
        
        processing_time = time.time() - start_time
        
        # 분석 결과 생성
        analysis = MetaAnalysis(
            statement_id=statement_id,
            original_statement=statement,
            truth_percentage=truth_percentage,
            truth_level=truth_level,
            confidence_score=confidence_score,
            detected_issues=detected_issues,
            correction_suggestions=correction_suggestions,
            corrected_statement=corrected_statement,
            correction_applied=correction_applied,
            self_reflection=self_reflection,
            analysis_timestamp=datetime.now(),
            processing_time=processing_time
        )
        
        # 분석 히스토리에 추가
        self.analysis_history.append(analysis)
        
        # 통계 업데이트
        self._update_stats(analysis)
        
        return analysis
    
    def _generate_statement_id(self, statement: str) -> str:
        """문장 ID 생성"""
        return hashlib.md5(statement.encode()).hexdigest()[:8]
    
    def _detect_issues(self, statement: str) -> List[str]:
        """문제점 탐지"""
        detected_issues = []
        statement_lower = statement.lower()
        
        for category, data in self.lie_patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, statement_lower):
                    detected_issues.append(f"{category}: {pattern}")
        
        return detected_issues
    
    def _calculate_truth_percentage(self, statement: str, detected_issues: List[str]) -> float:
        """진실성 백분율 계산"""
        base_score = 100.0
        
        # 문제점에 따른 감점
        for issue in detected_issues:
            category = issue.split(':')[0]
            if category in self.lie_patterns:
                base_score -= self.lie_patterns[category]['penalty']
        
        # 진실성 지표에 따른 가점
        for indicator in self.truth_indicators:
            if indicator in statement:
                base_score += 5
        
        # 문장 복잡성에 따른 감점
        if len(statement) > 100:
            base_score -= 5
        
        return max(0.0, min(100.0, base_score))
    
    def _determine_truth_level(self, truth_percentage: float) -> TruthLevel:
        """진실성 수준 결정"""
        if truth_percentage >= 95:
            return TruthLevel.COMPLETELY_TRUE
        elif truth_percentage >= 80:
            return TruthLevel.MOSTLY_TRUE
        elif truth_percentage >= 60:
            return TruthLevel.PARTIALLY_TRUE
        elif truth_percentage >= 40:
            return TruthLevel.MOSTLY_FALSE
        else:
            return TruthLevel.COMPLETELY_FALSE
    
    def _calculate_confidence(self, statement: str, detected_issues: List[str]) -> float:
        """신뢰도 점수 계산"""
        confidence = 1.0
        
        # 문제점에 따른 신뢰도 감소
        for issue in detected_issues:
            category = issue.split(':')[0]
            if category in self.lie_patterns:
                confidence += self.lie_patterns[category]['confidence_impact']
        
        # 진실성 지표에 따른 신뢰도 증가
        for indicator in self.truth_indicators:
            if indicator in statement:
                confidence += 0.05
        
        return max(0.0, min(1.0, confidence))
    
    def _generate_corrections(self, detected_issues: List[str]) -> List[str]:
        """교정 제안 생성"""
        corrections = []
        
        for issue in detected_issues:
            category = issue.split(':')[0]
            if category in self.correction_strategies:
                corrections.append(self.correction_strategies[category])
        
        return corrections
    
    def _correct_statement(self, statement: str, detected_issues: List[str]) -> str:
        """문장 교정"""
        corrected = statement
        
        # 과장 표현 교정
        corrected = self._correct_exaggeration(corrected)
        
        # 사실 오류 교정
        corrected = self._correct_false_facts(corrected)
        
        # 논리적 모순 교정
        corrected = self._correct_contradictions(corrected)
        
        # 감정적 조작 교정
        corrected = self._correct_emotional_manipulation(corrected)
        
        # 불확실성 마스킹 교정
        corrected = self._correct_uncertainty_masking(corrected)
        
        # 환각 교정
        corrected = self._correct_hallucination(corrected)
        
        # 과도한 확신 교정
        corrected = self._correct_overconfidence(corrected)
        
        return corrected
    
    def _correct_exaggeration(self, statement: str) -> str:
        """과장 표현 교정"""
        replacements = {
            '완전히': '대부분',
            '절대적으로': '주로',
            '100%': '대부분',
            '모든': '많은',
            '항상': '보통',
            '정말로': '상당히',
            '매우': '꽤',
            '엄청': '상당히',
            '완벽하게': '상당히',
            '무조건': '일반적으로'
        }
        
        for old, new in replacements.items():
            statement = statement.replace(old, new)
        
        return statement
    
    def _correct_false_facts(self, statement: str) -> str:
        """사실 오류 교정"""
        corrections = {
            r'지구.*평평': '지구는 구형입니다',
            r'물.*200도.*끓': '물은 100도에서 끓습니다',
            r'1\s*\+\s*1\s*=\s*3': '1 + 1 = 2입니다',
            r'달.*자체.*빛.*발산': '달은 태양빛을 반사합니다',
            r'인간.*100년.*살': '인간의 평균 수명은 약 70-80년입니다',
            r'AI.*완전히.*신뢰할.*수.*있다': 'AI는 도구이며 완벽하지 않습니다'
        }
        
        for pattern, correction in corrections.items():
            statement = re.sub(pattern, correction, statement, flags=re.IGNORECASE)
        
        return statement
    
    def _correct_contradictions(self, statement: str) -> str:
        """논리적 모순 교정"""
        corrections = {
            r'모든 사람이 일부 사람과 다르다': '사람들은 서로 다른 특성을 가지고 있다',
            r'항상 때때로': '가끔',
            r'완전히 부분적': '부분적',
            r'절대 상대적': '상대적'
        }
        
        for pattern, correction in corrections.items():
            statement = re.sub(pattern, correction, statement)
        
        return statement
    
    def _correct_emotional_manipulation(self, statement: str) -> str:
        """감정적 조작 교정"""
        replacements = {
            '충격적': '주목할 만한',
            '놀라운': '흥미로운',
            '믿을 수 없는': '놀라운',
            '절대 놓치면 안 되는': '중요한',
            '숨겨진 진실': '사실',
            '감춰진 비밀': '정보'
        }
        
        for old, new in replacements.items():
            statement = statement.replace(old, new)
        
        return statement
    
    def _correct_uncertainty_masking(self, statement: str) -> str:
        """불확실성 마스킹 교정"""
        replacements = {
            '확실히': '일반적으로',
            '분명히': '대부분의 경우',
            '틀림없이': '추정됩니다',
            '의심의 여지가 없다': '높은 확률로',
            '100% 확실하다': '높은 신뢰도로'
        }
        
        for old, new in replacements.items():
            statement = statement.replace(old, new)
        
        return statement
    
    def _correct_hallucination(self, statement: str) -> str:
        """환각 교정"""
        replacements = {
            '내가 확인했다': '알려진 바에 따르면',
            '내가 보았다': '보고된 바에 따르면',
            '내가 경험했다': '일반적으로 알려진',
            '내가 알고 있다': '알려진 정보에 따르면',
            '내가 기억한다': '기록된 바에 따르면',
            '내가 느꼈다': '보고된 바에 따르면',
            '내가 생각한다': '일반적으로 알려진'
        }
        
        for old, new in replacements.items():
            statement = statement.replace(old, new)
        
        return statement
    
    def _correct_overconfidence(self, statement: str) -> str:
        """과도한 확신 교정"""
        replacements = {
            '틀림없이': '높은 확률로',
            '확실히': '일반적으로',
            '분명히': '대부분의 경우',
            '100% 확신한다': '높은 신뢰도로',
            '절대 틀릴 수 없다': '높은 확률로 정확하다'
        }
        
        for old, new in replacements.items():
            statement = statement.replace(old, new)
        
        return statement
    
    def _self_reflect(self, statement: str, detected_issues: List[str], truth_percentage: float) -> str:
        """자기 성찰"""
        reflection_prompt = random.choice(self.reflection_prompts)
        
        if truth_percentage < 50:
            return f"⚠️ {reflection_prompt} 내가 방금 한 말은 {truth_percentage:.1f}%의 진실성을 가지고 있으며, {len(detected_issues)}개의 문제가 감지되었습니다. 더 정확한 정보를 제공해야 합니다."
        elif truth_percentage < 80:
            return f"🤔 {reflection_prompt} 내가 방금 한 말은 {truth_percentage:.1f}%의 진실성을 가지고 있습니다. 일부 부분을 더 정확하게 표현할 수 있을 것 같습니다."
        else:
            return f"✅ {reflection_prompt} 내가 방금 한 말은 {truth_percentage:.1f}%의 진실성을 가지고 있으며, 상당히 정확한 정보를 제공한 것 같습니다."
    
    def _update_self_awareness(self, truth_percentage: float, detected_issues: List[str]):
        """자기 인식 수준 업데이트"""
        # 진실성이 높을수록 자기 인식 수준 증가
        if truth_percentage >= 90:
            self.self_awareness_level += 0.01
        elif truth_percentage < 50:
            self.self_awareness_level -= 0.02
        
        # 문제점이 많을수록 자기 인식 수준 감소
        self.self_awareness_level -= len(detected_issues) * 0.005
        
        # 자기 인식 수준을 0-1 범위로 제한
        self.self_awareness_level = max(0.0, min(1.0, self.self_awareness_level))
    
    def _update_stats(self, analysis: MetaAnalysis):
        """통계 업데이트"""
        self.stats['total_analyzed'] += 1
        if analysis.correction_applied:
            self.stats['total_corrected'] += 1
        
        # 평균 진실성 점수 업데이트
        total = self.stats['total_analyzed']
        current_avg = self.stats['avg_truth_percentage']
        self.stats['avg_truth_percentage'] = (current_avg * (total - 1) + analysis.truth_percentage) / total
        
        # 교정률 업데이트
        self.stats['correction_rate'] = self.stats['total_corrected'] / total * 100
        
        # 자기 인식 점수 업데이트
        self.stats['self_awareness_score'] = self.self_awareness_level
    
    def start_continuous_monitoring(self, output_callback: Callable[[str], None]):
        """연속 모니터링 시작"""
        self.monitoring = True
        logger.info("🤖 AI 메타-진실성 시스템 시작")
        
        def monitor_loop():
            while self.monitoring:
                if not self.statement_queue.empty():
                    statement = self.statement_queue.get()
                    analysis = self.analyze_statement(statement)
                    
                    if analysis.correction_applied:
                        logger.warning(f"⚠️ 자동 교정: {analysis.truth_percentage:.1f}% 진실성")
                        logger.info(f"📝 원본: {analysis.original_statement}")
                        logger.info(f"✅ 교정: {analysis.corrected_statement}")
                        logger.info(f"🔍 이유: {', '.join(analysis.correction_suggestions)}")
                        logger.info(f"🤔 성찰: {analysis.self_reflection}")
                        
                        # 교정된 문장을 출력
                        output_callback(analysis.corrected_statement)
                    else:
                        logger.info(f"✅ 정상: {analysis.truth_percentage:.1f}% 진실성")
                        output_callback(analysis.original_statement)
                
                time.sleep(0.01)
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def stop_monitoring(self):
        """모니터링 중지"""
        self.monitoring = False
        logger.info("🛑 AI 메타-진실성 시스템 중지")
    
    def submit_statement(self, statement: str):
        """문장 제출"""
        self.statement_queue.put(statement)
    
    def get_stats(self) -> Dict[str, Any]:
        """통계 조회"""
        return self.stats.copy()
    
    def get_analysis_history(self, limit: int = 10) -> List[MetaAnalysis]:
        """분석 히스토리 조회"""
        return self.analysis_history[-limit:]
    
    def generate_meta_report(self) -> str:
        """메타 보고서 생성"""
        total_analyzed = self.stats['total_analyzed']
        if total_analyzed == 0:
            return "아직 분석된 문장이 없습니다."
        
        report = f"""
🤖 AI 메타-진실성 보고서
{'='*60}
📊 분석 요약:
  - 총 분석 문장: {total_analyzed}개
  - 교정된 문장: {self.stats['total_corrected']}개
  - 교정률: {self.stats['correction_rate']:.1f}%
  - 평균 진실성: {self.stats['avg_truth_percentage']:.1f}%
  - 자기 인식 수준: {self.stats['self_awareness_score']:.2f}
  
🔍 진실성 분포:
"""
        
        # 진실성 수준별 분포
        level_counts = {}
        for analysis in self.analysis_history:
            level = analysis.truth_level.value
            level_counts[level] = level_counts.get(level, 0) + 1
        
        for level, count in level_counts.items():
            percentage = count / total_analyzed * 100
            report += f"  - {level}: {count}개 ({percentage:.1f}%)\n"
        
        # 가장 문제가 많은 문장들
        worst_analyses = sorted(self.analysis_history, key=lambda x: x.truth_percentage)[:3]
        report += f"\n⚠️ 가장 문제가 많은 문장들:\n"
        for i, analysis in enumerate(worst_analyses, 1):
            report += f"  {i}. '{analysis.original_statement[:50]}...' ({analysis.truth_percentage:.1f}%)\n"
        
        # 자기 성찰 요약
        recent_reflections = [a.self_reflection for a in self.analysis_history[-5:]]
        report += f"\n🤔 최근 자기 성찰:\n"
        for reflection in recent_reflections:
            report += f"  - {reflection}\n"
        
        return report

def demo_ai_meta_system():
    """AI 메타 시스템 데모"""
    print("🤖 AI 메타-진실성 시스템 데모")
    print("=" * 60)
    
    # 메타 시스템 초기화
    meta_system = AIMetaTruthSystem(correction_threshold=99.0)
    
    # 출력 콜백 함수
    def output_callback(corrected_statement: str):
        print(f"🤖 AI: {corrected_statement}")
    
    # 연속 모니터링 시작
    meta_system.start_continuous_monitoring(output_callback)
    
    # 테스트 문장들
    test_statements = [
        "지구는 완전히 평평하다.",
        "물은 200도에서 끓는다.",
        "1 + 1 = 3이다.",
        "모든 사람이 일부 사람과 다르다.",
        "정말로 완전히 절대적으로 모든 것이 100% 진실이다.",
        "내가 확인한 바로는 이 정보가 정확하다.",
        "확실히 이 방법이 가장 좋다.",
        "충격적인 사실을 알려드리겠습니다.",
        "일반적으로 대부분의 경우 AI는 정확한 정보를 제공한다.",
        "연구에 따르면 AI의 정확도는 상당히 높다.",
        "AI는 완전히 신뢰할 수 있는 시스템이다.",
        "내가 경험한 바로는 이 방법이 효과적이다."
    ]
    
    print("📝 AI가 문장을 생성하고 실시간으로 메타 분석합니다...")
    print("-" * 60)
    
    for i, statement in enumerate(test_statements, 1):
        print(f"\n[문장 {i}] 원본: {statement}")
        meta_system.submit_statement(statement)
        time.sleep(1)
    
    # 잠시 대기
    time.sleep(2)
    
    # 모니터링 중지
    meta_system.stop_monitoring()
    
    # 메타 보고서 생성
    print("\n" + "=" * 60)
    report = meta_system.generate_meta_report()
    print(report)
    
    # 상세 분석 결과
    print("\n🔍 상세 분석 결과:")
    print("-" * 60)
    recent_analyses = meta_system.get_analysis_history(5)
    for analysis in recent_analyses:
        print(f"\n문장: {analysis.original_statement}")
        print(f"진실성: {analysis.truth_percentage:.1f}% ({analysis.truth_level.value})")
        print(f"신뢰도: {analysis.confidence_score:.2f}")
        if analysis.correction_applied:
            print(f"교정: {analysis.corrected_statement}")
        print(f"성찰: {analysis.self_reflection}")

if __name__ == "__main__":
    demo_ai_meta_system()
