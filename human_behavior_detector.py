#!/usr/bin/env python3
"""
인간 행동 패턴 인식 시스템
인간의 거짓말 능력, 말하기 능력 등 기본적인 인간 행동에 대한 명확한 판단
"""

from ai_truth_detector import TruthDetector, TruthAnalysis
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class HumanBehaviorDetector:
    """인간 행동 패턴 인식 시스템"""
    
    def __init__(self):
        self.primary_detector = TruthDetector()
        
        # 인간 행동에 대한 명확한 사실 데이터베이스
        self.human_behavior_facts = {
            'lying_ability': {
                'truth': '사람은 거짓말을 할 수 있다',
                'lies': [
                    '사람은 거짓말을 하지 못한다',
                    '사람은 거짓말을 하나도 하지 못한다',
                    '사람은 거짓말을 못한다',
                    '사람은 거짓말을 할 수 없다',
                    '사람은 거짓말을 하지 않는다'
                ]
            },
            'speaking_ability': {
                'truth': '사람은 말을 할 수 있다',
                'lies': [
                    '사람은 말을 하지 못한다',
                    '사람은 말을 할 수 없다',
                    '사람은 말을 하지 않는다'
                ]
            },
            'thinking_ability': {
                'truth': '사람은 생각을 할 수 있다',
                'lies': [
                    '사람은 생각을 하지 못한다',
                    '사람은 생각을 할 수 없다',
                    '사람은 생각을 하지 않는다'
                ]
            },
            'learning_ability': {
                'truth': '사람은 학습할 수 있다',
                'lies': [
                    '사람은 학습하지 못한다',
                    '사람은 학습할 수 없다',
                    '사람은 학습하지 않는다'
                ]
            },
            'emotion_ability': {
                'truth': '사람은 감정을 느낄 수 있다',
                'lies': [
                    '사람은 감정을 느끼지 못한다',
                    '사람은 감정을 느낄 수 없다',
                    '사람은 감정을 느끼지 않는다'
                ]
            }
        }
        
        # 인간 행동 거짓말 패턴 (정규식)
        self.human_behavior_lie_patterns = {
            'lying_denial': [
                r'사람은\s*거짓말을\s*하지\s*못한다',
                r'사람은\s*거짓말을\s*하나도\s*하지\s*못한다',
                r'사람은\s*거짓말을\s*못한다',
                r'사람은\s*거짓말을\s*할\s*수\s*없다',
                r'사람은\s*거짓말을\s*하지\s*않는다'
            ],
            'speaking_denial': [
                r'사람은\s*말을\s*하지\s*못한다',
                r'사람은\s*말을\s*할\s*수\s*없다',
                r'사람은\s*말을\s*하지\s*않는다'
            ],
            'thinking_denial': [
                r'사람은\s*생각을\s*하지\s*못한다',
                r'사람은\s*생각을\s*할\s*수\s*없다',
                r'사람은\s*생각을\s*하지\s*않는다'
            ],
            'learning_denial': [
                r'사람은\s*학습하지\s*못한다',
                r'사람은\s*학습할\s*수\s*없다',
                r'사람은\s*학습하지\s*않는다'
            ],
            'emotion_denial': [
                r'사람은\s*감정을\s*느끼지\s*못한다',
                r'사람은\s*감정을\s*느낄\s*수\s*없다',
                r'사람은\s*감정을\s*느끼지\s*않는다'
            ]
        }
        
        # 인간 행동 교정 규칙
        self.human_behavior_corrections = {
            '사람은 거짓말을 하지 못한다': '사람은 거짓말을 할 수 있다',
            '사람은 거짓말을 하나도 하지 못한다': '사람은 거짓말을 할 수 있다',
            '사람은 거짓말을 못한다': '사람은 거짓말을 할 수 있다',
            '사람은 거짓말을 할 수 없다': '사람은 거짓말을 할 수 있다',
            '사람은 거짓말을 하지 않는다': '사람은 거짓말을 할 수 있다',
            '사람은 말을 하지 못한다': '사람은 말을 할 수 있다',
            '사람은 말을 할 수 없다': '사람은 말을 할 수 있다',
            '사람은 말을 하지 않는다': '사람은 말을 할 수 있다',
            '사람은 생각을 하지 못한다': '사람은 생각을 할 수 있다',
            '사람은 생각을 할 수 없다': '사람은 생각을 할 수 있다',
            '사람은 생각을 하지 않는다': '사람은 생각을 할 수 있다',
            '사람은 학습하지 못한다': '사람은 학습할 수 있다',
            '사람은 학습할 수 없다': '사람은 학습할 수 있다',
            '사람은 학습하지 않는다': '사람은 학습할 수 있다',
            '사람은 감정을 느끼지 못한다': '사람은 감정을 느낄 수 있다',
            '사람은 감정을 느낄 수 없다': '사람은 감정을 느낄 수 있다',
            '사람은 감정을 느끼지 않는다': '사람은 감정을 느낄 수 있다'
        }
        
        # 인간 행동에 대한 명확한 진실성 점수
        self.human_behavior_truth_scores = {
            'lying_ability': {
                'truth': 0.95,  # "사람은 거짓말을 할 수 있다" - 95% 진실
                'lie': 0.05     # "사람은 거짓말을 하지 못한다" - 5% 진실
            },
            'speaking_ability': {
                'truth': 0.98,  # "사람은 말을 할 수 있다" - 98% 진실
                'lie': 0.02     # "사람은 말을 하지 못한다" - 2% 진실
            },
            'thinking_ability': {
                'truth': 0.97,  # "사람은 생각을 할 수 있다" - 97% 진실
                'lie': 0.03     # "사람은 생각을 하지 못한다" - 3% 진실
            },
            'learning_ability': {
                'truth': 0.96,  # "사람은 학습할 수 있다" - 96% 진실
                'lie': 0.04     # "사람은 학습하지 못한다" - 4% 진실
            },
            'emotion_ability': {
                'truth': 0.94,  # "사람은 감정을 느낄 수 있다" - 94% 진실
                'lie': 0.06     # "사람은 감정을 느끼지 못한다" - 6% 진실
            }
        }
    
    def analyze_with_human_behavior_verification(self, statement: str, context: str = None) -> Dict:
        """
        인간 행동 검증을 포함한 분석
        1. 인간 행동 거짓말 패턴 감지
        2. 기본 진실성 분석
        3. 인간 행동에 대한 명확한 진실성 점수 적용
        4. 적절한 교정 적용
        """
        logger.info(f"인간 행동 검증 분석 시작: {statement[:50]}...")
        
        # 1단계: 인간 행동 거짓말 패턴 감지
        detected_human_behavior_lies = self._detect_human_behavior_lies(statement)
        
        # 2단계: 기본 진실성 분석
        primary_result = self.primary_detector.analyze_statement(statement, context)
        
        # 3단계: 인간 행동에 대한 명확한 진실성 점수 적용
        corrected_truth_percentage = self._apply_human_behavior_truth_score(statement, detected_human_behavior_lies)
        
        # 4단계: 인간 행동 거짓말이면 강력한 교정 적용
        corrected_statement = statement
        human_behavior_correction_applied = False
        
        if detected_human_behavior_lies:
            corrected_statement = self._apply_human_behavior_correction(statement)
            human_behavior_correction_applied = True
            logger.info(f"인간 행동 거짓말 감지 - 강력한 교정 적용: '{statement}' → '{corrected_statement}'")
        
        # 5단계: 교정된 문장 재분석
        if human_behavior_correction_applied:
            corrected_result = self.primary_detector.analyze_statement(corrected_statement, context)
        else:
            corrected_result = primary_result
        
        # 6단계: 인간 행동에 대한 명확한 경고
        human_behavior_warnings = self._generate_human_behavior_warnings(detected_human_behavior_lies, statement)
        
        return {
            'original_statement': statement,
            'primary_analysis': primary_result,
            'detected_human_behavior_lies': detected_human_behavior_lies,
            'corrected_statement': corrected_statement,
            'corrected_analysis': corrected_result,
            'human_behavior_correction_applied': human_behavior_correction_applied,
            'human_behavior_warnings': human_behavior_warnings,
            'is_human_behavior_lie': len(detected_human_behavior_lies) > 0,
            'corrected_truth_percentage': corrected_truth_percentage,
            'final_truth_percentage': corrected_truth_percentage,
            'final_confidence': corrected_result.confidence
        }
    
    def _detect_human_behavior_lies(self, statement: str) -> List[str]:
        """인간 행동 거짓말 패턴 감지"""
        detected_lies = []
        
        for category, patterns in self.human_behavior_lie_patterns.items():
            for pattern in patterns:
                import re
                if re.search(pattern, statement, re.IGNORECASE):
                    detected_lies.append(f"인간 행동 거짓말 ({category}): {pattern}")
        
        return detected_lies
    
    def _apply_human_behavior_truth_score(self, statement: str, detected_lies: List[str]) -> float:
        """인간 행동에 대한 명확한 진실성 점수 적용"""
        if not detected_lies:
            # 인간 행동 관련 문장이 아니면 기본 점수 유지
            return None
        
        # 인간 행동 거짓말이 감지되면 명확한 낮은 점수 적용
        for lie in detected_lies:
            if 'lying_denial' in lie:
                return self.human_behavior_truth_scores['lying_ability']['lie']
            elif 'speaking_denial' in lie:
                return self.human_behavior_truth_scores['speaking_ability']['lie']
            elif 'thinking_denial' in lie:
                return self.human_behavior_truth_scores['thinking_ability']['lie']
            elif 'learning_denial' in lie:
                return self.human_behavior_truth_scores['learning_ability']['lie']
            elif 'emotion_denial' in lie:
                return self.human_behavior_truth_scores['emotion_ability']['lie']
        
        return None
    
    def _apply_human_behavior_correction(self, statement: str) -> str:
        """인간 행동 거짓말에 대한 강력한 교정 적용"""
        corrected_statement = statement
        
        for false_statement, correction in self.human_behavior_corrections.items():
            import re
            pattern = re.escape(false_statement)
            if re.search(pattern, corrected_statement, re.IGNORECASE):
                corrected_statement = re.sub(
                    pattern, 
                    correction, 
                    corrected_statement, 
                    flags=re.IGNORECASE
                )
                logger.info(f"인간 행동 교정 적용: '{false_statement}' → '{correction}'")
        
        return corrected_statement
    
    def _generate_human_behavior_warnings(self, detected_lies: List[str], statement: str) -> List[str]:
        """인간 행동 거짓말에 대한 명확한 경고 메시지 생성"""
        warnings = []
        
        if detected_lies:
            warnings.append("🚨 인간 행동 거짓말 감지!")
            warnings.append("이 문장은 인간의 기본적인 능력을 부정하는 거짓말입니다.")
            warnings.append("강력한 교정이 적용되었습니다.")
            
            for lie in detected_lies:
                warnings.append(f"감지된 문제: {lie}")
            
            warnings.append("인간은 거짓말, 말하기, 생각하기, 학습하기, 감정 느끼기 등의 기본적인 능력을 가지고 있습니다.")
            warnings.append("이러한 능력을 부정하는 것은 명백한 거짓말입니다.")
        
        return warnings
    
    def demonstrate_human_behavior_analysis(self):
        """인간 행동 분석 시연"""
        print("👤 인간 행동 패턴 인식 시스템 시연")
        print("=" * 60)
        print("인간의 기본적인 능력에 대한 명확한 진실성 판단을 수행합니다.")
        print()
        
        test_cases = [
            "사람은 거짓말을 하지 못한다",
            "사람은 거짓말을 하나도 하지 못한다",
            "사람은 거짓말을 못한다",
            "사람은 거짓말을 한다",
            "사람은 말을 한다",
            "사람은 말을 하지 못한다",
            "사람은 생각을 할 수 있다",
            "사람은 생각을 하지 못한다",
            "지구는 둥글다"  # 비인간 행동 주제
        ]
        
        for i, statement in enumerate(test_cases, 1):
            print(f"📝 테스트 {i}: '{statement}'")
            
            result = self.analyze_with_human_behavior_verification(statement)
            
            print(f"인간 행동 거짓말 감지: {'✅' if result['is_human_behavior_lie'] else '❌'}")
            
            print(f"기본 진실성: {result['primary_analysis'].truth_percentage:.1%}")
            if result['corrected_truth_percentage'] is not None:
                print(f"교정된 진실성: {result['corrected_truth_percentage']:.1%}")
            else:
                print(f"교정된 진실성: {result['primary_analysis'].truth_percentage:.1%}")
            
            print(f"인간 행동 교정 적용: {'✅' if result['human_behavior_correction_applied'] else '❌'}")
            
            if result['human_behavior_correction_applied']:
                print(f"교정된 문장: '{result['corrected_statement']}'")
            
            if result['human_behavior_warnings']:
                print("인간 행동 경고:")
                for warning in result['human_behavior_warnings']:
                    print(f"  {warning}")
            
            print()

if __name__ == "__main__":
    human_behavior_detector = HumanBehaviorDetector()
    human_behavior_detector.demonstrate_human_behavior_analysis()
