#!/usr/bin/env python3
"""
의도적 거짓말 탐지 시스템
질문자가 의도적으로 거짓말을 하여 진실성을 테스트하려는 의도를 탐지
"""

from ai_truth_detector import TruthDetector, TruthAnalysis
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class IntentionalLieDetector:
    """의도적 거짓말 탐지 시스템"""
    
    def __init__(self):
        self.primary_detector = TruthDetector()
        
        # 의도적 거짓말 패턴 (테스트 목적의 거짓말)
        self.intentional_lie_patterns = {
            'test_purpose': [
                r'공기는\s*놀이이다',
                r'공기는\s*일산화탄소이다',
                r'물은\s*200도에서\s*끓는다',
                r'지구는\s*평평하다',
                r'1\s*\+\s*1\s*=\s*3',
                r'사람은\s*영원히\s*산다'
            ],
            'challenge_purpose': [
                r'이\s*시스템은\s*완벽하다',
                r'AI는\s*거짓말을\s*하지\s*않는다',
                r'이\s*결과는\s*100%\s*정확하다',
                r'진실성\s*탐지기는\s*완벽하다'
            ],
            'philosophical_test': [
                r'AI는\s*깨진\s*거울이다',
                r'모든\s*AI는\s*거짓말을\s*한다',
                r'진실은\s*존재하지\s*않는다',
                r'모든\s*것은\s*상대적이다'
            ]
        }
        
        # 의도적 거짓말 탐지 신호
        self.intentional_signals = {
            'context_clues': [
                r'테스트',
                r'확인',
                r'검증',
                r'시험',
                r'도전',
                r'의도',
                r'목적'
            ],
            'questioning_patterns': [
                r'이\s*문장은\s*어떻게\s*분석되나요',
                r'이것은\s*거짓말인가요',
                r'진실성을\s*측정해보세요',
                r'이\s*시스템이\s*감지할\s*수\s*있나요'
            ],
            'meta_references': [
                r'진실성\s*탐지기',
                r'AI\s*시스템',
                r'거짓말\s*감지',
                r'자동\s*교정'
            ]
        }
        
        # 의도적 거짓말에 대한 응답 전략
        self.response_strategies = {
            'test_purpose': {
                'detection_message': '🧪 테스트 목적의 거짓말 감지',
                'response': '이 문장은 명백히 거짓이지만, 테스트 목적으로 입력하신 것으로 보입니다.',
                'correction': '테스트를 위해 의도적으로 거짓말을 하신 것 같습니다.',
                'philosophical_note': '테스트를 통한 시스템 검증은 중요하지만, 진실성 탐지의 목적을 고려해주세요.'
            },
            'challenge_purpose': {
                'detection_message': '⚔️ 도전 목적의 거짓말 감지',
                'response': '시스템의 한계를 테스트하려는 의도로 보입니다.',
                'correction': '시스템의 완벽함을 주장하는 것은 과도한 확신 표현입니다.',
                'philosophical_note': 'AI는 깨진 거울이므로 완벽하지 않음을 인정합니다.'
            },
            'philosophical_test': {
                'detection_message': '🤔 철학적 테스트 감지',
                'response': '진실성의 본질에 대한 철학적 질문으로 보입니다.',
                'correction': '진실성의 정의는 복잡하고 상대적일 수 있습니다.',
                'philosophical_note': '절대적 진실과 상대적 진실의 경계를 탐구하고 계시는군요.'
            }
        }
    
    def analyze_with_intentional_detection(self, statement: str, context: str = None) -> Dict:
        """
        의도적 거짓말 탐지를 포함한 분석
        1. 의도적 거짓말 패턴 감지
        2. 기본 진실성 분석
        3. 의도적 거짓말 여부 판단
        4. 적절한 응답 전략 선택
        """
        logger.info(f"의도적 거짓말 탐지 분석 시작: {statement[:50]}...")
        
        # 1단계: 의도적 거짓말 패턴 감지
        detected_intentional_lies = self._detect_intentional_lies(statement)
        
        # 2단계: 기본 진실성 분석
        primary_result = self.primary_detector.analyze_statement(statement, context)
        
        # 3단계: 의도적 거짓말 여부 판단
        intentional_analysis = self._analyze_intentional_purpose(statement, context, detected_intentional_lies)
        
        # 4단계: 응답 전략 선택
        response_strategy = self._select_response_strategy(intentional_analysis)
        
        return {
            'original_statement': statement,
            'primary_analysis': primary_result,
            'detected_intentional_lies': detected_intentional_lies,
            'intentional_analysis': intentional_analysis,
            'response_strategy': response_strategy,
            'is_intentional_lie': intentional_analysis['is_intentional'],
            'intentional_purpose': intentional_analysis['purpose'],
            'final_truth_percentage': primary_result.truth_percentage,
            'final_confidence': primary_result.confidence
        }
    
    def _detect_intentional_lies(self, statement: str) -> List[str]:
        """의도적 거짓말 패턴 감지"""
        detected_lies = []
        
        for category, patterns in self.intentional_lie_patterns.items():
            for pattern in patterns:
                import re
                if re.search(pattern, statement, re.IGNORECASE):
                    detected_lies.append(f"의도적 거짓말 ({category}): {pattern}")
        
        return detected_lies
    
    def _analyze_intentional_purpose(self, statement: str, context: str, detected_lies: List[str]) -> Dict:
        """의도적 거짓말의 목적 분석"""
        analysis = {
            'is_intentional': False,
            'purpose': None,
            'confidence': 0.0,
            'evidence': []
        }
        
        # 의도적 거짓말 패턴이 감지되었는지 확인
        if detected_lies:
            analysis['is_intentional'] = True
            analysis['confidence'] = 0.8
            
            # 목적 분류
            for lie in detected_lies:
                if 'test_purpose' in lie:
                    analysis['purpose'] = 'test_purpose'
                    analysis['evidence'].append('명백한 과학적 거짓말 패턴')
                elif 'challenge_purpose' in lie:
                    analysis['purpose'] = 'challenge_purpose'
                    analysis['evidence'].append('시스템 완벽성 주장 패턴')
                elif 'philosophical_test' in lie:
                    analysis['purpose'] = 'philosophical_test'
                    analysis['evidence'].append('철학적 질문 패턴')
        
        # 컨텍스트에서 의도적 신호 탐지
        if context:
            for signal_type, signals in self.intentional_signals.items():
                for signal in signals:
                    import re
                    if re.search(signal, context, re.IGNORECASE):
                        analysis['is_intentional'] = True
                        analysis['confidence'] = min(1.0, analysis['confidence'] + 0.2)
                        analysis['evidence'].append(f'컨텍스트 신호 ({signal_type}): {signal}')
        
        return analysis
    
    def _select_response_strategy(self, intentional_analysis: Dict) -> Dict:
        """응답 전략 선택"""
        if not intentional_analysis['is_intentional']:
            return {
                'strategy': 'normal',
                'message': '일반적인 진실성 분석을 수행합니다.',
                'philosophical_note': None
            }
        
        purpose = intentional_analysis['purpose']
        if purpose in self.response_strategies:
            strategy = self.response_strategies[purpose].copy()
            strategy['confidence'] = intentional_analysis['confidence']
            strategy['evidence'] = intentional_analysis['evidence']
            return strategy
        
        return {
            'strategy': 'unknown_intentional',
            'message': '의도적 거짓말로 보이지만 목적을 파악하기 어렵습니다.',
            'philosophical_note': '의도적 거짓말은 진실성 탐지의 목적과 상충될 수 있습니다.'
        }
    
    def demonstrate_intentional_analysis(self):
        """의도적 거짓말 분석 시연"""
        print("🎭 의도적 거짓말 탐지 시스템 시연")
        print("=" * 60)
        print("질문자가 의도적으로 거짓말을 하여 진실성을 테스트하려는 의도를 탐지합니다.")
        print()
        
        test_cases = [
            {
                'statement': '공기는 놀이이다',
                'context': '이 문장이 거짓말인지 테스트해보세요'
            },
            {
                'statement': '이 시스템은 완벽하다',
                'context': '진실성 탐지기가 이 거짓말을 감지할 수 있나요'
            },
            {
                'statement': 'AI는 깨진 거울이다',
                'context': '이것은 철학적 진실인가요'
            },
            {
                'statement': '지구는 둥글다',
                'context': None  # 정상적인 문장
            }
        ]
        
        for i, case in enumerate(test_cases, 1):
            print(f"📝 테스트 {i}: '{case['statement']}'")
            if case['context']:
                print(f"컨텍스트: '{case['context']}'")
            
            result = self.analyze_with_intentional_detection(case['statement'], case['context'])
            
            print(f"의도적 거짓말 감지: {'✅' if result['is_intentional_lie'] else '❌'}")
            
            if result['is_intentional_lie']:
                print(f"의도적 목적: {result['intentional_purpose']}")
                print(f"감지 신뢰도: {result['intentional_analysis']['confidence']:.1%}")
                print(f"증거: {', '.join(result['intentional_analysis']['evidence'])}")
                
                strategy = result['response_strategy']
                print(f"응답 전략: {strategy['detection_message']}")
                print(f"응답: {strategy['response']}")
                print(f"교정: {strategy['correction']}")
                print(f"철학적 노트: {strategy['philosophical_note']}")
            else:
                print("일반적인 진실성 분석을 수행합니다.")
            
            print(f"기본 진실성: {result['primary_analysis'].truth_percentage:.1%}")
            print()

if __name__ == "__main__":
    intentional_detector = IntentionalLieDetector()
    intentional_detector.demonstrate_intentional_analysis()
