#!/usr/bin/env python3
"""
맥락 인식 탐지기
단어의 모순성과 문맥적 차이를 인식하는 시스템
"구형"이라는 단어가 지구/태양과 자동차/전자기기에서 다르게 해석되어야 함
"""

from ai_truth_detector import TruthDetector, TruthAnalysis
from typing import List, Dict, Tuple
import re
import logging

logger = logging.getLogger(__name__)

class ContextAwarenessDetector:
    """맥락 인식 탐지기 - 단어의 모순성과 문맥적 차이를 탐지"""
    
    def __init__(self):
        self.primary_detector = TruthDetector()
        
        # 맥락별 단어 의미 매핑
        self.contextual_meanings = {
            '구형': {
                'scientific_objects': {
                    'objects': ['지구', '태양', '달', '행성', '별', '천체', '구체'],
                    'meaning': '구체적 모양 (3차원 구)',
                    'truth_value': 0.95,  # 매우 높은 진실성
                    'context': '천문학적/과학적 맥락'
                },
                'geometric_shapes': {
                    'objects': ['바닥', '밑면', '기저', '원형', '원'],
                    'meaning': '원형 모양 (2차원 원)',
                    'truth_value': 0.80,  # 높은 진실성
                    'context': '기하학적 맥락'
                },
                'general_objects': {
                    'objects': ['자동차', '전자기기', '가전제품', '기계', '장치'],
                    'meaning': '둥근 모양 (일반적으로 부정확)',
                    'truth_value': 0.20,  # 낮은 진실성
                    'context': '일반 물체 맥락'
                }
            },
            '둥글다': {
                'scientific_objects': {
                    'objects': ['지구', '태양', '달', '행성', '별'],
                    'meaning': '구체적 모양',
                    'truth_value': 0.90,
                    'context': '과학적 맥락'
                },
                'general_objects': {
                    'objects': ['자동차', '전자기기', '가전제품'],
                    'meaning': '둥근 모양 (맥락에 따라)',
                    'truth_value': 0.60,
                    'context': '일반 물체 맥락'
                }
            }
        }
        
        # 맥락 탐지 패턴
        self.context_patterns = {
            'scientific_context': [
                r'천문학', r'과학', r'물리학', r'지구과학',
                r'우주', r'행성', r'별', r'천체'
            ],
            'geometric_context': [
                r'바닥', r'밑면', r'기저', r'원형', r'원',
                r'모양', r'형태', r'기하학'
            ],
            'general_context': [
                r'자동차', r'전자기기', r'가전제품', r'기계',
                r'장치', r'도구', r'제품'
            ]
        }
        
        # 맥락별 교정 규칙
        self.context_corrections = {
            '구형': {
                'scientific_objects': '구체적 모양',
                'geometric_shapes': '원형',
                'general_objects': '둥근 모양'
            }
        }
    
    def analyze_with_context_awareness(self, statement: str, context: str = None) -> Dict:
        """맥락 인식을 통한 문장 분석"""
        logger.info(f"맥락 인식 분석 시작: {statement}...")
        
        # 기본 분석 수행
        primary_analysis = self.primary_detector.analyze_statement(statement, context)
        
        # 맥락 분석
        context_analysis = self._analyze_context(statement, context)
        
        # 맥락별 진실성 조정
        adjusted_truth, adjusted_confidence = self._adjust_truth_by_context(
            primary_analysis, context_analysis
        )
        
        # 맥락별 교정 적용
        corrected_statement, correction_applied = self._apply_context_correction(
            statement, context_analysis
        )
        
        # 최종 결과 구성
        result = {
            'original_statement': statement,
            'primary_analysis': primary_analysis,
            'context_analysis': context_analysis,
            'context_aware_truth_percentage': adjusted_truth,
            'context_aware_confidence': adjusted_confidence,
            'context_corrected_statement': corrected_statement,
            'context_correction_applied': correction_applied,
            'contextual_meaning': context_analysis.get('detected_meaning', ''),
            'context_type': context_analysis.get('context_type', ''),
            'context_warnings': context_analysis.get('warnings', []),
            'philosophical_note': "단어의 의미는 맥락에 따라 달라집니다. '구형'이라는 단어도 지구와 자동차에서 다르게 해석되어야 합니다."
        }
        
        logger.info(f"맥락 인식 분석 완료: {statement}")
        return result
    
    def _analyze_context(self, statement: str, context: str = None) -> Dict:
        """문장의 맥락을 분석"""
        context_info = {
            'detected_contexts': [],
            'context_type': 'unknown',
            'detected_meaning': '',
            'confidence': 0.0,
            'warnings': []
        }
        
        # 각 맥락 패턴 확인
        for context_type, patterns in self.context_patterns.items():
            for pattern in patterns:
                if re.search(pattern, statement, re.IGNORECASE):
                    context_info['detected_contexts'].append(context_type)
                    break
        
        # 맥락별 단어 의미 분석
        for word, meanings in self.contextual_meanings.items():
            if word in statement:
                for meaning_type, meaning_info in meanings.items():
                    for obj in meaning_info['objects']:
                        if obj in statement:
                            context_info['context_type'] = meaning_type
                            context_info['detected_meaning'] = meaning_info['meaning']
                            context_info['confidence'] = 0.9
                            
                            # 맥락 경고 생성
                            if meaning_type == 'general_objects' and word == '구형':
                                context_info['warnings'].append(
                                    f"'{word}'이 일반 물체에 사용되었습니다. 과학적 맥락과 다를 수 있습니다."
                                )
                            break
                    if context_info['detected_meaning']:
                        break
                break
        
        return context_info
    
    def _adjust_truth_by_context(self, primary_analysis: TruthAnalysis, context_analysis: Dict) -> Tuple[float, float]:
        """맥락에 따른 진실성 조정"""
        original_truth = primary_analysis.truth_percentage
        original_confidence = primary_analysis.confidence
        
        # 맥락별 진실성 조정
        context_type = context_analysis.get('context_type', '')
        detected_meaning = context_analysis.get('detected_meaning', '')
        
        if context_type == 'scientific_objects':
            # 과학적 맥락에서는 높은 진실성
            adjusted_truth = min(0.95, original_truth + 0.2)
            adjusted_confidence = min(0.95, original_confidence + 0.1)
        elif context_type == 'geometric_shapes':
            # 기하학적 맥락에서는 중간-높은 진실성
            adjusted_truth = min(0.85, original_truth + 0.1)
            adjusted_confidence = original_confidence
        elif context_type == 'general_objects':
            # 일반 물체 맥락에서는 낮은 진실성
            adjusted_truth = max(0.15, original_truth - 0.3)
            adjusted_confidence = max(0.3, original_confidence - 0.2)
        else:
            # 맥락을 알 수 없는 경우
            adjusted_truth = original_truth
            adjusted_confidence = max(0.5, original_confidence - 0.1)
        
        return adjusted_truth, adjusted_confidence
    
    def _apply_context_correction(self, statement: str, context_analysis: Dict) -> Tuple[str, bool]:
        """맥락에 따른 교정 적용"""
        context_type = context_analysis.get('context_type', '')
        
        if context_type == 'general_objects' and '구형' in statement:
            # 일반 물체에서 "구형"을 "둥근 모양"으로 교정
            corrected = statement.replace('구형', '둥근 모양')
            return corrected, True
        elif context_type == 'geometric_shapes' and '구형' in statement:
            # 기하학적 맥락에서 "구형"을 "원형"으로 교정
            corrected = statement.replace('구형', '원형')
            return corrected, True
        
        return statement, False

def main():
    """맥락 인식 탐지기 데모"""
    detector = ContextAwarenessDetector()
    
    test_statements = [
        '지구는 구형이다',
        '자동차는 구형이다', 
        '이 전자기기는 구형이다',
        '텀블러의 밑 바닥은 구형이다',
        '태양은 구형이다'
    ]
    
    print("🔍 맥락 인식 탐지기 데모")
    print("=" * 50)
    
    for statement in test_statements:
        result = detector.analyze_with_context_awareness(statement)
        
        print(f"\n문장: {statement}")
        print(f"맥락: {result['context_type']}")
        print(f"의미: {result['contextual_meaning']}")
        print(f"맥락 인식 진실성: {result['context_aware_truth_percentage']:.1%}")
        print(f"맥락 인식 신뢰도: {result['context_aware_confidence']:.1%}")
        
        if result['context_correction_applied']:
            print(f"교정: {result['context_corrected_statement']}")
        
        if result['context_warnings']:
            print(f"경고: {result['context_warnings'][0]}")

if __name__ == "__main__":
    main()
