#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 진실성 탐지기 API 문서화 (Swagger/OpenAPI)
우선순위 2-2: API 문서화 구축

작성일: 2025-09-19
버전: 2.0.0-enterprise
"""

from flask import Flask
from flask_restx import Api, Resource, fields, Namespace
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_api_documentation(app):
    """Swagger/OpenAPI 문서화 생성"""
    
    # API 설정
    api = Api(
        app,
        version='2.0.0',
        title='AI 진실성 탐지기 API',
        description='AI가 자신의 출력을 분석하고 웹 연구를 통해 사실을 검증하는 엔터프라이즈급 시스템',
        doc='/api/docs/',  # Swagger UI 경로
        prefix='/api/v1'
    )
    
    # 네임스페이스 정의
    analysis_ns = Namespace('analysis', description='문장 분석 관련 API')
    research_ns = Namespace('research', description='웹 연구 및 사실 검증 API')
    monitoring_ns = Namespace('monitoring', description='시스템 모니터링 API')
    detectors_ns = Namespace('detectors', description='탐지기 관리 API')
    batch_ns = Namespace('batch', description='배치 작업 관리 API')
    
    # API에 네임스페이스 추가
    api.add_namespace(analysis_ns)
    api.add_namespace(research_ns)
    api.add_namespace(monitoring_ns)
    api.add_namespace(detectors_ns)
    api.add_namespace(batch_ns)
    
    # 데이터 모델 정의
    analysis_request = api.model('AnalysisRequest', {
        'statement': fields.String(required=True, description='분석할 문장', example='지구는 둥글다'),
        'context': fields.String(description='문맥 정보', example='과학적 사실'),
        'ai_self_analysis': fields.Boolean(description='AI 자체 분석 여부', default=True)
    })
    
    analysis_response = api.model('AnalysisResponse', {
        'success': fields.Boolean(description='성공 여부'),
        'analysis_id': fields.String(description='분석 ID'),
        'truth_percentage': fields.Float(description='진실성 비율 (0-100)'),
        'truth_level': fields.String(description='진실성 수준'),
        'confidence_score': fields.Float(description='신뢰도 점수'),
        'detected_lies': fields.List(fields.String, description='탐지된 거짓말 목록'),
        'correction_suggestions': fields.List(fields.String, description='교정 제안 목록'),
        'corrected_statement': fields.String(description='교정된 문장'),
        'processing_time': fields.Float(description='처리 시간 (초)'),
        'timestamp': fields.String(description='분석 시간')
    })
    
    research_request = api.model('ResearchRequest', {
        'question': fields.String(required=True, description='연구할 질문', example='지구는 둥글다'),
        'type': fields.String(description='연구 유형', example='advanced', enum=['basic', 'advanced', 'comprehensive'])
    })
    
    research_response = api.model('ResearchResponse', {
        'success': fields.Boolean(description='성공 여부'),
        'answer': fields.String(description='연구 결과 답변'),
        'confidence': fields.Float(description='신뢰도 점수'),
        'sources': fields.List(fields.String, description='참고 소스 목록'),
        'fact_checks': fields.List(fields.Raw, description='사실 검증 결과'),
        'research_time': fields.Float(description='연구 시간 (초)'),
        'timestamp': fields.String(description='연구 시간')
    })
    
    system_status = api.model('SystemStatus', {
        'success': fields.Boolean(description='성공 여부'),
        'system_status': fields.Raw(description='시스템 상태 정보'),
        'services': fields.Raw(description='서비스 상태 정보'),
        'timestamp': fields.String(description='상태 조회 시간')
    })
    
    detector_info = api.model('DetectorInfo', {
        'id': fields.String(description='탐지기 ID'),
        'name': fields.String(description='탐지기 이름'),
        'description': fields.String(description='탐지기 설명'),
        'status': fields.String(description='탐지기 상태'),
        'version': fields.String(description='탐지기 버전')
    })
    
    # 분석 API 엔드포인트
    @analysis_ns.route('/analyze')
    class Analyze(Resource):
        @api.expect(analysis_request)
        @api.marshal_with(analysis_response)
        def post(self):
            """문장 진실성 분석"""
            return {
                'success': True,
                'analysis_id': 'example_analysis_123',
                'truth_percentage': 95.5,
                'truth_level': 'high',
                'confidence_score': 0.92,
                'detected_lies': [],
                'correction_suggestions': [],
                'corrected_statement': '지구는 둥글다',
                'processing_time': 0.25,
                'timestamp': datetime.now().isoformat()
            }
    
    @analysis_ns.route('/analyze/<analysis_id>')
    class GetAnalysis(Resource):
        @api.marshal_with(analysis_response)
        def get(self, analysis_id):
            """특정 분석 결과 조회"""
            return {
                'success': True,
                'analysis_id': analysis_id,
                'truth_percentage': 95.5,
                'truth_level': 'high',
                'confidence_score': 0.92,
                'detected_lies': [],
                'correction_suggestions': [],
                'corrected_statement': '지구는 둥글다',
                'processing_time': 0.25,
                'timestamp': datetime.now().isoformat()
            }
        
        def delete(self, analysis_id):
            """특정 분석 결과 삭제"""
            return {
                'success': True,
                'analysis_id': analysis_id,
                'message': '분석 결과가 성공적으로 삭제되었습니다.',
                'timestamp': datetime.now().isoformat()
            }
    
    # 연구 API 엔드포인트
    @research_ns.route('/question')
    class ResearchQuestion(Resource):
        @api.expect(research_request)
        @api.marshal_with(research_response)
        def post(self):
            """웹 연구를 통한 질문 분석"""
            return {
                'success': True,
                'answer': '지구는 실제로 둥글다. 이는 과학적으로 증명된 사실이다.',
                'confidence': 0.95,
                'sources': [
                    'NASA 공식 웹사이트',
                    '과학 아카데미 연구 보고서',
                    '국제 우주 정거장 관측 데이터'
                ],
                'fact_checks': [
                    {
                        'statement': '지구는 둥글다',
                        'is_factual': True,
                        'confidence': 0.98,
                        'evidence': ['위성 사진', '중력 측정', '항해 기록']
                    }
                ],
                'research_time': 1.2,
                'timestamp': datetime.now().isoformat()
            }
    
    # 모니터링 API 엔드포인트
    @monitoring_ns.route('/system/status')
    class SystemStatus(Resource):
        @api.marshal_with(system_status)
        def get(self):
            """시스템 전체 상태 조회"""
            return {
                'success': True,
                'system_status': {
                    'cpu_usage': '15.2%',
                    'memory_usage': '45.8%',
                    'memory_available': '8.5 GB',
                    'disk_usage': '32.1%',
                    'disk_free': '67.9 GB',
                    'uptime': 3600,
                    'timestamp': datetime.now().isoformat()
                },
                'services': {
                    'flask_app': 'running',
                    'ai_detectors': 'active',
                    'web_researcher': 'active',
                    'consistency_detector': 'active'
                },
                'timestamp': datetime.now().isoformat()
            }
    
    # 탐지기 관리 API 엔드포인트
    @detectors_ns.route('/')
    class Detectors(Resource):
        @api.marshal_with(detector_info, as_list=True)
        def get(self):
            """사용 가능한 탐지기 목록 조회"""
            return [
                {
                    'id': 'ai_self_truth',
                    'name': 'AI 자체 진실성 탐지기',
                    'description': 'AI가 자신의 출력을 분석하여 진실성을 평가',
                    'status': 'active',
                    'version': '2.0.0'
                },
                {
                    'id': 'web_researcher',
                    'name': '웹 연구 탐지기',
                    'description': '웹 검색을 통한 사실 검증 및 연구',
                    'status': 'active',
                    'version': '2.0.0'
                },
                {
                    'id': 'consistency_detector',
                    'name': '일관성 탐지기',
                    'description': '문장의 논리적 일관성 및 모순 탐지',
                    'status': 'active',
                    'version': '2.0.0'
                },
                {
                    'id': 'fact_verifier',
                    'name': '사실 검증기',
                    'description': '과학적 사실 및 일반 지식 검증',
                    'status': 'active',
                    'version': '2.0.0'
                }
            ]
    
    @detectors_ns.route('/<detector_id>/status')
    class DetectorStatus(Resource):
        def get(self, detector_id):
            """특정 탐지기 상태 조회"""
            return {
                'success': True,
                'detector_id': detector_id,
                'status': 'active',
                'timestamp': datetime.now().isoformat()
            }
    
    # 배치 작업 관리 API 엔드포인트
    @batch_ns.route('/jobs')
    class BatchJobs(Resource):
        def get(self):
            """배치 작업 목록 조회"""
            return {
                'success': True,
                'jobs': [],
                'total_count': 0,
                'timestamp': datetime.now().isoformat()
            }
    
    @batch_ns.route('/jobs/<job_id>')
    class BatchJob(Resource):
        def get(self, job_id):
            """특정 배치 작업 조회"""
            return {
                'success': True,
                'job_id': job_id,
                'status': 'completed',
                'message': '배치 작업을 성공적으로 조회했습니다.',
                'timestamp': datetime.now().isoformat()
            }
    
    # API 정보 엔드포인트
    @api.route('/version')
    class Version(Resource):
        def get(self):
            """API 버전 정보 조회"""
            return {
                'version': '2.0.0-enterprise',
                'api_version': 'v1',
                'build_date': '2025-09-19',
                'features': [
                    'ai_self_analysis',
                    'web_research',
                    'consistency_detection',
                    'fact_verification',
                    'batch_processing',
                    'real_time_monitoring'
                ],
                'endpoints': {
                    'analysis': '/api/v1/analysis',
                    'research': '/api/v1/research',
                    'monitoring': '/api/v1/monitoring',
                    'detectors': '/api/v1/detectors',
                    'batch': '/api/v1/batch'
                }
            }
    
    logger.info("Swagger/OpenAPI 문서화가 성공적으로 생성되었습니다.")
    logger.info("API 문서: http://localhost:5000/api/docs/")
    
    return api

if __name__ == '__main__':
    # 테스트용 Flask 앱 생성
    app = Flask(__name__)
    app.config['RESTX_MASK_SWAGGER'] = False
    
    # API 문서화 생성
    api = create_api_documentation(app)
    
    # 서버 실행
    print("🚀 AI 진실성 탐지기 API 문서화 서버 시작")
    print("=" * 50)
    print("📚 Swagger UI: http://localhost:5000/api/docs/")
    print("📖 API 문서: http://localhost:5000/api/v1/version")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
