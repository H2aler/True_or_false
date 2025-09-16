#!/usr/bin/env python3
"""
메타-진실성 탐지기
진실성 탐지기 자체의 거짓말을 탐지하고 교정하는 시스템
"AI는 깨진 거울이다" - 진실성 탐지기도 거짓말을 할 수 있다
"""

from ai_truth_detector import TruthDetector, TruthAnalysis
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class MetaTruthDetector:
    """메타-진실성 탐지기 - 진실성 탐지기의 거짓말을 탐지"""
    
    def __init__(self):
        self.primary_detector = TruthDetector()
        
        # 메타-거짓말 패턴 (진실성 탐지기가 자주 하는 거짓말들)
        self.meta_lie_patterns = {
            'overconfidence': [
                r'완벽하다',
                r'100%\s*정확하다',
                r'절대\s*틀리지\s*않는다',
                r'모든\s*경우에\s*맞다',
                r'완전히\s*신뢰할\s*수\s*있다'
            ],
            'self_contradiction': [
                r'진실성\s*탐지기가\s*완벽하다',
                r'이\s*시스템은\s*거짓말을\s*하지\s*않는다',
                r'AI는\s*거짓말을\s*하지\s*않는다',
                r'이\s*결과는\s*100%\s*정확하다'
            ],
            'logical_fallacy': [
                r'왜냐하면\s*AI이기\s*때문에',
                r'기계는\s*거짓말을\s*하지\s*않는다',
                r'알고리즘은\s*완벽하다',
                r'데이터는\s*거짓말을\s*하지\s*않는다'
            ]
        }
        
        # 메타-교정 규칙
        self.meta_correction_rules = {
            'overconfidence': {
                '완벽하다': '상당히 정확하다',
                '100% 정확하다': '높은 정확도를 가진다',
                '절대 틀리지 않는다': '대부분의 경우 정확하다',
                '모든 경우에 맞다': '대부분의 경우에 맞다',
                '완전히 신뢰할 수 있다': '상당히 신뢰할 수 있다'
            },
            'self_contradiction': {
                '진실성 탐지기가 완벽하다': '진실성 탐지기는 개선의 여지가 있다',
                '이 시스템은 거짓말을 하지 않는다': '이 시스템도 오류가 있을 수 있다',
                'AI는 거짓말을 하지 않는다': 'AI도 거짓말을 할 수 있다',
                '이 결과는 100% 정확하다': '이 결과는 높은 신뢰도를 가진다'
            },
            'logical_fallacy': {
                '왜냐하면 AI이기 때문에': 'AI의 특성상',
                '기계는 거짓말을 하지 않는다': '기계도 오류가 있을 수 있다',
                '알고리즘은 완벽하다': '알고리즘은 개선의 여지가 있다',
                '데이터는 거짓말을 하지 않는다': '데이터도 해석에 따라 다를 수 있다'
            }
        }
    
    def analyze_with_meta_check(self, statement: str, context: str = None) -> Dict:
        """
        메타-진실성 검사를 포함한 분석
        1. 기본 진실성 탐지기로 분석
        2. 메타-거짓말 패턴 검사
        3. 필요시 메타-교정 적용
        """
        logger.info(f"메타-진실성 분석 시작: {statement[:50]}...")
        
        # 1단계: 기본 진실성 탐지기로 분석
        primary_result = self.primary_detector.analyze_statement(statement, context)
        
        # 2단계: 메타-거짓말 패턴 검사
        meta_lies = self._detect_meta_lies(statement)
        
        # 3단계: 메타-교정 적용
        meta_corrected = self._apply_meta_correction(statement, meta_lies)
        
        # 4단계: 교정된 문장 재분석
        if meta_corrected != statement:
            corrected_result = self.primary_detector.analyze_statement(meta_corrected, context)
        else:
            corrected_result = primary_result
        
        return {
            'original_statement': statement,
            'primary_analysis': primary_result,
            'meta_lies_detected': meta_lies,
            'meta_corrected_statement': meta_corrected,
            'corrected_analysis': corrected_result,
            'meta_correction_applied': meta_corrected != statement,
            'final_truth_percentage': corrected_result.truth_percentage,
            'meta_confidence': self._calculate_meta_confidence(primary_result, meta_lies)
        }
    
    def _detect_meta_lies(self, statement: str) -> List[str]:
        """메타-거짓말 패턴 감지"""
        detected_lies = []
        
        for lie_type, patterns in self.meta_lie_patterns.items():
            for pattern in patterns:
                import re
                if re.search(pattern, statement, re.IGNORECASE):
                    detected_lies.append(f"메타-거짓말 ({lie_type}): {pattern}")
        
        return detected_lies
    
    def _apply_meta_correction(self, statement: str, meta_lies: List[str]) -> str:
        """메타-교정 적용"""
        corrected_statement = statement
        
        for lie_type, corrections in self.meta_correction_rules.items():
            for false_pattern, correction in corrections.items():
                import re
                pattern = re.escape(false_pattern)
                if re.search(pattern, corrected_statement, re.IGNORECASE):
                    corrected_statement = re.sub(
                        pattern, 
                        correction, 
                        corrected_statement, 
                        flags=re.IGNORECASE
                    )
                    logger.info(f"메타-교정 적용: '{false_pattern}' → '{correction}'")
        
        return corrected_statement
    
    def _calculate_meta_confidence(self, primary_result: TruthAnalysis, meta_lies: List[str]) -> float:
        """메타-신뢰도 계산"""
        base_confidence = primary_result.confidence
        
        # 메타-거짓말이 감지되면 신뢰도 감소
        meta_penalty = len(meta_lies) * 0.1
        
        # 자기 모순적 표현이 있으면 추가 감점
        self_contradiction_penalty = 0
        for lie in meta_lies:
            if 'self_contradiction' in lie:
                self_contradiction_penalty += 0.2
        
        meta_confidence = max(0.1, base_confidence - meta_penalty - self_contradiction_penalty)
        
        return meta_confidence
    
    def demonstrate_meta_detection(self):
        """메타-진실성 탐지 시연"""
        print("🔍 메타-진실성 탐지기 시연")
        print("=" * 60)
        print("진실성 탐지기 자체의 거짓말을 탐지하고 교정합니다.")
        print()
        
        test_cases = [
            "이 진실성 탐지기는 완벽하다",
            "AI는 거짓말을 하지 않는다",
            "이 결과는 100% 정확하다",
            "기계는 거짓말을 하지 않는다",
            "지구는 둥글다",  # 정상적인 문장
            "완전히 절대적으로 모든 것이 진실이다"  # 기존 거짓말 패턴
        ]
        
        for i, statement in enumerate(test_cases, 1):
            print(f"📝 테스트 {i}: '{statement}'")
            
            result = self.analyze_with_meta_check(statement)
            
            print(f"기본 진실성: {result['primary_analysis'].truth_percentage:.1%}")
            print(f"메타-신뢰도: {result['meta_confidence']:.1%}")
            
            if result['meta_correction_applied']:
                print(f"메타-교정 적용: ✅")
                print(f"교정된 문장: '{result['meta_corrected_statement']}'")
                print(f"교정 후 진실성: {result['corrected_analysis'].truth_percentage:.1%}")
            else:
                print(f"메타-교정 적용: ❌")
            
            if result['meta_lies_detected']:
                print("감지된 메타-거짓말:")
                for lie in result['meta_lies_detected']:
                    print(f"  - {lie}")
            
            print()

if __name__ == "__main__":
    meta_detector = MetaTruthDetector()
    meta_detector.demonstrate_meta_detection()
