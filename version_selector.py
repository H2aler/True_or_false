"""
버전 선택 시스템
기존 버전과 엔터프라이즈 버전을 선택할 수 있는 시스템
"""

import os
import sys
from typing import Dict, Any, Optional
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import logging

class VersionSelector:
    """버전 선택 관리자"""
    
    def __init__(self):
        self.versions = {
            'basic': {
                'name': 'Basic Version',
                'description': '기본 AI 진실성 탐지기',
                'features': [
                    '기본 진실성 탐지',
                    '웹 연구 기능',
                    '간단한 분석',
                    '기본 UI'
                ],
                'port': 5000,
                'app_file': 'app_basic.py',
                'template_dir': 'templates/basic',
                'static_dir': 'static/basic'
            },
            'enterprise': {
                'name': 'Enterprise Edition',
                'description': '엔터프라이즈급 AI 진실성 탐지기',
                'features': [
                    '고급 머신러닝 모델',
                    '45개 API 엔드포인트',
                    '실시간 알림 시스템',
                    'JWT 인증',
                    'Docker 지원',
                    '고급 분석 기능',
                    '다국어 지원'
                ],
                'port': 5001,
                'app_file': 'app.py',
                'template_dir': 'templates',
                'static_dir': 'static'
            }
        }
        
        self.current_version = None
        self.logger = logging.getLogger(__name__)
    
    def get_version_info(self, version: str) -> Optional[Dict[str, Any]]:
        """버전 정보 가져오기"""
        return self.versions.get(version)
    
    def get_all_versions(self) -> Dict[str, Any]:
        """모든 버전 정보 가져오기"""
        return self.versions
    
    def set_current_version(self, version: str) -> bool:
        """현재 버전 설정"""
        if version in self.versions:
            self.current_version = version
            return True
        return False
    
    def get_current_version(self) -> Optional[str]:
        """현재 버전 가져오기"""
        return self.current_version
    
    def is_version_available(self, version: str) -> bool:
        """버전 사용 가능 여부 확인"""
        if version not in self.versions:
            return False
        
        version_info = self.versions[version]
        app_file = version_info['app_file']
        
        # 앱 파일 존재 여부 확인
        return os.path.exists(app_file)
    
    def get_available_versions(self) -> Dict[str, Any]:
        """사용 가능한 버전들 가져오기"""
        available = {}
        for version, info in self.versions.items():
            if self.is_version_available(version):
                available[version] = info
        return available

# 버전 선택기 인스턴스
version_selector = VersionSelector()

def create_version_selector_app():
    """버전 선택 웹 애플리케이션 생성"""
    app = Flask(__name__)
    app.secret_key = 'version_selector_secret_key_2024'
    
    # CORS 설정
    CORS(app, origins=['*'], methods=['GET', 'POST'], allow_headers=['Content-Type'])
    
    @app.route('/')
    def index():
        """메인 페이지 - 버전 선택"""
        available_versions = version_selector.get_available_versions()
        return render_template('version_selector.html', 
                             versions=available_versions,
                             current_version=version_selector.get_current_version())
    
    @app.route('/select_version', methods=['POST'])
    def select_version():
        """버전 선택 처리"""
        try:
            data = request.get_json()
            version = data.get('version')
            
            if not version:
                return jsonify({'success': False, 'message': '버전이 지정되지 않았습니다.'}), 400
            
            if not version_selector.is_version_available(version):
                return jsonify({'success': False, 'message': f'버전 {version}을 사용할 수 없습니다.'}), 400
            
            # 버전 설정
            if version_selector.set_current_version(version):
                version_info = version_selector.get_version_info(version)
                session['selected_version'] = version
                
                return jsonify({
                    'success': True, 
                    'message': f'{version_info["name"]}이 선택되었습니다.',
                    'redirect_url': f'/launch/{version}'
                })
            else:
                return jsonify({'success': False, 'message': '버전 설정에 실패했습니다.'}), 500
                
        except Exception as e:
            return jsonify({'success': False, 'message': f'오류가 발생했습니다: {str(e)}'}), 500
    
    @app.route('/launch/<version>')
    def launch_version(version):
        """선택된 버전 실행"""
        if not version_selector.is_version_available(version):
            return render_template('error.html', 
                                 message=f'버전 {version}을 사용할 수 없습니다.')
        
        version_info = version_selector.get_version_info(version)
        session['selected_version'] = version
        
        return render_template('launch.html', 
                             version=version,
                             version_info=version_info)
    
    @app.route('/api/versions')
    def api_versions():
        """API: 사용 가능한 버전 목록"""
        available_versions = version_selector.get_available_versions()
        return jsonify({
            'success': True,
            'versions': available_versions,
            'current_version': version_selector.get_current_version()
        })
    
    @app.route('/api/version_info/<version>')
    def api_version_info(version):
        """API: 특정 버전 정보"""
        if not version_selector.is_version_available(version):
            return jsonify({'success': False, 'message': '버전을 찾을 수 없습니다.'}), 404
        
        version_info = version_selector.get_version_info(version)
        return jsonify({
            'success': True,
            'version': version,
            'info': version_info
        })
    
    return app

if __name__ == '__main__':
    app = create_version_selector_app()
    app.run(debug=True, host='0.0.0.0', port=3000)
