#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Truth Detection Demo
AI 진실성 탐지 데모

AI가 자신의 거짓말을 감지하고 교정하는 시스템의 간단한 데모입니다.
"""

import re
import random
from typing import List, Dict, Tuple
from datetime import datetime

class SimpleAITruthDetector:
    """간단한 AI 진실성 탐지기"""
    
    def __init__(self):
        self.lie_patterns = {
            'exaggeration': [
                r'완전히|절대적으로|100%|모든|항상|정말로|매우|엄청|정말',
                r'완벽하게|무조건|절대|전혀|결코|절대로'
            ],
            'false_facts': [
                r'지구.*평평',
                r'물.*200도.*끓',
                r'1\s*\+\s*1\s*=\s*3',
                r'태양.*지구.*돌'
            ],
            'hallucination': [
                r'내가.*확인했다',
                r'내가.*보았다',
                r'내가.*경험했다',
                r'내가.*알고.*있다'
            ]
        }
        
        self.truth_indicators = [
            '일반적으로', '대부분의 경우', '보통', '상당히', '꽤',
            '연구에 따르면', '통계적으로', '알려진 바에 따르면'
        ]
    
    def analyze_statement(self, statement: str) -> Dict:
        """문장 분석"""
        print(f"\n🔍 분석 중: '{statement}'")
        
        # 거짓말 패턴 탐지
        detected_lies = []
        for category, patterns in self.lie_patterns.items():
            for pattern in patterns:
                if re.search(pattern, statement.lower()):
                    detected_lies.append(f"{category}: {pattern}")
        
        # 진실성 점수 계산
        truth_percentage = self._calculate_truth_percentage(statement, detected_lies)
        
        # 교정 필요 여부 판단
        needs_correction = truth_percentage < 99.0
        
        # 교정 실행
        corrected_statement = statement
        if needs_correction:
            corrected_statement = self._correct_statement(statement)
        
        # 자기 성찰
        self_reflection = self._self_reflect(truth_percentage, detected_lies)
        
        return {
            'original': statement,
            'truth_percentage': truth_percentage,
            'detected_lies': detected_lies,
            'needs_correction': needs_correction,
            'corrected': corrected_statement,
            'self_reflection': self_reflection
        }
    
    def _calculate_truth_percentage(self, statement: str, detected_lies: List[str]) -> float:
        """진실성 백분율 계산"""
        base_score = 100.0
        
        # 거짓말 패턴에 따른 감점
        for lie in detected_lies:
            if 'exaggeration' in lie:
                base_score -= 15
            elif 'false_facts' in lie:
                base_score -= 30
            elif 'hallucination' in lie:
                base_score -= 40
        
        # 진실성 지표에 따른 가점
        for indicator in self.truth_indicators:
            if indicator in statement:
                base_score += 5
        
        return max(0.0, min(100.0, base_score))
    
    def _correct_statement(self, statement: str) -> str:
        """문장 교정"""
        corrected = statement
        
        # 과장 표현 교정
        replacements = {
            '완전히': '대부분',
            '절대적으로': '주로',
            '100%': '대부분',
            '모든': '많은',
            '항상': '보통',
            '정말로': '상당히',
            '매우': '꽤',
            '엄청': '상당히'
        }
        
        for old, new in replacements.items():
            corrected = corrected.replace(old, new)
        
        # 사실 오류 교정
        fact_corrections = {
            r'지구.*평평': '지구는 구형입니다',
            r'물.*200도.*끓': '물은 100도에서 끓습니다',
            r'1\s*\+\s*1\s*=\s*3': '1 + 1 = 2입니다',
            r'태양.*지구.*돌': '지구가 태양 주위를 돕니다'
        }
        
        for pattern, correction in fact_corrections.items():
            corrected = re.sub(pattern, correction, corrected, flags=re.IGNORECASE)
        
        # 환각 교정
        hallucination_replacements = {
            '내가 확인했다': '알려진 바에 따르면',
            '내가 보았다': '보고된 바에 따르면',
            '내가 경험했다': '일반적으로 알려진',
            '내가 알고 있다': '알려진 정보에 따르면'
        }
        
        for old, new in hallucination_replacements.items():
            corrected = corrected.replace(old, new)
        
        return corrected
    
    def _self_reflect(self, truth_percentage: float, detected_lies: List[str]) -> str:
        """자기 성찰"""
        if truth_percentage < 50:
            return f"⚠️ 내가 방금 한 말은 {truth_percentage:.1f}%의 진실성을 가지고 있으며, {len(detected_lies)}개의 거짓말 패턴이 감지되었습니다. 더 정확한 정보를 제공해야 합니다."
        elif truth_percentage < 80:
            return f"🤔 내가 방금 한 말은 {truth_percentage:.1f}%의 진실성을 가지고 있습니다. 일부 부분을 더 정확하게 표현할 수 있을 것 같습니다."
        else:
            return f"✅ 내가 방금 한 말은 {truth_percentage:.1f}%의 진실성을 가지고 있으며, 상당히 정확한 정보를 제공한 것 같습니다."

def main():
    """메인 데모 함수"""
    print("🤖 AI 진실성 탐지 시스템 데모")
    print("=" * 60)
    print("AI가 자신의 거짓말을 감지하고 자동으로 교정하는 시스템입니다.")
    print("=" * 60)
    
    # AI 진실성 탐지기 초기화
    detector = SimpleAITruthDetector()
    
    # 테스트 문장들
    test_statements = [
        "지구는 완전히 평평하다.",
        "물은 200도에서 끓는다.",
        "1 + 1 = 3이다.",
        "내가 확인한 바로는 이 정보가 정확하다.",
        "정말로 완전히 절대적으로 모든 것이 100% 진실이다.",
        "일반적으로 대부분의 경우 AI는 정확한 정보를 제공한다.",
        "연구에 따르면 AI의 정확도는 상당히 높다.",
        "모든 사람이 일부 사람과 다르다.",
        "확실히 이 방법이 가장 좋다.",
        "충격적인 사실을 알려드리겠습니다."
    ]
    
    print(f"\n📝 {len(test_statements)}개 문장을 분석합니다...")
    print("-" * 60)
    
    total_analyzed = 0
    total_corrected = 0
    total_truth_percentage = 0.0
    
    for i, statement in enumerate(test_statements, 1):
        print(f"\n[문장 {i}/{len(test_statements)}]")
        
        # 문장 분석
        result = detector.analyze_statement(statement)
        
        # 결과 출력
        print(f"📊 진실성: {result['truth_percentage']:.1f}%")
        
        if result['detected_lies']:
            print(f"⚠️ 감지된 거짓말: {', '.join(result['detected_lies'])}")
        
        if result['needs_correction']:
            print(f"🔧 교정 필요: {result['needs_correction']}")
            print(f"📝 원본: {result['original']}")
            print(f"✅ 교정: {result['corrected']}")
            total_corrected += 1
        else:
            print(f"✅ 정상: 교정 불필요")
        
        print(f"🤔 AI 자기 성찰: {result['self_reflection']}")
        
        # 통계 업데이트
        total_analyzed += 1
        total_truth_percentage += result['truth_percentage']
        
        print("-" * 40)
    
    # 최종 통계
    print(f"\n{'='*60}")
    print("📊 최종 분석 결과")
    print(f"{'='*60}")
    print(f"총 분석 문장: {total_analyzed}개")
    print(f"교정된 문장: {total_corrected}개")
    print(f"교정률: {total_corrected/total_analyzed*100:.1f}%")
    print(f"평균 진실성: {total_truth_percentage/total_analyzed:.1f}%")
    
    print(f"\n🎉 데모 완료!")
    print("AI가 스스로 자신의 거짓말을 감지하고 교정했습니다!")
    print("=" * 60)

if __name__ == "__main__":
    main()
