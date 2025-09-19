#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 진실성 탐지기 API 인증 시스템
우선순위 2-3: API 인증 시스템 구축

작성일: 2025-09-19
버전: 2.0.0-enterprise
"""

from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, 
    get_jwt_identity, get_jwt, create_refresh_token,
    jwt_required, get_jwt_identity
)
from datetime import datetime, timedelta
import hashlib
import secrets
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIAuthManager:
    """API 인증 관리자"""
    
    def __init__(self, app=None):
        self.app = app
        self.users = {}  # 실제 환경에서는 데이터베이스 사용
        self.api_keys = {}  # API 키 관리
        self.rate_limits = {}  # 요청 제한 관리
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Flask 앱 초기화"""
        self.app = app
        
        # JWT 설정
        app.config['JWT_SECRET_KEY'] = 'ai_truth_detector_jwt_secret_key_2024'
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
        app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
        
        # JWT 매니저 초기화
        self.jwt = JWTManager(app)
        
        # JWT 콜백 함수들
        self._setup_jwt_callbacks()
        
        # 기본 사용자 생성
        self._create_default_users()
        
        logger.info("API 인증 시스템이 초기화되었습니다.")
    
    def _setup_jwt_callbacks(self):
        """JWT 콜백 함수 설정"""
        
        @self.jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_payload):
            return jsonify({
                'error': '토큰이 만료되었습니다.',
                'code': 'TOKEN_EXPIRED'
            }), 401
        
        @self.jwt.invalid_token_loader
        def invalid_token_callback(error):
            return jsonify({
                'error': '유효하지 않은 토큰입니다.',
                'code': 'INVALID_TOKEN'
            }), 401
        
        @self.jwt.unauthorized_loader
        def missing_token_callback(error):
            return jsonify({
                'error': '인증 토큰이 필요합니다.',
                'code': 'MISSING_TOKEN'
            }), 401
        
        @self.jwt.needs_fresh_token_loader
        def token_not_fresh_callback(jwt_header, jwt_payload):
            return jsonify({
                'error': '새로운 토큰이 필요합니다.',
                'code': 'TOKEN_NOT_FRESH'
            }), 401
    
    def _create_default_users(self):
        """기본 사용자 생성"""
        # 관리자 계정
        admin_password = self._hash_password('admin123')
        self.users['admin'] = {
            'username': 'admin',
            'password_hash': admin_password,
            'role': 'admin',
            'permissions': ['read', 'write', 'delete', 'admin'],
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        
        # 일반 사용자 계정
        user_password = self._hash_password('user123')
        self.users['user'] = {
            'username': 'user',
            'password_hash': user_password,
            'role': 'user',
            'permissions': ['read', 'write'],
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        
        # API 키 생성
        self._generate_api_key('admin', 'admin_api_key')
        self._generate_api_key('user', 'user_api_key')
        
        logger.info("기본 사용자 계정이 생성되었습니다.")
        logger.info("관리자: admin / admin123")
        logger.info("사용자: user / user123")
    
    def _hash_password(self, password):
        """비밀번호 해시화"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{password_hash.hex()}"
    
    def _verify_password(self, password, password_hash):
        """비밀번호 검증"""
        try:
            salt, hash_hex = password_hash.split(':')
            password_hash_computed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return password_hash_computed.hex() == hash_hex
        except:
            return False
    
    def _generate_api_key(self, username, key_name):
        """API 키 생성"""
        api_key = secrets.token_urlsafe(32)
        self.api_keys[api_key] = {
            'username': username,
            'key_name': key_name,
            'permissions': self.users[username]['permissions'],
            'created_at': datetime.now().isoformat(),
            'last_used': None,
            'is_active': True
        }
        return api_key
    
    def authenticate_user(self, username, password):
        """사용자 인증"""
        if username not in self.users:
            return False
        
        user = self.users[username]
        if not self._verify_password(password, user['password_hash']):
            return False
        
        # 마지막 로그인 시간 업데이트
        user['last_login'] = datetime.now().isoformat()
        
        return user
    
    def authenticate_api_key(self, api_key):
        """API 키 인증"""
        if api_key not in self.api_keys:
            return False
        
        key_info = self.api_keys[api_key]
        if not key_info['is_active']:
            return False
        
        # 마지막 사용 시간 업데이트
        key_info['last_used'] = datetime.now().isoformat()
        
        return key_info
    
    def check_permission(self, user_or_key, required_permission):
        """권한 확인"""
        if isinstance(user_or_key, dict) and 'permissions' in user_or_key:
            permissions = user_or_key['permissions']
        else:
            return False
        
        return required_permission in permissions or 'admin' in permissions
    
    def check_rate_limit(self, identifier, limit=100, window=3600):
        """요청 제한 확인 (시간당 100회)"""
        now = datetime.now()
        current_time = now.timestamp()
        
        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = []
        
        # 시간 윈도우 밖의 요청 제거
        self.rate_limits[identifier] = [
            req_time for req_time in self.rate_limits[identifier]
            if current_time - req_time < window
        ]
        
        # 현재 요청 수 확인
        if len(self.rate_limits[identifier]) >= limit:
            return False
        
        # 현재 요청 추가
        self.rate_limits[identifier].append(current_time)
        return True

# 전역 인증 관리자 인스턴스
auth_manager = APIAuthManager()

def create_auth_routes(app):
    """인증 관련 라우트 생성"""
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """사용자 로그인"""
        try:
            data = request.get_json()
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            
            if not username or not password:
                return jsonify({
                    'error': '사용자명과 비밀번호를 입력해주세요.',
                    'code': 'MISSING_CREDENTIALS'
                }), 400
            
            user = auth_manager.authenticate_user(username, password)
            if not user:
                return jsonify({
                    'error': '잘못된 사용자명 또는 비밀번호입니다.',
                    'code': 'INVALID_CREDENTIALS'
                }), 401
            
            # JWT 토큰 생성
            access_token = create_access_token(
                identity=username,
                additional_claims={'role': user['role'], 'permissions': user['permissions']}
            )
            refresh_token = create_refresh_token(identity=username)
            
            return jsonify({
                'success': True,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'username': user['username'],
                    'role': user['role'],
                    'permissions': user['permissions']
                },
                'expires_in': 86400,  # 24시간
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"로그인 중 오류: {str(e)}")
            return jsonify({
                'error': f'로그인 중 오류가 발생했습니다: {str(e)}',
                'code': 'LOGIN_ERROR'
            }), 500
    
    @app.route('/api/auth/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        """토큰 갱신"""
        try:
            current_user = get_jwt_identity()
            user = auth_manager.users.get(current_user)
            
            if not user:
                return jsonify({
                    'error': '사용자를 찾을 수 없습니다.',
                    'code': 'USER_NOT_FOUND'
                }), 404
            
            # 새로운 액세스 토큰 생성
            new_token = create_access_token(
                identity=current_user,
                additional_claims={'role': user['role'], 'permissions': user['permissions']}
            )
            
            return jsonify({
                'success': True,
                'access_token': new_token,
                'expires_in': 86400,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"토큰 갱신 중 오류: {str(e)}")
            return jsonify({
                'error': f'토큰 갱신 중 오류가 발생했습니다: {str(e)}',
                'code': 'REFRESH_ERROR'
            }), 500
    
    @app.route('/api/auth/logout', methods=['POST'])
    @jwt_required()
    def logout():
        """사용자 로그아웃"""
        try:
            # JWT 블랙리스트에 추가 (실제 구현에서는 Redis 등 사용)
            jti = get_jwt()['jti']
            # 여기서는 간단히 성공 응답만 반환
            
            return jsonify({
                'success': True,
                'message': '성공적으로 로그아웃되었습니다.',
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"로그아웃 중 오류: {str(e)}")
            return jsonify({
                'error': f'로그아웃 중 오류가 발생했습니다: {str(e)}',
                'code': 'LOGOUT_ERROR'
            }), 500
    
    @app.route('/api/auth/profile', methods=['GET'])
    @jwt_required()
    def get_profile():
        """사용자 프로필 조회"""
        try:
            current_user = get_jwt_identity()
            user = auth_manager.users.get(current_user)
            
            if not user:
                return jsonify({
                    'error': '사용자를 찾을 수 없습니다.',
                    'code': 'USER_NOT_FOUND'
                }), 404
            
            return jsonify({
                'success': True,
                'user': {
                    'username': user['username'],
                    'role': user['role'],
                    'permissions': user['permissions'],
                    'created_at': user['created_at'],
                    'last_login': user['last_login']
                },
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"프로필 조회 중 오류: {str(e)}")
            return jsonify({
                'error': f'프로필 조회 중 오류가 발생했습니다: {str(e)}',
                'code': 'PROFILE_ERROR'
            }), 500
    
    @app.route('/api/auth/api-keys', methods=['GET'])
    @jwt_required()
    def get_api_keys():
        """API 키 목록 조회"""
        try:
            current_user = get_jwt_identity()
            user = auth_manager.users.get(current_user)
            
            if not user:
                return jsonify({
                    'error': '사용자를 찾을 수 없습니다.',
                    'code': 'USER_NOT_FOUND'
                }), 404
            
            # 사용자의 API 키들 조회
            user_api_keys = [
                {
                    'key_name': key_info['key_name'],
                    'created_at': key_info['created_at'],
                    'last_used': key_info['last_used'],
                    'is_active': key_info['is_active']
                }
                for api_key, key_info in auth_manager.api_keys.items()
                if key_info['username'] == current_user
            ]
            
            return jsonify({
                'success': True,
                'api_keys': user_api_keys,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"API 키 조회 중 오류: {str(e)}")
            return jsonify({
                'error': f'API 키 조회 중 오류가 발생했습니다: {str(e)}',
                'code': 'API_KEYS_ERROR'
            }), 500
    
    @app.route('/api/auth/api-keys', methods=['POST'])
    @jwt_required()
    def create_api_key():
        """새 API 키 생성"""
        try:
            current_user = get_jwt_identity()
            data = request.get_json()
            key_name = data.get('key_name', f'{current_user}_key_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
            
            # API 키 생성
            api_key = auth_manager._generate_api_key(current_user, key_name)
            
            return jsonify({
                'success': True,
                'api_key': api_key,
                'key_name': key_name,
                'message': 'API 키가 성공적으로 생성되었습니다.',
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"API 키 생성 중 오류: {str(e)}")
            return jsonify({
                'error': f'API 키 생성 중 오류가 발생했습니다: {str(e)}',
                'code': 'API_KEY_CREATE_ERROR'
            }), 500

def require_auth(permission='read'):
    """인증 데코레이터"""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            # JWT 토큰 확인
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({
                    'error': '인증 토큰이 필요합니다.',
                    'code': 'MISSING_TOKEN'
                }), 401
            
            token = auth_header.split(' ')[1]
            
            # 토큰 검증 (실제 구현에서는 JWT 검증 로직 사용)
            try:
                # 간단한 토큰 검증 (실제로는 JWT 라이브러리 사용)
                if token == 'valid_token':
                    return f(*args, **kwargs)
                else:
                    return jsonify({
                        'error': '유효하지 않은 토큰입니다.',
                        'code': 'INVALID_TOKEN'
                    }), 401
            except Exception as e:
                return jsonify({
                    'error': f'토큰 검증 중 오류가 발생했습니다: {str(e)}',
                    'code': 'TOKEN_VALIDATION_ERROR'
                }), 401
        
        return decorated_function
    return decorator

if __name__ == '__main__':
    # 테스트용 Flask 앱
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'test_secret_key'
    
    # 인증 시스템 초기화
    auth_manager.init_app(app)
    
    # 인증 라우트 생성
    create_auth_routes(app)
    
    print("🚀 API 인증 시스템 테스트 서버 시작")
    print("=" * 50)
    print("🔐 로그인: POST /api/auth/login")
    print("🔄 토큰 갱신: POST /api/auth/refresh")
    print("🚪 로그아웃: POST /api/auth/logout")
    print("👤 프로필: GET /api/auth/profile")
    print("🔑 API 키: GET/POST /api/auth/api-keys")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5002)
