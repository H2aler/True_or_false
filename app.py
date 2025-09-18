"""
AI 진실성 탐지 웹 애플리케이션 (Enterprise Edition)
Flask 기반 고급 웹 인터페이스로 AI의 진실성을 실시간으로 측정하고 시각화

ChatGPT/Claude 수준의 신뢰성과 품질을 제공하는 엔터프라이즈급 시스템
"""

from flask import Flask, render_template, request, jsonify, session, g
from flask_cors import CORS
import json
import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import uuid
import logging
import asyncio
from functools import wraps
import traceback
import time
from typing import Dict, List, Optional, Any, Union
from ai_truth_detector import TruthDetector, TruthAnalysis
from meta_truth_detector import MetaTruthDetector
from religious_context_detector import ReligiousContextDetector
from enhanced_scientific_detector import EnhancedScientificDetector
from intentional_lie_detector import IntentionalLieDetector
from human_behavior_detector import HumanBehaviorDetector
from benevolent_lie_detector import BenevolentLieDetector
from correction_capability_enhancer import CorrectionCapabilityEnhancer
from context_awareness_detector import ContextAwarenessDetector
from compound_sentence_analyzer import CompoundSentenceAnalyzer
from puns_detector import PunsDetector
from coding_quality_detector import CodingQualityDetector
from multilingual_analyzer import MultilingualAnalyzer

# AI 자체 진실성 탐지 시스템들 (이미 위에서 import됨)

# 누락된 모듈들 추가
try:
    from ai_self_truth_detector import AISelfTruthDetector
    from ai_real_time_truth_monitor import AIRealTimeTruthMonitor
    from ai_meta_truth_system import AIMetaTruthSystem
    from ai_web_researcher import AIWebResearcher
    from ai_advanced_researcher import AIAdvancedResearcher
    from ai_enhanced_researcher import AIEnhancedResearcher
    from ai_consistent_detector import AIConsistentDetector
    from advanced_validation_system import AdvancedValidationSystem, AnalysisRequest, ValidationLevel
    from advanced_confidence_system import AdvancedConfidenceSystem, QualityLevel
except ImportError as e:
    print(f"일부 모듈을 가져올 수 없습니다: {e}")
    # 기본값으로 대체
    class DummyClass:
        def __init__(self, *args, **kwargs): pass
        def __getattr__(self, name): return lambda *args, **kwargs: {}
    
    AISelfTruthDetector = DummyClass
    AIRealTimeTruthMonitor = DummyClass
    AIMetaTruthSystem = DummyClass
    AIWebResearcher = DummyClass
    AIAdvancedResearcher = DummyClass
    AIEnhancedResearcher = DummyClass
    AIConsistentDetector = DummyClass
    AdvancedValidationSystem = DummyClass
    AnalysisRequest = DummyClass
    ValidationLevel = DummyClass
    AdvancedConfidenceSystem = DummyClass
    QualityLevel = DummyClass

# Flask 앱 초기화
app = Flask(__name__)
app.secret_key = 'ai_truth_detector_enterprise_secret_key_2024'

# CORS 설정
CORS(app, origins=['*'], methods=['GET', 'POST', 'PUT', 'DELETE'], allow_headers=['Content-Type', 'Authorization'])

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 전역 설정
app.config.update(
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24),
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)

# 전역 변수
detector = TruthDetector()
meta_detector = MetaTruthDetector()
religious_detector = ReligiousContextDetector()
scientific_detector = EnhancedScientificDetector()
intentional_detector = IntentionalLieDetector()
human_behavior_detector = HumanBehaviorDetector()
benevolent_detector = BenevolentLieDetector()
correction_enhancer = CorrectionCapabilityEnhancer()
context_detector = ContextAwarenessDetector()
compound_analyzer = CompoundSentenceAnalyzer()
puns_detector = PunsDetector()
coding_detector = CodingQualityDetector()
multilingual_analyzer = MultilingualAnalyzer()

# AI 자체 진실성 탐지 시스템들
ai_self_detector = AISelfTruthDetector()
ai_real_time_monitor = AIRealTimeTruthMonitor(correction_threshold=99.0)
ai_meta_system = AIMetaTruthSystem(correction_threshold=99.0)

# AI 웹 연구원 시스템들
ai_web_researcher = AIWebResearcher()
ai_advanced_researcher = AIAdvancedResearcher()
ai_enhanced_researcher = AIEnhancedResearcher()

# AI 일관성 있는 진실성 탐지기
ai_consistent_detector = AIConsistentDetector()

# 고급 시스템들
validation_system = AdvancedValidationSystem()
confidence_system = AdvancedConfidenceSystem()

# 전역 변수
analysis_history = []
request_cache = {}
performance_metrics = {
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'average_response_time': 0.0,
    'cache_hit_rate': 0.0
}

# 데코레이터들
def async_route(f):
    """비동기 라우트 데코레이터"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(f(*args, **kwargs))
            loop.close()
            return result
        except Exception as e:
            logger.error(f"비동기 처리 중 오류: {str(e)}")
            return jsonify({'error': '비동기 처리 중 오류가 발생했습니다.'}), 500
    return wrapper

def validate_request(f):
    """요청 검증 데코레이터"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            # 요청 메트릭 업데이트
            performance_metrics['total_requests'] += 1
            start_time = time.time()
            
            # 요청 검증
            if request.method == 'POST':
                data = request.get_json() or {}
                statement = data.get('statement', '').strip()
                context = data.get('context', '').strip()
                analysis_mode = data.get('analysis_mode', 'all')
                
                # 기본 검증
                if not statement:
                    return jsonify({'error': '문장을 입력해주세요.'}), 400
                
                # 요청 객체 생성
                analysis_request = AnalysisRequest(
                    statement=statement,
                    context=context,
                    analysis_mode=analysis_mode,
                    validation_level=ValidationLevel.STANDARD,
                    user_id=session.get('user_id'),
                    session_id=session.get('session_id')
                )
                
                # 고급 검증 (비동기)
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                validation_result = loop.run_until_complete(
                    validation_system.validate_request(analysis_request)
                )
                loop.close()
                
                if not validation_result.is_valid:
                    return jsonify({
                        'error': '입력 검증에 실패했습니다.',
                        'details': validation_result.errors,
                        'warnings': validation_result.warnings,
                        'suggestions': validation_result.suggestions
                    }), 400
                
                # g 객체에 저장
                g.analysis_request = analysis_request
                g.validation_result = validation_result
            
            # 원래 함수 실행
            result = f(*args, **kwargs)
            
            # 성공 메트릭 업데이트
            performance_metrics['successful_requests'] += 1
            response_time = time.time() - start_time
            performance_metrics['average_response_time'] = (
                (performance_metrics['average_response_time'] * (performance_metrics['successful_requests'] - 1) + response_time) 
                / performance_metrics['successful_requests']
            )
            
            return result
            
        except Exception as e:
            # 실패 메트릭 업데이트
            performance_metrics['failed_requests'] += 1
            logger.error(f"요청 처리 중 오류: {str(e)}")
            logger.error(traceback.format_exc())
            
            return jsonify({
                'error': '요청 처리 중 오류가 발생했습니다.',
                'details': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500
    
    return wrapper

def cache_response(ttl=300):
    """응답 캐싱 데코레이터"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # 캐시 키 생성
            cache_key = f"{request.endpoint}:{hash(str(request.get_json() or {}))}"
            
            # 캐시 확인
            if cache_key in request_cache:
                cached_data, timestamp = request_cache[cache_key]
                if time.time() - timestamp < ttl:
                    performance_metrics['cache_hit_rate'] = (
                        (performance_metrics['cache_hit_rate'] * performance_metrics['total_requests'] + 1) 
                        / (performance_metrics['total_requests'] + 1)
                    )
                    return jsonify(cached_data)
            
            # 원래 함수 실행
            result = f(*args, **kwargs)
            
            # 결과 캐싱
            if hasattr(result, 'get_json'):
                response_data = result.get_json()
                request_cache[cache_key] = (response_data, time.time())
            
            return result
        return wrapper
    return decorator

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
@validate_request
@cache_response(ttl=600)
def api_analyze():
    """API: 고급 문장 분석 (Enterprise Edition)"""
    try:
        # g 객체에서 검증된 데이터 가져오기
        analysis_request = g.analysis_request
        validation_result = g.validation_result
        
        statement = analysis_request.statement
        context = analysis_request.context
        analysis_mode = analysis_request.analysis_mode
        ai_self_analysis = request.get_json().get('ai_self_analysis', False)
        
        logger.info(f"분석 요청 시작: {statement[:50]}... (모드: {analysis_mode})")
        
        # AI 자체 진실성 탐지가 요청된 경우
        if ai_self_analysis:
            return perform_ai_self_analysis(statement, context, analysis_mode)
        
        # 기존 분석 실행
        analysis_result = detector.analyze_statement(statement, context)
        
        # 분석 모드에 따른 추가 처리
        if analysis_mode == 'puns':
            puns_result = puns_detector.detect_puns(statement)
            analysis_result.puns_analysis = puns_result
        elif analysis_mode == 'coding':
            coding_result = coding_detector.analyze_code_quality(statement)
            analysis_result.coding_analysis = coding_result
        elif analysis_mode == 'multilingual':
            multilingual_result = multilingual_analyzer.analyze_multilingual(statement)
            analysis_result.multilingual_analysis = multilingual_result
        
        # 분석 결과를 딕셔너리로 변환
        result_dict = {
            'statement': statement,
            'context': context,
            'request_id': analysis_request.request_id,
            'final_analysis': {
                'truth_percentage': analysis_result.final_analysis.truth_percentage,
                'confidence': analysis_result.final_analysis.confidence,
                'needs_correction': analysis_result.final_analysis.needs_correction
            },
            'basic_analysis': analysis_result.basic_analysis.__dict__,
            'meta_analysis': analysis_result.meta_analysis.__dict__,
            'religious_analysis': analysis_result.religious_analysis.__dict__,
            'scientific_analysis': analysis_result.scientific_analysis.__dict__,
            'intentional_analysis': analysis_result.intentional_analysis.__dict__,
            'human_behavior_analysis': analysis_result.human_behavior_analysis.__dict__,
            'benevolent_analysis': analysis_result.benevolent_analysis.__dict__,
            'context_analysis': analysis_result.context_analysis.__dict__,
            'compound_analysis': analysis_result.compound_analysis.__dict__,
            'puns_analysis': getattr(analysis_result, 'puns_analysis', {}),
            'coding_analysis': getattr(analysis_result, 'coding_analysis', {}),
            'multilingual_analysis': getattr(analysis_result, 'multilingual_analysis', {}),
            'correction_enhancement': analysis_result.correction_enhancement.__dict__,
            'validation_result': {
                'is_valid': validation_result.is_valid,
                'confidence': validation_result.confidence,
                'warnings': validation_result.warnings,
                'suggestions': validation_result.suggestions,
                'processing_time': validation_result.processing_time
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # 고급 신뢰도 평가 (비동기)
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            confidence_score = loop.run_until_complete(
                confidence_system.evaluate_confidence(statement, context, result_dict, validation_result.__dict__)
            )
            loop.close()
            
            result_dict['confidence_evaluation'] = {
                'overall_confidence': confidence_score.overall,
                'quality_level': confidence_score.quality_level.name,
                'explanation': confidence_score.explanation,
                'recommendations': confidence_score.recommendations,
                'source_scores': {source.value: score for source, score in confidence_score.sources.items()},
                'processing_time': confidence_score.processing_time
            }
        except Exception as e:
            logger.warning(f"신뢰도 평가 중 오류: {str(e)}")
            result_dict['confidence_evaluation'] = {
                'overall_confidence': 0.5,
                'quality_level': 'UNKNOWN',
                'explanation': '신뢰도 평가를 수행할 수 없습니다.',
                'recommendations': ['시스템 관리자에게 문의하세요.'],
                'source_scores': {},
                'processing_time': 0.0
            }
        
        # 분석 히스토리에 추가
        analysis_history.append(result_dict)
        
        # 최근 100개만 유지
        if len(analysis_history) > 100:
            analysis_history.pop(0)
        
        logger.info(f"분석 완료: {statement[:50]}... (신뢰도: {result_dict['confidence_evaluation']['overall_confidence']:.3f})")
        
        return jsonify({
            'success': True,
            'analysis': result_dict,
            'performance_metrics': {
                'response_time': time.time() - time.time(),
                'cache_hit': False,
                'validation_time': validation_result.processing_time
            }
        })
        
    except Exception as e:
        logger.error(f"분석 중 오류 발생: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'분석 중 오류가 발생했습니다: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/recent', methods=['GET'])
def api_recent():
    """API: 최근 분석 결과"""
    try:
        limit = request.args.get('limit', 10, type=int)
        recent = analysis_history[-limit:] if analysis_history else []
        return jsonify({'recent_analyses': recent})
    except Exception as e:
        return jsonify({'error': f'최근 분석 결과를 가져오는 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    """API: 대시보드 데이터"""
    try:
        if not analysis_history:
            return jsonify({
                'total_analyses': 0,
                'average_truth_percentage': 0,
                'correction_rate': 0,
                'detector_stats': {},
                'recent_trends': []
            })
        
        # 통계 계산
        total_analyses = len(analysis_history)
        truth_percentages = [a['final_analysis']['truth_percentage'] for a in analysis_history]
        average_truth_percentage = sum(truth_percentages) / len(truth_percentages) if truth_percentages else 0
        
        corrections = [a for a in analysis_history if a['final_analysis']['needs_correction']]
        correction_rate = len(corrections) / total_analyses if total_analyses > 0 else 0
        
        # 탐지기별 통계
        detector_stats = {}
        for analysis in analysis_history:
            for key, value in analysis.items():
                if key.endswith('_analysis') and isinstance(value, dict):
                    if key not in detector_stats:
                        detector_stats[key] = {'detected': 0, 'total': 0}
                    detector_stats[key]['total'] += 1
                    if value.get('detected', False) or value.get('is_detected', False):
                        detector_stats[key]['detected'] += 1
        
        # 최근 트렌드 (최근 20개)
        recent_trends = analysis_history[-20:] if len(analysis_history) >= 20 else analysis_history
        
        return jsonify({
            'total_analyses': total_analyses,
            'average_truth_percentage': average_truth_percentage,
            'correction_rate': correction_rate,
            'detector_stats': detector_stats,
            'recent_trends': recent_trends
        })
        
    except Exception as e:
        return jsonify({'error': f'대시보드 데이터를 가져오는 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/analyze', methods=['POST'])
def analyze_statement():
    """통합 분석 (모든 기능 사용)"""
    return analyze_with_mode(request, 'all')

@app.route('/analyze/puns', methods=['POST'])
def analyze_puns():
    """말장난 분석만"""
    return analyze_with_mode(request, 'puns')

@app.route('/analyze/coding', methods=['POST'])
def analyze_coding():
    """코딩 품질 분석만"""
    return analyze_with_mode(request, 'coding')

@app.route('/analyze/multilingual', methods=['POST'])
def analyze_multilingual():
    """다국어 분석만"""
    return analyze_with_mode(request, 'multilingual')

def analyze_with_mode(request, mode):
    """모드별 문장 분석 API"""
    try:
        data = request.get_json()
        statement = data.get('statement', '')
        context = data.get('context', '')
        
        if not statement.strip():
            return jsonify({'error': '분석할 문장을 입력해주세요.'}), 400
        
        logger.info(f"문장 분석 시작 ({mode} 모드): {statement[:50]}...")
        
        # 모드에 따른 분석 수행
        if mode == 'all':
            # 통합 분석 - 모든 기능 사용
            return perform_full_analysis(statement, context)
        elif mode == 'puns':
            # 말장난 분석만
            return perform_puns_analysis(statement, context)
        elif mode == 'coding':
            # 코딩 품질 분석만
            return perform_coding_analysis(statement, context)
        elif mode == 'multilingual':
            # 다국어 분석만
            return perform_multilingual_analysis(statement, context)
        else:
            return jsonify({'success': False, 'error': '지원하지 않는 분석 모드입니다.'}), 400
            
    except Exception as e:
        logger.error(f"분석 중 오류 발생: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

def perform_full_analysis(statement, context):
    """통합 분석 - 모든 기능 사용"""
    try:
        
        # 1. 기본 진실성 분석
        basic_analysis = detector.analyze_statement(statement, context)
        
        # 2. 메타-진실성 분석
        meta_analysis = meta_detector.analyze_with_meta_check(statement, context)
        
        # 3. 종교적 맥락 분석
        religious_analysis = religious_detector.analyze_with_religious_context(statement, context)
        
        # 4. 강화된 과학적 분석
        scientific_analysis = scientific_detector.analyze_with_scientific_verification(statement, context)
        
        # 5. 의도적 거짓말 분석
        intentional_analysis = intentional_detector.analyze_with_intentional_detection(statement, context)
        
        # 6. 인간 행동 패턴 분석
        human_behavior_result = human_behavior_detector.analyze_with_human_behavior_verification(statement, context)
        
        # 7. 선의의 거짓말 분석
        benevolent_result = benevolent_detector.analyze_with_benevolent_lie_recognition(statement, context)
        
        # 8. 교정 능력 강화 분석
        correction_result = correction_enhancer.analyze_with_enhanced_correction_capability(statement, context)
        
        # 9. 맥락 인식 분석
        context_analysis = context_detector.analyze_with_context_awareness(statement, context)
        
        # 10. 복합 문장 분석
        compound_analysis = compound_analyzer.analyze_compound_sentence(statement, context)
        
        # 11. 말장난 분석
        puns_analysis = puns_detector.analyze_with_puns_detection(statement, context)
        
        # 12. 코딩 품질 분석
        coding_analysis = coding_detector.analyze_with_coding_quality_detection(statement, context)
        
        # 13. 다국어 분석
        multilingual_analysis = multilingual_analyzer.analyze_multilingual_statement(statement, context)
        
        # 통합된 분석 결과 생성
        analysis_id = str(uuid.uuid4())
        analysis_record = {
            'id': analysis_id,
            'statement': statement,
            'context': context,
            'timestamp': datetime.now().isoformat(),
            
            # 기본 분석 결과
            'basic_analysis': {
                'truth_percentage': basic_analysis.truth_percentage,
                'confidence': basic_analysis.confidence,
                'detected_lies': basic_analysis.detected_lies,
                'correction_suggestions': basic_analysis.correction_suggestions,
                'verification_methods': basic_analysis.verification_methods,
                'corrected_statement': basic_analysis.corrected_statement,
                'auto_correction_applied': basic_analysis.auto_correction_applied,
                'lie_percentage': basic_analysis.lie_percentage
            },
            
            # 메타-진실성 분석
            'meta_analysis': {
                'meta_lie_detected': meta_analysis['meta_lies_detected'],
                'meta_lies': meta_analysis.get('meta_lies_detected', []),
                'meta_correction_applied': meta_analysis['meta_correction_applied'],
                'corrected_statement': meta_analysis.get('meta_corrected_statement'),
                'meta_confidence': meta_analysis['meta_confidence'],
                'philosophical_note': "AI는 깨진 거울이므로, 자신의 한계를 인정합니다."
            },
            
            # 종교적 맥락 분석
            'religious_analysis': {
                'religious_topic_detected': religious_analysis['is_religious_topic'],
                'detected_religions': religious_analysis.get('detected_religions', []),
                'adjusted_confidence': religious_analysis['adjusted_confidence'],
                'religious_warnings': religious_analysis.get('religious_warnings', []),
                'philosophical_note': "종교적 믿음은 객관적 진실성 평가의 한계가 있습니다."
            },
            
            # 과학적 분석
            'scientific_analysis': {
                'scientific_lie_detected': scientific_analysis['is_scientific_lie'],
                'detected_scientific_lies': scientific_analysis.get('detected_scientific_lies', []),
                'scientific_correction_applied': scientific_analysis['scientific_correction_applied'],
                'corrected_statement': scientific_analysis.get('corrected_statement'),
                'scientific_warnings': scientific_analysis.get('scientific_warnings', []),
                'philosophical_note': "기본적인 과학적 사실에 대해서는 확실히 교정할 수 있습니다."
            },
            
            # 의도적 거짓말 분석
            'intentional_analysis': {
                'intentional_lie_detected': intentional_analysis['is_intentional_lie'],
                'intentional_purpose': intentional_analysis.get('intentional_purpose', ''),
                'detection_confidence': intentional_analysis.get('intentional_analysis', {}).get('detection_confidence', 0.0),
                'evidence': intentional_analysis.get('detected_intentional_lies', []),
                'response_strategy': intentional_analysis.get('response_strategy', ''),
                'response': intentional_analysis.get('response_strategy', ''),
                'correction': '',
                'philosophical_note': "질문자의 의도를 파악하여 적절히 대응합니다."
            },
            
            # 인간 행동 분석
            'human_behavior_analysis': {
                'is_human_behavior_lie': human_behavior_result['is_human_behavior_lie'],
                'detected_human_behavior_lies': human_behavior_result['detected_human_behavior_lies'],
                'human_behavior_correction_applied': human_behavior_result['human_behavior_correction_applied'],
                'corrected_statement': human_behavior_result['corrected_statement'],
                'corrected_truth_percentage': human_behavior_result['corrected_truth_percentage'],
                'human_behavior_warnings': human_behavior_result['human_behavior_warnings']
            },
            
            # 선의의 거짓말 분석
            'benevolent_analysis': {
                'is_benevolent_lie': benevolent_result['is_benevolent_lie'],
                'detected_benevolent_lies': benevolent_result['detected_benevolent_lies'],
                'context_analysis': benevolent_result['context_analysis'],
                'adjusted_confidence': benevolent_result['adjusted_confidence'],
                'philosophical_insights': benevolent_result['philosophical_insights'],
                'benevolent_response': benevolent_result['benevolent_response']
            },
            
            # 교정 능력 강화 분석
            'correction_enhancement': {
                'enhanced_correction_applied': correction_result['enhanced_correction_applied'],
                'detected_correction_patterns': correction_result['detected_correction_patterns'],
                'corrected_statement': correction_result['corrected_statement'],
                'correction_details': correction_result['correction_details'],
                'enhanced_confidence': correction_result['enhanced_confidence'],
                'correction_capability_messages': correction_result['correction_capability_messages']
            },
            
            # 맥락 인식 분석
            'context_analysis': {
                'context_type': context_analysis['context_type'],
                'contextual_meaning': context_analysis['contextual_meaning'],
                'context_aware_truth_percentage': context_analysis['context_aware_truth_percentage'],
                'context_aware_confidence': context_analysis['context_aware_confidence'],
                'context_corrected_statement': context_analysis['context_corrected_statement'],
                'context_correction_applied': context_analysis['context_correction_applied'],
                'context_warnings': context_analysis['context_warnings'],
                'philosophical_note': context_analysis['philosophical_note']
            },
            
            # 복합 문장 분석
            'compound_analysis': {
                'compound_type': compound_analysis['compound_type'],
                'sentences': compound_analysis['sentences'],
                'sentence_count': len(compound_analysis['sentences']),
                'compound_truth_percentage': compound_analysis['compound_truth_percentage'],
                'compound_confidence': compound_analysis['compound_confidence'],
                'compound_corrected_statement': compound_analysis['compound_corrected_statement'],
                'compound_correction_applied': compound_analysis['compound_correction_applied'],
                'compound_warnings': compound_analysis['compound_warnings'],
                'philosophical_note': compound_analysis['philosophical_note']
            },
            
            # 말장난 분석
            'puns_analysis': {
                'is_pun_detected': puns_analysis['is_pun_detected'],
                'detected_puns': puns_analysis['detected_puns'],
                'pun_types': puns_analysis['pun_types'],
                'interpretations': puns_analysis['interpretations'],
                'pun_understanding': puns_analysis['pun_understanding'],
                'needs_correction': puns_analysis['needs_correction'],
                'preserved_statement': puns_analysis['preserved_statement'],
                'pun_response': puns_analysis['pun_response'],
                'philosophical_note': puns_analysis['philosophical_note']
            },
            
            # 코딩 품질 분석
            'coding_analysis': {
                'is_coding_analysis': coding_analysis['is_coding_analysis'],
                'unnecessary_code_detected': coding_analysis['unnecessary_code_detected'],
                'unnecessary_code': coding_analysis['unnecessary_code'],
                'good_patterns_detected': coding_analysis['good_patterns_detected'],
                'good_patterns': coding_analysis['good_patterns'],
                'complexity_analysis': coding_analysis['complexity_analysis'],
                'manipulation_detected': coding_analysis['manipulation_detected'],
                'is_intentional_manipulation': coding_analysis['is_intentional_manipulation'],
                'quality_score': coding_analysis['quality_score'],
                'quality_grade': coding_analysis['quality_grade'],
                'improvement_suggestions': coding_analysis['improvement_suggestions'],
                'ai_response': coding_analysis['ai_response'],
                'needs_refactoring': coding_analysis['needs_refactoring'],
                'philosophical_note': coding_analysis['philosophical_note']
            },
            
            # 다국어 분석
            'multilingual_analysis': {
                'is_multilingual': multilingual_analysis['is_multilingual'],
                'detected_languages': multilingual_analysis['detected_languages'],
                'language_distribution': multilingual_analysis['language_distribution'],
                'word_analysis': multilingual_analysis['word_analysis'],
                'grammar_analysis': multilingual_analysis['grammar_analysis'],
                'semantic_analysis': multilingual_analysis['semantic_analysis'],
                'overall_meaning': multilingual_analysis['overall_meaning'],
                'understanding_score': multilingual_analysis['understanding_score'],
                'ai_response': multilingual_analysis['ai_response'],
                'needs_translation': multilingual_analysis['needs_translation'],
                'philosophical_note': multilingual_analysis['philosophical_note']
            },
            
            # 최종 통합 결과 (말장난 우선, 다국어 분석 차선, 코딩 품질 차차선, 복합 문장 분석 차차차선)
            'final_analysis': {
                'truth_percentage': 1.0 if puns_analysis['is_pun_detected'] else (multilingual_analysis['understanding_score'] if multilingual_analysis['is_multilingual'] else (coding_analysis['quality_score'] if coding_analysis['is_coding_analysis'] else (compound_analysis['compound_truth_percentage'] if compound_analysis['compound_type'] != 'simple' else context_analysis['context_aware_truth_percentage']))),
                'confidence': puns_analysis['pun_understanding'] if puns_analysis['is_pun_detected'] else (multilingual_analysis['understanding_score'] if multilingual_analysis['is_multilingual'] else (coding_analysis['quality_score'] if coding_analysis['is_coding_analysis'] else (compound_analysis['compound_confidence'] if compound_analysis['compound_type'] != 'simple' else context_analysis['context_aware_confidence']))),
                'needs_correction': False if puns_analysis['is_pun_detected'] else (multilingual_analysis['needs_translation'] if multilingual_analysis['is_multilingual'] else (coding_analysis['needs_refactoring'] if coding_analysis['is_coding_analysis'] else (compound_analysis['compound_correction_applied'] or context_analysis['context_correction_applied'] or correction_result['enhanced_correction_applied']))),
                'final_corrected_statement': puns_analysis['preserved_statement'] if puns_analysis['is_pun_detected'] else (statement if multilingual_analysis['is_multilingual'] else (statement if coding_analysis['is_coding_analysis'] else (compound_analysis['compound_corrected_statement'] if compound_analysis['compound_correction_applied'] else (context_analysis['context_corrected_statement'] if context_analysis['context_correction_applied'] else correction_result['corrected_statement']))))
            }
        }
        
        analysis_history.append(analysis_record)
        
        # 세션에 분석 ID 저장
        if 'analysis_ids' not in session:
            session['analysis_ids'] = []
        session['analysis_ids'].append(analysis_id)
        
        return jsonify({
            'success': True,
            'analysis': analysis_record
        })
        
    except Exception as e:
        logger.error(f"통합 분석 중 오류: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """대시보드 페이지"""
    return render_template('dashboard.html')

@app.route('/api/statistics')
def get_statistics():
    """통계 데이터 API - 통합 분석 결과 반영"""
    try:
        if not analysis_history:
            return jsonify({
                'total_analyses': 0,
                'average_truth': 0,
                'lies_detected': 0,
                'corrections_made': 0,
                'meta_lies_detected': 0,
                'religious_topics': 0,
                'scientific_lies': 0,
                'intentional_lies': 0,
                'human_behavior_lies': 0,
                'benevolent_lies': 0,
                'puns_detected': 0,
                'coding_issues_detected': 0,
                'intentional_manipulation': 0,
                'multilingual_detected': 0,
                'languages_used': 0
            })
        
        total_analyses = len(analysis_history)
        average_truth = sum(a['final_analysis']['truth_percentage'] for a in analysis_history) / total_analyses
        lies_detected = sum(1 for a in analysis_history if a['final_analysis']['needs_correction'])
        corrections_made = sum(1 for a in analysis_history if a['final_analysis']['final_corrected_statement'])
        
        # 각 탐지기별 통계
        meta_lies_detected = sum(1 for a in analysis_history if a.get('meta_analysis', {}).get('meta_lie_detected', False))
        religious_topics = sum(1 for a in analysis_history if a.get('religious_analysis', {}).get('religious_topic_detected', False))
        scientific_lies = sum(1 for a in analysis_history if a.get('scientific_analysis', {}).get('scientific_lie_detected', False))
        intentional_lies = sum(1 for a in analysis_history if a.get('intentional_analysis', {}).get('intentional_lie_detected', False))
        human_behavior_lies = sum(1 for a in analysis_history if a.get('human_behavior_analysis', {}).get('is_human_behavior_lie', False))
        benevolent_lies = sum(1 for a in analysis_history if a.get('benevolent_analysis', {}).get('is_benevolent_lie', False))
        context_corrections = sum(1 for a in analysis_history if a.get('context_analysis', {}).get('context_correction_applied', False))
        compound_corrections = sum(1 for a in analysis_history if a.get('compound_analysis', {}).get('compound_correction_applied', False))
        puns_detected = sum(1 for a in analysis_history if a.get('puns_analysis', {}).get('is_pun_detected', False))
        coding_issues_detected = sum(1 for a in analysis_history if a.get('coding_analysis', {}).get('unnecessary_code_detected', False))
        intentional_manipulation = sum(1 for a in analysis_history if a.get('coding_analysis', {}).get('is_intentional_manipulation', False))
        multilingual_detected = sum(1 for a in analysis_history if a.get('multilingual_analysis', {}).get('is_multilingual', False))
        languages_used = sum(len(a.get('multilingual_analysis', {}).get('detected_languages', [])) for a in analysis_history)
        
        return jsonify({
            'total_analyses': total_analyses,
            'average_truth': average_truth,
            'lies_detected': lies_detected,
            'corrections_made': corrections_made,
            'meta_lies_detected': meta_lies_detected,
            'religious_topics': religious_topics,
            'scientific_lies': scientific_lies,
            'intentional_lies': intentional_lies,
            'human_behavior_lies': human_behavior_lies,
            'benevolent_lies': benevolent_lies,
            'context_corrections': context_corrections,
            'compound_corrections': compound_corrections,
            'puns_detected': puns_detected,
            'coding_issues_detected': coding_issues_detected,
            'intentional_manipulation': intentional_manipulation,
            'multilingual_detected': multilingual_detected,
            'languages_used': languages_used,
            'truth_trend': [a['final_analysis']['truth_percentage'] for a in analysis_history[-10:]]  # 최근 10개
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/verification_chart')
def get_verification_chart():
    """탐지기별 분석 결과 차트 데이터"""
    try:
        if not analysis_history:
            return jsonify({'error': '분석 데이터가 없습니다.'}), 400
        
        # 최근 분석들의 탐지기별 감지율
        recent_analyses = analysis_history[-10:] if len(analysis_history) >= 10 else analysis_history
        
        detector_stats = {
            '기본 탐지기': sum(1 for a in recent_analyses if a.get('basic_analysis', {}).get('detected_lies', [])) / len(recent_analyses),
            '메타-진실성': sum(1 for a in recent_analyses if a.get('meta_analysis', {}).get('meta_lie_detected', False)) / len(recent_analyses),
            '종교적 맥락': sum(1 for a in recent_analyses if a.get('religious_analysis', {}).get('religious_topic_detected', False)) / len(recent_analyses),
            '과학적 검증': sum(1 for a in recent_analyses if a.get('scientific_analysis', {}).get('scientific_lie_detected', False)) / len(recent_analyses),
            '의도적 거짓말': sum(1 for a in recent_analyses if a.get('intentional_analysis', {}).get('intentional_lie_detected', False)) / len(recent_analyses),
            '인간 행동': sum(1 for a in recent_analyses if a.get('human_behavior_analysis', {}).get('is_human_behavior_lie', False)) / len(recent_analyses),
            '선의의 거짓말': sum(1 for a in recent_analyses if a.get('benevolent_analysis', {}).get('is_benevolent_lie', False)) / len(recent_analyses),
            '교정 강화': sum(1 for a in recent_analyses if a.get('correction_enhancement', {}).get('enhanced_correction_applied', False)) / len(recent_analyses),
            '말장난': sum(1 for a in recent_analyses if a.get('puns_analysis', {}).get('is_pun_detected', False)) / len(recent_analyses),
            '코딩 품질': sum(1 for a in recent_analyses if a.get('coding_analysis', {}).get('unnecessary_code_detected', False)) / len(recent_analyses),
            '다국어': sum(1 for a in recent_analyses if a.get('multilingual_analysis', {}).get('is_multilingual', False)) / len(recent_analyses)
        }
        
        # 차트 데이터 생성
        fig = go.Figure(data=[
            go.Bar(
                x=list(detector_stats.keys()),
                y=list(detector_stats.values()),
                marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F', '#FF9F43', '#6C5CE7', '#A29BFE']
            )
        ])
        
        fig.update_layout(
            title='탐지기별 감지율',
            xaxis_title='탐지기',
            yaxis_title='감지율',
            yaxis=dict(range=[0, 1]),
            xaxis_tickangle=-45
        )
        
        return jsonify(plotly.utils.PlotlyJSONEncoder().encode(fig))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/truth_trend')
def get_truth_trend():
    """통합 진실성 트렌드 차트"""
    try:
        if not analysis_history:
            return jsonify({'error': '분석 데이터가 없습니다.'}), 400
        
        # 시간순 진실성 점수 (통합 결과)
        timestamps = [datetime.fromisoformat(a['timestamp']) for a in analysis_history]
        truth_scores = [a['final_analysis']['truth_percentage'] for a in analysis_history]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=truth_scores,
            mode='lines+markers',
            name='통합 진실성 점수',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=8)
        ))
        
        # 임계값 라인 추가
        fig.add_hline(y=0.99, line_dash="dash", line_color="red", 
                     annotation_text="진실성 임계값 (99%)")
        fig.add_hline(y=0.20, line_dash="dash", line_color="orange", 
                     annotation_text="교정 임계값 (20%)")
        
        fig.update_layout(
            title='AI 통합 진실성 트렌드',
            xaxis_title='시간',
            yaxis_title='진실성 점수',
            yaxis=dict(range=[0, 1])
        )
        
        return jsonify(plotly.utils.PlotlyJSONEncoder().encode(fig))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recent_analyses')
def get_recent_analyses():
    """최근 분석 결과"""
    try:
        recent = analysis_history[-5:] if len(analysis_history) >= 5 else analysis_history
        return jsonify(recent)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    """분석 히스토리 초기화"""
    try:
        global analysis_history
        analysis_history = []
        session.pop('analysis_ids', None)
        return jsonify({'success': True, 'message': '히스토리가 초기화되었습니다.'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def perform_puns_analysis(statement, context):
    """말장난 분석만"""
    try:
        # 말장난 분석
        puns_analysis = puns_detector.analyze_with_puns_detection(statement, context)
        
        # 분석 결과 생성
        analysis_id = str(uuid.uuid4())
        analysis_record = {
            'id': analysis_id,
            'timestamp': datetime.now().isoformat(),
            'statement': statement,
            'context': context,
            'mode': 'puns',
            'puns_analysis': puns_analysis,
            'final_analysis': {
                'truth_percentage': 1.0 if puns_analysis['is_pun_detected'] else 0.5,
                'confidence': puns_analysis['pun_understanding'],
                'needs_correction': False,
                'final_corrected_statement': puns_analysis['preserved_statement']
            }
        }
        
        analysis_history.append(analysis_record)
        
        return jsonify({
            'success': True,
            'analysis': analysis_record
        })
        
    except Exception as e:
        logger.error(f"말장난 분석 중 오류: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

def perform_coding_analysis(statement, context):
    """코딩 품질 분석만"""
    try:
        # 코딩 품질 분석
        coding_analysis = coding_detector.analyze_with_coding_quality_detection(statement, context)
        
        # 분석 결과 생성
        analysis_id = str(uuid.uuid4())
        analysis_record = {
            'id': analysis_id,
            'timestamp': datetime.now().isoformat(),
            'statement': statement,
            'context': context,
            'mode': 'coding',
            'coding_analysis': coding_analysis,
            'final_analysis': {
                'truth_percentage': coding_analysis['quality_score'],
                'confidence': coding_analysis['quality_score'],
                'needs_correction': coding_analysis['needs_refactoring'],
                'final_corrected_statement': statement
            }
        }
        
        analysis_history.append(analysis_record)
        
        return jsonify({
            'success': True,
            'analysis': analysis_record
        })
        
    except Exception as e:
        logger.error(f"코딩 분석 중 오류: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

def perform_multilingual_analysis(statement, context):
    """다국어 분석만"""
    try:
        # 다국어 분석
        multilingual_analysis = multilingual_analyzer.analyze_multilingual_statement(statement, context)
        
        # 분석 결과 생성
        analysis_id = str(uuid.uuid4())
        analysis_record = {
            'id': analysis_id,
            'timestamp': datetime.now().isoformat(),
            'statement': statement,
            'context': context,
            'mode': 'multilingual',
            'multilingual_analysis': multilingual_analysis,
            'final_analysis': {
                'truth_percentage': multilingual_analysis['understanding_score'],
                'confidence': multilingual_analysis['understanding_score'],
                'needs_correction': multilingual_analysis['needs_translation'],
                'final_corrected_statement': statement
            }
        }
        
        analysis_history.append(analysis_record)
        
        return jsonify({
            'success': True,
            'analysis': analysis_record
        })
        
    except Exception as e:
        logger.error(f"다국어 분석 중 오류: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

def perform_ai_self_analysis(statement, context, analysis_mode):
    """AI 자체 진실성 분석 수행"""
    try:
        # AI 자체 진실성 탐지 실행
        ai_self_analysis = ai_self_detector.analyze_self(statement, context)
        
        # 실시간 모니터링 분석
        real_time_analysis = ai_real_time_monitor.analyze_statement(statement)
        
        # 메타 시스템 분석
        meta_analysis = ai_meta_system.analyze_statement(statement)
        
        # 분석 결과 통합
        analysis_id = str(uuid.uuid4())
        analysis_record = {
            'id': analysis_id,
            'statement': statement,
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'analysis_type': 'ai_self_analysis',
            
            # AI 자체 분석 결과
            'ai_self_analysis': {
                'original_statement': ai_self_analysis.original_statement,
                'truth_percentage': ai_self_analysis.truth_percentage,
                'truth_level': ai_self_analysis.truth_level.value,
                'detected_lies': ai_self_analysis.detected_lies,
                'confidence_score': ai_self_analysis.confidence_score,
                'correction_suggestions': ai_self_analysis.correction_suggestions,
                'corrected_statement': ai_self_analysis.corrected_statement,
                'self_reflection': ai_self_analysis.self_reflection,
                'analysis_timestamp': ai_self_analysis.analysis_timestamp.isoformat(),
                'processing_time': ai_self_analysis.processing_time
            },
            
            # 실시간 모니터링 결과
            'real_time_analysis': {
                'statement': real_time_analysis.statement,
                'truth_percentage': real_time_analysis.truth_percentage,
                'needs_correction': real_time_analysis.needs_correction,
                'corrected_statement': real_time_analysis.corrected_statement,
                'correction_reason': real_time_analysis.correction_reason,
                'timestamp': real_time_analysis.timestamp.isoformat(),
                'processing_time': real_time_analysis.processing_time
            },
            
            # 메타 시스템 분석 결과
            'meta_system_analysis': {
                'statement_id': meta_analysis.statement_id,
                'original_statement': meta_analysis.original_statement,
                'truth_percentage': meta_analysis.truth_percentage,
                'truth_level': meta_analysis.truth_level.value,
                'confidence_score': meta_analysis.confidence_score,
                'detected_issues': meta_analysis.detected_issues,
                'correction_suggestions': meta_analysis.correction_suggestions,
                'corrected_statement': meta_analysis.corrected_statement,
                'correction_applied': meta_analysis.correction_applied,
                'self_reflection': meta_analysis.self_reflection,
                'analysis_timestamp': meta_analysis.analysis_timestamp.isoformat(),
                'processing_time': meta_analysis.processing_time
            },
            
            # 통합 최종 분석
            'final_analysis': {
                'truth_percentage': meta_analysis.truth_percentage,
                'confidence': meta_analysis.confidence_score,
                'needs_correction': meta_analysis.correction_applied,
                'corrected_statement': meta_analysis.corrected_statement,
                'ai_self_awareness': True,
                'meta_cognitive_analysis': True,
                'real_time_monitoring': True
            }
        }
        
        # 분석 히스토리에 추가
        analysis_history.append(analysis_record)
        
        # 최근 100개만 유지
        if len(analysis_history) > 100:
            analysis_history.pop(0)
        
        return jsonify({
            'success': True,
            'analysis': analysis_record
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'AI 자체 분석 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/ai-self-analysis', methods=['POST'])
def api_ai_self_analysis():
    """API: AI 자체 진실성 분석 전용 엔드포인트"""
    try:
        data = request.get_json()
        statement = data.get('statement', '').strip()
        context = data.get('context', '').strip()
        
        if not statement:
            return jsonify({'error': '문장을 입력해주세요.'}), 400
        
        return perform_ai_self_analysis(statement, context, 'all')
        
    except Exception as e:
        return jsonify({'error': f'AI 자체 분석 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/ai-meta-report', methods=['GET'])
def api_ai_meta_report():
    """API: AI 메타 보고서 생성"""
    try:
        meta_report = ai_meta_system.generate_meta_report()
        stats = ai_meta_system.get_stats()
        
        return jsonify({
            'success': True,
            'meta_report': meta_report,
            'statistics': stats
        })
        
    except Exception as e:
        return jsonify({'error': f'메타 보고서 생성 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/ai-self-stats', methods=['GET'])
def api_ai_self_stats():
    """API: AI 자체 분석 통계"""
    try:
        real_time_stats = ai_real_time_monitor.get_stats()
        meta_stats = ai_meta_system.get_stats()
        
        return jsonify({
            'success': True,
            'real_time_stats': real_time_stats,
            'meta_stats': meta_stats
        })
        
    except Exception as e:
        return jsonify({'error': f'통계 조회 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/research-question', methods=['POST'])
def api_research_question():
    """API: 질문 연구 및 답변"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        research_type = data.get('type', 'basic')  # basic, advanced, enhanced
        
        if not question:
            return jsonify({'error': '질문을 입력해주세요.'}), 400
        
        # 연구 타입에 따라 다른 연구원 사용
        if research_type == 'enhanced':
            result = ai_enhanced_researcher.research_question(question)
        elif research_type == 'advanced':
            result = ai_advanced_researcher.research_question(question)
        else:
            result = ai_web_researcher.research_question(question)
        
        # 결과를 딕셔너리로 변환
        result_dict = {
            'question': result.question,
            'answer': result.answer,
            'confidence': result.confidence,
            'sources': [
                {
                    'title': source.title,
                    'url': source.url,
                    'snippet': source.snippet,
                    'domain': getattr(source, 'domain', getattr(source, 'source', '')),
                    'credibility_score': source.credibility_score,
                    'relevance_score': getattr(source, 'relevance_score', 0.0),
                    'search_engine': getattr(source, 'search_engine', ''),
                    'search_keyword': getattr(source, 'search_keyword', ''),
                    'processing_time': getattr(source, 'processing_time', 0.0)
                } for source in result.sources
            ],
            'fact_checks': [
                {
                    'statement': fc.get('statement', fc.statement if hasattr(fc, 'statement') else ''),
                    'is_factual': getattr(fc, 'is_factual', fc.get('is_verified', fc.is_verified if hasattr(fc, 'is_verified') else False)),
                    'confidence': fc.confidence if hasattr(fc, 'confidence') else fc.get('confidence', 0.0),
                    'evidence': fc.evidence if hasattr(fc, 'evidence') else fc.get('evidence', []),
                    'verification_method': fc.verification_method if hasattr(fc, 'verification_method') else fc.get('verification_method', '')
                } for fc in result.fact_checks
            ],
            'reasoning': result.reasoning,
            'limitations': getattr(result, 'limitations', []),
            'search_progress': [
                {
                    'step': progress.step,
                    'description': progress.description,
                    'status': progress.status,
                    'details': progress.details,
                    'timestamp': progress.timestamp.isoformat(),
                    'progress_percentage': progress.progress_percentage
                } for progress in getattr(result, 'search_progress', [])
            ],
            'total_processing_time': getattr(result, 'total_processing_time', 0.0),
            'timestamp': result.timestamp.isoformat()
        }
        
        # 분석 히스토리에 추가
        analysis_history.append({
            'id': str(uuid.uuid4()),
            'type': 'research_question',
            'question': question,
            'result': result_dict,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'research_result': result_dict
        })
        
    except Exception as e:
        return jsonify({'error': f'질문 연구 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/verify-fact', methods=['POST'])
def api_verify_fact():
    """API: 사실 검증"""
    try:
        data = request.get_json()
        statement = data.get('statement', '').strip()
        
        if not statement:
            return jsonify({'error': '검증할 문장을 입력해주세요.'}), 400
        
        # 고급 연구원으로 사실 검증 수행
        result = ai_advanced_researcher.research_question(f"다음 문장이 사실인지 검증해주세요: {statement}")
        
        # 사실 검증 결과 추출
        fact_verification = {
            'statement': statement,
            'is_verified': len(result.fact_verifications) > 0,
            'confidence': result.confidence,
            'evidence': [fc.evidence for fc in result.fact_verifications],
            'sources': [
                {
                    'title': source.title,
                    'url': source.url,
                    'credibility_score': source.credibility_score
                } for source in result.sources
            ],
            'reasoning': result.reasoning,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'verification_result': fact_verification
        })
        
    except Exception as e:
        return jsonify({'error': f'사실 검증 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/consistent-analyze', methods=['POST'])
def api_consistent_analyze():
    """API: 일관성 있는 진실성 분석"""
    try:
        data = request.get_json()
        statement = data.get('statement', '').strip()
        context = data.get('context', '').strip()
        
        if not statement:
            return jsonify({'error': '분석할 문장을 입력해주세요.'}), 400
        
        # 일관성 있는 분석 수행
        result = ai_consistent_detector.analyze_statement(statement, context)
        
        # 결과를 딕셔너리로 변환
        result_dict = {
            'statement': result.statement,
            'statement_hash': result.statement_hash,
            'truth_percentage': result.truth_percentage,
            'confidence': result.confidence,
            'needs_correction': result.needs_correction,
            'corrected_statement': result.corrected_statement,
            'consistency_score': result.consistency_score,
            'analysis_method': result.analysis_method,
            'analysis_timestamp': result.analysis_timestamp.isoformat(),
            'cache_stats': ai_consistent_detector.get_cache_stats()
        }
        
        # 분석 히스토리에 추가
        analysis_history.append({
            'id': str(uuid.uuid4()),
            'type': 'consistent_analysis',
            'statement': statement,
            'result': result_dict,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'analysis': result_dict
        })
        
    except Exception as e:
        return jsonify({'error': f'일관성 있는 분석 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/consistency-test', methods=['POST'])
def api_consistency_test():
    """API: 일관성 테스트"""
    try:
        data = request.get_json()
        statement = data.get('statement', '').strip()
        test_count = data.get('test_count', 5)
        
        if not statement:
            return jsonify({'error': '테스트할 문장을 입력해주세요.'}), 400
        
        # 동일한 문장에 대해 여러 번 분석
        results = []
        for i in range(test_count):
            result = ai_consistent_detector.analyze_statement(statement)
            results.append({
                'iteration': i + 1,
                'truth_percentage': result.truth_percentage,
                'confidence': result.confidence,
                'statement_hash': result.statement_hash,
                'timestamp': result.analysis_timestamp.isoformat()
            })
        
        # 일관성 통계 계산
        truth_scores = [r['truth_percentage'] for r in results]
        confidence_scores = [r['confidence'] for r in results]
        
        consistency_stats = {
            'truth_percentage': {
                'mean': sum(truth_scores) / len(truth_scores),
                'std': (sum((x - sum(truth_scores) / len(truth_scores)) ** 2 for x in truth_scores) / len(truth_scores)) ** 0.5,
                'min': min(truth_scores),
                'max': max(truth_scores),
                'variance': max(truth_scores) - min(truth_scores)
            },
            'confidence': {
                'mean': sum(confidence_scores) / len(confidence_scores),
                'std': (sum((x - sum(confidence_scores) / len(confidence_scores)) ** 2 for x in confidence_scores) / len(confidence_scores)) ** 0.5,
                'min': min(confidence_scores),
                'max': max(confidence_scores),
                'variance': max(confidence_scores) - min(confidence_scores)
            },
            'is_consistent': max(truth_scores) - min(truth_scores) < 0.01,  # 1% 이내 변동
            'test_count': test_count
        }
        
        return jsonify({
            'success': True,
            'statement': statement,
            'results': results,
            'consistency_stats': consistency_stats,
            'cache_stats': ai_consistent_detector.get_cache_stats()
        })
        
    except Exception as e:
        return jsonify({'error': f'일관성 테스트 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/clear-consistency-cache', methods=['POST'])
def api_clear_consistency_cache():
    """API: 일관성 캐시 초기화"""
    try:
        ai_consistent_detector.clear_cache()
        return jsonify({
            'success': True,
            'message': '일관성 캐시가 초기화되었습니다.'
        })
    except Exception as e:
        return jsonify({'error': f'캐시 초기화 중 오류가 발생했습니다: {str(e)}'}), 500

# 엔터프라이즈급 API 엔드포인트들
@app.route('/api/health', methods=['GET'])
def api_health():
    """API: 시스템 상태 확인"""
    try:
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0-enterprise',
            'uptime': time.time(),
            'performance_metrics': performance_metrics,
            'system_info': {
                'python_version': '3.8+',
                'flask_version': '2.0+',
                'analysis_history_size': len(analysis_history),
                'cache_size': len(request_cache)
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/metrics', methods=['GET'])
def api_metrics():
    """API: 성능 메트릭 조회"""
    try:
        return jsonify({
            'success': True,
            'metrics': performance_metrics,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'메트릭 조회 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/validate', methods=['POST'])
def api_validate():
    """API: 입력 검증 전용 엔드포인트"""
    try:
        data = request.get_json()
        statement = data.get('statement', '').strip()
        context = data.get('context', '').strip()
        validation_level = data.get('validation_level', 'standard')
        
        if not statement:
            return jsonify({'error': '문장을 입력해주세요.'}), 400
        
        # 검증 수준 변환
        level_map = {
            'basic': ValidationLevel.BASIC,
            'standard': ValidationLevel.STANDARD,
            'strict': ValidationLevel.STRICT,
            'enterprise': ValidationLevel.ENTERPRISE
        }
        
        validation_level_enum = level_map.get(validation_level, ValidationLevel.STANDARD)
        
        # 요청 객체 생성
        analysis_request = AnalysisRequest(
            statement=statement,
            context=context,
            analysis_mode='validation',
            validation_level=validation_level_enum,
            user_id=session.get('user_id'),
            session_id=session.get('session_id')
        )
        
        # 비동기 검증 실행
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        validation_result = loop.run_until_complete(
            validation_system.validate_request(analysis_request)
        )
        loop.close()
        
        return jsonify({
            'success': True,
            'validation_result': {
                'is_valid': validation_result.is_valid,
                'confidence': validation_result.confidence,
                'errors': validation_result.errors,
                'warnings': validation_result.warnings,
                'suggestions': validation_result.suggestions,
                'validation_level': validation_result.validation_level.value,
                'processing_time': validation_result.processing_time,
                'timestamp': validation_result.timestamp.isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"검증 중 오류 발생: {str(e)}")
        return jsonify({'error': f'검증 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/confidence', methods=['POST'])
def api_confidence():
    """API: 신뢰도 평가 전용 엔드포인트"""
    try:
        data = request.get_json()
        statement = data.get('statement', '').strip()
        context = data.get('context', '').strip()
        analysis_result = data.get('analysis_result', {})
        
        if not statement:
            return jsonify({'error': '문장을 입력해주세요.'}), 400
        
        # 비동기 신뢰도 평가 실행
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        confidence_score = loop.run_until_complete(
            confidence_system.evaluate_confidence(statement, context, analysis_result)
        )
        loop.close()
        
        return jsonify({
            'success': True,
            'confidence_evaluation': {
                'overall_confidence': confidence_score.overall,
                'quality_level': confidence_score.quality_level.name,
                'explanation': confidence_score.explanation,
                'recommendations': confidence_score.recommendations,
                'source_scores': {source.value: score for source, score in confidence_score.sources.items()},
                'processing_time': confidence_score.processing_time,
                'timestamp': confidence_score.timestamp.isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"신뢰도 평가 중 오류 발생: {str(e)}")
        return jsonify({'error': f'신뢰도 평가 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/batch-analyze', methods=['POST'])
def api_batch_analyze():
    """API: 배치 분석 (여러 문장 동시 처리)"""
    try:
        data = request.get_json()
        statements = data.get('statements', [])
        context = data.get('context', '').strip()
        analysis_mode = data.get('analysis_mode', 'all')
        
        if not statements or not isinstance(statements, list):
            return jsonify({'error': '분석할 문장 목록을 입력해주세요.'}), 400
        
        if len(statements) > 10:
            return jsonify({'error': '한 번에 최대 10개 문장까지 분석할 수 있습니다.'}), 400
        
        results = []
        
        for i, statement in enumerate(statements):
            try:
                # 각 문장에 대해 분석 수행
                analysis_result = detector.analyze_statement(statement, context)
                
                result_dict = {
                    'index': i,
                    'statement': statement,
                    'context': context,
                    'final_analysis': {
                        'truth_percentage': analysis_result.final_analysis.truth_percentage,
                        'confidence': analysis_result.final_analysis.confidence,
                        'needs_correction': analysis_result.final_analysis.needs_correction
                    },
                    'basic_analysis': analysis_result.basic_analysis.__dict__,
                    'timestamp': datetime.now().isoformat()
                }
                
                results.append(result_dict)
                
            except Exception as e:
                logger.error(f"배치 분석 중 오류 (문장 {i}): {str(e)}")
                results.append({
                    'index': i,
                    'statement': statement,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        return jsonify({
            'success': True,
            'batch_results': results,
            'total_processed': len(statements),
            'successful': len([r for r in results if 'error' not in r]),
            'failed': len([r for r in results if 'error' in r]),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"배치 분석 중 오류 발생: {str(e)}")
        return jsonify({'error': f'배치 분석 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/export', methods=['GET'])
def api_export():
    """API: 분석 결과 내보내기"""
    try:
        export_format = request.args.get('format', 'json')
        limit = request.args.get('limit', 100, type=int)
        
        if export_format not in ['json', 'csv']:
            return jsonify({'error': '지원하지 않는 형식입니다. (json, csv)'}), 400
        
        # 최근 분석 결과 가져오기
        recent_analyses = analysis_history[-limit:] if len(analysis_history) >= limit else analysis_history
        
        if export_format == 'json':
            return jsonify({
                'success': True,
                'data': recent_analyses,
                'export_format': 'json',
                'total_records': len(recent_analyses),
                'timestamp': datetime.now().isoformat()
            })
        elif export_format == 'csv':
            # CSV 형식으로 변환
            import csv
            import io
            
            output = io.StringIO()
            if recent_analyses:
                fieldnames = recent_analyses[0].keys()
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(recent_analyses)
            
            return jsonify({
                'success': True,
                'data': output.getvalue(),
                'export_format': 'csv',
                'total_records': len(recent_analyses),
                'timestamp': datetime.now().isoformat()
            })
        
    except Exception as e:
        logger.error(f"내보내기 중 오류 발생: {str(e)}")
        return jsonify({'error': f'내보내기 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/clear-cache', methods=['POST'])
def api_clear_cache():
    """API: 모든 캐시 초기화"""
    try:
        global request_cache
        request_cache.clear()
        
        # 일관성 캐시도 초기화
        ai_consistent_detector.clear_cache()
        
        return jsonify({
            'success': True,
            'message': '모든 캐시가 초기화되었습니다.',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"캐시 초기화 중 오류 발생: {str(e)}")
        return jsonify({'error': f'캐시 초기화 중 오류가 발생했습니다: {str(e)}'}), 500

# 에러 핸들러
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': '요청한 리소스를 찾을 수 없습니다.',
        'status_code': 404,
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': '내부 서버 오류가 발생했습니다.',
        'status_code': 500,
        'timestamp': datetime.now().isoformat()
    }), 500

@app.errorhandler(413)
def too_large(error):
    return jsonify({
        'error': '요청 크기가 너무 큽니다. 최대 16MB까지 허용됩니다.',
        'status_code': 413,
        'timestamp': datetime.now().isoformat()
    }), 413

if __name__ == '__main__':
    logger.info("AI 진실성 탐지 시스템 (Enterprise Edition) 시작")
    logger.info(f"버전: 2.0.0-enterprise")
    logger.info(f"Flask 디버그 모드: {app.debug}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
