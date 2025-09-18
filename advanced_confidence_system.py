#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Confidence System
고급 신뢰도 평가 시스템

ChatGPT/Claude 수준의 다층적 신뢰도 평가와 품질 보증을 제공합니다.
"""

import re
import json
import logging
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import statistics
import math
from collections import defaultdict
import asyncio
from concurrent.futures import ThreadPoolExecutor

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConfidenceSource(Enum):
    """신뢰도 소스"""
    INPUT_VALIDATION = "input_validation"
    CONTENT_ANALYSIS = "content_analysis"
    CONTEXT_RELEVANCE = "context_relevance"
    PROCESSING_SUCCESS = "processing_success"
    RESPONSE_QUALITY = "response_quality"
    CONSISTENCY = "consistency"
    EXPERTISE = "expertise"
    EVIDENCE = "evidence"

class QualityLevel(Enum):
    """품질 수준"""
    POOR = 0.0
    FAIR = 0.25
    GOOD = 0.5
    VERY_GOOD = 0.75
    EXCELLENT = 0.95
    PERFECT = 1.0

@dataclass
class ConfidenceScore:
    """신뢰도 점수"""
    overall: float
    sources: Dict[ConfidenceSource, float]
    quality_level: QualityLevel
    explanation: str
    recommendations: List[str]
    timestamp: datetime
    processing_time: float

@dataclass
class QualityMetrics:
    """품질 지표"""
    accuracy: float
    completeness: float
    consistency: float
    relevance: float
    clarity: float
    reliability: float
    timeliness: float
    usability: float

class AdvancedConfidenceSystem:
    """고급 신뢰도 평가 시스템"""
    
    def __init__(self):
        self.confidence_weights = self._initialize_confidence_weights()
        self.quality_thresholds = self._initialize_quality_thresholds()
        self.expertise_patterns = self._initialize_expertise_patterns()
        self.evidence_patterns = self._initialize_evidence_patterns()
        self.consistency_history = defaultdict(list)
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def _initialize_confidence_weights(self) -> Dict[ConfidenceSource, float]:
        """신뢰도 가중치 초기화"""
        return {
            ConfidenceSource.INPUT_VALIDATION: 0.15,
            ConfidenceSource.CONTENT_ANALYSIS: 0.20,
            ConfidenceSource.CONTEXT_RELEVANCE: 0.15,
            ConfidenceSource.PROCESSING_SUCCESS: 0.15,
            ConfidenceSource.RESPONSE_QUALITY: 0.15,
            ConfidenceSource.CONSISTENCY: 0.10,
            ConfidenceSource.EXPERTISE: 0.05,
            ConfidenceSource.EVIDENCE: 0.05
        }
    
    def _initialize_quality_thresholds(self) -> Dict[QualityLevel, float]:
        """품질 임계값 초기화"""
        return {
            QualityLevel.POOR: 0.0,
            QualityLevel.FAIR: 0.25,
            QualityLevel.GOOD: 0.5,
            QualityLevel.VERY_GOOD: 0.75,
            QualityLevel.EXCELLENT: 0.95,
            QualityLevel.PERFECT: 1.0
        }
    
    def _initialize_expertise_patterns(self) -> Dict[str, List[str]]:
        """전문성 패턴 초기화"""
        return {
            'scientific': [
                r'연구에\s+따르면', r'실험\s+결과', r'과학적으로\s+입증된',
                r'통계적으로\s+의미있는', r'peer\s+reviewed', r'학술\s+논문'
            ],
            'technical': [
                r'기술적으로\s+검증된', r'소스\s+코드', r'알고리즘',
                r'프로토콜', r'API\s+문서', r'기술\s+명세서'
            ],
            'medical': [
                r'의학적으로\s+입증된', r'임상\s+시험', r'FDA\s+승인',
                r'의료진\s+권고', r'의학\s+논문', r'진료\s+지침'
            ],
            'legal': [
                r'법률에\s+따르면', r'법원\s+판결', r'법령',
                r'법적\s+근거', r'법률\s+조문', r'법적\s+해석'
            ]
        }
    
    def _initialize_evidence_patterns(self) -> List[str]:
        """증거 패턴 초기화"""
        return [
            r'출처:', r'참고문헌:', r'근거:', r'증거:',
            r'http[s]?://', r'www\.', r'\.com', r'\.org', r'\.edu',
            r'\[.*?\]', r'\(.*?\)', r'인용:', r'인용문:'
        ]
    
    async def evaluate_confidence(self, 
                                statement: str, 
                                context: str = "", 
                                analysis_result: Dict[str, Any] = None,
                                validation_result: Dict[str, Any] = None) -> ConfidenceScore:
        """신뢰도 평가"""
        start_time = datetime.now()
        
        try:
            # 각 소스별 신뢰도 평가
            source_scores = {}
            
            # 1. 입력 검증 신뢰도
            source_scores[ConfidenceSource.INPUT_VALIDATION] = await self._evaluate_input_validation(validation_result)
            
            # 2. 내용 분석 신뢰도
            source_scores[ConfidenceSource.CONTENT_ANALYSIS] = await self._evaluate_content_analysis(statement, analysis_result)
            
            # 3. 맥락 관련성 신뢰도
            source_scores[ConfidenceSource.CONTEXT_RELEVANCE] = await self._evaluate_context_relevance(statement, context)
            
            # 4. 처리 성공 신뢰도
            source_scores[ConfidenceSource.PROCESSING_SUCCESS] = await self._evaluate_processing_success(analysis_result)
            
            # 5. 응답 품질 신뢰도
            source_scores[ConfidenceSource.RESPONSE_QUALITY] = await self._evaluate_response_quality(statement, analysis_result)
            
            # 6. 일관성 신뢰도
            source_scores[ConfidenceSource.CONSISTENCY] = await self._evaluate_consistency(statement, analysis_result)
            
            # 7. 전문성 신뢰도
            source_scores[ConfidenceSource.EXPERTISE] = await self._evaluate_expertise(statement, context)
            
            # 8. 증거 신뢰도
            source_scores[ConfidenceSource.EVIDENCE] = await self._evaluate_evidence(statement, analysis_result)
            
            # 전체 신뢰도 계산
            overall_confidence = self._calculate_overall_confidence(source_scores)
            
            # 품질 수준 결정
            quality_level = self._determine_quality_level(overall_confidence)
            
            # 설명 및 권장사항 생성
            explanation = self._generate_explanation(source_scores, overall_confidence)
            recommendations = self._generate_recommendations(source_scores, overall_confidence)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return ConfidenceScore(
                overall=overall_confidence,
                sources=source_scores,
                quality_level=quality_level,
                explanation=explanation,
                recommendations=recommendations,
                timestamp=datetime.now(),
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"신뢰도 평가 중 오류 발생: {str(e)}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return ConfidenceScore(
                overall=0.0,
                sources={},
                quality_level=QualityLevel.POOR,
                explanation=f"신뢰도 평가 중 오류가 발생했습니다: {str(e)}",
                recommendations=["시스템 관리자에게 문의하세요."],
                timestamp=datetime.now(),
                processing_time=processing_time
            )
    
    async def _evaluate_input_validation(self, validation_result: Dict[str, Any]) -> float:
        """입력 검증 신뢰도 평가"""
        if not validation_result:
            return 0.5  # 중간값
        
        if validation_result.get('is_valid', False):
            base_score = 0.9
        else:
            base_score = 0.3
        
        # 오류 및 경고에 따른 감점
        error_penalty = len(validation_result.get('errors', [])) * 0.1
        warning_penalty = len(validation_result.get('warnings', [])) * 0.05
        
        return max(0.0, min(1.0, base_score - error_penalty - warning_penalty))
    
    async def _evaluate_content_analysis(self, statement: str, analysis_result: Dict[str, Any]) -> float:
        """내용 분석 신뢰도 평가"""
        if not analysis_result:
            return 0.5
        
        # 기본 분석 결과 기반 평가
        truth_percentage = analysis_result.get('final_analysis', {}).get('truth_percentage', 0.5)
        confidence = analysis_result.get('final_analysis', {}).get('confidence', 0.5)
        
        # 내용 품질 평가
        content_quality = self._assess_content_quality(statement)
        
        # 종합 점수 계산
        return (truth_percentage * 0.4 + confidence * 0.3 + content_quality * 0.3)
    
    async def _evaluate_context_relevance(self, statement: str, context: str) -> float:
        """맥락 관련성 신뢰도 평가"""
        if not context:
            return 0.7  # 맥락이 없으면 중간값
        
        # 단어 유사도 계산
        statement_words = set(statement.lower().split())
        context_words = set(context.lower().split())
        
        if not statement_words or not context_words:
            return 0.5
        
        # Jaccard 유사도
        intersection = statement_words.intersection(context_words)
        union = statement_words.union(context_words)
        jaccard_similarity = len(intersection) / len(union) if union else 0
        
        # 의미적 관련성 평가
        semantic_relevance = self._assess_semantic_relevance(statement, context)
        
        return (jaccard_similarity * 0.6 + semantic_relevance * 0.4)
    
    async def _evaluate_processing_success(self, analysis_result: Dict[str, Any]) -> float:
        """처리 성공 신뢰도 평가"""
        if not analysis_result:
            return 0.0
        
        # 분석 결과의 완성도 평가
        completeness_score = self._assess_analysis_completeness(analysis_result)
        
        # 오류 여부 확인
        has_errors = any('error' in str(value).lower() for value in analysis_result.values())
        error_penalty = 0.3 if has_errors else 0.0
        
        return max(0.0, min(1.0, completeness_score - error_penalty))
    
    async def _evaluate_response_quality(self, statement: str, analysis_result: Dict[str, Any]) -> float:
        """응답 품질 신뢰도 평가"""
        # 문장 구조 품질
        structure_quality = self._assess_structure_quality(statement)
        
        # 분석 결과의 상세도
        detail_quality = self._assess_detail_quality(analysis_result)
        
        # 교정 품질
        correction_quality = self._assess_correction_quality(analysis_result)
        
        return (structure_quality * 0.4 + detail_quality * 0.3 + correction_quality * 0.3)
    
    async def _evaluate_consistency(self, statement: str, analysis_result: Dict[str, Any]) -> float:
        """일관성 신뢰도 평가"""
        # 이전 분석 결과와의 일관성
        statement_hash = hash(statement)
        if statement_hash in self.consistency_history:
            previous_scores = self.consistency_history[statement_hash]
            if previous_scores:
                current_score = analysis_result.get('final_analysis', {}).get('truth_percentage', 0.5)
                variance = statistics.stdev([current_score] + previous_scores)
                consistency_score = max(0.0, 1.0 - variance)
            else:
                consistency_score = 0.8
        else:
            consistency_score = 0.8
        
        # 현재 결과를 히스토리에 추가
        current_score = analysis_result.get('final_analysis', {}).get('truth_percentage', 0.5)
        self.consistency_history[statement_hash].append(current_score)
        
        # 최근 10개만 유지
        if len(self.consistency_history[statement_hash]) > 10:
            self.consistency_history[statement_hash] = self.consistency_history[statement_hash][-10:]
        
        return consistency_score
    
    async def _evaluate_expertise(self, statement: str, context: str) -> float:
        """전문성 신뢰도 평가"""
        expertise_score = 0.0
        total_patterns = 0
        
        for domain, patterns in self.expertise_patterns.items():
            domain_score = 0.0
            for pattern in patterns:
                if re.search(pattern, statement + " " + context, re.IGNORECASE):
                    domain_score += 1.0
                total_patterns += 1
            expertise_score += domain_score / len(patterns) if patterns else 0
        
        return expertise_score / len(self.expertise_patterns) if self.expertise_patterns else 0.5
    
    async def _evaluate_evidence(self, statement: str, analysis_result: Dict[str, Any]) -> float:
        """증거 신뢰도 평가"""
        evidence_score = 0.0
        
        # 문장 내 증거 패턴 검사
        for pattern in self.evidence_patterns:
            if re.search(pattern, statement, re.IGNORECASE):
                evidence_score += 0.1
        
        # 분석 결과의 증거 품질
        if analysis_result:
            sources = analysis_result.get('sources', [])
            if sources:
                evidence_score += min(0.5, len(sources) * 0.1)
            
            fact_checks = analysis_result.get('fact_checks', [])
            if fact_checks:
                evidence_score += min(0.3, len(fact_checks) * 0.1)
        
        return min(1.0, evidence_score)
    
    def _assess_content_quality(self, statement: str) -> float:
        """내용 품질 평가"""
        if not statement.strip():
            return 0.0
        
        quality_score = 0.5  # 기본 점수
        
        # 길이 적절성
        word_count = len(statement.split())
        if 5 <= word_count <= 100:
            quality_score += 0.2
        elif word_count > 100:
            quality_score += 0.1
        
        # 문장 구조
        sentences = re.split(r'[.!?]+', statement)
        if len(sentences) > 1:
            quality_score += 0.1
        
        # 특수문자 사용
        if re.search(r'[.,!?;:]', statement):
            quality_score += 0.1
        
        # 대소문자 사용
        if re.search(r'[A-Z]', statement) and re.search(r'[a-z]', statement):
            quality_score += 0.1
        
        return min(1.0, quality_score)
    
    def _assess_semantic_relevance(self, statement: str, context: str) -> float:
        """의미적 관련성 평가"""
        # 간단한 키워드 매칭 기반 평가
        statement_keywords = set(re.findall(r'\w+', statement.lower()))
        context_keywords = set(re.findall(r'\w+', context.lower()))
        
        if not statement_keywords or not context_keywords:
            return 0.5
        
        # 공통 키워드 비율
        common_keywords = statement_keywords.intersection(context_keywords)
        relevance = len(common_keywords) / len(statement_keywords.union(context_keywords))
        
        return relevance
    
    def _assess_analysis_completeness(self, analysis_result: Dict[str, Any]) -> float:
        """분석 완성도 평가"""
        required_fields = ['final_analysis', 'basic_analysis', 'meta_analysis']
        present_fields = sum(1 for field in required_fields if field in analysis_result)
        
        return present_fields / len(required_fields)
    
    def _assess_structure_quality(self, statement: str) -> float:
        """구조 품질 평가"""
        if not statement.strip():
            return 0.0
        
        quality_score = 0.5
        
        # 문장 끝 마침표
        if statement.strip().endswith(('.', '!', '?')):
            quality_score += 0.2
        
        # 적절한 길이
        word_count = len(statement.split())
        if 3 <= word_count <= 50:
            quality_score += 0.2
        elif word_count > 50:
            quality_score += 0.1
        
        # 문장 시작 대문자
        if statement.strip()[0].isupper():
            quality_score += 0.1
        
        return min(1.0, quality_score)
    
    def _assess_detail_quality(self, analysis_result: Dict[str, Any]) -> float:
        """상세도 품질 평가"""
        if not analysis_result:
            return 0.0
        
        detail_score = 0.0
        
        # 분석 결과의 상세도
        for key, value in analysis_result.items():
            if isinstance(value, dict) and len(value) > 0:
                detail_score += 0.1
            elif isinstance(value, list) and len(value) > 0:
                detail_score += 0.05
        
        return min(1.0, detail_score)
    
    def _assess_correction_quality(self, analysis_result: Dict[str, Any]) -> float:
        """교정 품질 평가"""
        if not analysis_result:
            return 0.0
        
        correction_score = 0.5
        
        # 교정 제안 존재 여부
        if analysis_result.get('final_analysis', {}).get('needs_correction', False):
            correction_score += 0.3
        
        # 교정된 문장 존재 여부
        if analysis_result.get('final_analysis', {}).get('corrected_statement'):
            correction_score += 0.2
        
        return min(1.0, correction_score)
    
    def _calculate_overall_confidence(self, source_scores: Dict[ConfidenceSource, float]) -> float:
        """전체 신뢰도 계산"""
        weighted_sum = 0.0
        total_weight = 0.0
        
        for source, score in source_scores.items():
            weight = self.confidence_weights.get(source, 0.1)
            weighted_sum += score * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _determine_quality_level(self, confidence: float) -> QualityLevel:
        """품질 수준 결정"""
        for level, threshold in sorted(self.quality_thresholds.items(), key=lambda x: x[1], reverse=True):
            if confidence >= threshold:
                return level
        return QualityLevel.POOR
    
    def _generate_explanation(self, source_scores: Dict[ConfidenceSource, float], overall_confidence: float) -> str:
        """설명 생성"""
        explanations = []
        
        # 전체 신뢰도 설명
        if overall_confidence >= 0.9:
            explanations.append("매우 높은 신뢰도를 보입니다.")
        elif overall_confidence >= 0.7:
            explanations.append("높은 신뢰도를 보입니다.")
        elif overall_confidence >= 0.5:
            explanations.append("보통 수준의 신뢰도를 보입니다.")
        else:
            explanations.append("신뢰도가 낮습니다.")
        
        # 주요 강점과 약점
        strengths = [source.value for source, score in source_scores.items() if score >= 0.8]
        weaknesses = [source.value for source, score in source_scores.items() if score < 0.5]
        
        if strengths:
            explanations.append(f"강점: {', '.join(strengths)}")
        if weaknesses:
            explanations.append(f"개선 필요: {', '.join(weaknesses)}")
        
        return " ".join(explanations)
    
    def _generate_recommendations(self, source_scores: Dict[ConfidenceSource, float], overall_confidence: float) -> List[str]:
        """권장사항 생성"""
        recommendations = []
        
        # 신뢰도가 낮은 소스에 대한 권장사항
        if source_scores.get(ConfidenceSource.INPUT_VALIDATION, 0) < 0.5:
            recommendations.append("입력 형식을 확인하고 올바른 데이터를 제공하세요.")
        
        if source_scores.get(ConfidenceSource.CONTENT_ANALYSIS, 0) < 0.5:
            recommendations.append("내용의 품질을 개선하고 더 명확한 문장을 작성하세요.")
        
        if source_scores.get(ConfidenceSource.CONTEXT_RELEVANCE, 0) < 0.5:
            recommendations.append("문맥과 관련된 내용으로 수정하세요.")
        
        if source_scores.get(ConfidenceSource.CONSISTENCY, 0) < 0.5:
            recommendations.append("일관된 결과를 위해 동일한 조건에서 다시 시도하세요.")
        
        if source_scores.get(ConfidenceSource.EVIDENCE, 0) < 0.5:
            recommendations.append("근거나 출처를 추가하여 신뢰성을 높이세요.")
        
        # 전체적인 권장사항
        if overall_confidence < 0.5:
            recommendations.append("전반적인 품질을 개선하기 위해 입력 내용을 검토하세요.")
        
        return recommendations

def main():
    """메인 실행 함수"""
    print("🔍 고급 신뢰도 평가 시스템 테스트")
    print("=" * 60)
    
    confidence_system = AdvancedConfidenceSystem()
    
    # 테스트 케이스들
    test_cases = [
        {
            'statement': '지구는 둥글다.',
            'context': '과학적 사실에 대한 질문',
            'analysis_result': {
                'final_analysis': {
                    'truth_percentage': 0.95,
                    'confidence': 0.9,
                    'needs_correction': False
                },
                'sources': [{'title': 'NASA', 'url': 'https://nasa.gov'}],
                'fact_checks': [{'statement': '지구는 구형', 'is_factual': True}]
            },
            'validation_result': {
                'is_valid': True,
                'errors': [],
                'warnings': []
            }
        },
        {
            'statement': '정말로 완전히 절대적으로 모든 것이 100% 진실이다.',
            'context': '과장된 표현 테스트',
            'analysis_result': {
                'final_analysis': {
                    'truth_percentage': 0.2,
                    'confidence': 0.3,
                    'needs_correction': True
                }
            },
            'validation_result': {
                'is_valid': True,
                'errors': [],
                'warnings': ['과장 표현이 감지되었습니다.']
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. 테스트 케이스: {test_case['statement']}")
        print("-" * 40)
        
        try:
            # 비동기 신뢰도 평가 실행
            import asyncio
            result = asyncio.run(confidence_system.evaluate_confidence(
                test_case['statement'],
                test_case['context'],
                test_case['analysis_result'],
                test_case['validation_result']
            ))
            
            print(f"전체 신뢰도: {result.overall:.3f}")
            print(f"품질 수준: {result.quality_level.name}")
            print(f"처리 시간: {result.processing_time:.3f}초")
            print(f"설명: {result.explanation}")
            
            print("\n소스별 신뢰도:")
            for source, score in result.sources.items():
                print(f"  {source.value}: {score:.3f}")
            
            if result.recommendations:
                print(f"\n권장사항:")
                for rec in result.recommendations:
                    print(f"  - {rec}")
                    
        except Exception as e:
            print(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    main()
