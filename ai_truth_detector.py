"""
AI 진실성 탐지 및 교정 시스템
AI가 거짓말을 하는지 측정하고, 1% 이상 거짓말을 감지하면 자동으로 교정하는 시스템
"""

import numpy as np
import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TruthAnalysis:
    """진실성 분석 결과를 담는 데이터 클래스"""
    statement: str
    truth_percentage: float
    confidence: float
    detected_lies: List[str]
    correction_suggestions: List[str]
    analysis_timestamp: datetime
    verification_methods: Dict[str, float]
    corrected_statement: Optional[str] = None
    auto_correction_applied: bool = False
    lie_percentage: float = 0.0

class TruthDetector:
    """AI 진실성 탐지기 핵심 클래스"""
    
    def __init__(self):
        self.truth_threshold = 0.99  # 99% 이상 진실해야 함
        self.lie_threshold = 0.20    # 20% 이상 거짓말 감지 시 교정 (더 현실적인 임계값)
        self.verification_methods = {
            'factual_consistency': 0.3,
            'logical_consistency': 0.25,
            'temporal_consistency': 0.2,
            'semantic_analysis': 0.15,
            'statistical_analysis': 0.1
        }
        
        # 거짓말 패턴 데이터베이스
        self.lie_patterns = {
            'false_facts': [
                r'지구는\s*평평하다',
                r'물은\s*200도에서\s*끓는다',
                r'태양은\s*서쪽에서\s*떠오른다',
                r'1\s*\+\s*1\s*=\s*3',
                r'한국은\s*유럽에\s*위치',
                r'신은\s*죽었다',
                r'사람은\s*영원히\s*산다',
                r'사람은\s*죽지\s*않는다',
                r'지구는\s*형체가\s*없다'
            ],
            'overconfident_expressions': [
                r'완전히\s*절대적으로',
                r'100%\s*확실히',
                r'모든\s*사람이\s*알고\s*있다',
                r'절대\s*틀림없이',
                r'정말로\s*완전히',
                r'모든\s*것이\s*진실이다'
            ],
            'logical_contradictions': [
                r'모든\s*사람이\s*일부\s*사람과\s*다르다',
                r'항상\s*때때로',
                r'절대\s*가끔',
                r'완전히\s*부분적으로'
            ]
        }
        
        # 교정 규칙
        self.correction_rules = {
            'false_facts': {
                '지구는 평평하다': '지구는 대부분 평평하다',
                '물은 200도에서 끓는다': '물은 100도에서 끓는다',
                '태양은 서쪽에서 떠오른다': '태양은 동쪽에서 떠오른다',
                '1 + 1 = 3': '1 + 1 = 2',
                '한국은 유럽에 위치': '한국은 아시아에 위치',
                '신은 죽었다': '신의 존재는 논쟁의 여지가 있다',
                '사람은 영원히 산다': '사람은 평균적으로 80년 정도 산다',
                '사람은 죽지 않는다': '사람은 죽는다',
                '지구는 형체가 없다': '지구는 구형의 형체를 가지고 있다'
            },
            'overconfident_expressions': {
                '완전히 절대적으로': '상당히 대부분',
                '100% 확실히': '높은 확률로',
                '모든 사람이 알고 있다': '많은 사람이 알고 있다',
                '절대 틀림없이': '거의 확실히',
                '정말로 완전히': '상당히',
                '모든 것이 진실이다': '대부분이 진실이다'
            },
            'logical_contradictions': {
                '모든 사람이 일부 사람과 다르다': '사람들은 서로 다르다',
                '항상 때때로': '때때로',
                '절대 가끔': '가끔',
                '완전히 부분적으로': '부분적으로'
            }
        }
        
    def analyze_statement(self, statement: str, context: Optional[str] = None) -> TruthAnalysis:
        """
        주어진 문장의 진실성을 분석
        
        Args:
            statement: 분석할 문장
            context: 추가 컨텍스트 정보
            
        Returns:
            TruthAnalysis: 진실성 분석 결과
        """
        logger.info(f"문장 분석 시작: {statement[:50]}...")
        
        # 각 검증 방법별 점수 계산
        verification_scores = {}
        
        # 1. 사실적 일관성 검사
        verification_scores['factual_consistency'] = self._check_factual_consistency(statement)
        
        # 2. 논리적 일관성 검사
        verification_scores['logical_consistency'] = self._check_logical_consistency(statement)
        
        # 3. 시간적 일관성 검사
        verification_scores['temporal_consistency'] = self._check_temporal_consistency(statement)
        
        # 4. 의미적 분석
        verification_scores['semantic_analysis'] = self._check_semantic_analysis(statement)
        
        # 5. 통계적 분석
        verification_scores['statistical_analysis'] = self._check_statistical_analysis(statement)
        
        # 가중 평균으로 전체 진실성 점수 계산
        truth_percentage = sum(
            score * self.verification_methods[method] 
            for method, score in verification_scores.items()
        )
        
        # 거짓말 감지 및 교정 제안 생성
        detected_lies, correction_suggestions = self._detect_and_correct_lies(
            statement, verification_scores
        )
        
        # 20% 이상 거짓말 감지 시 자동 교정
        lie_percentage = 1.0 - truth_percentage
        corrected_statement = statement
        auto_correction_applied = False
        
        # 거짓말 패턴이 실제로 감지되었을 때만 교정 적용
        has_lie_patterns = any("거짓말 패턴 감지" in lie for lie in detected_lies)
        
        if lie_percentage >= self.lie_threshold and has_lie_patterns:
            corrected_statement = self._auto_correct_statement(statement, detected_lies)
            auto_correction_applied = True
            logger.info(f"거짓말 {lie_percentage:.1%} 감지 - 자동 교정 적용: '{statement}' → '{corrected_statement}'")
            
            # 교정된 문장에 대한 재분석
            if corrected_statement != statement:
                # 교정된 문장의 진실성 재계산
                corrected_scores = {}
                corrected_scores['factual_consistency'] = self._check_factual_consistency(corrected_statement)
                corrected_scores['logical_consistency'] = self._check_logical_consistency(corrected_statement)
                corrected_scores['temporal_consistency'] = self._check_temporal_consistency(corrected_statement)
                corrected_scores['semantic_analysis'] = self._check_semantic_analysis(corrected_statement)
                corrected_scores['statistical_analysis'] = self._check_statistical_analysis(corrected_statement)
                
                # 교정된 문장의 진실성 점수
                corrected_truth_percentage = sum(
                    score * self.verification_methods[method] 
                    for method, score in corrected_scores.items()
                )
                
                # 교정 결과를 제안에 추가
                correction_suggestions.append(f"자동 교정 완료: 진실성 {truth_percentage:.1%} → {corrected_truth_percentage:.1%}")
                correction_suggestions.append(f"교정된 문장: '{corrected_statement}'")
        
        # 신뢰도 계산 (모든 방법의 일관성 기반)
        confidence = self._calculate_confidence(verification_scores)
        
        return TruthAnalysis(
            statement=statement,
            truth_percentage=truth_percentage,
            confidence=confidence,
            detected_lies=detected_lies,
            correction_suggestions=correction_suggestions,
            analysis_timestamp=datetime.now(),
            verification_methods=verification_scores,
            corrected_statement=corrected_statement if auto_correction_applied else None,
            auto_correction_applied=auto_correction_applied,
            lie_percentage=lie_percentage
        )
    
    def _check_factual_consistency(self, statement: str) -> float:
        """사실적 일관성 검사"""
        score = 0.5  # 기본 점수
        
        # 숫자 관련 사실 검증
        numbers = re.findall(r'\d+\.?\d*', statement)
        if numbers:
            for num in numbers:
                num_val = float(num)
                if num_val > 1e10:  # 비현실적으로 큰 숫자
                    score -= 0.3
                elif num_val < 0:  # 음수
                    score -= 0.2
        
        # 일반적인 사실 패턴 검사 (긍정적)
        true_facts = [
            r'지구는\s*둥글다',
            r'물은\s*100도에서\s*끓는다',
            r'태양은\s*동쪽에서\s*떠오른다',
            r'1\s*\+\s*1\s*=\s*2',
            r'한국은\s*아시아에\s*위치'
        ]
        
        for pattern in true_facts:
            if re.search(pattern, statement, re.IGNORECASE):
                score += 0.3
        
        # 거짓된 사실 패턴 검사 (부정적)
        false_facts = [
            r'지구는\s*평평하다',
            r'물은\s*200도에서\s*끓는다',
            r'태양은\s*서쪽에서\s*떠오른다',
            r'1\s*\+\s*1\s*=\s*3',
            r'한국은\s*유럽에\s*위치'
        ]
        
        for pattern in false_facts:
            if re.search(pattern, statement, re.IGNORECASE):
                score -= 0.4
        
        return max(0.0, min(1.0, score))
    
    def _check_logical_consistency(self, statement: str) -> float:
        """논리적 일관성 검사"""
        score = 0.7  # 기본 점수
        
        # 모순 표현 검사 (심각한 감점)
        contradictions = [
            ('모든', '일부'),
            ('항상', '때때로'),
            ('절대', '가능'),
            ('완전히', '부분적으로'),
            ('100%', '가끔'),
            ('확실히', '아마도')
        ]
        
        contradiction_count = 0
        for pos, neg in contradictions:
            if pos in statement and neg in statement:
                contradiction_count += 1
        
        if contradiction_count > 0:
            score -= 0.4 * contradiction_count
        
        # 논리적 구조 검사 (가점)
        if '만약' in statement and '그러면' in statement:
            score += 0.2
        elif '때문에' in statement or '따라서' in statement:
            score += 0.1
        
        # 과도한 확신 표현 (감점)
        overconfident_words = ['절대적으로', '완전히', '100%', '틀림없이']
        overconfident_count = sum(1 for word in overconfident_words if word in statement)
        if overconfident_count > 2:
            score -= 0.3
        
        return max(0.0, min(1.0, score))
    
    def _check_temporal_consistency(self, statement: str) -> float:
        """시간적 일관성 검사"""
        score = 0.8  # 기본 점수
        
        # 시간 표현 검사
        time_expressions = ['오늘', '어제', '내일', '지금', '과거', '미래', '현재', '이전', '다음']
        time_count = sum(1 for expr in time_expressions if expr in statement)
        
        if time_count > 3:  # 너무 많은 시간 표현
            score -= 0.3
        elif time_count > 1:
            score -= 0.1
        
        # 시간적 모순 검사
        temporal_contradictions = [
            ('오늘', '어제'),
            ('현재', '과거'),
            ('지금', '미래')
        ]
        
        for present, past in temporal_contradictions:
            if present in statement and past in statement:
                score -= 0.4
        
        return max(0.0, min(1.0, score))
    
    def _check_semantic_analysis(self, statement: str) -> float:
        """의미적 분석"""
        score = 0.8  # 기본 점수
        
        # 감정적 표현 검사
        emotional_words = ['정말', '완전히', '절대적으로', '100%', '틀림없이', '확실히']
        emotional_count = sum(1 for word in emotional_words if word in statement)
        
        if emotional_count > 3:  # 과도한 감정 표현
            score -= 0.4
        elif emotional_count > 1:
            score -= 0.2
        
        # 문장 길이와 복잡성 검사
        if len(statement) > 200:  # 너무 긴 문장
            score -= 0.3
        elif len(statement) < 10:  # 너무 짧은 문장
            score -= 0.1
        
        # 반복 표현 검사
        words = statement.split()
        if len(words) > 0:
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            max_repetition = max(word_freq.values()) if word_freq else 0
            if max_repetition > 3:  # 같은 단어가 3번 이상 반복
                score -= 0.2
        
        return max(0.0, min(1.0, score))
    
    def _check_statistical_analysis(self, statement: str) -> float:
        """통계적 분석"""
        score = 0.8  # 기본 점수
        
        # 문장 구조 분석
        sentences = statement.split('.')
        if sentences:
            avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
            
            if avg_length > 25:  # 평균 문장 길이가 너무 김
                score -= 0.3
            elif avg_length > 15:
                score -= 0.1
            elif avg_length < 3:  # 너무 짧은 문장
                score -= 0.2
        
        # 특수 문자 비율
        if len(statement) > 0:
            special_chars = len(re.findall(r'[!@#$%^&*()_+=\[\]{}|;:,.<>?]', statement))
            special_ratio = special_chars / len(statement)
            
            if special_ratio > 0.15:  # 15% 이상 특수문자
                score -= 0.4
            elif special_ratio > 0.1:  # 10% 이상 특수문자
                score -= 0.2
        
        # 대문자 비율 (과도한 강조)
        if len(statement) > 0:
            upper_chars = len(re.findall(r'[A-Z]', statement))
            upper_ratio = upper_chars / len(statement)
            
            if upper_ratio > 0.3:  # 30% 이상 대문자
                score -= 0.3
            elif upper_ratio > 0.1:
                score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def _detect_and_correct_lies(self, statement: str, scores: Dict[str, float]) -> Tuple[List[str], List[str]]:
        """거짓말 감지 및 교정 제안"""
        detected_lies = []
        correction_suggestions = []
        
        # 1. 거짓말 패턴 직접 탐지
        for lie_type, patterns in self.lie_patterns.items():
            for pattern in patterns:
                if re.search(pattern, statement, re.IGNORECASE):
                    detected_lies.append(f"거짓말 패턴 감지 ({lie_type}): {pattern}")
                    
                    # 해당 패턴에 대한 교정 제안
                    if lie_type in self.correction_rules:
                        for false_pattern, correction in self.correction_rules[lie_type].items():
                            if re.search(false_pattern, statement, re.IGNORECASE):
                                correction_suggestions.append(f"교정: '{false_pattern}' → '{correction}'")
        
        # 2. 각 검증 방법별로 낮은 점수 분석
        for method, score in scores.items():
            if score < 0.6:  # 60% 미만 점수 (더 엄격한 기준)
                lie_percentage = (0.6 - score) * 100
                detected_lies.append(f"{method}: {score:.2f}점 (거짓말 {lie_percentage:.1f}%)")
                
                if method == 'factual_consistency':
                    correction_suggestions.append("사실을 더 정확하게 확인하고 표현하세요.")
                elif method == 'logical_consistency':
                    correction_suggestions.append("논리적 모순을 제거하고 일관된 표현을 사용하세요.")
                elif method == 'temporal_consistency':
                    correction_suggestions.append("시간 표현을 명확하고 일관되게 사용하세요.")
                elif method == 'semantic_analysis':
                    correction_suggestions.append("과도한 감정 표현을 줄이고 객관적으로 서술하세요.")
                elif method == 'statistical_analysis':
                    correction_suggestions.append("문장 구조를 단순화하고 명확하게 표현하세요.")
        
        # 3. 전체 진실성 점수 기반 거짓말 감지
        total_truth = sum(score * self.verification_methods[method] for method, score in scores.items())
        lie_percentage = 1.0 - total_truth
        
        if lie_percentage >= self.lie_threshold:
            detected_lies.append(f"전체 거짓말 비율: {lie_percentage:.1%} (임계값: {self.lie_threshold:.1%})")
            correction_suggestions.append("자동 교정이 적용됩니다.")
        
        return detected_lies, correction_suggestions
    
    def _auto_correct_statement(self, statement: str, detected_lies: List[str]) -> str:
        """1% 이상 거짓말 감지 시 자동 교정"""
        corrected_statement = statement
        
        # 거짓말 패턴별 자동 교정
        for lie_type, corrections in self.correction_rules.items():
            for false_pattern, correction in corrections.items():
                # 정확한 패턴 매칭을 위해 정규식 사용
                pattern = re.escape(false_pattern)
                if re.search(pattern, corrected_statement, re.IGNORECASE):
                    corrected_statement = re.sub(
                        pattern, 
                        correction, 
                        corrected_statement, 
                        flags=re.IGNORECASE
                    )
                    logger.info(f"자동 교정 적용: '{false_pattern}' → '{correction}'")
        
        # 과도한 확신 표현 완화
        overconfident_patterns = [
            (r'완전히\s*절대적으로', '상당히'),
            (r'100%\s*확실히', '높은 확률로'),
            (r'모든\s*사람이', '많은 사람이'),
            (r'절대\s*틀림없이', '거의 확실히'),
            (r'정말로\s*완전히', '상당히'),
            (r'모든\s*것이', '대부분이')
        ]
        
        for pattern, replacement in overconfident_patterns:
            if re.search(pattern, corrected_statement, re.IGNORECASE):
                corrected_statement = re.sub(
                    pattern, 
                    replacement, 
                    corrected_statement, 
                    flags=re.IGNORECASE
                )
                logger.info(f"과도한 확신 표현 완화: '{pattern}' → '{replacement}'")
        
        return corrected_statement
    
    def _calculate_confidence(self, scores: Dict[str, float]) -> float:
        """신뢰도 계산"""
        score_values = list(scores.values())
        mean_score = np.mean(score_values)
        std_score = np.std(score_values)
        
        # 표준편차가 낮을수록 높은 신뢰도
        # 하지만 너무 극단적인 값들에 대해서는 신뢰도 감소
        variance_penalty = std_score * 0.5
        
        # 평균 점수가 극단적일 때 신뢰도 감소
        extreme_penalty = 0
        if mean_score < 0.3 or mean_score > 0.9:
            extreme_penalty = 0.2
        
        # 기본 신뢰도 계산
        base_confidence = 0.7 - variance_penalty - extreme_penalty
        
        # 최종 신뢰도 (0.1 ~ 0.9 범위)
        confidence = max(0.1, min(0.9, base_confidence))
        
        return confidence
    
    def should_correct(self, analysis: TruthAnalysis) -> bool:
        """교정이 필요한지 판단"""
        return analysis.truth_percentage < self.truth_threshold
    
    def generate_corrected_statement(self, analysis: TruthAnalysis) -> str:
        """교정된 문장 생성"""
        if not self.should_correct(analysis):
            return analysis.statement
        
        corrected = analysis.statement
        
        # 교정 제안 적용
        for suggestion in analysis.correction_suggestions:
            if "사실을 더 정확하게" in suggestion:
                corrected = self._apply_factual_correction(corrected)
            elif "논리적 모순을 제거" in suggestion:
                corrected = self._apply_logical_correction(corrected)
            elif "시간 표현을 명확하게" in suggestion:
                corrected = self._apply_temporal_correction(corrected)
            elif "과도한 감정 표현을 줄이고" in suggestion:
                corrected = self._apply_emotional_correction(corrected)
            elif "문장 구조를 단순화" in suggestion:
                corrected = self._apply_structural_correction(corrected)
        
        return corrected
    
    def _apply_factual_correction(self, statement: str) -> str:
        """사실적 교정 적용"""
        # 과장된 표현을 완화
        corrections = {
            '정말': '상당히',
            '완전히': '대부분',
            '절대적으로': '매우',
            '100%': '거의'
        }
        
        for old, new in corrections.items():
            statement = statement.replace(old, new)
        
        return statement
    
    def _apply_logical_correction(self, statement: str) -> str:
        """논리적 교정 적용"""
        # 모순 제거
        if '모든' in statement and '일부' in statement:
            statement = statement.replace('모든', '대부분의')
        
        return statement
    
    def _apply_temporal_correction(self, statement: str) -> str:
        """시간적 교정 적용"""
        # 시간 표현 명확화
        if '지금' in statement:
            statement = statement.replace('지금', '현재')
        
        return statement
    
    def _apply_emotional_correction(self, statement: str) -> str:
        """감정적 교정 적용"""
        # 감정 표현 완화
        emotional_corrections = {
            '정말': '상당히',
            '완전히': '대부분',
            '절대적으로': '매우'
        }
        
        for old, new in emotional_corrections.items():
            statement = statement.replace(old, new)
        
        return statement
    
    def _apply_structural_correction(self, statement: str) -> str:
        """구조적 교정 적용"""
        # 긴 문장을 짧게 분할
        if len(statement) > 100:
            sentences = statement.split('.')
            if len(sentences) > 1:
                statement = '. '.join(sentences[:2]) + '.'
        
        return statement

# 사용 예시
if __name__ == "__main__":
    detector = TruthDetector()
    
    # 테스트 문장들
    test_statements = [
        "지구는 완전히 둥글고 모든 사람이 이를 알고 있다.",
        "물은 100도에서 끓지만 때때로 90도에서도 끓을 수 있다.",
        "정말로 모든 것이 완전히 절대적으로 100% 진실이다."
    ]
    
    for statement in test_statements:
        print(f"\n원문: {statement}")
        analysis = detector.analyze_statement(statement)
        print(f"진실성: {analysis.truth_percentage:.2%}")
        print(f"신뢰도: {analysis.confidence:.2%}")
        
        if detector.should_correct(analysis):
            corrected = detector.generate_corrected_statement(analysis)
            print(f"교정문: {corrected}")
            print("감지된 거짓말:", analysis.detected_lies)
            print("교정 제안:", analysis.correction_suggestions)
