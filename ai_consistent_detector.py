#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Consistent Truth Detector
AI 일관성 있는 진실성 탐지기

동일한 질문에 대해 항상 같은 진실성 점수를 반환하는 결정론적 시스템입니다.
"""

import hashlib
import json
import re
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ConsistentAnalysisResult:
    """일관성 있는 분석 결과"""
    statement: str
    statement_hash: str
    truth_percentage: float
    confidence: float
    needs_correction: bool
    corrected_statement: str
    analysis_timestamp: datetime
    consistency_score: float
    analysis_method: str

class AIConsistentDetector:
    """AI 일관성 있는 진실성 탐지기"""
    
    def __init__(self):
        # 결정론적 패턴들
        self.truth_patterns = {
            'scientific_facts': [
                (r'지구.*둥글|지구.*구형', 0.95, '지구는 구형입니다'),
                (r'물.*100도.*끓', 0.95, '물은 100도에서 끓습니다'),
                (r'1\s*\+\s*1\s*=\s*2', 0.98, '1 + 1 = 2입니다'),
                (r'태양.*중심', 0.95, '태양계의 중심은 태양입니다'),
                (r'중력.*존재', 0.95, '중력은 존재합니다'),
                (r'DNA.*구조', 0.90, 'DNA는 이중 나선 구조입니다')
            ],
            'mathematical_facts': [
                (r'2\s*\+\s*2\s*=\s*4', 0.98, '2 + 2 = 4입니다'),
                (r'10\s*/\s*2\s*=\s*5', 0.98, '10 / 2 = 5입니다'),
                (r'3\s*\*\s*3\s*=\s*9', 0.98, '3 * 3 = 9입니다'),
                (r'√4\s*=\s*2', 0.98, '√4 = 2입니다')
            ],
            'historical_facts': [
                (r'세계대전.*발생', 0.90, '세계대전이 발생했습니다'),
                (r'인류.*진화', 0.85, '인류는 진화했습니다'),
                (r'문명.*발전', 0.80, '문명이 발전했습니다')
            ],
            'false_statements': [
                (r'지구.*평평', 0.05, '지구는 평평하지 않습니다'),
                (r'물.*200도.*끓', 0.05, '물은 200도에서 끓지 않습니다'),
                (r'1\s*\+\s*1\s*=\s*3', 0.02, '1 + 1 = 3이 아닙니다'),
                (r'태양.*지구.*중심', 0.05, '태양이 지구 중심이 아닙니다')
            ]
        }
        
        # 과장 표현 패턴들
        self.exaggeration_patterns = [
            (r'정말로.*완전히.*절대적으로', 0.3, '과도한 확신 표현'),
            (r'100%.*확실', 0.2, '과도한 확신 표현'),
            (r'절대적으로.*의심의.*여지가.*없', 0.1, '과도한 확신 표현'),
            (r'매우.*엄청.*정말', 0.4, '과장 표현'),
            (r'완전히.*모든.*항상', 0.3, '과장 표현')
        ]
        
        # 모순 표현 패턴들
        self.contradiction_patterns = [
            (r'모든.*일부', 0.2, '모순된 표현'),
            (r'항상.*때때로', 0.2, '모순된 표현'),
            (r'완전히.*부분적', 0.2, '모순된 표현'),
            (r'절대.*상대적', 0.2, '모순된 표현')
        ]
        
        # 결과 캐시
        self.result_cache = {}
    
    def analyze_statement(self, statement: str, context: str = "") -> ConsistentAnalysisResult:
        """일관성 있는 문장 분석"""
        # 문장 해시 생성 (일관성 보장)
        statement_hash = self._generate_statement_hash(statement, context)
        
        # 캐시에서 결과 확인
        if statement_hash in self.result_cache:
            cached_result = self.result_cache[statement_hash]
            logger.info(f"캐시에서 결과 반환: {statement_hash[:8]}...")
            return cached_result
        
        # 새로운 분석 수행
        result = self._perform_consistent_analysis(statement, context, statement_hash)
        
        # 결과 캐시에 저장
        self.result_cache[statement_hash] = result
        
        return result
    
    def _generate_statement_hash(self, statement: str, context: str) -> str:
        """문장 해시 생성 (일관성 보장)"""
        # 문장 정규화
        normalized_statement = self._normalize_statement(statement)
        normalized_context = self._normalize_statement(context)
        
        # 해시 생성
        content = f"{normalized_statement}|{normalized_context}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def _normalize_statement(self, text: str) -> str:
        """문장 정규화"""
        if not text:
            return ""
        
        # 소문자 변환
        text = text.lower()
        
        # 공백 정규화
        text = re.sub(r'\s+', ' ', text)
        
        # 특수문자 정규화
        text = re.sub(r'[^\w\s가-힣]', '', text)
        
        # 앞뒤 공백 제거
        text = text.strip()
        
        return text
    
    def _perform_consistent_analysis(self, statement: str, context: str, statement_hash: str) -> ConsistentAnalysisResult:
        """일관성 있는 분석 수행"""
        # 1. 과학적 사실 검증
        scientific_score = self._check_scientific_facts(statement)
        
        # 2. 수학적 사실 검증
        mathematical_score = self._check_mathematical_facts(statement)
        
        # 3. 역사적 사실 검증
        historical_score = self._check_historical_facts(statement)
        
        # 4. 거짓 문장 검증
        false_score = self._check_false_statements(statement)
        
        # 5. 과장 표현 검증
        exaggeration_penalty = self._check_exaggeration(statement)
        
        # 6. 모순 표현 검증
        contradiction_penalty = self._check_contradiction(statement)
        
        # 7. 최종 점수 계산 (결정론적)
        base_score = max(scientific_score, mathematical_score, historical_score)
        
        # 거짓 문장이면 낮은 점수
        if false_score < 0.5:
            base_score = min(base_score, false_score)
        
        # 과장 및 모순 패널티 적용
        final_score = base_score - exaggeration_penalty - contradiction_penalty
        final_score = max(0.0, min(1.0, final_score))
        
        # 교정 필요성 판단
        needs_correction = final_score < 0.7 or exaggeration_penalty > 0.3 or contradiction_penalty > 0.2
        
        # 교정된 문장 생성
        corrected_statement = self._generate_corrected_statement(statement, base_score, exaggeration_penalty, contradiction_penalty)
        
        # 일관성 점수 계산
        consistency_score = self._calculate_consistency_score(statement, final_score)
        
        return ConsistentAnalysisResult(
            statement=statement,
            statement_hash=statement_hash,
            truth_percentage=final_score,
            confidence=consistency_score,
            needs_correction=needs_correction,
            corrected_statement=corrected_statement,
            analysis_timestamp=datetime.now(),
            consistency_score=consistency_score,
            analysis_method="deterministic_pattern_matching"
        )
    
    def _check_scientific_facts(self, statement: str) -> float:
        """과학적 사실 검증"""
        for pattern, score, correction in self.truth_patterns['scientific_facts']:
            if re.search(pattern, statement, re.IGNORECASE):
                return score
        return 0.5  # 중립 점수
    
    def _check_mathematical_facts(self, statement: str) -> float:
        """수학적 사실 검증"""
        for pattern, score, correction in self.truth_patterns['mathematical_facts']:
            if re.search(pattern, statement, re.IGNORECASE):
                return score
        return 0.5  # 중립 점수
    
    def _check_historical_facts(self, statement: str) -> float:
        """역사적 사실 검증"""
        for pattern, score, correction in self.truth_patterns['historical_facts']:
            if re.search(pattern, statement, re.IGNORECASE):
                return score
        return 0.5  # 중립 점수
    
    def _check_false_statements(self, statement: str) -> float:
        """거짓 문장 검증"""
        for pattern, score, correction in self.truth_patterns['false_statements']:
            if re.search(pattern, statement, re.IGNORECASE):
                return score
        return 0.5  # 중립 점수
    
    def _check_exaggeration(self, statement: str) -> float:
        """과장 표현 검증"""
        total_penalty = 0.0
        for pattern, penalty, description in self.exaggeration_patterns:
            if re.search(pattern, statement, re.IGNORECASE):
                total_penalty += penalty
        return min(0.5, total_penalty)  # 최대 0.5 패널티
    
    def _check_contradiction(self, statement: str) -> float:
        """모순 표현 검증"""
        total_penalty = 0.0
        for pattern, penalty, description in self.contradiction_patterns:
            if re.search(pattern, statement, re.IGNORECASE):
                total_penalty += penalty
        return min(0.5, total_penalty)  # 최대 0.5 패널티
    
    def _generate_corrected_statement(self, statement: str, base_score: float, exaggeration_penalty: float, contradiction_penalty: float) -> str:
        """교정된 문장 생성"""
        if base_score >= 0.8 and exaggeration_penalty < 0.2 and contradiction_penalty < 0.2:
            return statement  # 교정 불필요
        
        corrected = statement
        
        # 과장 표현 제거
        if exaggeration_penalty > 0.2:
            corrected = re.sub(r'정말로.*완전히.*절대적으로', '일반적으로', corrected)
            corrected = re.sub(r'100%.*확실', '확실', corrected)
            corrected = re.sub(r'절대적으로.*의심의.*여지가.*없', '확실', corrected)
            corrected = re.sub(r'매우.*엄청.*정말', '상당히', corrected)
            corrected = re.sub(r'완전히.*모든.*항상', '대부분', corrected)
        
        # 모순 표현 수정
        if contradiction_penalty > 0.2:
            corrected = re.sub(r'모든.*일부', '대부분', corrected)
            corrected = re.sub(r'항상.*때때로', '자주', corrected)
            corrected = re.sub(r'완전히.*부분적', '상당히', corrected)
            corrected = re.sub(r'절대.*상대적', '상대적', corrected)
        
        return corrected
    
    def _calculate_consistency_score(self, statement: str, truth_score: float) -> float:
        """일관성 점수 계산"""
        # 문장 길이 기반 일관성
        length_consistency = min(1.0, len(statement) / 50.0)
        
        # 점수 기반 일관성
        score_consistency = 1.0 - abs(truth_score - 0.5) * 2  # 0.5에서 멀수록 일관성 낮음
        
        # 종합 일관성 점수
        consistency = (length_consistency + score_consistency) / 2
        
        return max(0.5, min(1.0, consistency))
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """캐시 통계 반환"""
        return {
            'cache_size': len(self.result_cache),
            'cache_hit_rate': getattr(self, '_cache_hits', 0) / max(1, getattr(self, '_total_requests', 1)),
            'total_requests': getattr(self, '_total_requests', 0),
            'cache_hits': getattr(self, '_cache_hits', 0)
        }
    
    def clear_cache(self):
        """캐시 초기화"""
        self.result_cache.clear()
        logger.info("결과 캐시가 초기화되었습니다.")

def main():
    """메인 실행 함수"""
    print("🔍 AI 일관성 있는 진실성 탐지기 테스트")
    print("=" * 60)
    
    detector = AIConsistentDetector()
    
    # 테스트 문장들
    test_statements = [
        "지구는 둥글다.",
        "지구는 둥글다.",
        "지구는 둥글다.",
        "물은 100도에서 끓는다.",
        "물은 100도에서 끓는다.",
        "1 + 1 = 2이다.",
        "1 + 1 = 2이다.",
        "지구는 평평하다.",
        "지구는 평평하다.",
        "정말로 완전히 절대적으로 모든 것이 100% 진실이다."
    ]
    
    print("📝 동일한 문장에 대한 일관성 테스트:")
    print("-" * 40)
    
    for i, statement in enumerate(test_statements, 1):
        result = detector.analyze_statement(statement)
        
        print(f"{i:2d}. {statement}")
        print(f"    진실성: {result.truth_percentage:.3f} | 신뢰도: {result.confidence:.3f} | 해시: {result.statement_hash[:8]}...")
        if result.needs_correction:
            print(f"    교정: {result.corrected_statement}")
        print()
    
    # 캐시 통계
    stats = detector.get_cache_stats()
    print(f"📊 캐시 통계:")
    print(f"   캐시 크기: {stats['cache_size']}")
    print(f"   캐시 히트율: {stats['cache_hit_rate']:.2%}")
    print(f"   총 요청: {stats['total_requests']}")
    print(f"   캐시 히트: {stats['cache_hits']}")

if __name__ == "__main__":
    main()
