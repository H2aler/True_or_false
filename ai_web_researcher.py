#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Web Researcher
AI 웹 연구원

AI가 인터넷에서 정보를 검색하고 진실성을 검증하여 질문에 답변하는 시스템입니다.
"""

import requests
import re
import json
import time
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
import random

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    """검색 결과"""
    title: str
    url: str
    snippet: str
    source: str
    credibility_score: float
    relevance_score: float
    timestamp: datetime

@dataclass
class FactCheckResult:
    """사실 검증 결과"""
    statement: str
    is_factual: bool
    confidence: float
    evidence: List[str]
    contradictory_sources: List[str]
    verification_method: str
    timestamp: datetime

@dataclass
class AnswerResult:
    """답변 결과"""
    question: str
    answer: str
    confidence: float
    sources: List[SearchResult]
    fact_checks: List[FactCheckResult]
    reasoning: str
    timestamp: datetime

class AIWebResearcher:
    """AI 웹 연구원"""
    
    def __init__(self):
        self.search_engines = {
            'google': self._search_google,
            'bing': self._search_bing,
            'duckduckgo': self._search_duckduckgo
        }
        
        # 신뢰할 수 있는 소스 도메인들
        self.credible_domains = [
            'wikipedia.org', 'britannica.com', 'nasa.gov', 'nih.gov',
            'who.int', 'cdc.gov', 'nature.com', 'science.org',
            'reuters.com', 'ap.org', 'bbc.com', 'cnn.com',
            'nytimes.com', 'washingtonpost.com', 'theguardian.com',
            'scientificamerican.com', 'nationalgeographic.com',
            'mayoclinic.org', 'webmd.com', 'harvard.edu',
            'mit.edu', 'stanford.edu', 'berkeley.edu'
        ]
        
        # 의심스러운 소스 도메인들
        self.suspicious_domains = [
            'conspiracy.com', 'truth.com', 'realnews.com',
            'alternative.com', 'hidden.com', 'secret.com'
        ]
        
        # 사실 검증 패턴들
        self.fact_check_patterns = {
            'scientific_facts': [
                r'지구.*둥글', r'물.*100도.*끓', r'1\s*\+\s*1\s*=\s*2',
                r'태양.*중심', r'중력.*존재', r'DNA.*구조'
            ],
            'historical_facts': [
                r'세계대전.*발생', r'인류.*진화', r'문명.*발전'
            ],
            'medical_facts': [
                r'백신.*효과', r'세균.*질병', r'의학.*발전'
            ]
        }
        
        # 헤더 설정 (봇 탐지 회피)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def research_question(self, question: str, max_sources: int = 5) -> AnswerResult:
        """질문에 대한 연구 수행"""
        logger.info(f"질문 연구 시작: {question}")
        
        # 1. 질문 분석 및 검색 키워드 생성
        search_keywords = self._generate_search_keywords(question)
        
        # 2. 웹 검색 수행
        search_results = []
        for keyword in search_keywords[:3]:  # 상위 3개 키워드만 사용
            results = self._search_web(keyword, max_results=3)
            search_results.extend(results)
        
        # 3. 검색 결과 정리 및 신뢰도 평가
        search_results = self._evaluate_sources(search_results)
        search_results = sorted(search_results, key=lambda x: x.credibility_score, reverse=True)[:max_sources]
        
        # 4. 사실 검증 수행
        fact_checks = []
        for result in search_results:
            fact_check = self._verify_facts(result.snippet)
            if fact_check:
                fact_checks.append(fact_check)
        
        # 5. 답변 생성
        answer, confidence, reasoning = self._generate_answer(question, search_results, fact_checks)
        
        return AnswerResult(
            question=question,
            answer=answer,
            confidence=confidence,
            sources=search_results,
            fact_checks=fact_checks,
            reasoning=reasoning,
            timestamp=datetime.now()
        )
    
    def _generate_search_keywords(self, question: str) -> List[str]:
        """질문에서 검색 키워드 생성"""
        # 기본 키워드
        keywords = [question]
        
        # 질문 유형별 키워드 추가
        if any(word in question for word in ['무엇', '뭐', 'what']):
            keywords.append(question.replace('무엇', '').replace('뭐', '').strip())
        
        if any(word in question for word in ['언제', 'when']):
            keywords.append(question + ' 날짜 시간')
        
        if any(word in question for word in ['어디', 'where']):
            keywords.append(question + ' 위치 장소')
        
        if any(word in question for word in ['왜', '어떻게', 'why', 'how']):
            keywords.append(question + ' 이유 원인')
        
        # 영어 키워드도 추가
        if not any(ord(char) > 127 for char in question):  # 한글이 없는 경우
            keywords.append(question + ' facts information')
        
        return keywords
    
    def _search_web(self, query: str, max_results: int = 5) -> List[SearchResult]:
        """웹 검색 수행"""
        results = []
        
        # 여러 검색 엔진 사용
        for engine_name, search_func in self.search_engines.items():
            try:
                engine_results = search_func(query, max_results)
                results.extend(engine_results)
                time.sleep(1)  # 요청 간격 조절
            except Exception as e:
                logger.warning(f"{engine_name} 검색 실패: {e}")
                continue
        
        return results
    
    def _search_google(self, query: str, max_results: int) -> List[SearchResult]:
        """Google 검색 (시뮬레이션)"""
        # 실제 Google API 대신 시뮬레이션
        results = []
        
        # 시뮬레이션된 검색 결과
        mock_results = [
            {
                'title': f'{query}에 대한 정보 - Wikipedia',
                'url': 'https://ko.wikipedia.org/wiki/' + quote(query),
                'snippet': f'{query}에 대한 상세한 정보가 위키피디아에 있습니다.',
                'source': 'wikipedia.org'
            },
            {
                'title': f'{query} 관련 뉴스 - BBC',
                'url': 'https://www.bbc.com/news/' + quote(query),
                'snippet': f'{query}에 대한 최신 뉴스와 분석을 제공합니다.',
                'source': 'bbc.com'
            },
            {
                'title': f'{query} 과학적 연구 - Nature',
                'url': 'https://www.nature.com/articles/' + quote(query),
                'snippet': f'{query}에 대한 과학적 연구 결과와 논문입니다.',
                'source': 'nature.com'
            }
        ]
        
        for i, result in enumerate(mock_results[:max_results]):
            results.append(SearchResult(
                title=result['title'],
                url=result['url'],
                snippet=result['snippet'],
                source=result['source'],
                credibility_score=self._calculate_credibility(result['source']),
                relevance_score=0.9 - (i * 0.1),
                timestamp=datetime.now()
            ))
        
        return results
    
    def _search_bing(self, query: str, max_results: int) -> List[SearchResult]:
        """Bing 검색 (시뮬레이션)"""
        # Bing 검색 시뮬레이션
        results = []
        
        mock_results = [
            {
                'title': f'{query} - Britannica',
                'url': 'https://www.britannica.com/topic/' + quote(query),
                'snippet': f'{query}에 대한 백과사전 정보입니다.',
                'source': 'britannica.com'
            },
            {
                'title': f'{query} 의학 정보 - Mayo Clinic',
                'url': 'https://www.mayoclinic.org/diseases-conditions/' + quote(query),
                'snippet': f'{query}에 대한 의학적 정보와 치료법입니다.',
                'source': 'mayoclinic.org'
            }
        ]
        
        for i, result in enumerate(mock_results[:max_results]):
            results.append(SearchResult(
                title=result['title'],
                url=result['url'],
                snippet=result['snippet'],
                source=result['source'],
                credibility_score=self._calculate_credibility(result['source']),
                relevance_score=0.8 - (i * 0.1),
                timestamp=datetime.now()
            ))
        
        return results
    
    def _search_duckduckgo(self, query: str, max_results: int) -> List[SearchResult]:
        """DuckDuckGo 검색 (시뮬레이션)"""
        # DuckDuckGo 검색 시뮬레이션
        results = []
        
        mock_results = [
            {
                'title': f'{query} - Scientific American',
                'url': 'https://www.scientificamerican.com/article/' + quote(query),
                'snippet': f'{query}에 대한 과학적 설명과 분석입니다.',
                'source': 'scientificamerican.com'
            }
        ]
        
        for i, result in enumerate(mock_results[:max_results]):
            results.append(SearchResult(
                title=result['title'],
                url=result['url'],
                snippet=result['snippet'],
                source=result['source'],
                credibility_score=self._calculate_credibility(result['source']),
                relevance_score=0.85 - (i * 0.1),
                timestamp=datetime.now()
            ))
        
        return results
    
    def _calculate_credibility(self, domain: str) -> float:
        """도메인 신뢰도 계산"""
        if domain in self.credible_domains:
            return 0.9
        elif domain in self.suspicious_domains:
            return 0.1
        elif any(edu in domain for edu in ['.edu', '.ac.']):
            return 0.8
        elif any(gov in domain for gov in ['.gov', '.go.kr']):
            return 0.85
        elif any(org in domain for org in ['.org']):
            return 0.7
        else:
            return 0.5
    
    def _evaluate_sources(self, results: List[SearchResult]) -> List[SearchResult]:
        """검색 결과 신뢰도 평가"""
        for result in results:
            # 도메인 기반 신뢰도
            domain_credibility = self._calculate_credibility(result.source)
            
            # 내용 기반 신뢰도
            content_credibility = self._evaluate_content_credibility(result.snippet)
            
            # 최종 신뢰도 계산
            result.credibility_score = (domain_credibility * 0.7 + content_credibility * 0.3)
        
        return results
    
    def _evaluate_content_credibility(self, content: str) -> float:
        """내용 신뢰도 평가"""
        credibility = 0.5
        
        # 신뢰할 수 있는 표현들
        credible_phrases = [
            '연구에 따르면', '과학적으로', '통계적으로', '실험 결과',
            '전문가가', '학술적으로', '검증된', '입증된'
        ]
        
        # 의심스러운 표현들
        suspicious_phrases = [
            '확실히', '100%', '절대적으로', '의심의 여지가 없다',
            '숨겨진 진실', '음모론', '정부가 숨긴'
        ]
        
        for phrase in credible_phrases:
            if phrase in content:
                credibility += 0.1
        
        for phrase in suspicious_phrases:
            if phrase in content:
                credibility -= 0.2
        
        return max(0.0, min(1.0, credibility))
    
    def _verify_facts(self, content: str) -> Optional[FactCheckResult]:
        """사실 검증 수행"""
        for category, patterns in self.fact_check_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return FactCheckResult(
                        statement=content,
                        is_factual=True,
                        confidence=0.8,
                        evidence=[f"패턴 '{pattern}' 매칭"],
                        contradictory_sources=[],
                        verification_method=category,
                        timestamp=datetime.now()
                    )
        
        return None
    
    def _generate_answer(self, question: str, sources: List[SearchResult], fact_checks: List[FactCheckResult]) -> Tuple[str, float, str]:
        """답변 생성"""
        if not sources:
            return "죄송합니다. 이 질문에 대한 신뢰할 수 있는 정보를 찾을 수 없습니다.", 0.0, "검색 결과가 없음"
        
        # 신뢰도가 높은 소스들만 사용
        reliable_sources = [s for s in sources if s.credibility_score > 0.7]
        
        if not reliable_sources:
            return "찾은 정보의 신뢰도가 낮아 정확한 답변을 제공하기 어렵습니다.", 0.3, "신뢰할 수 있는 소스 부족"
        
        # 답변 생성
        answer_parts = []
        confidence_scores = []
        
        for source in reliable_sources[:3]:  # 상위 3개 소스만 사용
            answer_parts.append(f"• {source.snippet}")
            confidence_scores.append(source.credibility_score)
        
        # 사실 검증 결과 추가
        if fact_checks:
            verified_facts = [fc for fc in fact_checks if fc.is_factual]
            if verified_facts:
                answer_parts.append(f"• 검증된 사실: {len(verified_facts)}개 항목 확인됨")
                confidence_scores.append(0.9)
        
        answer = f"질문: {question}\n\n답변:\n" + "\n".join(answer_parts)
        
        # 신뢰도 계산
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
        
        # 추론 과정
        reasoning = f"총 {len(sources)}개의 소스에서 정보를 수집했으며, 그 중 {len(reliable_sources)}개의 신뢰할 수 있는 소스를 기반으로 답변을 생성했습니다."
        
        return answer, avg_confidence, reasoning

def main():
    """메인 실행 함수"""
    print("🔍 AI 웹 연구원 시작")
    print("=" * 60)
    
    researcher = AIWebResearcher()
    
    # 테스트 질문들
    test_questions = [
        "지구는 둥글까요?",
        "물은 몇 도에서 끓나요?",
        "1 + 1은 얼마인가요?",
        "코로나19는 무엇인가요?",
        "인공지능은 어떻게 작동하나요?"
    ]
    
    for question in test_questions:
        print(f"\n❓ 질문: {question}")
        print("-" * 40)
        
        try:
            result = researcher.research_question(question)
            
            print(f"💡 답변: {result.answer}")
            print(f"🎯 신뢰도: {result.confidence:.2f}")
            print(f"🔍 추론: {result.reasoning}")
            print(f"📚 소스 수: {len(result.sources)}개")
            
            if result.sources:
                print("\n📖 주요 소스:")
                for i, source in enumerate(result.sources[:3], 1):
                    print(f"  {i}. {source.title} (신뢰도: {source.credibility_score:.2f})")
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        
        print("=" * 60)
        time.sleep(2)

if __name__ == "__main__":
    main()
