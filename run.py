#!/usr/bin/env python3
"""
AI 진실성 탐지기 실행 스크립트
시스템을 시작하고 초기 설정을 수행합니다.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """의존성 패키지 확인"""
    print("🔍 의존성 패키지 확인 중...")
    
    required_packages = [
        'flask', 'numpy', 'scikit-learn', 'transformers', 
        'torch', 'requests', 'beautifulsoup4', 'textblob', 
        'nltk', 'plotly', 'dash', 'pandas', 'matplotlib', 'seaborn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  누락된 패키지: {', '.join(missing_packages)}")
        print("다음 명령어로 설치하세요:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ 모든 의존성 패키지가 설치되어 있습니다.")
    return True

def run_tests():
    """테스트 실행"""
    print("\n🧪 테스트 실행 중...")
    
    try:
        result = subprocess.run([sys.executable, 'test_truth_detector.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ 모든 테스트가 통과했습니다.")
            return True
        else:
            print("❌ 일부 테스트가 실패했습니다.")
            print("에러 출력:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ 테스트 실행 시간이 초과되었습니다.")
        return False
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {e}")
        return False

def start_web_app():
    """웹 애플리케이션 시작"""
    print("\n🚀 웹 애플리케이션 시작 중...")
    
    try:
        # Flask 앱 실행
        os.system(f"{sys.executable} app.py")
        
    except KeyboardInterrupt:
        print("\n👋 애플리케이션이 종료되었습니다.")
    except Exception as e:
        print(f"❌ 애플리케이션 실행 중 오류 발생: {e}")

def show_banner():
    """시작 배너 표시"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                🤖 AI 진실성 탐지기 🛡️                        ║
    ║                                                              ║
    ║  "AI는 깨진 거울이다"                                        ║
    ║  AI의 거짓말을 탐지하고 교정하는 시스템                      ║
    ║                                                              ║
    ║  ✨ 주요 기능:                                               ║
    ║     • 다중 검증 방법으로 진실성 측정                         ║
    ║     • 1% 이상 거짓말 감지 시 자동 교정                       ║
    ║     • 실시간 대시보드 및 시각화                              ║
    ║     • 웹 기반 사용자 인터페이스                              ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """메인 실행 함수"""
    show_banner()
    
    # 의존성 확인
    if not check_dependencies():
        print("\n❌ 의존성 패키지가 누락되어 있습니다. 설치 후 다시 실행하세요.")
        return
    
    # 테스트 실행 (선택사항)
    print("\n❓ 테스트를 실행하시겠습니까? (y/n): ", end="")
    run_test = input().lower().strip()
    
    if run_test in ['y', 'yes', '예', 'ㅇ']:
        if not run_tests():
            print("\n⚠️  테스트가 실패했지만 계속 진행합니다.")
    
    # 웹 애플리케이션 시작
    print("\n🌐 웹 애플리케이션을 시작합니다...")
    print("브라우저에서 http://localhost:5000 으로 접속하세요.")
    print("종료하려면 Ctrl+C를 누르세요.\n")
    
    time.sleep(2)
    start_web_app()

if __name__ == "__main__":
    main()
