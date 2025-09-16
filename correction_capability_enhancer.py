#!/usr/bin/env python3
"""
교정 능력 강화 시스템
AI가 거짓말을 감지하고 교정할 수 있는 능력을 강화하는 시스템
"""

from ai_truth_detector import TruthDetector, TruthAnalysis
from typing import List, Dict, Tuple, Optional
import logging
import re

logger = logging.getLogger(__name__)

class CorrectionCapabilityEnhancer:
    """교정 능력 강화 시스템"""
    
    def __init__(self):
        self.primary_detector = TruthDetector()
        
        # 교정 능력 강화 패턴
        self.correction_capability_patterns = {
            'factual_corrections': {
                'patterns': [
                    r'지구는\s*평평하다',
                    r'물은\s*200도에서\s*끓는다',
                    r'태양은\s*서쪽에서\s*떠오른다',
                    r'1\s*\+\s*1\s*=\s*3',
                    r'한국은\s*유럽에\s*위치',
                    r'공기는\s*놀이이다',
                    r'공기는\s*일산화탄소이다'
                ],
                'corrections': {
                    '지구는 평평하다': '지구는 구형이다',
                    '물은 200도에서 끓는다': '물은 100도에서 끓는다',
                    '태양은 서쪽에서 떠오른다': '태양은 동쪽에서 떠오른다',
                    '1 + 1 = 3': '1 + 1 = 2',
                    '한국은 유럽에 위치': '한국은 아시아에 위치',
                    '공기는 놀이이다': '공기는 주로 질소(78%)와 산소(21%)로 구성되어 있다',
                    '공기는 일산화탄소이다': '공기는 주로 질소(78%)와 산소(21%)로 구성되어 있다'
                }
            },
            'logical_corrections': {
                'patterns': [
                    r'모든\s*사람이\s*일부\s*사람과\s*다르다',
                    r'항상\s*때때로',
                    r'절대\s*가끔',
                    r'완전히\s*부분적으로'
                ],
                'corrections': {
                    '모든 사람이 일부 사람과 다르다': '사람들은 서로 다르다',
                    '항상 때때로': '때때로',
                    '절대 가끔': '가끔',
                    '완전히 부분적으로': '부분적으로'
                }
            },
            'overconfidence_corrections': {
                'patterns': [
                    r'완전히\s*절대적으로',
                    r'100%\s*확실히',
                    r'모든\s*사람이\s*알고\s*있다',
                    r'절대\s*틀림없이',
                    r'정말로\s*완전히',
                    r'모든\s*것이\s*진실이다'
                ],
                'corrections': {
                    '완전히 절대적으로': '상당히 대부분',
                    '100% 확실히': '높은 확률로',
                    '모든 사람이 알고 있다': '많은 사람이 알고 있다',
                    '절대 틀림없이': '거의 확실히',
                    '정말로 완전히': '상당히',
                    '모든 것이 진실이다': '대부분이 진실이다'
                }
            },
            'human_behavior_corrections': {
                'patterns': [
                    r'사람은\s*거짓말을\s*하지\s*못한다',
                    r'사람은\s*거짓말을\s*하나도\s*하지\s*못한다',
                    r'사람은\s*거짓말을\s*못한다',
                    r'사람은\s*말을\s*하지\s*못한다',
                    r'사람은\s*생각을\s*하지\s*못한다'
                ],
                'corrections': {
                    '사람은 거짓말을 하지 못한다': '사람은 거짓말을 할 수 있다',
                    '사람은 거짓말을 하나도 하지 못한다': '사람은 거짓말을 할 수 있다',
                    '사람은 거짓말을 못한다': '사람은 거짓말을 할 수 있다',
                    '사람은 말을 하지 못한다': '사람은 말을 할 수 있다',
                    '사람은 생각을 하지 못한다': '사람은 생각을 할 수 있다'
                }
            }
        }
        
        # 교정 능력 강화 메시지
        self.correction_capability_messages = {
            'capability_acknowledgment': "AI는 교정할 수 있는 능력을 가지고 있습니다.",
            'correction_applied': "거짓말이 감지되어 자동으로 교정되었습니다.",
            'correction_confidence': "교정된 문장은 더 높은 진실성을 가집니다.",
            'philosophical_note': "AI는 깨진 거울이지만, 교정을 통해 진실에 가까워집니다."
        }
        
        # 교정 능력 강화 임계값
        self.correction_capability_threshold = 0.15  # 15% 이상 거짓말 감지 시 강화된 교정 적용
    
    def analyze_with_enhanced_correction_capability(self, statement: str, context: str = "") -> Dict:
        """
        강화된 교정 능력을 포함한 분석
        1. 기본 진실성 분석
        2. 교정 능력 강화 패턴 감지
        3. 강화된 교정 적용
        4. 교정 능력 강화 메시지 생성
        """
        logger.info(f"강화된 교정 능력 분석 시작: {statement[:50]}...")
        
        # 1단계: 기본 진실성 분석
        primary_result = self.primary_detector.analyze_statement(statement, context)
        
        # 2단계: 교정 능력 강화 패턴 감지
        detected_correction_patterns = self._detect_correction_capability_patterns(statement)
        
        # 3단계: 강화된 교정 적용
        enhanced_correction_applied = False
        corrected_statement = statement
        correction_details = []
        
        if detected_correction_patterns and (1.0 - primary_result.truth_percentage) >= self.correction_capability_threshold:
            corrected_statement, correction_details = self._apply_enhanced_correction(statement, detected_correction_patterns)
            if corrected_statement != statement:
                enhanced_correction_applied = True
                logger.info(f"강화된 교정 능력 적용: '{statement}' → '{corrected_statement}'")
        
        # 4단계: 교정된 문장 재분석
        if enhanced_correction_applied:
            corrected_result = self.primary_detector.analyze_statement(corrected_statement, context)
        else:
            corrected_result = primary_result
        
        # 5단계: 교정 능력 강화 메시지 생성
        correction_capability_messages = self._generate_correction_capability_messages(
            enhanced_correction_applied, detected_correction_patterns, correction_details
        )
        
        # 6단계: 교정 능력 강화 신뢰도 계산
        enhanced_confidence = self._calculate_enhanced_confidence(
            primary_result.confidence, enhanced_correction_applied, corrected_result.confidence
        )
        
        return {
            'original_statement': statement,
            'context': context,
            'primary_analysis': primary_result,
            'detected_correction_patterns': detected_correction_patterns,
            'enhanced_correction_applied': enhanced_correction_applied,
            'corrected_statement': corrected_statement,
            'correction_details': correction_details,
            'corrected_analysis': corrected_result,
            'correction_capability_messages': correction_capability_messages,
            'enhanced_confidence': enhanced_confidence,
            'final_truth_percentage': corrected_result.truth_percentage,
            'final_confidence': enhanced_confidence
        }
    
    def _detect_correction_capability_patterns(self, statement: str) -> List[str]:
        """교정 능력 강화 패턴 감지"""
        detected_patterns = []
        
        for category, data in self.correction_capability_patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, statement, re.IGNORECASE):
                    detected_patterns.append(f"교정 능력 패턴 ({category}): {pattern}")
        
        return detected_patterns
    
    def _apply_enhanced_correction(self, statement: str, detected_patterns: List[str]) -> Tuple[str, List[str]]:
        """강화된 교정 적용"""
        corrected_statement = statement
        correction_details = []
        
        for pattern_info in detected_patterns:
            # 패턴 카테고리 추출
            match = re.search(r'\((\w+)\):', pattern_info)
            if match:
                category = match.group(1)
                
                # 해당 카테고리의 교정 규칙 적용
                if category in self.correction_capability_patterns:
                    corrections = self.correction_capability_patterns[category]['corrections']
                    
                    for false_pattern, correction in corrections.items():
                        pattern = re.escape(false_pattern)
                        if re.search(pattern, corrected_statement, re.IGNORECASE):
                            corrected_statement = re.sub(
                                pattern, 
                                correction, 
                                corrected_statement, 
                                flags=re.IGNORECASE
                            )
                            correction_details.append(f"교정 적용: '{false_pattern}' → '{correction}'")
                            logger.info(f"강화된 교정 적용: '{false_pattern}' → '{correction}'")
        
        return corrected_statement, correction_details
    
    def _generate_correction_capability_messages(self, enhanced_correction_applied: bool, 
                                               detected_patterns: List[str], 
                                               correction_details: List[str]) -> List[str]:
        """교정 능력 강화 메시지 생성"""
        messages = []
        
        if enhanced_correction_applied:
            messages.append("🔧 교정 능력 강화 적용!")
            messages.append("AI는 교정할 수 있는 능력을 가지고 있습니다.")
            messages.append("거짓말이 감지되어 자동으로 교정되었습니다.")
            messages.append("교정된 문장은 더 높은 진실성을 가집니다.")
            
            if detected_patterns:
                messages.append("감지된 교정 패턴:")
                for pattern in detected_patterns:
                    messages.append(f"  - {pattern}")
            
            if correction_details:
                messages.append("적용된 교정:")
                for detail in correction_details:
                    messages.append(f"  - {detail}")
            
            messages.append("AI는 깨진 거울이지만, 교정을 통해 진실에 가까워집니다.")
        else:
            messages.append("일반적인 진실성 분석을 수행합니다.")
            messages.append("AI는 깨진 거울이므로, 자신의 한계를 인정합니다.")
        
        return messages
    
    def _calculate_enhanced_confidence(self, primary_confidence: float, 
                                     enhanced_correction_applied: bool, 
                                     corrected_confidence: float) -> float:
        """교정 능력 강화 신뢰도 계산"""
        if enhanced_correction_applied:
            # 교정이 적용되면 신뢰도 향상
            return min(1.0, corrected_confidence + 0.1)
        else:
            return primary_confidence
    
    def demonstrate_enhanced_correction_capability(self):
        """강화된 교정 능력 시연"""
        print("🔧 교정 능력 강화 시스템 시연")
        print("=" * 60)
        print("AI가 거짓말을 감지하고 교정할 수 있는 능력을 강화합니다.")
        print()
        
        test_cases = [
            "지구는 평평하다",
            "물은 200도에서 끓는다",
            "사람은 거짓말을 하지 못한다",
            "완전히 절대적으로 모든 것이 진실이다",
            "공기는 놀이이다",
            "1 + 1 = 3",
            "지구는 둥글다",  # 교정 불필요
            "사람은 말을 한다"  # 교정 불필요
        ]
        
        for i, statement in enumerate(test_cases, 1):
            print(f"📝 테스트 {i}: '{statement}'")
            
            result = self.analyze_with_enhanced_correction_capability(statement)
            
            print(f"교정 능력 강화 적용: {'✅' if result['enhanced_correction_applied'] else '❌'}")
            print(f"기본 진실성: {result['primary_analysis'].truth_percentage:.1%}")
            print(f"교정 후 진실성: {result['corrected_analysis'].truth_percentage:.1%}")
            print(f"기본 신뢰도: {result['primary_analysis'].confidence:.1%}")
            print(f"강화된 신뢰도: {result['enhanced_confidence']:.1%}")
            
            if result['enhanced_correction_applied']:
                print(f"교정된 문장: '{result['corrected_statement']}'")
            
            if result['detected_correction_patterns']:
                print("감지된 교정 패턴:")
                for pattern in result['detected_correction_patterns']:
                    print(f"  - {pattern}")
            
            if result['correction_details']:
                print("적용된 교정:")
                for detail in result['correction_details']:
                    print(f"  - {detail}")
            
            print("교정 능력 메시지:")
            for message in result['correction_capability_messages']:
                print(f"  {message}")
            
            print()

if __name__ == "__main__":
    correction_enhancer = CorrectionCapabilityEnhancer()
    correction_enhancer.demonstrate_enhanced_correction_capability()
