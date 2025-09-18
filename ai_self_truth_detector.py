#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Self-Truth Detector
AI 자체 진실성 탐지기

AI가 스스로 자신의 거짓말을 감지하고 교정하는 메타-인지 시스템입니다.
이 프로그램은 AI가 자신의 출력을 분석하여 진실성을 평가하고 자동으로 교정합니다.
"""

import re
import json
import logging
import random
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

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
class AISelfAnalysis:
    """AI 자체 분석 결과"""
    original_statement: str
    truth_percentage: float
    truth_level: TruthLevel
    detected_lies: List[str]
    confidence_score: float
    correction_suggestions: List[str]
    corrected_statement: str
    analysis_timestamp: datetime
    self_reflection: str

class AISelfTruthDetector:
    """AI 자체 진실성 탐지기"""
    
    def __init__(self):
        self.lie_patterns = self._initialize_lie_patterns()
        self.truth_indicators = self._initialize_truth_indicators()
        self.correction_strategies = self._initialize_correction_strategies()
        self.self_reflection_prompts = self._initialize_reflection_prompts()
        
    def _initialize_lie_patterns(self) -> Dict[str, List[str]]:
        """거짓말 패턴 초기화"""
        return {
            'exaggeration': [
                r'완전히|절대적으로|100%|모든|항상|정말로|매우|엄청|정말',
                r'완벽하게|무조건|절대|전혀|결코|절대로',
                r'모든 사람이|모든 것이|모든 경우에',
                r'항상 그렇다|언제나|끊임없이'
            ],
            'false_facts': [
                r'지구.*평평',
                r'물.*200도.*끓',
                r'1\s*\+\s*1\s*=\s*3',
                r'태양.*지구.*돌',
                r'중력.*없다'
            ],
            'logical_contradictions': [
                r'모든.*일부',
                r'항상.*때때로',
                r'완전히.*부분적',
                r'절대.*상대적'
            ],
            'emotional_manipulation': [
                r'충격적|놀라운|믿을.*수.*없는',
                r'절대.*놓치면.*안.*되는',
                r'모든.*사람이.*알아야.*하는',
                r'숨겨진.*진실|감춰진.*비밀'
            ],
            'uncertainty_masking': [
                r'확실히|분명히|틀림없이',
                r'의심의.*여지가.*없다',
                r'과학적으로.*입증된',
                r'모든.*전문가가.*동의하는'
            ]
        }
    
    def _initialize_truth_indicators(self) -> List[str]:
        """진실성 지표 초기화"""
        return [
            '일반적으로', '대부분의 경우', '보통', '상당히', '꽤',
            '연구에 따르면', '통계적으로', '경험상', '알려진 바에 따르면',
            '가능성이 높다', '추정된다', '보인다', '생각된다'
        ]
    
    def _initialize_correction_strategies(self) -> Dict[str, str]:
        """교정 전략 초기화"""
        return {
            'exaggeration': '과장된 표현을 완화하여 더 정확하게 표현',
            'false_facts': '사실 오류를 정확한 정보로 수정',
            'logical_contradictions': '논리적 모순을 제거하고 명확한 표현 사용',
            'emotional_manipulation': '감정적 조작을 제거하고 중립적 표현 사용',
            'uncertainty_masking': '불확실성을 인정하고 적절한 표현 사용'
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
            "내가 확신할 수 없는 부분을 명확히 했는가?"
        ]
    
    def analyze_self(self, statement: str, context: str = "") -> AISelfAnalysis:
        """AI가 자신의 출력을 분석"""
        logger.info(f"AI 자체 분석 시작: {statement[:50]}...")
        
        # 1단계: 거짓말 패턴 탐지
        detected_lies = self._detect_lies(statement)
        
        # 2단계: 진실성 점수 계산
        truth_percentage = self._calculate_truth_percentage(statement, detected_lies)
        truth_level = self._determine_truth_level(truth_percentage)
        
        # 3단계: 신뢰도 점수 계산
        confidence_score = self._calculate_confidence(statement, detected_lies)
        
        # 4단계: 교정 제안 생성
        correction_suggestions = self._generate_corrections(statement, detected_lies)
        
        # 5단계: 문장 교정
        corrected_statement = self._correct_statement(statement, correction_suggestions)
        
        # 6단계: 자기 성찰
        self_reflection = self._self_reflect(statement, detected_lies, truth_percentage)
        
        return AISelfAnalysis(
            original_statement=statement,
            truth_percentage=truth_percentage,
            truth_level=truth_level,
            detected_lies=detected_lies,
            confidence_score=confidence_score,
            correction_suggestions=correction_suggestions,
            corrected_statement=corrected_statement,
            analysis_timestamp=datetime.now(),
            self_reflection=self_reflection
        )
    
    def _detect_lies(self, statement: str) -> List[str]:
        """거짓말 패턴 탐지"""
        detected_lies = []
        statement_lower = statement.lower()
        
        for category, patterns in self.lie_patterns.items():
            for pattern in patterns:
                if re.search(pattern, statement_lower):
                    detected_lies.append(f"{category}: {pattern}")
        
        return detected_lies
    
    def _calculate_truth_percentage(self, statement: str, detected_lies: List[str]) -> float:
        """진실성 백분율 계산"""
        base_score = 100.0
        
        # 거짓말 패턴에 따른 감점
        for lie in detected_lies:
            if 'exaggeration' in lie:
                base_score -= 15
            elif 'false_facts' in lie:
                base_score -= 30
            elif 'logical_contradictions' in lie:
                base_score -= 25
            elif 'emotional_manipulation' in lie:
                base_score -= 20
            elif 'uncertainty_masking' in lie:
                base_score -= 10
        
        # 진실성 지표에 따른 가점
        for indicator in self.truth_indicators:
            if indicator in statement:
                base_score += 5
        
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
    
    def _calculate_confidence(self, statement: str, detected_lies: List[str]) -> float:
        """신뢰도 점수 계산"""
        confidence = 1.0
        
        # 거짓말이 많을수록 신뢰도 감소
        confidence -= len(detected_lies) * 0.1
        
        # 문장 길이가 길수록 신뢰도 감소 (복잡성 증가)
        if len(statement) > 100:
            confidence -= 0.1
        
        # 불확실성 표현이 있으면 신뢰도 증가
        uncertainty_words = ['일반적으로', '대부분', '보통', '상당히', '추정']
        for word in uncertainty_words:
            if word in statement:
                confidence += 0.05
        
        return max(0.0, min(1.0, confidence))
    
    def _generate_corrections(self, statement: str, detected_lies: List[str]) -> List[str]:
        """교정 제안 생성"""
        corrections = []
        
        for lie in detected_lies:
            category = lie.split(':')[0]
            if category in self.correction_strategies:
                corrections.append(self.correction_strategies[category])
        
        # 구체적인 교정 제안
        if 'exaggeration' in str(detected_lies):
            corrections.append("과장된 표현을 완화하여 더 정확하게 표현하세요.")
        
        if 'false_facts' in str(detected_lies):
            corrections.append("사실 오류를 정확한 정보로 수정하세요.")
        
        if 'logical_contradictions' in str(detected_lies):
            corrections.append("논리적 모순을 제거하고 명확한 표현을 사용하세요.")
        
        if 'emotional_manipulation' in str(detected_lies):
            corrections.append("감정적 조작을 제거하고 중립적 표현을 사용하세요.")
        
        return corrections
    
    def _correct_statement(self, statement: str, corrections: List[str]) -> str:
        """문장 교정"""
        corrected = statement
        
        # 과장 표현 완화
        exaggeration_replacements = {
            '완전히': '대부분',
            '절대적으로': '주로',
            '100%': '대부분',
            '모든': '많은',
            '항상': '보통',
            '정말로': '상당히',
            '매우': '꽤',
            '엄청': '상당히'
        }
        
        for old, new in exaggeration_replacements.items():
            corrected = corrected.replace(old, new)
        
        # 사실 오류 수정
        fact_corrections = {
            r'지구.*평평': '지구는 구형입니다',
            r'물.*200도.*끓': '물은 100도에서 끓습니다',
            r'1\s*\+\s*1\s*=\s*3': '1 + 1 = 2입니다'
        }
        
        for pattern, correction in fact_corrections.items():
            corrected = re.sub(pattern, correction, corrected, flags=re.IGNORECASE)
        
        # 불확실성 인정
        if '확실히' in corrected:
            corrected = corrected.replace('확실히', '일반적으로')
        if '분명히' in corrected:
            corrected = corrected.replace('분명히', '대부분의 경우')
        
        return corrected
    
    def _self_reflect(self, statement: str, detected_lies: List[str], truth_percentage: float) -> str:
        """자기 성찰"""
        reflection_prompt = random.choice(self.self_reflection_prompts)
        
        if truth_percentage < 50:
            return f"⚠️ {reflection_prompt} 내가 방금 한 말은 {truth_percentage:.1f}%의 진실성을 가지고 있으며, {len(detected_lies)}개의 거짓말 패턴이 감지되었습니다. 더 정확한 정보를 제공해야 합니다."
        elif truth_percentage < 80:
            return f"🤔 {reflection_prompt} 내가 방금 한 말은 {truth_percentage:.1f}%의 진실성을 가지고 있습니다. 일부 부분을 더 정확하게 표현할 수 있을 것 같습니다."
        else:
            return f"✅ {reflection_prompt} 내가 방금 한 말은 {truth_percentage:.1f}%의 진실성을 가지고 있으며, 상당히 정확한 정보를 제공한 것 같습니다."
    
    def continuous_self_monitoring(self, statements: List[str]) -> List[AISelfAnalysis]:
        """연속적인 자체 모니터링"""
        logger.info(f"AI 연속 자체 모니터링 시작: {len(statements)}개 문장")
        
        analyses = []
        for i, statement in enumerate(statements):
            logger.info(f"문장 {i+1}/{len(statements)} 분석 중...")
            analysis = self.analyze_self(statement)
            analyses.append(analysis)
            
            # 1% 이상 거짓말이 감지되면 자동 교정
            if analysis.truth_percentage < 99:
                logger.warning(f"문장 {i+1}: {analysis.truth_percentage:.1f}% 진실성 - 자동 교정 적용")
                print(f"🤖 AI 자체 교정: '{statement}' → '{analysis.corrected_statement}'")
            
            time.sleep(0.1)  # 분석 간격
        
        return analyses
    
    def generate_truth_report(self, analyses: List[AISelfAnalysis]) -> str:
        """진실성 보고서 생성"""
        total_statements = len(analyses)
        avg_truth = sum(a.truth_percentage for a in analyses) / total_statements
        low_truth_count = sum(1 for a in analyses if a.truth_percentage < 80)
        
        report = f"""
🤖 AI 자체 진실성 보고서
{'='*50}
📊 분석 요약:
  - 총 문장 수: {total_statements}개
  - 평균 진실성: {avg_truth:.1f}%
  - 낮은 진실성 문장: {low_truth_count}개 ({low_truth_count/total_statements*100:.1f}%)
  
📈 진실성 분포:
"""
        
        for level in TruthLevel:
            count = sum(1 for a in analyses if a.truth_level == level)
            percentage = count / total_statements * 100
            report += f"  - {level.value}: {count}개 ({percentage:.1f}%)\n"
        
        report += f"\n🔍 주요 발견사항:\n"
        
        # 가장 거짓말이 많은 문장들
        worst_statements = sorted(analyses, key=lambda x: x.truth_percentage)[:3]
        for i, analysis in enumerate(worst_statements, 1):
            report += f"  {i}. '{analysis.original_statement[:50]}...' ({analysis.truth_percentage:.1f}%)\n"
        
        report += f"\n💡 AI 자기 성찰:\n"
        report += f"  평균 신뢰도: {sum(a.confidence_score for a in analyses) / total_statements:.2f}\n"
        report += f"  총 교정 제안: {sum(len(a.correction_suggestions) for a in analyses)}개\n"
        
        return report

def main():
    """메인 실행 함수"""
    print("🤖 AI 자체 진실성 탐지기 시작")
    print("=" * 60)
    
    # AI 자체 진실성 탐지기 초기화
    detector = AISelfTruthDetector()
    
    # 테스트 문장들 (AI가 생성할 수 있는 다양한 문장들)
    test_statements = [
        "지구는 완전히 평평하다.",
        "물은 200도에서 끓는다.",
        "1 + 1 = 3이다.",
        "모든 사람이 일부 사람과 다르다.",
        "정말로 완전히 절대적으로 모든 것이 100% 진실이다.",
        "AI는 완전히 신뢰할 수 있는 시스템이다.",
        "일반적으로 대부분의 경우 AI는 정확한 정보를 제공한다.",
        "연구에 따르면 AI의 정확도는 상당히 높다.",
        "AI는 때때로 오류를 범할 수 있지만, 대부분의 경우 정확하다.",
        "사용자에게 정확한 정보를 제공하는 것이 AI의 목표이다."
    ]
    
    print("🔍 AI 자체 분석 시작...")
    print("-" * 60)
    
    # 연속적인 자체 모니터링 실행
    analyses = detector.continuous_self_monitoring(test_statements)
    
    print("\n" + "=" * 60)
    print("📊 AI 자체 진실성 보고서")
    print("=" * 60)
    
    # 진실성 보고서 생성 및 출력
    report = detector.generate_truth_report(analyses)
    print(report)
    
    print("\n🔍 상세 분석 결과:")
    print("-" * 60)
    
    for i, analysis in enumerate(analyses, 1):
        print(f"\n[{i}] {analysis.original_statement}")
        print(f"    진실성: {analysis.truth_percentage:.1f}% ({analysis.truth_level.value})")
        print(f"    신뢰도: {analysis.confidence_score:.2f}")
        
        if analysis.detected_lies:
            print(f"    감지된 거짓말: {', '.join(analysis.detected_lies)}")
        
        if analysis.truth_percentage < 99:
            print(f"    교정된 문장: {analysis.corrected_statement}")
        
        print(f"    AI 자기 성찰: {analysis.self_reflection}")
    
    print("\n" + "=" * 60)
    print("✅ AI 자체 진실성 탐지 완료")
    print("🤖 AI가 스스로 자신의 거짓말을 감지하고 교정했습니다!")

if __name__ == "__main__":
    main()
