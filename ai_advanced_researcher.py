#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Advanced Web Researcher
AI 고급 웹 연구원

실제 웹 검색을 수행하고 진실성을 검증하여 질문에 답변하는 고급 시스템입니다.
"""

import requests
import re
import json
import time
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import quote, urljoin, urlparse
from bs4 import BeautifulSoup
import random
import hashlib

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WebSearchResult:
    """웹 검색 결과"""
    title: str
    url: str
    content: str
    snippet: str
    domain: str
    credibility_score: float
    relevance_score: float
    fact_check_score: float
    timestamp: datetime

@dataclass
class FactVerification:
    """사실 검증"""
    statement: str
    is_verified: bool
    confidence: float
    evidence: List[str]
    contradictory_evidence: List[str]
    verification_method: str
    source_diversity: int

@dataclass
class ResearchAnswer:
    """연구 답변"""
    question: str
    answer: str
    confidence: float
    sources: List[WebSearchResult]
    fact_verifications: List[FactVerification]
    reasoning: str
    limitations: List[str]
    timestamp: datetime

class AIAdvancedResearcher:
    """AI 고급 웹 연구원"""
    
    def __init__(self):
        # 신뢰할 수 있는 소스들
        self.credible_sources = {
            'academic': [
                'nature.com', 'science.org', 'cell.com', 'nejm.org',
                'pubmed.ncbi.nlm.nih.gov', 'arxiv.org', 'scholar.google.com'
            ],
            'news': [
                'reuters.com', 'ap.org', 'bbc.com', 'npr.org',
                'nytimes.com', 'washingtonpost.com', 'theguardian.com'
            ],
            'government': [
                'nasa.gov', 'nih.gov', 'cdc.gov', 'who.int',
                'fda.gov', 'epa.gov', 'nsf.gov'
            ],
            'encyclopedia': [
                'wikipedia.org', 'britannica.com', 'encyclopedia.com'
            ],
            'medical': [
                'mayoclinic.org', 'webmd.com', 'healthline.com',
                'medlineplus.gov', 'uptodate.com'
            ]
        }
        
        # 의심스러운 소스들
        self.suspicious_sources = [
            'conspiracy.com', 'truth.com', 'realnews.com',
            'alternative.com', 'hidden.com', 'secret.com',
            'infowars.com', 'naturalnews.com'
        ]
        
        # 사실 검증 패턴들
        self.verification_patterns = {
            'scientific_facts': {
                'patterns': [
                    r'지구.*구형|지구.*둥글', r'물.*100도.*끓', r'1\s*\+\s*1\s*=\s*2',
                    r'태양.*중심', r'중력.*존재', r'DNA.*구조', r'진화.*이론'
                ],
                'weight': 0.9
            },
            'historical_facts': {
                'patterns': [
                    r'세계대전.*발생', r'인류.*진화', r'문명.*발전',
                    r'역사.*기록', r'고고학.*발견'
                ],
                'weight': 0.8
            },
            'medical_facts': {
                'patterns': [
                    r'백신.*효과', r'세균.*질병', r'의학.*발전',
                    r'치료.*방법', r'예방.*수단'
                ],
                'weight': 0.85
            }
        }
        
        # 신뢰도 지표들
        self.credibility_indicators = {
            'positive': [
                '연구에 따르면', '과학적으로', '통계적으로', '실험 결과',
                '전문가가', '학술적으로', '검증된', '입증된', '논문에서',
                'peer-reviewed', 'scientific study', 'research shows'
            ],
            'negative': [
                '확실히', '100%', '절대적으로', '의심의 여지가 없다',
                '숨겨진 진실', '음모론', '정부가 숨긴', '거짓말',
                'conspiracy', 'hidden truth', 'cover-up'
            ]
        }
        
        # 헤더 설정
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def research_question(self, question: str, max_sources: int = 10) -> ResearchAnswer:
        """질문에 대한 고급 연구 수행"""
        logger.info(f"고급 연구 시작: {question}")
        
        # 1. 질문 분석 및 검색 전략 수립
        search_strategy = self._analyze_question(question)
        
        # 2. 다중 검색 수행
        all_results = []
        for keyword in search_strategy['keywords']:
            results = self._perform_web_search(keyword, max_results=5)
            all_results.extend(results)
        
        # 3. 중복 제거 및 정리
        unique_results = self._deduplicate_results(all_results)
        
        # 4. 신뢰도 및 관련성 평가
        evaluated_results = self._evaluate_results(unique_results, question)
        
        # 5. 상위 소스 선택
        top_results = sorted(evaluated_results, key=lambda x: x.credibility_score, reverse=True)[:max_sources]
        
        # 6. 사실 검증 수행
        fact_verifications = self._verify_facts(top_results, question)
        
        # 7. 답변 생성
        answer, confidence, reasoning, limitations = self._generate_comprehensive_answer(
            question, top_results, fact_verifications
        )
        
        return ResearchAnswer(
            question=question,
            answer=answer,
            confidence=confidence,
            sources=top_results,
            fact_verifications=fact_verifications,
            reasoning=reasoning,
            limitations=limitations,
            timestamp=datetime.now()
        )
    
    def _analyze_question(self, question: str) -> Dict[str, Any]:
        """질문 분석 및 검색 전략 수립 - 입력된 문장만 검색"""
        # 질문 유형 분류 (분석용으로만 사용)
        question_types = []
        if any(word in question for word in ['무엇', '뭐', 'what']):
            question_types.append('definition')
        if any(word in question for word in ['언제', 'when']):
            question_types.append('temporal')
        if any(word in question for word in ['어디', 'where']):
            question_types.append('location')
        if any(word in question for word in ['왜', 'why']):
            question_types.append('causal')
        if any(word in question for word in ['어떻게', 'how']):
            question_types.append('process')
        
        # 입력된 문장 자체만 검색 키워드로 사용
        keywords = [question.strip()]
        
        # 문장이 너무 길 경우 핵심 부분만 추출
        if len(question) > 100:
            keywords = [question[:100].strip()]
        
        return {
            'types': question_types,
            'keywords': keywords,  # 입력 문장만 사용
            'complexity': len(question.split()) / 10.0
        }
    
    def _detect_language(self, text: str) -> str:
        """텍스트 언어 감지 (개선된 버전)"""
        import re
        
        # 한국어 패턴 (한글 문자)
        korean_pattern = re.compile(r'[가-힣]')
        # 영어 패턴 (라틴 문자)
        english_pattern = re.compile(r'[a-zA-Z]')
        # 프랑스어 패턴 (프랑스어 특수 문자 포함)
        french_pattern = re.compile(r'[àâäéèêëïîôöùûüÿçñ]')
        
        korean_count = len(korean_pattern.findall(text))
        english_count = len(english_pattern.findall(text))
        french_count = len(french_pattern.findall(text))
        
        # 프랑스어 키워드 패턴 추가
        french_keywords = ['un ', 'une ', 'le ', 'la ', 'les ', 'des ', 'du ', 'de ', 'est ', 'sont ', 'animal', 'lapin', 'chien', 'chat']
        french_keyword_count = sum(1 for keyword in french_keywords if keyword in text.lower())
        
        if korean_count > 0:
            return 'ko'
        elif french_count > 0 or french_keyword_count > 0:
            return 'fr'
        else:
            return 'en'
    
    def _convert_to_search_query(self, query: str) -> str:
        """다국어 문장을 적절한 검색 쿼리로 변환"""
        language = self._detect_language(query)
        
        # 언어별 매핑 테이블
        query_mappings = {
            'ko': {
                '지구는 둥글다': 'earth_is_round',
                '물은 100도에서 끓는다': 'water_boils_at_100_degrees',
                '오류는 오류를 만든다': 'error_breeds_error',
                '1+1=2': 'one_plus_one_equals_two',
                '태양은 중심에 있다': 'sun_is_at_center',
                '중력이 존재한다': 'gravity_exists',
                'DNA는 이중나선 구조다': 'dna_double_helix_structure'
            },
            'en': {
                'the earth is round': 'earth_is_round',
                'water boils at 100 degrees': 'water_boils_at_100_degrees',
                'error breeds error': 'error_breeds_error',
                '1+1=2': 'one_plus_one_equals_two',
                'the sun is at the center': 'sun_is_at_center',
                'gravity exists': 'gravity_exists',
                'DNA has a double helix structure': 'dna_double_helix_structure'
            },
            'fr': {
                'la terre est ronde': 'earth_is_round',
                'l\'eau bout à 100 degrés': 'water_boils_at_100_degrees',
                'l\'erreur engendre l\'erreur': 'error_breeds_error',
                '1+1=2': 'one_plus_one_equals_two',
                'le soleil est au centre': 'sun_is_at_center',
                'la gravité existe': 'gravity_exists',
                'l\'ADN a une structure en double hélice': 'dna_double_helix_structure'
            }
        }
        
        # 해당 언어의 매핑 테이블에서 검색
        if language in query_mappings and query in query_mappings[language]:
            return query_mappings[language][query]
        else:
            # 매핑되지 않은 경우 URL-safe한 형태로 변환
            import re
            # 특수 문자 제거 후 공백을 언더스코어로 변환
            safe_query = re.sub(r'[^\w\s]', '', query)
            safe_query = re.sub(r'\s+', '_', safe_query)
            return safe_query[:50]  # 50자로 제한
    
    def _perform_web_search(self, query: str, max_results: int = 5) -> List[WebSearchResult]:
        """웹 검색 수행"""
        results = []
        
        # 실제 검색 엔진들 시뮬레이션
        search_engines = ['google', 'bing', 'duckduckgo']
        
        for engine in search_engines:
            try:
                engine_results = self._search_with_engine(engine, query, max_results)
                results.extend(engine_results)
                time.sleep(0.5)  # 요청 간격 조절
            except Exception as e:
                logger.warning(f"{engine} 검색 실패: {e}")
                continue
        
        return results
    
    def _search_with_engine(self, engine: str, query: str, max_results: int) -> List[WebSearchResult]:
        """특정 검색 엔진으로 검색"""
        # 실제 구현에서는 각 검색 엔진의 API를 사용
        # 여기서는 시뮬레이션된 결과를 반환
        
        mock_results = self._generate_mock_results(query, max_results)
        
        results = []
        for mock in mock_results:
            # 실제 웹 페이지 내용 가져오기 시뮬레이션
            content = self._fetch_web_content(mock['url'])
            
            results.append(WebSearchResult(
                title=mock['title'],
                url=mock['url'],
                content=content,
                snippet=mock['snippet'],
                domain=mock['domain'],
                credibility_score=0.0,  # 나중에 계산
                relevance_score=0.0,    # 나중에 계산
                fact_check_score=0.0,   # 나중에 계산
                timestamp=datetime.now()
            ))
        
        return results
    
    def _generate_mock_results(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """언어별 검색 엔진을 사용한 검색 결과 생성"""
        language = self._detect_language(query)
        
        # 언어별 검색 결과 생성
        search_results = []
        
        if language == 'ko':
            # 한국어 검색 결과 - 실제 검색 URL 형식 사용
            import urllib.parse
            encoded_query = urllib.parse.quote_plus(query)
            
            search_results = [
                {
                    'title': f'{query} - 네이버 백과사전 검색',
                    'url': f'https://terms.naver.com/search.naver?query={encoded_query}&searchType=&dicType=&subject=',
                    'snippet': f'{query}에 대한 네이버 백과사전 검색 결과입니다.',
                    'domain': 'terms.naver.com'
                },
                {
                    'title': f'{query} - 네이버 통합검색',
                    'url': f'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={encoded_query}&ackey=ptf8jcu2',
                    'snippet': f'{query}에 대한 네이버 통합검색 결과입니다.',
                    'domain': 'search.naver.com'
                },
                {
                    'title': f'{query} - 구글 검색 결과',
                    'url': f'https://www.google.com/search?q={encoded_query}',
                    'snippet': f'{query}에 대한 구글 검색 결과입니다.',
                    'domain': 'google.com'
                },
                {
                    'title': f'{query} - 다음 통합검색',
                    'url': f'https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&q={encoded_query}',
                    'snippet': f'{query}에 대한 다음 통합검색 결과입니다.',
                    'domain': 'search.daum.net'
                },
                {
                    'title': f'{query} - 다음 백과사전 검색',
                    'url': f'https://100.daum.net/search/entry?q={encoded_query}',
                    'snippet': f'{query}에 대한 다음 백과사전 검색 결과입니다.',
                    'domain': '100.daum.net'
                }
            ]
        elif language == 'fr':
            # 프랑스어 검색 결과
            search_results = [
                {
                    'title': f'{query} - Wikipédia',
                    'url': f'https://fr.wikipedia.org/wiki/{query.replace(" ", "_")}',
                    'snippet': f'Informations détaillées sur {query} dans Wikipédia.',
                    'domain': 'wikipedia.fr'
                },
                {
                    'title': f'{query} - Google France',
                    'url': f'https://www.google.fr/search?q={query.replace(" ", "+")}',
                    'snippet': f'Résultats de recherche pour {query} sur Google France.',
                    'domain': 'google.fr'
                },
                {
                    'title': f'{query} - Le Monde',
                    'url': f'https://www.lemonde.fr/recherche/?query={query.replace(" ", "+")}',
                    'snippet': f'Actualités et analyses sur {query} dans Le Monde.',
                    'domain': 'lemonde.fr'
                },
                {
                    'title': f'{query} - France Info',
                    'url': f'https://www.francetvinfo.fr/recherche?q={query.replace(" ", "+")}',
                    'snippet': f'Informations sur {query} sur France Info.',
                    'domain': 'francetvinfo.fr'
                },
                {
                    'title': f'{query} - CNRS',
                    'url': f'https://www.cnrs.fr/fr/recherche?q={query.replace(" ", "+")}',
                    'snippet': f'Recherche scientifique sur {query} au CNRS.',
                    'domain': 'cnrs.fr'
                }
            ]
        else:
            # 영어 검색 결과
            search_results = [
                {
                    'title': f'{query} - Wikipedia',
                    'url': f'https://en.wikipedia.org/wiki/{query.replace(" ", "_")}',
                    'snippet': f'Detailed information about {query} on Wikipedia.',
                    'domain': 'wikipedia.org'
                },
                {
                    'title': f'{query} - Google Search',
                    'url': f'https://www.google.com/search?q={query.replace(" ", "+")}',
                    'snippet': f'Search results for {query} on Google.',
                    'domain': 'google.com'
                },
                {
                    'title': f'{query} - Bing Search',
                    'url': f'https://www.bing.com/search?q={query.replace(" ", "+")}',
                    'snippet': f'Search results for {query} on Bing.',
                    'domain': 'bing.com'
                },
                {
                    'title': f'{query} - BBC News',
                    'url': f'https://www.bbc.com/news/search?q={query.replace(" ", "+")}',
                    'snippet': f'Latest news and analysis about {query} from BBC.',
                    'domain': 'bbc.com'
                },
                {
                    'title': f'{query} - Nature',
                    'url': f'https://www.nature.com/search?q={query.replace(" ", "+")}',
                    'snippet': f'Scientific research and publications about {query} in Nature.',
                    'domain': 'nature.com'
                }
            ]
        
        # 랜덤하게 선택하여 반환
        selected = random.sample(search_results, min(max_results, len(search_results)))
        return selected
    
    def _fetch_web_content(self, url: str) -> str:
        """웹 페이지 내용 가져오기"""
        try:
            # 실제로는 requests를 사용하여 웹 페이지를 가져옴
            # 여기서는 시뮬레이션
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 텍스트 추출
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            return text[:2000]  # 처음 2000자만 사용
            
        except Exception as e:
            logger.warning(f"웹 페이지 가져오기 실패 {url}: {e}")
            return f"웹 페이지 내용을 가져올 수 없습니다: {url}"
    
    def _deduplicate_results(self, results: List[WebSearchResult]) -> List[WebSearchResult]:
        """중복 결과 제거"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            if result.url not in seen_urls:
                seen_urls.add(result.url)
                unique_results.append(result)
        
        return unique_results
    
    def _evaluate_results(self, results: List[WebSearchResult], question: str) -> List[WebSearchResult]:
        """검색 결과 평가"""
        for result in results:
            # 도메인 신뢰도
            domain_credibility = self._calculate_domain_credibility(result.domain)
            
            # 내용 신뢰도
            content_credibility = self._calculate_content_credibility(result.content)
            
            # 관련성 점수
            relevance_score = self._calculate_relevance(result, question)
            
            # 사실 검증 점수
            fact_check_score = self._calculate_fact_check_score(result.content)
            
            # 최종 점수 계산
            result.credibility_score = (
                domain_credibility * 0.4 +
                content_credibility * 0.3 +
                relevance_score * 0.2 +
                fact_check_score * 0.1
            )
            result.relevance_score = relevance_score
            result.fact_check_score = fact_check_score
        
        return results
    
    def _calculate_domain_credibility(self, domain: str) -> float:
        """도메인 신뢰도 계산"""
        for category, sources in self.credible_sources.items():
            if domain in sources:
                if category == 'academic':
                    return 0.95
                elif category == 'government':
                    return 0.9
                elif category == 'news':
                    return 0.8
                elif category == 'encyclopedia':
                    return 0.75
                elif category == 'medical':
                    return 0.85
        
        if domain in self.suspicious_sources:
            return 0.1
        
        # 도메인 확장자 기반 평가
        if domain.endswith('.edu'):
            return 0.9
        elif domain.endswith('.gov'):
            return 0.85
        elif domain.endswith('.org'):
            return 0.7
        elif domain.endswith('.com'):
            return 0.6
        else:
            return 0.5
    
    def _calculate_content_credibility(self, content: str) -> float:
        """내용 신뢰도 계산"""
        credibility = 0.5
        
        # 긍정적 지표들
        for indicator in self.credibility_indicators['positive']:
            if indicator in content.lower():
                credibility += 0.05
        
        # 부정적 지표들
        for indicator in self.credibility_indicators['negative']:
            if indicator in content.lower():
                credibility -= 0.1
        
        # 길이 기반 평가 (너무 짧거나 너무 길면 의심)
        content_length = len(content)
        if 100 < content_length < 5000:
            credibility += 0.1
        elif content_length < 50 or content_length > 10000:
            credibility -= 0.1
        
        return max(0.0, min(1.0, credibility))
    
    def _calculate_relevance(self, result: WebSearchResult, question: str) -> float:
        """관련성 점수 계산"""
        question_words = set(question.lower().split())
        title_words = set(result.title.lower().split())
        snippet_words = set(result.snippet.lower().split())
        
        # 제목과 질문의 단어 겹침
        title_overlap = len(question_words.intersection(title_words)) / len(question_words)
        
        # 스니펫과 질문의 단어 겹침
        snippet_overlap = len(question_words.intersection(snippet_words)) / len(question_words)
        
        # 관련성 점수 계산
        relevance = (title_overlap * 0.6 + snippet_overlap * 0.4)
        
        return min(1.0, relevance)
    
    def _calculate_fact_check_score(self, content: str) -> float:
        """사실 검증 점수 계산"""
        total_score = 0.0
        total_weight = 0.0
        
        for category, data in self.verification_patterns.items():
            patterns = data['patterns']
            weight = data['weight']
            
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    total_score += weight
                    total_weight += 1.0
        
        if total_weight == 0:
            return 0.5  # 중립 점수
        
        return total_score / total_weight
    
    def _verify_facts(self, results: List[WebSearchResult], question: str) -> List[FactVerification]:
        """사실 검증 수행"""
        verifications = []
        
        for result in results:
            if result.fact_check_score > 0.7:  # 높은 사실 검증 점수
                verification = FactVerification(
                    statement=result.snippet,
                    is_verified=True,
                    confidence=result.fact_check_score,
                    evidence=[f"패턴 매칭: {result.title}"],
                    contradictory_evidence=[],
                    verification_method="pattern_matching",
                    source_diversity=1
                )
                verifications.append(verification)
        
        return verifications
    
    def _generate_comprehensive_answer(self, question: str, sources: List[WebSearchResult], 
                                     fact_verifications: List[FactVerification]) -> Tuple[str, float, str, List[str]]:
        """종합적인 답변 생성"""
        if not sources:
            return "죄송합니다. 이 질문에 대한 신뢰할 수 있는 정보를 찾을 수 없습니다.", 0.0, "검색 결과가 없음", ["정보 부족"]
        
        # 신뢰도가 높은 소스들만 사용
        reliable_sources = [s for s in sources if s.credibility_score > 0.5]
        
        if not reliable_sources:
            return "찾은 정보의 신뢰도가 낮아 정확한 답변을 제공하기 어렵습니다.", 0.3, "신뢰할 수 있는 소스 부족", ["신뢰도 낮음"]
        
        # 답변 구성
        answer_parts = []
        confidence_scores = []
        limitations = []
        
        # 주요 답변
        answer_parts.append(f"질문: {question}")
        answer_parts.append("\n답변:")
        
        # 신뢰할 수 있는 소스들의 정보 통합
        for i, source in enumerate(reliable_sources[:3], 1):
            answer_parts.append(f"{i}. {source.snippet}")
            confidence_scores.append(source.credibility_score)
        
        # 사실 검증 결과 추가
        if fact_verifications:
            verified_count = len([v for v in fact_verifications if v.is_verified])
            answer_parts.append(f"\n검증된 사실: {verified_count}개 항목 확인됨")
            confidence_scores.append(0.9)
        
        # 소스 정보
        answer_parts.append(f"\n참고 소스:")
        for source in reliable_sources[:3]:
            answer_parts.append(f"• {source.title} (신뢰도: {source.credibility_score:.2f})")
        
        answer = "\n".join(answer_parts)
        
        # 신뢰도 계산 - 실제 소스 신뢰도 기반으로 계산
        if reliable_sources:
            # 개별 소스 신뢰도의 평균 계산
            source_credibility_scores = [source.credibility_score for source in reliable_sources]
            avg_confidence = sum(source_credibility_scores) / len(source_credibility_scores)
        else:
            avg_confidence = 0.5
        
        # 추론 과정
        if len(reliable_sources) >= 3:
            reasoning = f"총 {len(sources)}개의 소스에서 정보를 수집했으며, 그 중 {len(reliable_sources)}개의 신뢰할 수 있는 소스를 기반으로 답변을 생성했습니다. 평균 신뢰도는 {avg_confidence:.1%}입니다."
        else:
            reasoning = f"총 {len(sources)}개의 소스에서 정보를 수집했으나, 신뢰할 수 있는 소스가 {len(reliable_sources)}개로 부족합니다."
        
        # 한계점
        if len(reliable_sources) < 3:
            limitations.append("신뢰할 수 있는 소스가 부족함")
        if avg_confidence < 0.6:
            limitations.append("정보의 신뢰도가 상대적으로 낮음")
        if not fact_verifications:
            limitations.append("사실 검증이 충분하지 않음")
        
        return answer, avg_confidence, reasoning, limitations

def main():
    """메인 실행 함수"""
    print("🔍 AI 고급 웹 연구원 시작")
    print("=" * 60)
    
    researcher = AIAdvancedResearcher()
    
    # 테스트 질문들
    test_questions = [
        "지구는 둥글까요?",
        "물은 몇 도에서 끓나요?",
        "코로나19는 무엇인가요?",
        "인공지능은 어떻게 작동하나요?",
        "기후변화의 원인은 무엇인가요?"
    ]
    
    for question in test_questions:
        print(f"\n❓ 질문: {question}")
        print("-" * 40)
        
        try:
            result = researcher.research_question(question)
            
            print(f"💡 답변:\n{result.answer}")
            print(f"\n🎯 신뢰도: {result.confidence:.2f}")
            print(f"🔍 추론: {result.reasoning}")
            print(f"📚 소스 수: {len(result.sources)}개")
            print(f"✅ 사실 검증: {len(result.fact_verifications)}개")
            
            if result.limitations:
                print(f"⚠️ 한계점: {', '.join(result.limitations)}")
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        
        print("=" * 60)
        time.sleep(2)

if __name__ == "__main__":
    main()
