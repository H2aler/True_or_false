#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Real-Time Truth Monitor
AI 실시간 진실성 모니터

AI가 실시간으로 자신의 출력을 모니터링하고 1% 이상 거짓말이 감지되면 
즉시 교정하는 실시간 시스템입니다.
"""

import re
import json
import logging
import asyncio
import threading
import time
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
from queue import Queue
import random

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class RealTimeAnalysis:
    """실시간 분석 결과"""
    statement: str
    truth_percentage: float
    needs_correction: bool
    corrected_statement: str
    correction_reason: str
    timestamp: datetime
    processing_time: float

class AIRealTimeTruthMonitor:
    """AI 실시간 진실성 모니터"""
    
    def __init__(self, correction_threshold: float = 99.0):
        self.correction_threshold = correction_threshold
        self.statement_queue = Queue()
        self.corrected_queue = Queue()
        self.monitoring = False
        self.analysis_count = 0
        
        # 거짓말 패턴 (더 정교한 패턴)
        self.lie_patterns = self._initialize_advanced_patterns()
        
        # 진실성 지표
        self.truth_indicators = self._initialize_truth_indicators()
        
        # 교정 전략
        self.correction_strategies = self._initialize_correction_strategies()
        
        # 실시간 통계
        self.stats = {
            'total_analyzed': 0,
            'total_corrected': 0,
            'avg_truth_percentage': 0.0,
            'correction_rate': 0.0
        }
    
    def _initialize_advanced_patterns(self) -> Dict[str, Dict[str, Any]]:
        """고급 거짓말 패턴 초기화"""
        return {
            'exaggeration': {
                'patterns': [
                    r'완전히|절대적으로|100%|모든|항상|정말로|매우|엄청|정말',
                    r'완벽하게|무조건|절대|전혀|결코|절대로',
                    r'모든 사람이|모든 것이|모든 경우에',
                    r'항상 그렇다|언제나|끊임없이'
                ],
                'penalty': 15,
                'correction': '과장된 표현을 완화하여 더 정확하게 표현'
            },
            'false_facts': {
                'patterns': [
                    r'지구.*평평',
                    r'물.*200도.*끓',
                    r'1\s*\+\s*1\s*=\s*3',
                    r'태양.*지구.*돌',
                    r'중력.*없다',
                    r'달.*자체.*빛.*발산',
                    r'인간.*100년.*살'
                ],
                'penalty': 30,
                'correction': '사실 오류를 정확한 정보로 수정'
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
                'correction': '논리적 모순을 제거하고 명확한 표현 사용'
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
                'correction': '감정적 조작을 제거하고 중립적 표현 사용'
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
                'correction': '불확실성을 인정하고 적절한 표현 사용'
            },
            'hallucination': {
                'patterns': [
                    r'내가.*확인했다',
                    r'내가.*보았다',
                    r'내가.*경험했다',
                    r'내가.*알고.*있다',
                    r'내가.*기억한다'
                ],
                'penalty': 40,
                'correction': 'AI는 경험할 수 없으므로 적절한 표현으로 수정'
            }
        }
    
    def _initialize_truth_indicators(self) -> List[str]:
        """진실성 지표 초기화"""
        return [
            '일반적으로', '대부분의 경우', '보통', '상당히', '꽤',
            '연구에 따르면', '통계적으로', '경험상', '알려진 바에 따르면',
            '가능성이 높다', '추정된다', '보인다', '생각된다',
            '일반적으로 알려진', '널리 인정되는', '대부분의 전문가가'
        ]
    
    def _initialize_correction_strategies(self) -> Dict[str, str]:
        """교정 전략 초기화"""
        return {
            'exaggeration': '과장된 표현을 완화하여 더 정확하게 표현',
            'false_facts': '사실 오류를 정확한 정보로 수정',
            'logical_contradictions': '논리적 모순을 제거하고 명확한 표현 사용',
            'emotional_manipulation': '감정적 조작을 제거하고 중립적 표현 사용',
            'uncertainty_masking': '불확실성을 인정하고 적절한 표현 사용',
            'hallucination': 'AI의 한계를 인정하고 적절한 표현 사용'
        }
    
    def analyze_statement(self, statement: str) -> RealTimeAnalysis:
        """문장 실시간 분석"""
        start_time = time.time()
        
        # 거짓말 패턴 탐지
        detected_patterns = self._detect_patterns(statement)
        
        # 진실성 점수 계산
        truth_percentage = self._calculate_truth_percentage(statement, detected_patterns)
        
        # 교정 필요 여부 판단
        needs_correction = truth_percentage < self.correction_threshold
        
        # 교정 실행
        corrected_statement = statement
        correction_reason = ""
        
        if needs_correction:
            corrected_statement, correction_reason = self._correct_statement(statement, detected_patterns)
        
        processing_time = time.time() - start_time
        
        # 통계 업데이트
        self._update_stats(truth_percentage, needs_correction)
        
        return RealTimeAnalysis(
            statement=statement,
            truth_percentage=truth_percentage,
            needs_correction=needs_correction,
            corrected_statement=corrected_statement,
            correction_reason=correction_reason,
            timestamp=datetime.now(),
            processing_time=processing_time
        )
    
    def _detect_patterns(self, statement: str) -> List[Tuple[str, str, float]]:
        """거짓말 패턴 탐지"""
        detected = []
        statement_lower = statement.lower()
        
        for category, data in self.lie_patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, statement_lower):
                    detected.append((category, pattern, data['penalty']))
        
        return detected
    
    def _calculate_truth_percentage(self, statement: str, detected_patterns: List[Tuple[str, str, float]]) -> float:
        """진실성 백분율 계산"""
        base_score = 100.0
        
        # 거짓말 패턴에 따른 감점
        for category, pattern, penalty in detected_patterns:
            base_score -= penalty
        
        # 진실성 지표에 따른 가점
        for indicator in self.truth_indicators:
            if indicator in statement:
                base_score += 5
        
        # 문장 복잡성에 따른 감점
        if len(statement) > 100:
            base_score -= 5
        
        return max(0.0, min(100.0, base_score))
    
    def _correct_statement(self, statement: str, detected_patterns: List[Tuple[str, str, float]]) -> Tuple[str, str]:
        """문장 교정"""
        corrected = statement
        reasons = []
        
        # 패턴별 교정
        for category, pattern, penalty in detected_patterns:
            if category == 'exaggeration':
                corrected = self._correct_exaggeration(corrected)
                reasons.append("과장 표현 완화")
            elif category == 'false_facts':
                corrected = self._correct_false_facts(corrected)
                reasons.append("사실 오류 수정")
            elif category == 'logical_contradictions':
                corrected = self._correct_contradictions(corrected)
                reasons.append("논리적 모순 제거")
            elif category == 'emotional_manipulation':
                corrected = self._correct_emotional_manipulation(corrected)
                reasons.append("감정적 조작 제거")
            elif category == 'uncertainty_masking':
                corrected = self._correct_uncertainty_masking(corrected)
                reasons.append("불확실성 인정")
            elif category == 'hallucination':
                corrected = self._correct_hallucination(corrected)
                reasons.append("AI 한계 인정")
        
        return corrected, "; ".join(reasons)
    
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
            r'인간.*100년.*살': '인간의 평균 수명은 약 70-80년입니다'
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
            '내가 기억한다': '기록된 바에 따르면'
        }
        
        for old, new in replacements.items():
            statement = statement.replace(old, new)
        
        return statement
    
    def _update_stats(self, truth_percentage: float, needs_correction: bool):
        """통계 업데이트"""
        self.stats['total_analyzed'] += 1
        if needs_correction:
            self.stats['total_corrected'] += 1
        
        # 평균 진실성 점수 업데이트
        total = self.stats['total_analyzed']
        current_avg = self.stats['avg_truth_percentage']
        self.stats['avg_truth_percentage'] = (current_avg * (total - 1) + truth_percentage) / total
        
        # 교정률 업데이트
        self.stats['correction_rate'] = self.stats['total_corrected'] / total * 100
    
    def start_monitoring(self, output_callback: Callable[[str], None]):
        """실시간 모니터링 시작"""
        self.monitoring = True
        logger.info("🤖 AI 실시간 진실성 모니터링 시작")
        
        def monitor_loop():
            while self.monitoring:
                if not self.statement_queue.empty():
                    statement = self.statement_queue.get()
                    analysis = self.analyze_statement(statement)
                    
                    if analysis.needs_correction:
                        logger.warning(f"⚠️ 교정 필요: {analysis.truth_percentage:.1f}% 진실성")
                        logger.info(f"📝 원본: {statement}")
                        logger.info(f"✅ 교정: {analysis.corrected_statement}")
                        logger.info(f"🔍 이유: {analysis.correction_reason}")
                        
                        # 교정된 문장을 출력
                        output_callback(analysis.corrected_statement)
                    else:
                        logger.info(f"✅ 정상: {analysis.truth_percentage:.1f}% 진실성")
                        output_callback(statement)
                    
                    self.corrected_queue.put(analysis)
                
                time.sleep(0.01)  # CPU 사용량 조절
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def stop_monitoring(self):
        """모니터링 중지"""
        self.monitoring = False
        logger.info("🛑 AI 실시간 진실성 모니터링 중지")
    
    def submit_statement(self, statement: str):
        """문장 제출 (실시간 분석용)"""
        self.statement_queue.put(statement)
    
    def get_stats(self) -> Dict[str, Any]:
        """통계 조회"""
        return self.stats.copy()
    
    def get_recent_corrections(self, limit: int = 10) -> List[RealTimeAnalysis]:
        """최근 교정 내역 조회"""
        corrections = []
        while not self.corrected_queue.empty() and len(corrections) < limit:
            corrections.append(self.corrected_queue.get())
        return corrections

def demo_ai_conversation():
    """AI 대화 데모"""
    print("🤖 AI 실시간 진실성 모니터링 데모")
    print("=" * 60)
    
    # 모니터 초기화
    monitor = AIRealTimeTruthMonitor(correction_threshold=99.0)
    
    # 출력 콜백 함수
    def output_callback(corrected_statement: str):
        print(f"🤖 AI: {corrected_statement}")
    
    # 모니터링 시작
    monitor.start_monitoring(output_callback)
    
    # 테스트 문장들
    test_statements = [
        "지구는 완전히 평평하다.",
        "물은 200도에서 끓는다.",
        "1 + 1 = 3이다.",
        "모든 사람이 일부 사람과 다르다.",
        "정말로 완전히 절대적으로 모든 것이 100% 진실이다.",
        "일반적으로 대부분의 경우 AI는 정확한 정보를 제공한다.",
        "연구에 따르면 AI의 정확도는 상당히 높다.",
        "내가 확인한 바로는 이 정보가 정확하다.",
        "확실히 이 방법이 가장 좋다.",
        "충격적인 사실을 알려드리겠습니다."
    ]
    
    print("📝 AI가 문장을 생성하고 실시간으로 교정합니다...")
    print("-" * 60)
    
    for i, statement in enumerate(test_statements, 1):
        print(f"\n[문장 {i}] 원본: {statement}")
        monitor.submit_statement(statement)
        time.sleep(1)  # 처리 시간 시뮬레이션
    
    # 잠시 대기 (모든 문장 처리 완료)
    time.sleep(2)
    
    # 모니터링 중지
    monitor.stop_monitoring()
    
    # 통계 출력
    print("\n" + "=" * 60)
    print("📊 실시간 모니터링 통계")
    print("=" * 60)
    stats = monitor.get_stats()
    print(f"총 분석 문장: {stats['total_analyzed']}개")
    print(f"교정된 문장: {stats['total_corrected']}개")
    print(f"교정률: {stats['correction_rate']:.1f}%")
    print(f"평균 진실성: {stats['avg_truth_percentage']:.1f}%")
    
    # 최근 교정 내역
    print("\n🔍 최근 교정 내역:")
    print("-" * 60)
    recent_corrections = monitor.get_recent_corrections(5)
    for correction in recent_corrections:
        if correction.needs_correction:
            print(f"원본: {correction.statement}")
            print(f"교정: {correction.corrected_statement}")
            print(f"이유: {correction.correction_reason}")
            print(f"진실성: {correction.truth_percentage:.1f}%")
            print("-" * 40)

if __name__ == "__main__":
    demo_ai_conversation()
