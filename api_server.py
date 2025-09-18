#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Truth Detector API Server
AI 진실성 탐지기 API 서버

RESTful API를 제공하여 웹 애플리케이션과 연동할 수 있는 서버입니다.
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import logging
from datetime import datetime
from typing import Dict, Any
import traceback

from enhanced_truth_detector import TruthDetector, AnalysisResult

# Flask 앱 초기화
app = Flask(__name__)
CORS(app)  # CORS 허용

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 전역 탐지기 인스턴스
truth_detector = TruthDetector()

# HTML 템플릿
API_DOCS_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 진실성 탐지기 API</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { background: rgba(255, 255, 255, 0.95); border-radius: 20px; margin-top: 20px; padding: 30px; }
        .endpoint { background: #f8f9fa; border-radius: 10px; padding: 20px; margin: 10px 0; }
        .method { font-weight: bold; padding: 5px 10px; border-radius: 5px; color: white; }
        .get { background: #28a745; }
        .post { background: #007bff; }
        .code { background: #f8f9fa; padding: 15px; border-radius: 5px; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-4">
            <i class="fas fa-shield-alt text-primary me-3"></i>
            AI 진실성 탐지기 API
        </h1>
        
        <div class="row">
            <div class="col-md-6">
                <div class="endpoint">
                    <h4><span class="method get">GET</span> /api/health</h4>
                    <p>서버 상태 확인</p>
                    <div class="code">
GET /api/health
                    </div>
                </div>
                
                <div class="endpoint">
                    <h4><span class="method get">GET</span> /api/statistics</h4>
                    <p>분석 통계 조회</p>
                    <div class="code">
GET /api/statistics
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="endpoint">
                    <h4><span class="method post">POST</span> /api/analyze</h4>
                    <p>문장 분석</p>
                    <div class="code">
POST /api/analyze
Content-Type: application/json

{
    "statement": "분석할 문장",
    "context": "선택적 컨텍스트"
}
                    </div>
                </div>
                
                <div class="endpoint">
                    <h4><span class="method post">POST</span> /api/batch-analyze</h4>
                    <p>여러 문장 일괄 분석</p>
                    <div class="code">
POST /api/batch-analyze
Content-Type: application/json

{
    "statements": ["문장1", "문장2", "문장3"]
}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="text-center mt-4">
            <p class="text-muted">API 서버가 정상적으로 실행 중입니다.</p>
            <p><strong>서버 시작 시간:</strong> {{ start_time }}</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """API 문서 페이지"""
    return render_template_string(API_DOCS_TEMPLATE, start_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/api/health', methods=['GET'])
def health_check():
    """서버 상태 확인"""
    try:
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0',
            'detectors_count': len(truth_detector.detectors),
            'correction_engines_count': len(truth_detector.correction_engines)
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_statement():
    """단일 문장 분석"""
    try:
        data = request.get_json()
        
        if not data or 'statement' not in data:
            return jsonify({
                'error': 'statement 필드가 필요합니다.',
                'code': 'MISSING_STATEMENT'
            }), 400
        
        statement = data['statement'].strip()
        context = data.get('context', '').strip() if data.get('context') else None
        
        if not statement:
            return jsonify({
                'error': '문장이 비어있습니다.',
                'code': 'EMPTY_STATEMENT'
            }), 400
        
        # 분석 실행
        result = truth_detector.analyze(statement, context)
        
        # 결과 변환
        response = {
            'analysis_id': result.analysis_id,
            'statement': result.statement,
            'truth_percentage': result.truth_percentage,
            'confidence': result.confidence,
            'needs_correction': result.needs_correction,
            'detected_issues': result.detected_issues,
            'correction_suggestions': result.correction_suggestions,
            'detector_results': result.detector_results,
            'timestamp': result.timestamp.isoformat(),
            'processing_time': (datetime.now() - result.timestamp).total_seconds()
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': '분석 중 오류가 발생했습니다.',
            'details': str(e),
            'code': 'ANALYSIS_ERROR'
        }), 500

@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    """여러 문장 일괄 분석"""
    try:
        data = request.get_json()
        
        if not data or 'statements' not in data:
            return jsonify({
                'error': 'statements 필드가 필요합니다.',
                'code': 'MISSING_STATEMENTS'
            }), 400
        
        statements = data['statements']
        context = data.get('context', '').strip() if data.get('context') else None
        
        if not isinstance(statements, list):
            return jsonify({
                'error': 'statements는 배열이어야 합니다.',
                'code': 'INVALID_STATEMENTS_TYPE'
            }), 400
        
        if len(statements) == 0:
            return jsonify({
                'error': '분석할 문장이 없습니다.',
                'code': 'EMPTY_STATEMENTS'
            }), 400
        
        if len(statements) > 10:
            return jsonify({
                'error': '한 번에 최대 10개 문장까지만 분석할 수 있습니다.',
                'code': 'TOO_MANY_STATEMENTS'
            }), 400
        
        # 일괄 분석 실행
        results = []
        for i, statement in enumerate(statements):
            try:
                if not statement or not statement.strip():
                    results.append({
                        'index': i,
                        'error': '빈 문장입니다.',
                        'statement': statement
                    })
                    continue
                
                result = truth_detector.analyze(statement.strip(), context)
                results.append({
                    'index': i,
                    'analysis_id': result.analysis_id,
                    'statement': result.statement,
                    'truth_percentage': result.truth_percentage,
                    'confidence': result.confidence,
                    'needs_correction': result.needs_correction,
                    'detected_issues': result.detected_issues,
                    'correction_suggestions': result.correction_suggestions,
                    'timestamp': result.timestamp.isoformat()
                })
            except Exception as e:
                results.append({
                    'index': i,
                    'error': str(e),
                    'statement': statement
                })
        
        return jsonify({
            'total_statements': len(statements),
            'successful_analyses': len([r for r in results if 'error' not in r]),
            'failed_analyses': len([r for r in results if 'error' in r]),
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Batch analysis error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': '일괄 분석 중 오류가 발생했습니다.',
            'details': str(e),
            'code': 'BATCH_ANALYSIS_ERROR'
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """분석 통계 조회"""
    try:
        stats = truth_detector.get_statistics()
        return jsonify({
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Statistics error: {e}")
        return jsonify({
            'error': '통계 조회 중 오류가 발생했습니다.',
            'details': str(e),
            'code': 'STATISTICS_ERROR'
        }), 500

@app.route('/api/detectors', methods=['GET'])
def get_detectors():
    """탐지기 목록 조회"""
    try:
        detectors_info = {}
        for name, detector in truth_detector.detectors.items():
            detectors_info[name] = {
                'name': detector.name,
                'weight': detector.weight,
                'description': detector.__doc__ or f"{name} 탐지기"
            }
        
        return jsonify({
            'detectors': detectors_info,
            'total_count': len(detectors_info),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Detectors info error: {e}")
        return jsonify({
            'error': '탐지기 정보 조회 중 오류가 발생했습니다.',
            'details': str(e),
            'code': 'DETECTORS_ERROR'
        }), 500

@app.route('/api/correctors', methods=['GET'])
def get_correctors():
    """교정 엔진 목록 조회"""
    try:
        correctors_info = {}
        for name, corrector in truth_detector.correction_engines.items():
            correctors_info[name] = {
                'name': corrector.name,
                'description': corrector.description,
                'icon': corrector.icon,
                'color': corrector.color
            }
        
        return jsonify({
            'correctors': correctors_info,
            'total_count': len(correctors_info),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Correctors info error: {e}")
        return jsonify({
            'error': '교정 엔진 정보 조회 중 오류가 발생했습니다.',
            'details': str(e),
            'code': 'CORRECTORS_ERROR'
        }), 500

@app.route('/api/analyze/<analysis_id>', methods=['GET'])
def get_analysis(analysis_id: str):
    """특정 분석 결과 조회"""
    try:
        # 분석 히스토리에서 해당 ID 찾기
        for result in truth_detector.analysis_history:
            if result.analysis_id == analysis_id:
                return jsonify({
                    'analysis_id': result.analysis_id,
                    'statement': result.statement,
                    'truth_percentage': result.truth_percentage,
                    'confidence': result.confidence,
                    'needs_correction': result.needs_correction,
                    'detected_issues': result.detected_issues,
                    'correction_suggestions': result.correction_suggestions,
                    'detector_results': result.detector_results,
                    'timestamp': result.timestamp.isoformat()
                })
        
        return jsonify({
            'error': '해당 분석 ID를 찾을 수 없습니다.',
            'code': 'ANALYSIS_NOT_FOUND'
        }), 404
        
    except Exception as e:
        logger.error(f"Get analysis error: {e}")
        return jsonify({
            'error': '분석 결과 조회 중 오류가 발생했습니다.',
            'details': str(e),
            'code': 'GET_ANALYSIS_ERROR'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """404 에러 핸들러"""
    return jsonify({
        'error': '요청한 엔드포인트를 찾을 수 없습니다.',
        'code': 'NOT_FOUND',
        'available_endpoints': [
            'GET /',
            'GET /api/health',
            'POST /api/analyze',
            'POST /api/batch-analyze',
            'GET /api/statistics',
            'GET /api/detectors',
            'GET /api/correctors',
            'GET /api/analyze/<analysis_id>'
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """405 에러 핸들러"""
    return jsonify({
        'error': '허용되지 않는 HTTP 메서드입니다.',
        'code': 'METHOD_NOT_ALLOWED'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """500 에러 핸들러"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': '서버 내부 오류가 발생했습니다.',
        'code': 'INTERNAL_SERVER_ERROR'
    }), 500

def create_app():
    """Flask 앱 팩토리 함수"""
    return app

if __name__ == '__main__':
    print("🚀 AI Truth Detector API Server 시작")
    print("=" * 50)
    print("📡 API 엔드포인트:")
    print("  GET  /                    - API 문서")
    print("  GET  /api/health          - 서버 상태 확인")
    print("  POST /api/analyze         - 단일 문장 분석")
    print("  POST /api/batch-analyze   - 여러 문장 일괄 분석")
    print("  GET  /api/statistics      - 분석 통계")
    print("  GET  /api/detectors       - 탐지기 목록")
    print("  GET  /api/correctors      - 교정 엔진 목록")
    print("  GET  /api/analyze/<id>    - 특정 분석 결과 조회")
    print("=" * 50)
    print("🌐 서버 주소: http://localhost:5000")
    print("📚 API 문서: http://localhost:5000")
    print("=" * 50)
    
    # 개발 모드로 실행
    app.run(host='0.0.0.0', port=5000, debug=True)
