#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrated System Starter
통합 시스템 시작 스크립트

웹 서버와 파이썬 API 서버를 함께 실행하는 통합 시스템입니다.
"""

import subprocess
import threading
import time
import webbrowser
import os
import sys
from pathlib import Path

def start_python_api_server():
    """파이썬 API 서버 시작"""
    print("🐍 파이썬 API 서버 시작 중...")
    try:
        # api_server.py 실행
        subprocess.run([sys.executable, "api_server.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 파이썬 API 서버 시작 실패: {e}")
    except KeyboardInterrupt:
        print("🛑 파이썬 API 서버 중단됨")

def start_web_server():
    """웹 서버 시작"""
    print("🌐 웹 서버 시작 중...")
    try:
        # Python의 내장 HTTP 서버 사용
        import http.server
        import socketserver
        from urllib.parse import urlparse
        
        PORT = 8080
        
        class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
            def end_headers(self):
                # CORS 헤더 추가
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                super().end_headers()
            
            def do_OPTIONS(self):
                # OPTIONS 요청 처리
                self.send_response(200)
                self.end_headers()
        
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"🌐 웹 서버가 http://localhost:{PORT} 에서 실행 중입니다.")
            print(f"📱 모바일에서 접속: http://{get_local_ip()}:{PORT}")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("🛑 웹 서버 중단됨")
    except Exception as e:
        print(f"❌ 웹 서버 시작 실패: {e}")

def get_local_ip():
    """로컬 IP 주소 가져오기"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def check_dependencies():
    """의존성 확인"""
    print("🔍 의존성 확인 중...")
    
    required_files = [
        "api_server.py",
        "enhanced_truth_detector.py", 
        "index.html",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 누락된 파일들: {', '.join(missing_files)}")
        return False
    
    # Python 패키지 확인
    try:
        import flask
        import flask_cors
        print("✅ Flask 및 Flask-CORS 설치됨")
    except ImportError as e:
        print(f"❌ 필요한 패키지가 설치되지 않음: {e}")
        print("💡 다음 명령어로 설치하세요: pip install -r requirements.txt")
        return False
    
    print("✅ 모든 의존성 확인 완료")
    return True

def open_browser():
    """브라우저 열기"""
    time.sleep(3)  # 서버 시작 대기
    try:
        webbrowser.open("http://localhost:8080")
        print("🌐 브라우저에서 웹 애플리케이션을 열었습니다.")
    except Exception as e:
        print(f"⚠️ 브라우저 자동 열기 실패: {e}")
        print("💡 수동으로 http://localhost:8080 에 접속하세요.")

def main():
    """메인 함수"""
    print("🚀 AI Truth Detector 통합 시스템 시작")
    print("=" * 60)
    
    # 의존성 확인
    if not check_dependencies():
        print("❌ 의존성 확인 실패. 시스템을 종료합니다.")
        sys.exit(1)
    
    print("\n📋 시스템 구성:")
    print("  🌐 웹 서버: http://localhost:8080")
    print("  🐍 API 서버: http://localhost:5000")
    print("  📱 모바일 접속: http://" + get_local_ip() + ":8080")
    print("\n💡 사용법:")
    print("  1. 웹 브라우저에서 http://localhost:8080 접속")
    print("  2. 문장을 입력하고 분석 버튼 클릭")
    print("  3. 파이썬 백엔드가 자동으로 연동됩니다")
    print("  4. Ctrl+C로 시스템 종료")
    print("=" * 60)
    
    try:
        # 파이썬 API 서버를 별도 스레드에서 실행
        api_thread = threading.Thread(target=start_python_api_server, daemon=True)
        api_thread.start()
        
        # 브라우저 열기를 별도 스레드에서 실행
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # 웹 서버를 메인 스레드에서 실행
        start_web_server()
        
    except KeyboardInterrupt:
        print("\n🛑 시스템 종료 중...")
        print("👋 AI Truth Detector를 사용해주셔서 감사합니다!")
    except Exception as e:
        print(f"❌ 시스템 오류: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
