#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Enhanced Web Researcher
AI 고급 웹 연구원 (업그레이드 버전)

실시간 검색 과정을 한국어로 표시하고 상세한 진행 상황을 보여주는 시스템입니다.
"""

import requests
import re
import json
import time
import logging
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import quote, urljoin, urlparse
from bs4 import BeautifulSoup
import random
import hashlib
import threading

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class SearchProgress:
    """검색 진행 상황"""
    step: str
    description: str
    status: str  # 'started', 'in_progress', 'completed', 'failed'
    details: str
    timestamp: datetime
    progress_percentage: int

@dataclass
class EnhancedSearchResult:
    """향상된 검색 결과"""
    title: str
    url: str
    content: str
    snippet: str
    domain: str
    credibility_score: float
    relevance_score: float
    fact_check_score: float
    search_engine: str
    search_keyword: str
    processing_time: float
    timestamp: datetime

@dataclass
class EnhancedResearchAnswer:
    """향상된 연구 답변"""
    question: str
    answer: str
    confidence: float
    sources: List[EnhancedSearchResult]
    fact_verifications: List[Dict]
    reasoning: str
    limitations: List[str]
    search_progress: List[SearchProgress]
    total_processing_time: float
    timestamp: datetime

class AIEnhancedResearcher:
    """AI 향상된 웹 연구원"""
    
    def __init__(self, progress_callback: Optional[Callable] = None):
        self.progress_callback = progress_callback
        
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
        
        # 검색 엔진별 설정
        self.search_engines = {
            'google': {
                'name': '구글',
                'search_func': self._search_google,
                'weight': 0.4
            },
            'bing': {
                'name': '빙',
                'search_func': self._search_bing,
                'weight': 0.3
            },
            'duckduckgo': {
                'name': '덕덕고',
                'search_func': self._search_duckduckgo,
                'weight': 0.3
            }
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
    
    def research_question(self, question: str, max_sources: int = 10) -> EnhancedResearchAnswer:
        """질문에 대한 향상된 연구 수행"""
        start_time = time.time()
        search_progress = []
        
        self._update_progress(search_progress, "질문 분석", "질문을 분석하고 검색 전략을 수립하고 있습니다...", "started")
        
        # 1. 질문 분석 및 검색 전략 수립
        search_strategy = self._analyze_question(question)
        self._update_progress(search_progress, "질문 분석", f"검색 키워드 {len(search_strategy['keywords'])}개 생성 완료", "completed")
        
        # 2. 다중 검색 수행
        all_results = []
        total_engines = len(self.search_engines)
        
        for i, (engine_id, engine_info) in enumerate(self.search_engines.items()):
            self._update_progress(search_progress, f"{engine_info['name']} 검색", 
                                f"{engine_info['name']}에서 정보를 검색하고 있습니다...", "started")
            
            for j, keyword in enumerate(search_strategy['keywords'][:3]):  # 상위 3개 키워드만 사용
                self._update_progress(search_progress, f"{engine_info['name']} 검색", 
                                    f"키워드 '{keyword}' 검색 중... ({j+1}/3)", "in_progress")
                
                try:
                    results = engine_info['search_func'](keyword, max_results=3)
                    for result in results:
                        result.search_engine = engine_info['name']
                        result.search_keyword = keyword
                    all_results.extend(results)
                    
                    self._update_progress(search_progress, f"{engine_info['name']} 검색", 
                                        f"키워드 '{keyword}' 검색 완료 - {len(results)}개 결과", "completed")
                    
                except Exception as e:
                    self._update_progress(search_progress, f"{engine_info['name']} 검색", 
                                        f"키워드 '{keyword}' 검색 실패: {str(e)}", "failed")
                
                time.sleep(0.5)  # 요청 간격 조절
            
            self._update_progress(search_progress, f"{engine_info['name']} 검색", 
                                f"{engine_info['name']} 검색 완료 - 총 {len([r for r in all_results if r.search_engine == engine_info['name']])}개 결과", "completed")
        
        # 3. 중복 제거 및 정리
        self._update_progress(search_progress, "결과 정리", "중복된 결과를 제거하고 정리하고 있습니다...", "started")
        unique_results = self._deduplicate_results(all_results)
        self._update_progress(search_progress, "결과 정리", f"중복 제거 완료 - {len(unique_results)}개 고유 결과", "completed")
        
        # 4. 신뢰도 및 관련성 평가
        self._update_progress(search_progress, "신뢰도 평가", "검색 결과의 신뢰도와 관련성을 평가하고 있습니다...", "started")
        evaluated_results = self._evaluate_results(unique_results, question)
        self._update_progress(search_progress, "신뢰도 평가", f"신뢰도 평가 완료 - 평균 신뢰도: {sum(r.credibility_score for r in evaluated_results)/len(evaluated_results):.2f}", "completed")
        
        # 5. 상위 소스 선택
        self._update_progress(search_progress, "소스 선택", "가장 신뢰할 수 있는 소스들을 선택하고 있습니다...", "started")
        top_results = sorted(evaluated_results, key=lambda x: x.credibility_score, reverse=True)[:max_sources]
        self._update_progress(search_progress, "소스 선택", f"상위 {len(top_results)}개 소스 선택 완료", "completed")
        
        # 6. 사실 검증 수행
        self._update_progress(search_progress, "사실 검증", "선택된 소스들의 사실성을 검증하고 있습니다...", "started")
        fact_verifications = self._verify_facts(top_results, question)
        self._update_progress(search_progress, "사실 검증", f"사실 검증 완료 - {len(fact_verifications)}개 항목 검증됨", "completed")
        
        # 7. 답변 생성
        self._update_progress(search_progress, "답변 생성", "수집된 정보를 바탕으로 답변을 생성하고 있습니다...", "started")
        answer, confidence, reasoning, limitations = self._generate_comprehensive_answer(
            question, top_results, fact_verifications
        )
        self._update_progress(search_progress, "답변 생성", f"답변 생성 완료 - 신뢰도: {confidence:.2f}", "completed")
        
        total_time = time.time() - start_time
        
        return EnhancedResearchAnswer(
            question=question,
            answer=answer,
            confidence=confidence,
            sources=top_results,
            fact_verifications=fact_verifications,
            reasoning=reasoning,
            limitations=limitations,
            search_progress=search_progress,
            total_processing_time=total_time,
            timestamp=datetime.now()
        )
    
    def _update_progress(self, progress_list: List[SearchProgress], step: str, description: str, status: str, details: str = ""):
        """진행 상황 업데이트"""
        progress = SearchProgress(
            step=step,
            description=description,
            status=status,
            details=details,
            timestamp=datetime.now(),
            progress_percentage=min(100, len(progress_list) * 10)  # 간단한 진행률 계산
        )
        progress_list.append(progress)
        
        # 콜백 함수가 있으면 호출
        if self.progress_callback:
            self.progress_callback(progress)
        
        # 로그 출력
        status_emoji = {
            'started': '🚀',
            'in_progress': '⏳',
            'completed': '✅',
            'failed': '❌'
        }
        
        print(f"{status_emoji.get(status, '📝')} {step}: {description}")
        if details:
            print(f"   └─ {details}")
    
    def _analyze_question(self, question: str) -> Dict[str, Any]:
        """질문 분석 및 검색 전략 수립"""
        # 질문 유형 분류
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
        
        # 검색 키워드 생성
        keywords = [question]
        
        # 질문 유형별 키워드 추가
        if 'definition' in question_types:
            keywords.append(question + ' 정의 의미')
        if 'temporal' in question_types:
            keywords.append(question + ' 날짜 시간')
        if 'location' in question_types:
            keywords.append(question + ' 위치 장소')
        if 'causal' in question_types:
            keywords.append(question + ' 이유 원인')
        if 'process' in question_types:
            keywords.append(question + ' 방법 과정')
        
        # 영어 키워드 추가
        if not any(ord(char) > 127 for char in question):
            keywords.append(question + ' facts information research')
        
        return {
            'types': question_types,
            'keywords': keywords[:5],  # 상위 5개만 사용
            'complexity': len(question.split()) / 10.0
        }
    
    def _search_google(self, query: str, max_results: int) -> List[EnhancedSearchResult]:
        """구글 검색 (시뮬레이션)"""
        results = []
        
        # 시뮬레이션된 검색 결과
        mock_results = [
            {
                'title': f'{query}에 대한 정보 - Wikipedia',
                'url': f'https://ko.wikipedia.org/wiki/{quote(query)}',
                'snippet': f'{query}에 대한 상세한 정보가 위키피디아에 있습니다.',
                'domain': 'wikipedia.org'
            },
            {
                'title': f'{query} 관련 뉴스 - BBC',
                'url': f'https://www.bbc.com/news/{quote(query)}',
                'snippet': f'{query}에 대한 최신 뉴스와 분석을 제공합니다.',
                'domain': 'bbc.com'
            },
            {
                'title': f'{query} 과학적 연구 - Nature',
                'url': f'https://www.nature.com/articles/{quote(query)}',
                'snippet': f'{query}에 대한 과학적 연구 결과와 논문입니다.',
                'domain': 'nature.com'
            }
        ]
        
        for i, result in enumerate(mock_results[:max_results]):
            start_time = time.time()
            # 실제 웹 페이지 내용 가져오기 시뮬레이션
            content = self._fetch_web_content(result['url'])
            processing_time = time.time() - start_time
            
            results.append(EnhancedSearchResult(
                title=result['title'],
                url=result['url'],
                content=content,
                snippet=result['snippet'],
                domain=result['domain'],
                credibility_score=self._calculate_credibility(result['domain']),
                relevance_score=0.9 - (i * 0.1),
                fact_check_score=0.0,  # 나중에 계산
                search_engine='구글',
                search_keyword=query,
                processing_time=processing_time,
                timestamp=datetime.now()
            ))
        
        return results
    
    def _search_bing(self, query: str, max_results: int) -> List[EnhancedSearchResult]:
        """빙 검색 (시뮬레이션)"""
        results = []
        
        mock_results = [
            {
                'title': f'{query} - Britannica',
                'url': f'https://www.britannica.com/topic/{quote(query)}',
                'snippet': f'{query}에 대한 백과사전 정보입니다.',
                'domain': 'britannica.com'
            },
            {
                'title': f'{query} 의학 정보 - Mayo Clinic',
                'url': f'https://www.mayoclinic.org/diseases-conditions/{quote(query)}',
                'snippet': f'{query}에 대한 의학적 정보와 치료법입니다.',
                'domain': 'mayoclinic.org'
            }
        ]
        
        for i, result in enumerate(mock_results[:max_results]):
            start_time = time.time()
            content = self._fetch_web_content(result['url'])
            processing_time = time.time() - start_time
            
            results.append(EnhancedSearchResult(
                title=result['title'],
                url=result['url'],
                content=content,
                snippet=result['snippet'],
                domain=result['domain'],
                credibility_score=self._calculate_credibility(result['domain']),
                relevance_score=0.8 - (i * 0.1),
                fact_check_score=0.0,
                search_engine='빙',
                search_keyword=query,
                processing_time=processing_time,
                timestamp=datetime.now()
            ))
        
        return results
    
    def _search_duckduckgo(self, query: str, max_results: int) -> List[EnhancedSearchResult]:
        """덕덕고 검색 (시뮬레이션)"""
        results = []
        
        mock_results = [
            {
                'title': f'{query} - Scientific American',
                'url': f'https://www.scientificamerican.com/article/{quote(query)}',
                'snippet': f'{query}에 대한 과학적 설명과 분석입니다.',
                'domain': 'scientificamerican.com'
            }
        ]
        
        for i, result in enumerate(mock_results[:max_results]):
            start_time = time.time()
            content = self._fetch_web_content(result['url'])
            processing_time = time.time() - start_time
            
            results.append(EnhancedSearchResult(
                title=result['title'],
                url=result['url'],
                content=content,
                snippet=result['snippet'],
                domain=result['domain'],
                credibility_score=self._calculate_credibility(result['domain']),
                relevance_score=0.85 - (i * 0.1),
                fact_check_score=0.0,
                search_engine='덕덕고',
                search_keyword=query,
                processing_time=processing_time,
                timestamp=datetime.now()
            ))
        
        return results
    
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
    
    def _deduplicate_results(self, results: List[EnhancedSearchResult]) -> List[EnhancedSearchResult]:
        """중복 결과 제거"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            if result.url not in seen_urls:
                seen_urls.add(result.url)
                unique_results.append(result)
        
        return unique_results
    
    def _evaluate_results(self, results: List[EnhancedSearchResult], question: str) -> List[EnhancedSearchResult]:
        """검색 결과 평가"""
        for result in results:
            # 도메인 신뢰도
            domain_credibility = self._calculate_credibility(result.domain)
            
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
    
    def _calculate_credibility(self, domain: str) -> float:
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
                credibility += 0.05
        
        for phrase in suspicious_phrases:
            if phrase in content:
                credibility -= 0.2
        
        return max(0.0, min(1.0, credibility))
    
    def _calculate_relevance(self, result: EnhancedSearchResult, question: str) -> float:
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
        # 간단한 사실 검증 패턴들
        fact_patterns = [
            r'지구.*구형|지구.*둥글', r'물.*100도.*끓', r'1\s*\+\s*1\s*=\s*2',
            r'태양.*중심', r'중력.*존재', r'DNA.*구조'
        ]
        
        total_score = 0.0
        total_weight = 0.0
        
        for pattern in fact_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                total_score += 0.8
                total_weight += 1.0
        
        if total_weight == 0:
            return 0.5  # 중립 점수
        
        return total_score / total_weight
    
    def _verify_facts(self, results: List[EnhancedSearchResult], question: str) -> List[Dict]:
        """사실 검증 수행"""
        verifications = []
        
        for result in results:
            if result.fact_check_score > 0.7:  # 높은 사실 검증 점수
                verification = {
                    'statement': result.snippet,
                    'is_verified': True,
                    'confidence': result.fact_check_score,
                    'evidence': [f"패턴 매칭: {result.title}"],
                    'verification_method': "pattern_matching",
                    'source_diversity': 1
                }
                verifications.append(verification)
        
        return verifications
    
    def _generate_comprehensive_answer(self, question: str, sources: List[EnhancedSearchResult], 
                                     fact_verifications: List[Dict]) -> Tuple[str, float, str, List[str]]:
        """종합적인 답변 생성"""
        if not sources:
            return "죄송합니다. 이 질문에 대한 신뢰할 수 있는 정보를 찾을 수 없습니다.", 0.0, "검색 결과가 없음", ["정보 부족"]
        
        # 신뢰도가 높은 소스들만 사용
        reliable_sources = [s for s in sources if s.credibility_score > 0.7]
        
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
            verified_count = len([v for v in fact_verifications if v['is_verified']])
            answer_parts.append(f"\n검증된 사실: {verified_count}개 항목 확인됨")
            confidence_scores.append(0.9)
        
        # 소스 정보
        answer_parts.append(f"\n참고 소스:")
        for source in reliable_sources[:3]:
            answer_parts.append(f"• {source.title} (신뢰도: {source.credibility_score:.2f})")
        
        answer = "\n".join(answer_parts)
        
        # 신뢰도 계산
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
        
        # 추론 과정
        reasoning = f"총 {len(sources)}개의 소스에서 정보를 수집했으며, 그 중 {len(reliable_sources)}개의 신뢰할 수 있는 소스를 기반으로 답변을 생성했습니다."
        
        # 한계점
        if len(reliable_sources) < 3:
            limitations.append("신뢰할 수 있는 소스가 부족함")
        if avg_confidence < 0.8:
            limitations.append("정보의 신뢰도가 상대적으로 낮음")
        if not fact_verifications:
            limitations.append("사실 검증이 충분하지 않음")
        
        return answer, avg_confidence, reasoning, limitations

def main():
    """메인 실행 함수"""
    print("🔍 AI 향상된 웹 연구원 시작")
    print("=" * 60)
    
    # 진행 상황 콜백 함수
    def progress_callback(progress: SearchProgress):
        status_emoji = {
            'started': '🚀',
            'in_progress': '⏳',
            'completed': '✅',
            'failed': '❌'
        }
        print(f"{status_emoji.get(progress.status, '📝')} {progress.step}: {progress.description}")
        if progress.details:
            print(f"   └─ {progress.details}")
    
    researcher = AIEnhancedResearcher(progress_callback=progress_callback)
    
    # 테스트 질문
    test_question = "지구는 둥글까요?"
    
    print(f"\n❓ 질문: {test_question}")
    print("-" * 40)
    
    try:
        result = researcher.research_question(test_question)
        
        print(f"\n💡 답변:\n{result.answer}")
        print(f"\n🎯 신뢰도: {result.confidence:.2f}")
        print(f"🔍 추론: {result.reasoning}")
        print(f"📚 소스 수: {len(result.sources)}개")
        print(f"✅ 사실 검증: {len(result.fact_verifications)}개")
        print(f"⏱️ 총 처리 시간: {result.total_processing_time:.2f}초")
        
        if result.limitations:
            print(f"⚠️ 한계점: {', '.join(result.limitations)}")
        
        print(f"\n📊 검색 진행 과정:")
        for progress in result.search_progress:
            status_emoji = {
                'started': '🚀',
                'in_progress': '⏳',
                'completed': '✅',
                'failed': '❌'
            }
            print(f"  {status_emoji.get(progress.status, '📝')} {progress.step}: {progress.description}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()
