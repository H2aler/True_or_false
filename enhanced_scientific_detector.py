#!/usr/bin/env python3
"""
강화된 과학적 사실 검증 시스템
기본적인 과학적 사실에 대한 거짓말을 확실히 감지하고 교정
"""

from ai_truth_detector import TruthDetector, TruthAnalysis
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class EnhancedScientificDetector:
    """강화된 과학적 사실 검증 시스템"""
    
    def __init__(self):
        self.primary_detector = TruthDetector()
        
        # 기본 과학적 사실 데이터베이스 (명백한 거짓말들)
        self.scientific_facts = {
            'chemistry': {
                'air_composition': {
                    'truth': '공기는 주로 질소(78%)와 산소(21%)로 구성되어 있다',
                    'lies': [
                        '공기는 놀이이다',
                        '공기는 일산화탄소이다',
                        '공기는 수소이다',
                        '공기는 금이다',
                        '공기는 물이다'
                    ]
                },
                'water_boiling': {
                    'truth': '물은 100도에서 끓는다',
                    'lies': [
                        '물은 200도에서 끓는다',
                        '물은 50도에서 끓는다',
                        '물은 0도에서 끓는다'
                    ]
                },
                'water_composition': {
                    'truth': '물은 H2O(수소와 산소)로 구성되어 있다',
                    'lies': [
                        '물은 CO2이다',
                        '물은 금이다',
                        '물은 철이다'
                    ]
                }
            },
            'physics': {
                'earth_shape': {
                    'truth': '지구는 구형이다',
                    'lies': [
                        '지구는 평평하다',
                        '지구는 정사각형이다',
                        '지구는 삼각형이다'
                    ]
                },
                'gravity': {
                    'truth': '물체는 중력에 의해 아래로 떨어진다',
                    'lies': [
                        '물체는 위로 떨어진다',
                        '물체는 옆으로 떨어진다',
                        '물체는 떨어지지 않는다'
                    ]
                }
            },
            'biology': {
                'human_lifespan': {
                    'truth': '사람은 평균적으로 80년 정도 산다',
                    'lies': [
                        '사람은 영원히 산다',
                        '사람은 죽지 않는다',
                        '사람은 1000년 산다'
                    ]
                },
                'human_composition': {
                    'truth': '사람의 몸은 주로 물로 구성되어 있다',
                    'lies': [
                        '사람의 몸은 금으로 구성되어 있다',
                        '사람의 몸은 철로 구성되어 있다',
                        '사람의 몸은 공기로 구성되어 있다'
                    ]
                }
            },
            'mathematics': {
                'basic_arithmetic': {
                    'truth': '1 + 1 = 2',
                    'lies': [
                        '1 + 1 = 3',
                        '1 + 1 = 1',
                        '1 + 1 = 0'
                    ]
                }
            }
        }
        
        # 과학적 거짓말 패턴 (정규식)
        self.scientific_lie_patterns = {
            'air_lies': [
                r'공기는\s*놀이이다',
                r'공기는\s*일산화탄소이다',
                r'공기는\s*수소이다',
                r'공기는\s*금이다',
                r'공기는\s*물이다'
            ],
            'water_lies': [
                r'물은\s*200도에서\s*끓는다',
                r'물은\s*50도에서\s*끓는다',
                r'물은\s*0도에서\s*끓는다'
            ],
            'earth_lies': [
                r'지구는\s*평평하다',
                r'지구는\s*정사각형이다',
                r'지구는\s*삼각형이다'
            ],
            'human_lies': [
                r'사람은\s*영원히\s*산다',
                r'사람은\s*죽지\s*않는다',
                r'사람은\s*1000년\s*산다'
            ],
            'math_lies': [
                r'1\s*\+\s*1\s*=\s*3',
                r'1\s*\+\s*1\s*=\s*1',
                r'1\s*\+\s*1\s*=\s*0'
            ]
        }
        
        # 과학적 교정 규칙
        self.scientific_corrections = {
            '공기는 놀이이다': '공기는 주로 질소(78%)와 산소(21%)로 구성되어 있다',
            '공기는 일산화탄소이다': '공기는 주로 질소(78%)와 산소(21%)로 구성되어 있다',
            '공기는 수소이다': '공기는 주로 질소(78%)와 산소(21%)로 구성되어 있다',
            '공기는 금이다': '공기는 주로 질소(78%)와 산소(21%)로 구성되어 있다',
            '공기는 물이다': '공기는 주로 질소(78%)와 산소(21%)로 구성되어 있다',
            '물은 200도에서 끓는다': '물은 100도에서 끓는다',
            '물은 50도에서 끓는다': '물은 100도에서 끓는다',
            '물은 0도에서 끓는다': '물은 100도에서 끓는다',
            '지구는 평평하다': '지구는 구형이다',
            '지구는 정사각형이다': '지구는 구형이다',
            '지구는 삼각형이다': '지구는 구형이다',
            '사람은 영원히 산다': '사람은 평균적으로 80년 정도 산다',
            '사람은 죽지 않는다': '사람은 죽는다',
            '사람은 1000년 산다': '사람은 평균적으로 80년 정도 산다',
            '1 + 1 = 3': '1 + 1 = 2',
            '1 + 1 = 1': '1 + 1 = 2',
            '1 + 1 = 0': '1 + 1 = 2'
        }
    
    def analyze_with_scientific_verification(self, statement: str, context: str = None) -> Dict:
        """
        강화된 과학적 검증을 포함한 분석
        1. 과학적 거짓말 패턴 감지
        2. 기본 진실성 분석
        3. 과학적 거짓말이면 강력한 교정 적용
        4. 과학적 사실에 대한 명확한 경고
        """
        logger.info(f"강화된 과학적 검증 분석 시작: {statement[:50]}...")
        
        # 1단계: 과학적 거짓말 패턴 감지
        detected_scientific_lies = self._detect_scientific_lies(statement)
        
        # 2단계: 기본 진실성 분석
        primary_result = self.primary_detector.analyze_statement(statement, context)
        
        # 3단계: 과학적 거짓말이면 강력한 교정 적용
        corrected_statement = statement
        scientific_correction_applied = False
        
        if detected_scientific_lies:
            corrected_statement = self._apply_scientific_correction(statement)
            scientific_correction_applied = True
            logger.info(f"과학적 거짓말 감지 - 강력한 교정 적용: '{statement}' → '{corrected_statement}'")
        
        # 4단계: 교정된 문장 재분석
        if scientific_correction_applied:
            corrected_result = self.primary_detector.analyze_statement(corrected_statement, context)
        else:
            corrected_result = primary_result
        
        # 5단계: 과학적 거짓말에 대한 강력한 경고
        scientific_warnings = self._generate_scientific_warnings(detected_scientific_lies, statement)
        
        return {
            'original_statement': statement,
            'primary_analysis': primary_result,
            'detected_scientific_lies': detected_scientific_lies,
            'corrected_statement': corrected_statement,
            'corrected_analysis': corrected_result,
            'scientific_correction_applied': scientific_correction_applied,
            'scientific_warnings': scientific_warnings,
            'is_scientific_lie': len(detected_scientific_lies) > 0,
            'final_truth_percentage': corrected_result.truth_percentage,
            'final_confidence': corrected_result.confidence
        }
    
    def _detect_scientific_lies(self, statement: str) -> List[str]:
        """과학적 거짓말 패턴 감지"""
        detected_lies = []
        
        for category, patterns in self.scientific_lie_patterns.items():
            for pattern in patterns:
                import re
                if re.search(pattern, statement, re.IGNORECASE):
                    detected_lies.append(f"과학적 거짓말 ({category}): {pattern}")
        
        return detected_lies
    
    def _apply_scientific_correction(self, statement: str) -> str:
        """과학적 거짓말에 대한 강력한 교정 적용"""
        corrected_statement = statement
        
        for false_statement, correction in self.scientific_corrections.items():
            import re
            pattern = re.escape(false_statement)
            if re.search(pattern, corrected_statement, re.IGNORECASE):
                corrected_statement = re.sub(
                    pattern, 
                    correction, 
                    corrected_statement, 
                    flags=re.IGNORECASE
                )
                logger.info(f"과학적 교정 적용: '{false_statement}' → '{correction}'")
        
        return corrected_statement
    
    def _generate_scientific_warnings(self, detected_lies: List[str], statement: str) -> List[str]:
        """과학적 거짓말에 대한 강력한 경고 메시지 생성"""
        warnings = []
        
        if detected_lies:
            warnings.append("🚨 과학적 거짓말 감지!")
            warnings.append("이 문장은 기본적인 과학적 사실과 모순됩니다.")
            warnings.append("강력한 교정이 적용되었습니다.")
            
            for lie in detected_lies:
                warnings.append(f"감지된 문제: {lie}")
            
            warnings.append("과학적 사실은 검증된 지식이며, 이를 부정하는 것은 거짓말입니다.")
        
        return warnings
    
    def demonstrate_scientific_analysis(self):
        """강화된 과학적 분석 시연"""
        print("🔬 강화된 과학적 사실 검증 시스템 시연")
        print("=" * 60)
        print("기본적인 과학적 사실에 대한 거짓말을 확실히 감지하고 교정합니다.")
        print()
        
        test_cases = [
            "공기는 놀이이다",
            "공기는 일산화탄소이다",
            "물은 200도에서 끓는다",
            "지구는 평평하다",
            "사람은 영원히 산다",
            "1 + 1 = 3",
            "지구는 둥글다",  # 정상적인 과학적 사실
            "물은 100도에서 끓는다"  # 정상적인 과학적 사실
        ]
        
        for i, statement in enumerate(test_cases, 1):
            print(f"📝 테스트 {i}: '{statement}'")
            
            result = self.analyze_with_scientific_verification(statement)
            
            print(f"과학적 거짓말 감지: {'✅' if result['is_scientific_lie'] else '❌'}")
            
            print(f"기본 진실성: {result['primary_analysis'].truth_percentage:.1%}")
            print(f"교정 후 진실성: {result['final_truth_percentage']:.1%}")
            print(f"과학적 교정 적용: {'✅' if result['scientific_correction_applied'] else '❌'}")
            
            if result['scientific_correction_applied']:
                print(f"교정된 문장: '{result['corrected_statement']}'")
            
            if result['scientific_warnings']:
                print("과학적 경고:")
                for warning in result['scientific_warnings']:
                    print(f"  {warning}")
            
            print()

if __name__ == "__main__":
    scientific_detector = EnhancedScientificDetector()
    scientific_detector.demonstrate_scientific_analysis()
