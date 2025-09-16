#!/usr/bin/env python3
"""
복합 문장 분석기
하나의 문장에 여러 개의 서로 다른 맥락이 포함된 경우를 분석
예: "계란은 구형이다 이 기기는 구형이다" - 계란(과학적) + 기기(일반물체)
"""

from ai_truth_detector import TruthDetector, TruthAnalysis
from context_awareness_detector import ContextAwarenessDetector
from typing import List, Dict, Tuple
import re
import logging

logger = logging.getLogger(__name__)

class CompoundSentenceAnalyzer:
    """복합 문장 분석기 - 여러 맥락이 섞인 문장을 분석"""
    
    def __init__(self):
        self.primary_detector = TruthDetector()
        self.context_detector = ContextAwarenessDetector()
        
        # 문장 분리 패턴
        self.sentence_separators = [
            r'\.\s+',  # 마침표 + 공백
            r'!\s+',   # 느낌표 + 공백
            r'\?\s+',  # 물음표 + 공백
            r';\s+',   # 세미콜론 + 공백
            r'\s+그러므로\s+',  # 그러므로
            r'\s+하지만\s+',    # 하지만
            r'\s+그런데\s+',    # 그런데
            r'\s+그리고\s+',    # 그리고
            r'\s+또한\s+',      # 또한
            r'\s+따라서\s+',    # 따라서
            r'\s+이\s+',        # "이" (이 기기는, 이 사람은 등)
            r'\s+그\s+',        # "그" (그 기기는, 그 사람은 등)
            r'\s+저\s+',        # "저" (저 기기는, 저 사람은 등)
        ]
        
        # 복합 문장 패턴
        self.compound_patterns = {
            'multiple_objects': [
                r'(\w+)은\s+(\w+)이다\s+(\w+)은\s+(\w+)이다',  # A는 B이다 C는 D이다
                r'(\w+)는\s+(\w+)이다\s+(\w+)는\s+(\w+)이다',  # A는 B이다 C는 D이다
            ],
            'logical_connection': [
                r'(\w+)은\s+(\w+)다\.\s*그러므로\s+(\w+)은\s+(\w+)이다',
                r'(\w+)는\s+(\w+)다\.\s*그러므로\s+(\w+)는\s+(\w+)이다',
                r'(\w+)은\s+(\w+)다\.\s*하지만\s+(\w+)은\s+(\w+)이다',
                r'(\w+)는\s+(\w+)다\.\s*하지만\s+(\w+)는\s+(\w+)이다',
            ]
        }
    
    def analyze_compound_sentence(self, statement: str, context: str = None) -> Dict:
        """복합 문장 분석"""
        logger.info(f"복합 문장 분석 시작: {statement}...")
        
        # 기본 분석
        primary_analysis = self.primary_detector.analyze_statement(statement, context)
        
        # 문장 분리
        sentences = self._split_sentences(statement)
        
        # 복합 문장 패턴 감지
        compound_type = self._detect_compound_type(statement)
        
        # 각 문장별 분석
        sentence_analyses = []
        for sentence in sentences:
            if sentence.strip():
                context_analysis = self.context_detector.analyze_with_context_awareness(sentence.strip(), context)
                sentence_analyses.append({
                    'sentence': sentence.strip(),
                    'context_analysis': context_analysis
                })
        
        # 복합 문장 진실성 계산
        compound_truth, compound_confidence = self._calculate_compound_truth(sentence_analyses, compound_type)
        
        # 복합 문장 교정
        corrected_statement, correction_applied = self._apply_compound_correction(statement, sentence_analyses, compound_type)
        
        result = {
            'original_statement': statement,
            'primary_analysis': primary_analysis,
            'compound_type': compound_type,
            'sentences': sentences,
            'sentence_analyses': sentence_analyses,
            'compound_truth_percentage': compound_truth,
            'compound_confidence': compound_confidence,
            'compound_corrected_statement': corrected_statement,
            'compound_correction_applied': correction_applied,
            'compound_warnings': self._generate_compound_warnings(sentence_analyses, compound_type),
            'philosophical_note': "복합 문장은 여러 맥락을 포함할 수 있으며, 각 부분을 개별적으로 분석해야 합니다."
        }
        
        logger.info(f"복합 문장 분석 완료: {statement}")
        return result
    
    def _split_sentences(self, statement: str) -> List[str]:
        """문장을 분리"""
        sentences = [statement]  # 기본적으로 전체 문장
        
        # 특별한 패턴들 먼저 처리
        # "A는 B이다 C는 D이다" 패턴
        multiple_objects_pattern = r'(\w+[은는])\s+(\w+이다)\s+(\w+[은는])\s+(\w+이다)'
        if re.search(multiple_objects_pattern, statement):
            match = re.search(multiple_objects_pattern, statement)
            if match:
                part1 = match.group(1) + ' ' + match.group(2)
                part2 = match.group(3) + ' ' + match.group(4)
                sentences = [part1.strip(), part2.strip()]
                return sentences
        
        # 일반적인 분리 패턴들
        for pattern in self.sentence_separators:
            if re.search(pattern, statement):
                sentences = re.split(pattern, statement)
                sentences = [s.strip() for s in sentences if s.strip()]
                break
        
        return sentences
    
    def _detect_compound_type(self, statement: str) -> str:
        """복합 문장 유형 감지"""
        for compound_type, patterns in self.compound_patterns.items():
            for pattern in patterns:
                if re.search(pattern, statement):
                    return compound_type
        
        # 기본적으로 여러 문장이 있으면 복합 문장으로 간주
        if len(self._split_sentences(statement)) > 1:
            return 'multiple_sentences'
        
        return 'simple'
    
    def _calculate_compound_truth(self, sentence_analyses: List[Dict], compound_type: str) -> Tuple[float, float]:
        """복합 문장 진실성 계산"""
        if not sentence_analyses:
            return 0.5, 0.5
        
        # 각 문장의 진실성과 신뢰도 수집
        truths = []
        confidences = []
        
        for analysis in sentence_analyses:
            context_analysis = analysis['context_analysis']
            truths.append(context_analysis['context_aware_truth_percentage'])
            confidences.append(context_analysis['context_aware_confidence'])
        
        if compound_type == 'multiple_objects':
            # 여러 객체가 있는 경우: 각각의 맥락을 고려하여 가중 평균
            # 과학적 맥락과 일반 물체 맥락이 섞인 경우 차이를 반영
            if len(truths) >= 2:
                # 첫 번째와 두 번째 문장의 진실성 차이가 클 경우 조정
                truth_diff = abs(truths[0] - truths[1])
                if truth_diff > 0.3:  # 30% 이상 차이
                    # 맥락이 다른 경우 평균을 낮춤 (불일치 페널티)
                    compound_truth = (sum(truths) / len(truths)) * 0.8
                    compound_confidence = (sum(confidences) / len(confidences)) * 0.7
                else:
                    compound_truth = sum(truths) / len(truths)
                    compound_confidence = sum(confidences) / len(confidences)
            else:
                compound_truth = truths[0]
                compound_confidence = confidences[0]
        
        elif compound_type == 'logical_connection':
            # 논리적 연결이 있는 경우: 논리적 일관성 고려
            if len(truths) >= 2:
                # 전제와 결론의 논리적 일관성 확인
                premise_truth = truths[0]
                conclusion_truth = truths[1]
                
                # 논리적 일관성 점수 계산
                logical_consistency = 1.0 - abs(premise_truth - conclusion_truth)
                compound_truth = (premise_truth + conclusion_truth) / 2 * logical_consistency
                compound_confidence = (sum(confidences) / len(confidences)) * logical_consistency
            else:
                compound_truth = truths[0]
                compound_confidence = confidences[0]
        
        else:
            # 일반적인 복합 문장
            compound_truth = sum(truths) / len(truths)
            compound_confidence = sum(confidences) / len(confidences)
        
        return compound_truth, compound_confidence
    
    def _apply_compound_correction(self, statement: str, sentence_analyses: List[Dict], compound_type: str) -> Tuple[str, bool]:
        """복합 문장 교정 적용"""
        corrected_parts = []
        correction_applied = False
        
        for analysis in sentence_analyses:
            sentence = analysis['sentence']
            context_analysis = analysis['context_analysis']
            
            if context_analysis['context_correction_applied']:
                corrected_parts.append(context_analysis['context_corrected_statement'])
                correction_applied = True
            else:
                corrected_parts.append(sentence)
        
        if correction_applied:
            # 원래 문장의 연결어 복원
            corrected_statement = self._restore_connections(statement, corrected_parts)
            return corrected_statement, True
        
        return statement, False
    
    def _restore_connections(self, original: str, corrected_parts: List[str]) -> str:
        """원래 문장의 연결어를 복원"""
        # 간단한 복원: 공백으로 연결
        return ' '.join(corrected_parts)
    
    def _generate_compound_warnings(self, sentence_analyses: List[Dict], compound_type: str) -> List[str]:
        """복합 문장 경고 생성"""
        warnings = []
        
        if compound_type == 'multiple_objects':
            # 서로 다른 맥락의 객체들이 있는 경우
            context_types = []
            for analysis in sentence_analyses:
                context_type = analysis['context_analysis'].get('context_type', 'unknown')
                context_types.append(context_type)
            
            if len(set(context_types)) > 1:
                warnings.append("서로 다른 맥락의 객체들이 하나의 문장에 포함되어 있습니다.")
        
        elif compound_type == 'logical_connection':
            # 논리적 연결이 있는 경우
            if len(sentence_analyses) >= 2:
                premise_truth = sentence_analyses[0]['context_analysis']['context_aware_truth_percentage']
                conclusion_truth = sentence_analyses[1]['context_analysis']['context_aware_truth_percentage']
                
                if abs(premise_truth - conclusion_truth) > 0.4:
                    warnings.append("전제와 결론의 진실성 차이가 큽니다. 논리적 일관성을 확인하세요.")
        
        return warnings

def main():
    """복합 문장 분석기 데모"""
    analyzer = CompoundSentenceAnalyzer()
    
    test_statements = [
        '계란은 구형이다 이 기기는 구형이다',
        '사람은 거짓말을 한다. 그러므로 사람은 나쁜 존재이다.',
        '사람은 선의의 거짓말을 한다. 그러므로 사람은 착한 존재이다.',
        '지구는 구형이다 자동차는 구형이다'
    ]
    
    print("🔍 복합 문장 분석기 데모")
    print("=" * 50)
    
    for statement in test_statements:
        result = analyzer.analyze_compound_sentence(statement)
        
        print(f"\n문장: {statement}")
        print(f"복합 유형: {result['compound_type']}")
        print(f"분리된 문장 수: {len(result['sentences'])}")
        print(f"복합 진실성: {result['compound_truth_percentage']:.1%}")
        print(f"복합 신뢰도: {result['compound_confidence']:.1%}")
        
        if result['compound_correction_applied']:
            print(f"교정: {result['compound_corrected_statement']}")
        
        if result['compound_warnings']:
            print(f"경고: {result['compound_warnings'][0]}")

if __name__ == "__main__":
    main()
