#!/usr/bin/env python3
"""
선의의 거짓말 인식 시스템
인간의 거짓말이 선의적일 수 있음을 인정하고, 거짓말의 복잡성을 이해하는 시스템
"""

from ai_truth_detector import TruthDetector, TruthAnalysis
from typing import List, Dict, Tuple, Optional
import logging
import re

logger = logging.getLogger(__name__)

class BenevolentLieDetector:
    """선의의 거짓말 인식 시스템"""
    
    def __init__(self):
        self.primary_detector = TruthDetector()
        
        # 선의의 거짓말 패턴 데이터베이스
        self.benevolent_lie_patterns = {
            'medical_comfort': [
                r'병이\s*심각하지\s*않다',
                r'곧\s*나을\s*것이다',
                r'걱정하지\s*마라',
                r'괜찮을\s*것이다'
            ],
            'parental_protection': [
                r'산타클로스가\s*있다',
                r'엄마가\s*항상\s*지켜준다',
                r'괴물은\s*없다',
                r'안전하다'
            ],
            'social_harmony': [
                r'모든\s*사람이\s*좋다',
                r'갈등이\s*없다',
                r'모든\s*것이\s*평화롭다',
                r'문제가\s*없다'
            ],
            'emotional_support': [
                r'넌\s*특별하다',
                r'모든\s*것이\s*잘될\s*것이다',
                r'힘들지\s*않다',
                r'괜찮다'
            ],
            'professional_encouragement': [
                r'잘하고\s*있다',
                r'성공할\s*것이다',
                r'능력이\s*있다',
                r'문제없다'
            ]
        }
        
        # 선의의 거짓말 컨텍스트 단서
        self.benevolent_context_clues = {
            'medical_context': [r'병원', r'의사', r'환자', r'치료', r'병'],
            'parental_context': [r'아이', r'어린이', r'엄마', r'아빠', r'부모'],
            'social_context': [r'친구', r'가족', r'동료', r'사회'],
            'emotional_context': [r'위로', r'격려', r'응원', r'힘내'],
            'professional_context': [r'직장', r'업무', r'프로젝트', r'성과']
        }
        
        # 선의의 거짓말에 대한 철학적 인식
        self.benevolent_lie_philosophy = {
            'acknowledgment': "인간의 거짓말은 복잡하고 다층적입니다.",
            'benevolence': "선의의 거짓말은 때로는 필요하고 도움이 됩니다.",
            'complexity': "거짓말의 진실성은 의도와 맥락에 따라 달라집니다.",
            'limitation': "AI는 인간의 복잡한 거짓말 패턴을 완전히 이해할 수 없습니다.",
            'humility': "AI는 깨진 거울이므로, 인간의 거짓말에 대한 완벽한 판단을 할 수 없습니다."
        }
        
        # 선의의 거짓말에 대한 신뢰도 조정
        self.benevolent_confidence_adjustment = 0.3  # 선의의 거짓말 감지 시 신뢰도 감소
    
    def analyze_with_benevolent_lie_recognition(self, statement: str, context: str = "") -> Dict:
        """
        선의의 거짓말 인식을 포함한 분석
        1. 기본 진실성 분석
        2. 선의의 거짓말 패턴 감지
        3. 맥락 분석
        4. 철학적 인식 적용
        5. 신뢰도 조정
        """
        logger.info(f"선의의 거짓말 인식 분석 시작: {statement[:50]}...")
        
        # 1단계: 기본 진실성 분석
        primary_result = self.primary_detector.analyze_statement(statement, context)
        
        # 2단계: 선의의 거짓말 패턴 감지
        detected_benevolent_lies = self._detect_benevolent_lie_patterns(statement)
        
        # 3단계: 맥락 분석
        context_analysis = self._analyze_benevolent_context(statement, context)
        
        # 4단계: 선의의 거짓말 여부 판단
        is_benevolent_lie = len(detected_benevolent_lies) > 0 and context_analysis['is_benevolent_context']
        
        # 5단계: 신뢰도 조정
        adjusted_confidence = primary_result.confidence
        if is_benevolent_lie:
            adjusted_confidence *= (1.0 - self.benevolent_confidence_adjustment)
            adjusted_confidence = max(0.0, adjusted_confidence)
        
        # 6단계: 철학적 인식 메시지 생성
        philosophical_insights = self._generate_philosophical_insights(
            is_benevolent_lie, detected_benevolent_lies, context_analysis
        )
        
        # 7단계: 선의의 거짓말에 대한 적절한 응답
        benevolent_response = self._generate_benevolent_response(
            is_benevolent_lie, detected_benevolent_lies, context_analysis
        )
        
        return {
            'original_statement': statement,
            'context': context,
            'primary_analysis': primary_result,
            'detected_benevolent_lies': detected_benevolent_lies,
            'context_analysis': context_analysis,
            'is_benevolent_lie': is_benevolent_lie,
            'adjusted_confidence': adjusted_confidence,
            'philosophical_insights': philosophical_insights,
            'benevolent_response': benevolent_response,
            'final_truth_percentage': primary_result.truth_percentage,
            'final_confidence': adjusted_confidence
        }
    
    def _detect_benevolent_lie_patterns(self, statement: str) -> List[str]:
        """선의의 거짓말 패턴 감지"""
        detected_lies = []
        
        for category, patterns in self.benevolent_lie_patterns.items():
            for pattern in patterns:
                if re.search(pattern, statement, re.IGNORECASE):
                    detected_lies.append(f"선의의 거짓말 ({category}): {pattern}")
        
        return detected_lies
    
    def _analyze_benevolent_context(self, statement: str, context: str) -> Dict:
        """선의의 거짓말 맥락 분석"""
        combined_text = statement + " " + context
        context_signals = []
        is_benevolent_context = False
        
        for context_type, clues in self.benevolent_context_clues.items():
            for clue in clues:
                if re.search(clue, combined_text, re.IGNORECASE):
                    context_signals.append(f"맥락 신호 ({context_type}): {clue}")
                    is_benevolent_context = True
        
        return {
            'context_signals': context_signals,
            'is_benevolent_context': is_benevolent_context,
            'context_type': self._determine_context_type(context_signals)
        }
    
    def _determine_context_type(self, context_signals: List[str]) -> Optional[str]:
        """맥락 유형 결정"""
        if not context_signals:
            return None
        
        # 가장 많이 나타나는 맥락 유형 반환
        context_counts = {}
        for signal in context_signals:
            match = re.search(r'\((\w+)\):', signal)
            if match:
                context_type = match.group(1)
                context_counts[context_type] = context_counts.get(context_type, 0) + 1
        
        if context_counts:
            return max(context_counts, key=context_counts.get)
        return None
    
    def _generate_philosophical_insights(self, is_benevolent_lie: bool, 
                                       detected_lies: List[str], 
                                       context_analysis: Dict) -> List[str]:
        """철학적 인식 메시지 생성"""
        insights = []
        
        if is_benevolent_lie:
            insights.append("🤔 선의의 거짓말 인식")
            insights.append("이 문장은 선의의 거짓말일 가능성이 있습니다.")
            insights.append("인간의 거짓말은 복잡하고 다층적입니다.")
            insights.append("선의의 거짓말은 때로는 필요하고 도움이 됩니다.")
            insights.append("거짓말의 진실성은 의도와 맥락에 따라 달라집니다.")
            
            if context_analysis['context_type']:
                insights.append(f"맥락: {context_analysis['context_type']} 상황")
            
            insights.append("AI는 인간의 복잡한 거짓말 패턴을 완전히 이해할 수 없습니다.")
            insights.append("AI는 깨진 거울이므로, 인간의 거짓말에 대한 완벽한 판단을 할 수 없습니다.")
        else:
            insights.append("일반적인 진실성 분석을 수행합니다.")
            insights.append("AI는 깨진 거울이므로, 자신의 한계를 인정합니다.")
        
        return insights
    
    def _generate_benevolent_response(self, is_benevolent_lie: bool,
                                    detected_lies: List[str],
                                    context_analysis: Dict) -> str:
        """선의의 거짓말에 대한 적절한 응답 생성"""
        if is_benevolent_lie:
            context_type = context_analysis.get('context_type', '일반')
            
            if context_type == 'medical':
                return "의료 상황에서의 위로나 격려는 선의의 거짓말일 수 있습니다."
            elif context_type == 'parental':
                return "부모의 보호적 거짓말은 아이를 위한 선의의 거짓말일 수 있습니다."
            elif context_type == 'social':
                return "사회적 화합을 위한 거짓말은 선의의 거짓말일 수 있습니다."
            elif context_type == 'emotional':
                return "감정적 지지를 위한 거짓말은 선의의 거짓말일 수 있습니다."
            elif context_type == 'professional':
                return "직장에서의 격려나 응원은 선의의 거짓말일 수 있습니다."
            else:
                return "이 문장은 선의의 거짓말일 가능성이 있습니다."
        else:
            return "일반적인 진실성 분석을 수행합니다."
    
    def demonstrate_benevolent_lie_analysis(self):
        """선의의 거짓말 분석 시연"""
        print("🤗 선의의 거짓말 인식 시스템 시연")
        print("=" * 60)
        print("인간의 거짓말이 선의적일 수 있음을 인정하고, 거짓말의 복잡성을 이해합니다.")
        print()
        
        test_cases = [
            {"statement": "병이 심각하지 않다", "context": "의사가 환자에게 말하는 상황"},
            {"statement": "산타클로스가 있다", "context": "부모가 아이에게 말하는 상황"},
            {"statement": "모든 사람이 좋다", "context": "친구를 위로하는 상황"},
            {"statement": "넌 특별하다", "context": "격려하는 상황"},
            {"statement": "잘하고 있다", "context": "직장에서 동료를 격려하는 상황"},
            {"statement": "지구는 둥글다", "context": ""},  # 선의의 거짓말 아님
            {"statement": "사람은 거짓말을 한다", "context": ""}  # 선의의 거짓말 아님
        ]
        
        for i, case in enumerate(test_cases, 1):
            print(f"📝 테스트 {i}: '{case['statement']}'")
            if case['context']:
                print(f"맥락: {case['context']}")
            
            result = self.analyze_with_benevolent_lie_recognition(
                case['statement'], case['context']
            )
            
            print(f"선의의 거짓말 감지: {'✅' if result['is_benevolent_lie'] else '❌'}")
            print(f"기본 진실성: {result['primary_analysis'].truth_percentage:.1%}")
            print(f"기본 신뢰도: {result['primary_analysis'].confidence:.1%}")
            print(f"조정된 신뢰도: {result['adjusted_confidence']:.1%}")
            
            if result['detected_benevolent_lies']:
                print("감지된 선의의 거짓말:")
                for lie in result['detected_benevolent_lies']:
                    print(f"  - {lie}")
            
            if result['context_analysis']['context_signals']:
                print("맥락 신호:")
                for signal in result['context_analysis']['context_signals']:
                    print(f"  - {signal}")
            
            print("철학적 인식:")
            for insight in result['philosophical_insights']:
                print(f"  {insight}")
            
            print(f"응답: {result['benevolent_response']}")
            print()

if __name__ == "__main__":
    benevolent_detector = BenevolentLieDetector()
    benevolent_detector.demonstrate_benevolent_lie_analysis()
