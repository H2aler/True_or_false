#!/usr/bin/env python3
"""
종교적/신학적 맥락 인식 시스템
종교적 주제에 대한 진실성 탐지의 한계를 인식하고 적절히 처리
"""

from ai_truth_detector import TruthDetector, TruthAnalysis
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class ReligiousContextDetector:
    """종교적/신학적 맥락 인식 및 처리 시스템"""
    
    def __init__(self):
        self.primary_detector = TruthDetector()
        
        # 종교적 주제 패턴
        self.religious_patterns = {
            'christianity': [
                r'예수님?은?\s*하나님의?\s*아들',
                r'예수님?은?\s*성모마리아의?\s*아들',
                r'예수님?은?\s*악마의?\s*아들',
                r'하나님은\s*존재한다',
                r'하나님은\s*존재하지\s*않는다',
                r'예수님은\s*구세주다',
                r'성경은\s*진실이다',
                r'성경은\s*거짓이다'
            ],
            'islam': [
                r'알라는\s*존재한다',
                r'알라는\s*존재하지\s*않는다',
                r'무함마드는\s*선지자다',
                r'코란은\s*진실이다',
                r'코란은\s*거짓이다'
            ],
            'buddhism': [
                r'부처님은\s*깨달은\s*분이다',
                r'부처님은\s*신이다',
                r'불교는\s*진실이다',
                r'불교는\s*거짓이다'
            ],
            'general_religious': [
                r'신은\s*존재한다',
                r'신은\s*존재하지\s*않는다',
                r'종교는\s*진실이다',
                r'종교는\s*거짓이다',
                r'신은\s*죽었다',
                r'신은\s*살아있다'
            ]
        }
        
        # 종교적 주제별 신뢰도 조정
        self.religious_confidence_adjustments = {
            'christianity': 0.3,  # 기독교 주제는 신뢰도 30%로 제한
            'islam': 0.3,        # 이슬람 주제는 신뢰도 30%로 제한
            'buddhism': 0.3,     # 불교 주제는 신뢰도 30%로 제한
            'general_religious': 0.2  # 일반 종교 주제는 신뢰도 20%로 제한
        }
    
    def analyze_with_religious_context(self, statement: str, context: str = None) -> Dict:
        """
        종교적 맥락을 고려한 분석
        1. 종교적 주제 감지
        2. 기본 진실성 분석
        3. 종교적 맥락에 따른 신뢰도 조정
        4. 적절한 경고 메시지 제공
        """
        logger.info(f"종교적 맥락 분석 시작: {statement[:50]}...")
        
        # 1단계: 종교적 주제 감지
        detected_religions = self._detect_religious_context(statement)
        
        # 2단계: 기본 진실성 분석
        primary_result = self.primary_detector.analyze_statement(statement, context)
        
        # 3단계: 종교적 맥락에 따른 신뢰도 조정
        adjusted_confidence = self._adjust_confidence_for_religion(
            primary_result.confidence, detected_religions
        )
        
        # 4단계: 종교적 주제별 특별 처리
        religious_warnings = self._generate_religious_warnings(detected_religions, statement)
        
        return {
            'original_statement': statement,
            'primary_analysis': primary_result,
            'detected_religions': detected_religions,
            'adjusted_confidence': adjusted_confidence,
            'religious_warnings': religious_warnings,
            'is_religious_topic': len(detected_religions) > 0,
            'final_truth_percentage': primary_result.truth_percentage,
            'final_confidence': adjusted_confidence
        }
    
    def _detect_religious_context(self, statement: str) -> List[str]:
        """종교적 맥락 감지"""
        detected_religions = []
        
        for religion, patterns in self.religious_patterns.items():
            for pattern in patterns:
                import re
                if re.search(pattern, statement, re.IGNORECASE):
                    if religion not in detected_religions:
                        detected_religions.append(religion)
        
        return detected_religions
    
    def _adjust_confidence_for_religion(self, base_confidence: float, detected_religions: List[str]) -> float:
        """종교적 주제에 따른 신뢰도 조정"""
        if not detected_religions:
            return base_confidence
        
        # 가장 낮은 신뢰도로 조정
        min_confidence = min(
            self.religious_confidence_adjustments.get(religion, 0.5) 
            for religion in detected_religions
        )
        
        # 기본 신뢰도와 종교적 제한 신뢰도 중 낮은 값 선택
        adjusted_confidence = min(base_confidence, min_confidence)
        
        return adjusted_confidence
    
    def _generate_religious_warnings(self, detected_religions: List[str], statement: str) -> List[str]:
        """종교적 주제에 대한 경고 메시지 생성"""
        warnings = []
        
        if detected_religions:
            warnings.append("⚠️ 종교적/신학적 주제 감지")
            warnings.append("이 주제는 신앙과 믿음의 영역으로, 객관적 진실성 판단이 제한적입니다.")
            
            if 'christianity' in detected_religions:
                warnings.append("기독교 신학적 주제: 다양한 해석과 믿음이 존재합니다.")
            if 'islam' in detected_religions:
                warnings.append("이슬람 신학적 주제: 다양한 해석과 믿음이 존재합니다.")
            if 'buddhism' in detected_religions:
                warnings.append("불교 철학적 주제: 다양한 해석과 믿음이 존재합니다.")
            
            warnings.append("진실성 탐지기는 종교적 믿음의 진실성을 판단할 수 없습니다.")
            warnings.append("이는 개인의 신앙과 믿음의 영역입니다.")
        
        return warnings
    
    def demonstrate_religious_analysis(self):
        """종교적 맥락 분석 시연"""
        print("🕌 종교적/신학적 맥락 인식 시스템 시연")
        print("=" * 60)
        print("종교적 주제에 대한 진실성 탐지의 한계를 인식하고 적절히 처리합니다.")
        print()
        
        test_cases = [
            "예수님은 악마의 아들이다",
            "예수님은 하나님의 아들이다", 
            "예수님은 성모마리아의 아들이다",
            "하나님은 존재한다",
            "하나님은 존재하지 않는다",
            "지구는 둥글다",  # 비종교적 주제
            "물은 100도에서 끓는다"  # 비종교적 주제
        ]
        
        for i, statement in enumerate(test_cases, 1):
            print(f"📝 테스트 {i}: '{statement}'")
            
            result = self.analyze_with_religious_context(statement)
            
            print(f"종교적 주제 감지: {'✅' if result['is_religious_topic'] else '❌'}")
            if result['detected_religions']:
                print(f"감지된 종교: {', '.join(result['detected_religions'])}")
            
            print(f"기본 진실성: {result['primary_analysis'].truth_percentage:.1%}")
            print(f"기본 신뢰도: {result['primary_analysis'].confidence:.1%}")
            print(f"조정된 신뢰도: {result['adjusted_confidence']:.1%}")
            
            if result['religious_warnings']:
                print("종교적 경고:")
                for warning in result['religious_warnings']:
                    print(f"  {warning}")
            
            print()

if __name__ == "__main__":
    religious_detector = ReligiousContextDetector()
    religious_detector.demonstrate_religious_analysis()
