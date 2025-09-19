"""
AI 진실성 탐지 웹 애플리케이션 (Basic Version)
Flask 기반 기본 웹 인터페이스로 AI의 진실성을 측정

기본 기능만 제공하는 간단한 버전
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import uuid
import logging
import traceback
import time
from typing import Dict, List, Optional, Any, Union
from ai_truth_detector import TruthDetector, TruthAnalysis
from ai_self_truth_detector import AISelfTruthDetector
from ai_web_researcher import AIWebResearcher

# Flask 앱 초기화
app = Flask(__name__)
app.secret_key = 'ai_truth_detector_basic_secret_key_2024'

# CORS 설정
CORS(app, origins=['*'], methods=['GET', 'POST'], allow_headers=['Content-Type'])

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# 기본 진실성 탐지 시스템 초기화
# =============================================================================

# 기본 진실성 탐지기
truth_detector = TruthDetector()

# AI 자체 진실성 탐지기
ai_self_detector = AISelfTruthDetector()

# 웹 연구자
web_researcher = AIWebResearcher()

# =============================================================================
# 웹 인터페이스 라우트
# =============================================================================

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('basic/index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """문장 분석 API"""
    try:
        data = request.get_json()
        sentence = data.get('sentence', '').strip()
        
        if not sentence:
            return jsonify({
                'success': False,
                'message': '분석할 문장을 입력해주세요.'
            }), 400
        
        # 기본 진실성 분석
        start_time = time.time()
        analysis = truth_detector.analyze(sentence)
        analysis_time = time.time() - start_time
        
        # AI 자체 분석
        ai_analysis = ai_self_detector.analyze(sentence)
        
        # 웹 연구 (간단한 버전)
        web_results = web_researcher.search(sentence, max_results=3)
        
        # 결과 정리
        result = {
            'success': True,
            'sentence': sentence,
            'analysis': {
                'truth_score': analysis.truth_score,
                'confidence': analysis.confidence,
                'analysis_time': analysis_time,
                'details': analysis.details
            },
            'ai_analysis': {
                'self_awareness': ai_analysis.self_awareness,
                'confidence_level': ai_analysis.confidence_level,
                'uncertainty_detected': ai_analysis.uncertainty_detected,
                'suggestions': ai_analysis.suggestions
            },
            'web_research': {
                'results_count': len(web_results),
                'results': [
                    {
                        'title': result.title,
                        'url': result.url,
                        'snippet': result.snippet,
                        'credibility_score': result.credibility_score
                    } for result in web_results
                ]
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"분석 중 오류 발생: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': f'분석 중 오류가 발생했습니다: {str(e)}'
        }), 500

@app.route('/batch_analyze', methods=['POST'])
def batch_analyze():
    """배치 분석 API"""
    try:
        data = request.get_json()
        sentences = data.get('sentences', [])
        
        if not sentences or not isinstance(sentences, list):
            return jsonify({
                'success': False,
                'message': '분석할 문장 목록을 입력해주세요.'
            }), 400
        
        if len(sentences) > 10:
            return jsonify({
                'success': False,
                'message': '한 번에 최대 10개 문장만 분석할 수 있습니다.'
            }), 400
        
        results = []
        total_start_time = time.time()
        
        for i, sentence in enumerate(sentences):
            try:
                sentence = sentence.strip()
                if not sentence:
                    continue
                
                # 기본 분석
                analysis = truth_detector.analyze(sentence)
                
                results.append({
                    'index': i,
                    'sentence': sentence,
                    'truth_score': analysis.truth_score,
                    'confidence': analysis.confidence,
                    'success': True
                })
                
            except Exception as e:
                results.append({
                    'index': i,
                    'sentence': sentence,
                    'error': str(e),
                    'success': False
                })
        
        total_time = time.time() - total_start_time
        
        return jsonify({
            'success': True,
            'results': results,
            'total_sentences': len(sentences),
            'successful_analyses': len([r for r in results if r.get('success', False)]),
            'total_time': total_time,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"배치 분석 중 오류 발생: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'배치 분석 중 오류가 발생했습니다: {str(e)}'
        }), 500

@app.route('/web_research', methods=['POST'])
def web_research():
    """웹 연구 API"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        max_results = data.get('max_results', 5)
        
        if not query:
            return jsonify({
                'success': False,
                'message': '검색할 쿼리를 입력해주세요.'
            }), 400
        
        # 웹 연구 실행
        start_time = time.time()
        results = web_researcher.search(query, max_results=max_results)
        research_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'query': query,
            'results': [
                {
                    'title': result.title,
                    'url': result.url,
                    'snippet': result.snippet,
                    'source': result.source,
                    'credibility_score': result.credibility_score,
                    'relevance_score': result.relevance_score
                } for result in results
            ],
            'results_count': len(results),
            'research_time': research_time,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"웹 연구 중 오류 발생: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'웹 연구 중 오류가 발생했습니다: {str(e)}'
        }), 500

@app.route('/health')
def health():
    """헬스 체크 API"""
    return jsonify({
        'status': 'healthy',
        'version': 'basic',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/info')
def api_info():
    """API 정보"""
    return jsonify({
        'name': 'AI 진실성 탐지기 (Basic Version)',
        'version': '1.0.0',
        'description': '기본 AI 진실성 탐지 기능을 제공하는 웹 애플리케이션',
        'features': [
            '기본 진실성 탐지',
            'AI 자체 분석',
            '웹 연구',
            '배치 분석'
        ],
        'endpoints': [
            'POST /analyze - 문장 분석',
            'POST /batch_analyze - 배치 분석',
            'POST /web_research - 웹 연구',
            'GET /health - 헬스 체크',
            'GET /api/info - API 정보'
        ]
    })

# =============================================================================
# 에러 핸들러
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': '요청한 리소스를 찾을 수 없습니다.'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': '서버 내부 오류가 발생했습니다.'
    }), 500

# =============================================================================
# 애플리케이션 실행
# =============================================================================

if __name__ == '__main__':
    logger.info("AI 진실성 탐지기 (Basic Version) 시작...")
    app.run(debug=True, host='0.0.0.0', port=5000)
