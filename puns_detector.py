#!/usr/bin/env python3
"""
말장난 탐지기 (Puns Detector)
AI가 말장난을 이해하고 적절히 응답할 수 있도록 하는 시스템
"""

import re
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class PunsDetector:
    """말장난 탐지기 - 언어적 유머와 말장난을 인식하고 이해"""
    
    def __init__(self):
        # 말장난 패턴 데이터베이스 (다국어 지원)
        self.pun_patterns = {
            '동어반복': [
                # 한글 패턴
                r'(\w+)는\s+\1(?:이다|다|야|이야)',
                r'(\w+)은\s+\1(?:이다|다|야|이야)',
                r'(\w+)가\s+\1(?:이다|다|야|이야)',
                r'(\w+)이\s+\1(?:이다|다|야|이야)',
                # 영어 패턴
                r'(\w+)는\s+(\w+)(?:이다|다|야|이야)',
                r'(\w+)은\s+(\w+)(?:이다|다|야|이야)',
                r'(\w+)가\s+(\w+)(?:이다|다|야|이야)',
                r'(\w+)이\s+(\w+)(?:이다|다|야|이야)'
            ],
            '모순적_표현': [
                # 한글 패턴
                r'(\w+)는\s+\1가\s+아니다',
                r'(\w+)은\s+\1이\s+아니다',
                r'(\w+)가\s+\1는\s+아니다',
                r'(\w+)이\s+\1은\s+아니다',
                # 영어 패턴
                r'(\w+)는\s+(\w+)가\s+아니다',
                r'(\w+)은\s+(\w+)이\s+아니다',
                r'(\w+)가\s+(\w+)는\s+아니다',
                r'(\w+)이\s+(\w+)은\s+아니다'
            ],
            '논리적_말장난': [
                # 한글 패턴
                r'(\w+)는\s+(\w+)이지만\s+\2는\s+\1이\s+아니다',
                r'(\w+)은\s+(\w+)이지만\s+\2은\s+\1이\s+아니다',
                r'(\w+)가\s+(\w+)이지만\s+\2가\s+\1이\s+아니다',
                r'(\w+)이\s+(\w+)이지만\s+\2이\s+\1이\s+아니다',
                # 영어 패턴
                r'(\w+)는\s+(\w+)이지만\s+(\w+)는\s+(\w+)이\s+아니다',
                r'(\w+)은\s+(\w+)이지만\s+(\w+)은\s+(\w+)이\s+아니다'
            ],
            '동음이의어': [
                # 한글 패턴
                r'(\w+)는\s+(\w+)다\s*,\s*(\w+)는\s+(\w+)다',
                r'(\w+)은\s+(\w+)다\s*,\s*(\w+)은\s+(\w+)다',
                # 영어 패턴
                r'(\w+)는\s+(\w+)다\s*,\s*(\w+)는\s+(\w+)다',
                r'(\w+)은\s+(\w+)다\s*,\s*(\w+)은\s+(\w+)다'
            ],
            '철자_말장난': [
                # 한글 패턴
                r'(\w+)는\s+(\w+)가\s+아니다\s*,\s*(\w+)는\s+(\w+)다',
                r'(\w+)은\s+(\w+)이\s+아니다\s*,\s*(\w+)은\s+(\w+)다',
                # 영어 패턴
                r'(\w+)는\s+(\w+)가\s+아니다\s*,\s*(\w+)는\s+(\w+)다',
                r'(\w+)은\s+(\w+)이\s+아니다\s*,\s*(\w+)은\s+(\w+)다'
            ]
        }
        
        # 말장난 유형별 해석
        self.pun_interpretations = {
            '동어반복': {
                'description': '동일한 단어를 반복하여 의미를 강조하거나 유머를 만드는 표현',
                'example': '개는 개고 고양이는 고양이다',
                'interpretation': '동물의 정체성을 강조하는 유머적 표현'
            },
            '모순적_표현': {
                'description': '같은 단어를 긍정과 부정으로 사용하여 모순을 만드는 표현',
                'example': '바나나는 바나나가 아니다',
                'interpretation': '단어의 다의성을 이용한 언어적 유머'
            },
            '논리적_말장난': {
                'description': '논리적으로 모순되지만 언어적으로는 의미가 있는 표현',
                'example': '물은 물이지만 얼음은 물이 아니다',
                'interpretation': '물질의 상태 변화를 이용한 과학적 유머'
            },
            '동음이의어': {
                'description': '같은 소리지만 다른 의미의 단어를 사용한 표현',
                'example': '개는 개다, 개는 개다',
                'interpretation': '동음이의어를 이용한 언어적 장난'
            },
            '철자_말장난': {
                'description': '철자나 발음의 유사성을 이용한 표현',
                'example': '사과는 사과가 아니다, 사과는 사과다',
                'interpretation': '철자 유사성을 이용한 언어적 유머'
            }
        }
        
        # 말장난 응답 템플릿
        self.pun_responses = {
            '인식': "아, 말장난이네요! 😄",
            '이해': "이해했습니다. 언어적 유머를 사용하셨군요!",
            '응답': "재미있는 표현이네요. AI도 이런 언어적 장난을 이해할 수 있습니다.",
            '설명': "이런 말장난은 인간 언어의 창의성을 보여주는 좋은 예시입니다."
        }
    
    def analyze_with_puns_detection(self, statement: str, context: Optional[str] = None) -> Dict:
        """
        말장난을 포함한 문장을 분석
        
        Args:
            statement: 분석할 문장
            context: 추가 컨텍스트
            
        Returns:
            Dict: 말장난 분석 결과
        """
        logger.info(f"말장난 분석 시작: {statement[:50]}...")
        
        # 말장난 탐지
        detected_puns = self._detect_puns(statement)
        
        # 말장난 유형 분석
        pun_types = self._analyze_pun_types(statement)
        
        # 말장난 해석
        interpretations = self._interpret_puns(statement, detected_puns, pun_types)
        
        # 말장난 응답 생성
        response = self._generate_pun_response(statement, detected_puns, pun_types)
        
        # 말장난 인식 여부
        is_pun_detected = len(detected_puns) > 0
        
        # 말장난 이해도 (0.0 ~ 1.0)
        pun_understanding = self._calculate_pun_understanding(detected_puns, pun_types)
        
        # 말장난 교정 필요성 (말장난은 교정하지 않음)
        needs_correction = False
        
        # 말장난 보존된 문장 (원문 유지)
        preserved_statement = statement
        
        return {
            'is_pun_detected': is_pun_detected,
            'detected_puns': detected_puns,
            'pun_types': pun_types,
            'interpretations': interpretations,
            'pun_understanding': pun_understanding,
            'needs_correction': needs_correction,
            'preserved_statement': preserved_statement,
            'pun_response': response,
            'philosophical_note': "말장난은 인간 언어의 창의성을 보여주는 중요한 표현입니다. AI도 이를 이해하고 존중할 수 있습니다."
        }
    
    def _detect_puns(self, statement: str) -> List[Dict]:
        """말장난 패턴 탐지 (다국어 지원)"""
        detected_puns = []
        
        # 기본 패턴 탐지
        for pun_type, patterns in self.pun_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, statement, re.IGNORECASE)
                for match in matches:
                    # 말장난 패턴인지 더 정확히 확인
                    if self._is_valid_pun_pattern(match, pun_type):
                        detected_puns.append({
                            'type': pun_type,
                            'pattern': pattern,
                            'match': match.group(),
                            'groups': match.groups(),
                            'start': match.start(),
                            'end': match.end()
                        })
        
        # 다국어 말장난 특별 탐지
        multilingual_puns = self._detect_multilingual_puns(statement)
        detected_puns.extend(multilingual_puns)
        
        return detected_puns
    
    def _detect_multilingual_puns(self, statement: str) -> List[Dict]:
        """다국어 말장난 탐지"""
        detected_puns = []
        
        # 한글-영어 혼합 말장난 패턴
        multilingual_patterns = {
            '동어반복_다국어': [
                r'(\w+)는\s+(\w+)(?:이다|다|야|이야)',
                r'(\w+)은\s+(\w+)(?:이다|다|야|이야)',
                r'(\w+)가\s+(\w+)(?:이다|다|야|이야)',
                r'(\w+)이\s+(\w+)(?:이다|다|야|이야)'
            ],
            '모순적_표현_다국어': [
                r'(\w+)는\s+(\w+)가\s+아니다',
                r'(\w+)은\s+(\w+)이\s+아니다',
                r'(\w+)가\s+(\w+)는\s+아니다',
                r'(\w+)이\s+(\w+)은\s+아니다'
            ]
        }
        
        for pun_type, patterns in multilingual_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, statement, re.IGNORECASE)
                for match in matches:
                    groups = match.groups()
                    if len(groups) >= 2:
                        # 한글과 영어가 섞여있는지 확인
                        korean_chars = re.search(r'[가-힣]', groups[0])
                        english_chars = re.search(r'[a-zA-Z]', groups[1])
                        
                        # 반대 방향도 확인 (영어-한글)
                        english_chars_first = re.search(r'[a-zA-Z]', groups[0])
                        korean_chars_second = re.search(r'[가-힣]', groups[1])
                        
                        if (korean_chars and english_chars) or (english_chars_first and korean_chars_second):
                            detected_puns.append({
                                'type': pun_type,
                                'pattern': pattern,
                                'match': match.group(),
                                'groups': groups,
                                'start': match.start(),
                                'end': match.end(),
                                'multilingual': True,
                                'korean_word': groups[0] if korean_chars else groups[1],
                                'english_word': groups[1] if korean_chars else groups[0]
                            })
        
        return detected_puns
    
    def _is_valid_pun_pattern(self, match, pun_type: str) -> bool:
        """말장난 패턴이 유효한지 확인"""
        groups = match.groups()
        
        if pun_type == '동어반복':
            # 동어반복: 같은 단어가 반복되어야 함
            if len(groups) >= 2:
                return groups[0] == groups[1]
        
        elif pun_type == '모순적_표현':
            # 모순적 표현: 같은 단어가 긍정과 부정으로 사용되어야 함
            if len(groups) >= 2:
                return groups[0] == groups[1]
        
        elif pun_type == '논리적_말장난':
            # 논리적 말장난: 특정 패턴이어야 함
            if len(groups) >= 4:
                return groups[0] == groups[2] and groups[1] == groups[3]
        
        # 다른 유형들은 기본적으로 유효하다고 간주
        return True
    
    def _analyze_pun_types(self, statement: str) -> List[str]:
        """말장난 유형 분석"""
        pun_types = []
        
        for pun_type, patterns in self.pun_patterns.items():
            for pattern in patterns:
                if re.search(pattern, statement, re.IGNORECASE):
                    if pun_type not in pun_types:
                        pun_types.append(pun_type)
        
        return pun_types
    
    def _interpret_puns(self, statement: str, detected_puns: List[Dict], pun_types: List[str]) -> List[Dict]:
        """말장난 해석"""
        interpretations = []
        
        for pun_type in pun_types:
            if pun_type in self.pun_interpretations:
                interpretation = self.pun_interpretations[pun_type].copy()
                interpretation['detected_in'] = statement
                interpretations.append(interpretation)
        
        return interpretations
    
    def _generate_pun_response(self, statement: str, detected_puns: List[Dict], pun_types: List[str]) -> str:
        """말장난 응답 생성 (다국어 지원)"""
        if not detected_puns:
            return "말장난이 감지되지 않았습니다."
        
        response_parts = []
        
        # 기본 인식 메시지
        response_parts.append(self.pun_responses['인식'])
        
        # 다국어 말장난 특별 처리
        multilingual_puns = [p for p in detected_puns if p.get('multilingual', False)]
        if multilingual_puns:
            response_parts.append("🌍 다국어 말장난을 감지했습니다!")
            for pun in multilingual_puns:
                korean_word = pun.get('korean_word', '')
                english_word = pun.get('english_word', '')
                response_parts.append(f"• '{korean_word}'는 '{english_word}'이다 - 언어를 바꿔서 같은 의미를 표현한 창의적인 말장난!")
        
        # 말장난 유형별 설명
        for pun_type in pun_types:
            if pun_type in self.pun_interpretations:
                description = self.pun_interpretations[pun_type]['description']
                response_parts.append(f"• {pun_type}: {description}")
        
        # 이해 메시지
        response_parts.append(self.pun_responses['이해'])
        
        # 창의성 인정
        response_parts.append(self.pun_responses['설명'])
        
        return "\n".join(response_parts)
    
    def _calculate_pun_understanding(self, detected_puns: List[Dict], pun_types: List[str]) -> float:
        """말장난 이해도 계산"""
        if not detected_puns:
            return 0.0
        
        # 기본 이해도
        base_understanding = 0.5
        
        # 탐지된 말장난 개수에 따른 가점
        pun_count_bonus = min(len(detected_puns) * 0.1, 0.3)
        
        # 말장난 유형 다양성에 따른 가점
        type_diversity_bonus = min(len(pun_types) * 0.1, 0.2)
        
        # 최종 이해도 계산
        understanding = base_understanding + pun_count_bonus + type_diversity_bonus
        
        return min(1.0, understanding)
    
    def is_pun_statement(self, statement: str) -> bool:
        """문장이 말장난인지 판단"""
        detected_puns = self._detect_puns(statement)
        return len(detected_puns) > 0
    
    def get_pun_explanation(self, statement: str) -> str:
        """말장난에 대한 설명 반환"""
        analysis = self.analyze_with_puns_detection(statement)
        
        if not analysis['is_pun_detected']:
            return "이 문장은 말장난이 아닙니다."
        
        explanation_parts = []
        explanation_parts.append("🎭 말장난 분석 결과:")
        explanation_parts.append("")
        
        for interpretation in analysis['interpretations']:
            explanation_parts.append(f"📝 {interpretation['description']}")
            explanation_parts.append(f"💡 해석: {interpretation['interpretation']}")
            explanation_parts.append("")
        
        explanation_parts.append(f"🎯 이해도: {analysis['pun_understanding']:.1%}")
        explanation_parts.append("")
        explanation_parts.append("✨ AI도 말장난을 이해할 수 있습니다!")
        
        return "\n".join(explanation_parts)

# 사용 예시
if __name__ == "__main__":
    detector = PunsDetector()
    
    # 테스트 문장들
    test_statements = [
        "개는 개고 고양이는 고양이다",
        "바나나는 바나나가 아니다",
        "물은 물이지만 얼음은 물이 아니다",
        "사과는 사과지만 사과는 사과가 아니다",
        "시간은 시간이지만 시간은 시간이 아니다"
    ]
    
    for statement in test_statements:
        print(f"\n문장: {statement}")
        analysis = detector.analyze_with_puns_detection(statement)
        
        if analysis['is_pun_detected']:
            print("🎭 말장난 감지!")
            print(f"이해도: {analysis['pun_understanding']:.1%}")
            print(f"응답: {analysis['pun_response']}")
        else:
            print("말장난이 감지되지 않았습니다.")
