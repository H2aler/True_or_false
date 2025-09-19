"""
AI 진실성 탐지기 버전 통합 실행 스크립트
기존 버전과 엔터프라이즈 버전을 선택하여 실행할 수 있는 통합 시스템
"""

import os
import sys
import subprocess
import threading
import time
import signal
import logging
from typing import Dict, Any, Optional
import webbrowser
from flask import Flask
from version_selector import create_version_selector_app

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VersionManager:
    """버전 관리자"""
    
    def __init__(self):
        self.processes = {}
        self.ports = {
            'selector': 3000,
            'basic': 5000,
            'enterprise': 5001
        }
        self.running = False
        
    def start_version_selector(self):
        """버전 선택기 시작"""
        try:
            logger.info("버전 선택기 시작 중...")
            app = create_version_selector_app()
            app.run(debug=False, host='0.0.0.0', port=self.ports['selector'])
        except Exception as e:
            logger.error(f"버전 선택기 시작 실패: {e}")
    
    def start_basic_version(self):
        """기본 버전 시작"""
        try:
            logger.info("기본 버전 시작 중...")
            # app_basic.py 실행
            process = subprocess.Popen([
                sys.executable, 'app_basic.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes['basic'] = process
            logger.info(f"기본 버전이 포트 {self.ports['basic']}에서 시작되었습니다.")
            
        except Exception as e:
            logger.error(f"기본 버전 시작 실패: {e}")
    
    def start_enterprise_version(self):
        """엔터프라이즈 버전 시작"""
        try:
            logger.info("엔터프라이즈 버전 시작 중...")
            # app.py 실행
            process = subprocess.Popen([
                sys.executable, 'app.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes['enterprise'] = process
            logger.info(f"엔터프라이즈 버전이 포트 {self.ports['enterprise']}에서 시작되었습니다.")
            
        except Exception as e:
            logger.error(f"엔터프라이즈 버전 시작 실패: {e}")
    
    def stop_all_versions(self):
        """모든 버전 중지"""
        logger.info("모든 버전 중지 중...")
        
        for name, process in self.processes.items():
            try:
                if process and process.poll() is None:
                    process.terminate()
                    process.wait(timeout=5)
                    logger.info(f"{name} 버전이 중지되었습니다.")
            except Exception as e:
                logger.error(f"{name} 버전 중지 실패: {e}")
        
        self.processes.clear()
        self.running = False
    
    def check_version_status(self, version: str) -> bool:
        """버전 상태 확인"""
        if version not in self.processes:
            return False
        
        process = self.processes[version]
        return process and process.poll() is None
    
    def get_version_url(self, version: str) -> str:
        """버전별 URL 가져오기"""
        if version == 'basic':
            return f"http://localhost:{self.ports['basic']}"
        elif version == 'enterprise':
            return f"http://localhost:{self.ports['enterprise']}"
        else:
            return f"http://localhost:{self.ports['selector']}"

def signal_handler(signum, frame):
    """시그널 핸들러"""
    logger.info("종료 신호를 받았습니다. 모든 프로세스를 중지합니다...")
    version_manager.stop_all_versions()
    sys.exit(0)

def main():
    """메인 함수"""
    global version_manager
    version_manager = VersionManager()
    
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        print("=" * 60)
        print("🤖 AI 진실성 탐지기 - 버전 통합 실행 시스템")
        print("=" * 60)
        print()
        print("사용 가능한 옵션:")
        print("1. 버전 선택기 시작 (웹 인터페이스)")
        print("2. 기본 버전 직접 시작")
        print("3. 엔터프라이즈 버전 직접 시작")
        print("4. 모든 버전 동시 시작")
        print("5. 종료")
        print()
        
        while True:
            try:
                choice = input("선택하세요 (1-5): ").strip()
                
                if choice == '1':
                    print("\n🌐 버전 선택기를 시작합니다...")
                    print(f"웹 브라우저에서 http://localhost:{version_manager.ports['selector']} 을 열어주세요.")
                    print("Ctrl+C를 눌러 종료할 수 있습니다.")
                    print()
                    
                    # 웹 브라우저 자동 열기
                    try:
                        webbrowser.open(f"http://localhost:{version_manager.ports['selector']}")
                    except:
                        pass
                    
                    version_manager.start_version_selector()
                    break
                
                elif choice == '2':
                    print("\n⭐ 기본 버전을 시작합니다...")
                    print(f"웹 브라우저에서 http://localhost:{version_manager.ports['basic']} 을 열어주세요.")
                    print("Ctrl+C를 눌러 종료할 수 있습니다.")
                    print()
                    
                    # 웹 브라우저 자동 열기
                    try:
                        webbrowser.open(f"http://localhost:{version_manager.ports['basic']}")
                    except:
                        pass
                    
                    version_manager.start_basic_version()
                    break
                
                elif choice == '3':
                    print("\n🚀 엔터프라이즈 버전을 시작합니다...")
                    print(f"웹 브라우저에서 http://localhost:{version_manager.ports['enterprise']} 을 열어주세요.")
                    print("Ctrl+C를 눌러 종료할 수 있습니다.")
                    print()
                    
                    # 웹 브라우저 자동 열기
                    try:
                        webbrowser.open(f"http://localhost:{version_manager.ports['enterprise']}")
                    except:
                        pass
                    
                    version_manager.start_enterprise_version()
                    break
                
                elif choice == '4':
                    print("\n🔄 모든 버전을 동시에 시작합니다...")
                    print("버전 선택기: http://localhost:3000")
                    print("기본 버전: http://localhost:5000")
                    print("엔터프라이즈 버전: http://localhost:5001")
                    print("Ctrl+C를 눌러 종료할 수 있습니다.")
                    print()
                    
                    # 모든 버전 시작
                    version_manager.running = True
                    
                    # 기본 버전 시작
                    basic_thread = threading.Thread(target=version_manager.start_basic_version)
                    basic_thread.daemon = True
                    basic_thread.start()
                    
                    # 엔터프라이즈 버전 시작
                    enterprise_thread = threading.Thread(target=version_manager.start_enterprise_version)
                    enterprise_thread.daemon = True
                    enterprise_thread.start()
                    
                    # 잠시 대기
                    time.sleep(3)
                    
                    # 버전 선택기 시작
                    try:
                        webbrowser.open("http://localhost:3000")
                    except:
                        pass
                    
                    version_manager.start_version_selector()
                    break
                
                elif choice == '5':
                    print("\n👋 프로그램을 종료합니다.")
                    break
                
                else:
                    print("❌ 잘못된 선택입니다. 1-5 중에서 선택해주세요.")
                    print()
            
            except KeyboardInterrupt:
                print("\n\n👋 프로그램을 종료합니다.")
                break
            except Exception as e:
                print(f"❌ 오류가 발생했습니다: {e}")
                print()
    
    except Exception as e:
        logger.error(f"프로그램 실행 중 오류: {e}")
    finally:
        version_manager.stop_all_versions()

if __name__ == '__main__':
    main()
