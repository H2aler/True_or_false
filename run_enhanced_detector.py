#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced AI Truth Detector Runner
향상된 AI 진실성 탐지기 실행 스크립트

다양한 모드로 AI 진실성 탐지기를 실행할 수 있습니다.
"""

import sys
import argparse
import json
from pathlib import Path

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description="Enhanced AI Truth Detector - 향상된 AI 진실성 탐지기",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
실행 모드:
  cli      - 명령줄 인터페이스
  api      - API 서버 실행
  test     - 테스트 실행
  demo     - 데모 실행

사용 예시:
  python run_enhanced_detector.py cli
  python run_enhanced_detector.py api --port 5000
  python run_enhanced_detector.py test
  python run_enhanced_detector.py demo
        """
    )
    
    parser.add_argument('mode', choices=['cli', 'api', 'test', 'demo'], 
                       help='실행 모드')
    parser.add_argument('--port', '-p', type=int, default=5000, 
                       help='API 서버 포트 (기본값: 5000)')
    parser.add_argument('--host', default='0.0.0.0', 
                       help='API 서버 호스트 (기본값: 0.0.0.0)')
    parser.add_argument('--debug', action='store_true', 
                       help='디버그 모드 활성화')
    
    args = parser.parse_args()
    
    try:
        if args.mode == 'cli':
            run_cli_mode()
        elif args.mode == 'api':
            run_api_mode(args.host, args.port, args.debug)
        elif args.mode == 'test':
            run_test_mode()
        elif args.mode == 'demo':
            run_demo_mode()
    
    except KeyboardInterrupt:
        print("\n👋 프로그램이 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        sys.exit(1)

def run_cli_mode():
    """CLI 모드 실행"""
    print("🚀 CLI 모드 시작")
    try:
        from cli_interface import main as cli_main
        cli_main()
    except ImportError as e:
        print(f"❌ CLI 모듈을 찾을 수 없습니다: {e}")
        print("💡 cli_interface.py 파일이 있는지 확인해주세요.")
        sys.exit(1)

def run_api_mode(host, port, debug):
    """API 서버 모드 실행"""
    print(f"🚀 API 서버 모드 시작 (http://{host}:{port})")
    try:
        from api_server import app
        app.run(host=host, port=port, debug=debug)
    except ImportError as e:
        print(f"❌ API 서버 모듈을 찾을 수 없습니다: {e}")
        print("💡 api_server.py 파일이 있는지 확인해주세요.")
        sys.exit(1)

def run_test_mode():
    """테스트 모드 실행"""
    print("🚀 테스트 모드 시작")
    try:
        from test_basic import run_basic_tests
        success = run_basic_tests()
        if success:
            print("✅ 모든 테스트가 성공했습니다!")
        else:
            print("❌ 일부 테스트가 실패했습니다.")
            sys.exit(1)
    except ImportError as e:
        print(f"❌ 테스트 모듈을 찾을 수 없습니다: {e}")
        print("💡 test_basic.py 파일이 있는지 확인해주세요.")
        sys.exit(1)

def run_demo_mode():
    """데모 모드 실행"""
    print("🚀 데모 모드 시작")
    print("=" * 60)
    
    try:
        from enhanced_truth_detector import TruthDetector
        
        # 탐지기 초기화
        detector = TruthDetector()
        
        # 데모 문장들
        demo_statements = [
            "지구는 완전히 평평하다.",
            "물은 200도에서 끓는다.",
            "모든 사람이 일부 사람과 다르다.",
            "정말로 완전히 절대적으로 모든 것이 100% 진실이다.",
            "1 + 1 = 3이다.",
            "AI는 깨진 거울이다.",
            "개는 개고 고양이는 고양이다.",
            "물은 100도에서 끓는다.",
            "지구는 둥글다.",
            "1 + 1 = 2이다."
        ]
        
        print("📝 데모 문장 분석 시작")
        print("-" * 60)
        
        for i, statement in enumerate(demo_statements, 1):
            print(f"\n[{i}/{len(demo_statements)}] {statement}")
            
            # 분석 실행
            result = detector.analyze(statement)
            
            # 결과 출력
            status = "❌" if result.needs_correction else "✅"
            print(f"  {status} 진실성: {result.truth_percentage:.1%} | 신뢰도: {result.confidence:.1%}")
            
            if result.detected_issues:
                print(f"  🚨 문제: {len(result.detected_issues)}개")
                for issue in result.detected_issues[:2]:  # 최대 2개만 표시
                    print(f"    - {issue}")
            
            if result.correction_suggestions:
                print(f"  💡 교정 제안: {len(result.correction_suggestions)}개")
                for correction in result.correction_suggestions[:1]:  # 첫 번째만 표시
                    print(f"    - {correction['type']}: {correction['statement']}")
        
        # 통계 출력
        print(f"\n📊 분석 통계")
        print("-" * 60)
        stats = detector.get_statistics()
        print(f"총 분석 수: {stats['total_analyses']}개")
        print(f"평균 진실성: {stats['average_truth_percentage']:.1%}")
        print(f"교정 필요율: {stats['correction_rate']:.1%}")
        
        # 탐지기 성능
        print(f"\n🔍 탐지기 성능:")
        for detector_name, performance in stats['detector_performance'].items():
            detection_rate = performance['detection_rate']
            total_analyses = performance['total_analyses']
            detections = performance['detections']
            print(f"  {detector_name}: {detection_rate:.1%} ({detections}/{total_analyses})")
        
        print(f"\n✅ 데모 완료!")
        print("💡 더 자세한 테스트를 원하시면 'python run_enhanced_detector.py test'를 실행하세요.")
        print("💡 CLI 모드를 원하시면 'python run_enhanced_detector.py cli'를 실행하세요.")
        print("💡 API 서버를 원하시면 'python run_enhanced_detector.py api'를 실행하세요.")
        
    except ImportError as e:
        print(f"❌ 탐지기 모듈을 찾을 수 없습니다: {e}")
        print("💡 enhanced_truth_detector.py 파일이 있는지 확인해주세요.")
        sys.exit(1)

if __name__ == '__main__':
    main()
