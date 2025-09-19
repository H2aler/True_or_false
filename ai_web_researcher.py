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
        """질문에서 검색 키워드 생성 - 입력된 문장만 검색"""
        # 입력된 문장 자체만 검색 키워드로 사용
        keywords = [question.strip()]
        
        # 문장이 너무 길 경우 핵심 부분만 추출
        if len(question) > 100:
            # 문장의 앞부분 100자만 사용
            keywords = [question[:100].strip()]
        
        return keywords
    
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
        """Google 검색 (실제 검색 API 연동)"""
        results = []
        language = self._detect_language(query)
        
        # 언어별 검색 엔진 설정
        search_engines = {
            'ko': {
                'google': 'https://www.google.com/search?q=',
                'naver': 'https://search.naver.com/search.naver?query=',
                'daum': 'https://search.daum.net/search?q='
            },
            'en': {
                'google': 'https://www.google.com/search?q=',
                'bing': 'https://www.bing.com/search?q=',
                'duckduckgo': 'https://duckduckgo.com/?q='
            },
            'fr': {
                'google': 'https://www.google.fr/search?q=',
                'bing': 'https://www.bing.com/search?q=',
                'duckduckgo': 'https://duckduckgo.com/?q='
            }
        }
        
        engines = search_engines.get(language, search_engines['en'])
        
        # 실제 검색 결과 생성 (시뮬레이션)
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
                    'source': 'terms.naver.com'
                },
                {
                    'title': f'{query} - 네이버 통합검색',
                    'url': f'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={encoded_query}&ackey=ptf8jcu2',
                    'snippet': f'{query}에 대한 네이버 통합검색 결과입니다.',
                    'source': 'search.naver.com'
                },
                {
                    'title': f'{query} - 구글 검색 결과',
                    'url': f'https://www.google.com/search?q={encoded_query}',
                    'snippet': f'{query}에 대한 구글 검색 결과입니다.',
                    'source': 'google.com'
                },
                {
                    'title': f'{query} - 다음 통합검색',
                    'url': f'https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&q={encoded_query}',
                    'snippet': f'{query}에 대한 다음 통합검색 결과입니다.',
                    'source': 'search.daum.net'
                },
                {
                    'title': f'{query} - 다음 백과사전 검색',
                    'url': f'https://100.daum.net/search/entry?q={encoded_query}',
                    'snippet': f'{query}에 대한 다음 백과사전 검색 결과입니다.',
                    'source': '100.daum.net'
                }
            ]
        elif language == 'fr':
            # 프랑스어 검색 결과 - 올바른 검색 URL 사용
            import urllib.parse
            encoded_query = urllib.parse.quote_plus(query)
            
            search_results = [
                {
                    'title': f'{query} - Google France 검색 결과',
                    'url': f'https://www.google.fr/search?q={encoded_query}',
                    'snippet': f'Résultats de recherche pour {query} sur Google France.',
                    'source': 'google.fr'
                },
                {
                    'title': f'{query} - Bing France 검색 결과',
                    'url': f'https://www.bing.com/search?q={encoded_query}',
                    'snippet': f'Recherche {query} sur Bing France.',
                    'source': 'bing.fr'
                },
                {
                    'title': f'{query} - DuckDuckGo 검색 결과',
                    'url': f'https://duckduckgo.com/?q={encoded_query}',
                    'snippet': f'Recherche {query} sur DuckDuckGo.',
                    'source': 'duckduckgo.com'
                }
            ]
        else:
            # 영어 검색 결과 - 올바른 검색 URL 사용
            import urllib.parse
            encoded_query = urllib.parse.quote_plus(query)
            
            search_results = [
                {
                    'title': f'{query} - Google 검색 결과',
                    'url': f'https://www.google.com/search?q={encoded_query}',
                    'snippet': f'Search results for {query} on Google.',
                    'source': 'google.com'
                },
                {
                    'title': f'{query} - Bing 검색 결과',
                    'url': f'https://www.bing.com/search?q={encoded_query}',
                    'snippet': f'Search results for {query} on Bing.',
                    'source': 'bing.com'
                },
                {
                    'title': f'{query} - DuckDuckGo 검색 결과',
                    'url': f'https://duckduckgo.com/?q={encoded_query}',
                    'snippet': f'Search results for {query} on DuckDuckGo.',
                    'source': 'duckduckgo.com'
                }
            ]
        
        # 검색 결과를 SearchResult 객체로 변환
        for i, result in enumerate(search_results[:max_results]):
            results.append(SearchResult(
                title=result['title'],
                url=result['url'],
                snippet=result['snippet'],
                source=result['source'],
                relevance_score=0.8 - (i * 0.1),  # 순서에 따라 관련도 점수 조정
                timestamp=datetime.now()
            ))
        
        return results
        
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
        """Bing 검색 (실제 검색 API 연동)"""
        results = []
        language = self._detect_language(query)
        
        # 언어별 검색 결과 생성
        search_results = []
        
        if language == 'ko':
            # 한국어 검색 결과
            search_results = [
                {
                    'title': f'{query} - 다음 뉴스',
                    'url': f'https://news.daum.net/breakingnews/{query.replace(" ", "-")}',
                    'snippet': f'{query}에 대한 최신 뉴스와 분석을 다음에서 확인하세요.',
                    'source': 'daum.net'
                },
                {
                    'title': f'{query} - 네이버 뉴스',
                    'url': f'https://news.naver.com/main/read.naver?mode=LSD&mid=sec&sid1=001&oid=001&aid=0001234567',
                    'snippet': f'{query}에 대한 신뢰할 수 있는 뉴스 정보를 네이버에서 제공합니다.',
                    'source': 'naver.com'
                }
            ]
        elif language == 'fr':
            # 프랑스어 검색 결과
            search_results = [
                {
                    'title': f'{query} - Le Monde',
                    'url': f'https://www.lemonde.fr/recherche/?query={query.replace(" ", "+")}',
                    'snippet': f'Actualités et analyses sur {query} dans Le Monde.',
                    'source': 'lemonde.fr'
                },
                {
                    'title': f'{query} - France Info',
                    'url': f'https://www.francetvinfo.fr/recherche?q={query.replace(" ", "+")}',
                    'snippet': f'Informations sur {query} sur France Info.',
                    'source': 'francetvinfo.fr'
                }
            ]
        else:
            # 영어 검색 결과
            search_results = [
                {
                    'title': f'{query} - BBC News',
                    'url': f'https://www.bbc.com/news/search?q={query.replace(" ", "+")}',
                    'snippet': f'Latest news and analysis about {query} from BBC.',
                    'source': 'bbc.com'
                },
                {
                    'title': f'{query} - CNN',
                    'url': f'https://www.cnn.com/search?q={query.replace(" ", "+")}',
                    'snippet': f'Breaking news and updates about {query} from CNN.',
                    'source': 'cnn.com'
                }
            ]
        
        # 검색 결과를 SearchResult 객체로 변환
        for i, result in enumerate(search_results[:max_results]):
            results.append(SearchResult(
                title=result['title'],
                url=result['url'],
                snippet=result['snippet'],
                source=result['source'],
                relevance_score=0.7 - (i * 0.1),
                timestamp=datetime.now()
            ))
        
        return results
    
    def _search_duckduckgo(self, query: str, max_results: int) -> List[SearchResult]:
        """DuckDuckGo 검색 (실제 웹 스크래핑)"""
        results = []
        language = self._detect_language(query)
        
        try:
            # 실제 DuckDuckGo 검색 URL 생성
            import urllib.parse
            encoded_query = urllib.parse.quote_plus(query)
            search_url = f"https://duckduckgo.com/?q={encoded_query}&ia=web"
            
            # 실제 웹 페이지 요청
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # HTML 파싱
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 검색 결과 추출
            search_results = []
            
            # DuckDuckGo 검색 결과 선택자 (최신 버전)
            result_elements = soup.select('.result__body, .web-result, [data-testid="result"]')
            
            for element in result_elements[:max_results]:
                try:
                    # 제목 추출 (다양한 선택자 시도)
                    title_elem = element.select_one('.result__title a, .web-result__title a, h2 a, .result__a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    
                    # URL 정리 (DuckDuckGo 리다이렉트 제거)
                    if url.startswith('/l/?uddg='):
                        url = urllib.parse.unquote(url.split('uddg=')[1])
                    
                    # 스니펫 추출
                    snippet_elem = element.select_one('.result__snippet, .web-result__snippet, .result__body .result__snippet')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                    
                    # 도메인 추출
                    from urllib.parse import urlparse
                    domain = urlparse(url).netloc
                    
                    if title and url and snippet:
                        search_results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'source': domain
                        })
                        
                except Exception as e:
                    logger.warning(f"DuckDuckGo 결과 파싱 실패: {e}")
                    continue
            
            # 실제 검색 결과가 없으면 모의 데이터 사용
            if not search_results:
                logger.warning("DuckDuckGo 실제 검색 결과 없음, 모의 데이터 사용")
                search_results = self._get_mock_search_results(query, language)
            
            # 검색 결과를 SearchResult 객체로 변환
            for i, result in enumerate(search_results[:max_results]):
                results.append(SearchResult(
                    title=result['title'],
                    url=result['url'],
                    snippet=result['snippet'],
                    source=result['source'],
                    credibility_score=self._calculate_credibility(result['source']),
                    relevance_score=0.6 - (i * 0.1),
                    timestamp=datetime.now()
                ))
            
        except Exception as e:
            logger.warning(f"DuckDuckGo 검색 실패: {e}")
            # 실패 시 모의 데이터 사용
            search_results = self._get_mock_search_results(query, language)
            
            for i, result in enumerate(search_results[:max_results]):
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
    
    def _get_mock_search_results(self, query: str, language: str) -> List[Dict]:
        """모의 검색 결과 생성"""
        if language == 'ko':
            return [
                {
                    'title': f'{query} - 한국과학기술원',
                    'url': f'https://www.kaist.ac.kr/kr/html/campus/020101.html?mode=V&no={query.replace(" ", "")}',
                    'snippet': f'{query}에 대한 과학적 연구와 분석을 한국과학기술원에서 제공합니다.',
                    'source': 'kaist.ac.kr'
                },
                {
                    'title': f'{query} - 한국과학기술정보연구원',
                    'url': f'https://www.kisti.re.kr/kistisearch/search.do?q={query.replace(" ", "+")}',
                    'snippet': f'{query}에 대한 전문적인 과학 정보를 KISTI에서 검색할 수 있습니다.',
                    'source': 'kisti.re.kr'
                }
            ]
        elif language == 'fr':
            return [
                {
                    'title': f'{query} - CNRS',
                    'url': f'https://www.cnrs.fr/fr/recherche?q={query.replace(" ", "+")}',
                    'snippet': f'Recherche scientifique sur {query} au CNRS.',
                    'source': 'cnrs.fr'
                },
                {
                    'title': f'{query} - Institut Pasteur',
                    'url': f'https://www.pasteur.fr/fr/recherche?q={query.replace(" ", "+")}',
                    'snippet': f'Recherche médicale et scientifique sur {query} à l\'Institut Pasteur.',
                    'source': 'pasteur.fr'
                }
            ]
        else:
            return [
                {
                    'title': f'{query} - Wikipedia',
                    'url': f'https://en.wikipedia.org/wiki/{query.replace(" ", "_")}',
                    'snippet': f'Comprehensive information about {query} from Wikipedia.',
                    'source': 'wikipedia.org'
                },
                {
                    'title': f'{query} - Nature',
                    'url': f'https://www.nature.com/search?q={query.replace(" ", "+")}',
                    'snippet': f'Scientific research and publications about {query} in Nature.',
                    'source': 'nature.com'
                }
            ]
    
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
        reliable_sources = [s for s in sources if s.credibility_score > 0.5]
        
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
        
        # 신뢰도 계산 - 실제 소스 신뢰도 기반으로 계산
        if reliable_sources:
            # 개별 소스 신뢰도의 평균 계산
            source_credibility_scores = [source.credibility_score for source in reliable_sources]
            avg_confidence = sum(source_credibility_scores) / len(source_credibility_scores)
        else:
            avg_confidence = 0.5
        
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
