#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI Interface for AI Truth Detector
AI 진실성 탐지기 명령줄 인터페이스

터미널에서 직접 사용할 수 있는 명령줄 인터페이스입니다.
"""

import argparse
import json
import sys
from typing import List, Optional
from enhanced_truth_detector import TruthDetector

class TruthDetectorCLI:
    """AI 진실성 탐지기 CLI 클래스"""
    
    def __init__(self):
        self.detector = TruthDetector()
    
    def analyze_single(self, statement: str, context: Optional[str] = None, 
                      show_details: bool = False, show_corrections: bool = True) -> None:
        """단일 문장 분석"""
        print(f"\n📝 분석 문장: {statement}")
        if context:
            print(f"📋 컨텍스트: {context}")
        print("-" * 60)
        
        # 분석 실행
        result = self.detector.analyze(statement, context)
        
        # 기본 결과 출력
        print(f"🎯 진실성: {result.truth_percentage:.1%}")
        print(f"🔍 신뢰도: {result.confidence:.1%}")
        print(f"⚠️  교정 필요: {'예' if result.needs_correction else '아니오'}")
        
        # 감지된 문제 출력
        if result.detected_issues:
            print(f"\n🚨 감지된 문제 ({len(result.detected_issues)}개):")
            for i, issue in enumerate(result.detected_issues, 1):
                print(f"  {i}. {issue}")
        
        # 교정 제안 출력
        if result.correction_suggestions and show_corrections:
            print(f"\n💡 교정 제안 ({len(result.correction_suggestions)}개):")
            for i, correction in enumerate(result.correction_suggestions, 1):
                print(f"  {i}. [{correction['type']}] {correction['statement']}")
                print(f"     📝 {correction['description']}")
        
        # 상세 정보 출력
        if show_details:
            print(f"\n🔬 상세 분석 결과:")
            print(f"  - 분석 ID: {result.analysis_id}")
            print(f"  - 분석 시간: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  - 탐지기 결과:")
            for detector_name, detector_result in result.detector_results.items():
                if 'error' not in detector_result:
                    truth_score = detector_result.get('truth_score', 0)
                    confidence = detector_result.get('confidence', 0)
                    issues = detector_result.get('issues', [])
                    print(f"    • {detector_name}: {truth_score:.2f} (신뢰도: {confidence:.2f})")
                    if issues:
                        print(f"      - {', '.join(issues)}")
    
    def analyze_batch(self, statements: List[str], context: Optional[str] = None,
                     show_summary: bool = True) -> None:
        """여러 문장 일괄 분석"""
        print(f"\n📚 일괄 분석 시작 ({len(statements)}개 문장)")
        if context:
            print(f"📋 컨텍스트: {context}")
        print("=" * 60)
        
        results = []
        for i, statement in enumerate(statements, 1):
            print(f"\n[{i}/{len(statements)}] {statement}")
            result = self.detector.analyze(statement, context)
            results.append(result)
            
            # 간단한 결과 출력
            status = "❌" if result.needs_correction else "✅"
            print(f"  {status} 진실성: {result.truth_percentage:.1%} | 신뢰도: {result.confidence:.1%}")
            
            if result.detected_issues:
                print(f"  🚨 문제: {len(result.detected_issues)}개")
        
        # 요약 통계 출력
        if show_summary:
            self._print_batch_summary(results)
    
    def _print_batch_summary(self, results: List) -> None:
        """일괄 분석 요약 출력"""
        print(f"\n📊 분석 요약")
        print("-" * 40)
        
        total = len(results)
        corrections_needed = sum(1 for r in results if r.needs_correction)
        avg_truth = sum(r.truth_percentage for r in results) / total
        avg_confidence = sum(r.confidence for r in results) / total
        
        print(f"총 분석 문장: {total}개")
        print(f"교정 필요: {corrections_needed}개 ({corrections_needed/total:.1%})")
        print(f"평균 진실성: {avg_truth:.1%}")
        print(f"평균 신뢰도: {avg_confidence:.1%}")
        
        # 진실성 분포
        high_truth = sum(1 for r in results if r.truth_percentage >= 0.8)
        medium_truth = sum(1 for r in results if 0.5 <= r.truth_percentage < 0.8)
        low_truth = sum(1 for r in results if r.truth_percentage < 0.5)
        
        print(f"\n진실성 분포:")
        print(f"  높음 (≥80%): {high_truth}개 ({high_truth/total:.1%})")
        print(f"  중간 (50-79%): {medium_truth}개 ({medium_truth/total:.1%})")
        print(f"  낮음 (<50%): {low_truth}개 ({low_truth/total:.1%})")
    
    def show_statistics(self) -> None:
        """통계 정보 출력"""
        stats = self.detector.get_statistics()
        
        print(f"\n📈 시스템 통계")
        print("=" * 40)
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
        
        # 최근 트렌드
        if stats['recent_trends']:
            print(f"\n📊 최근 트렌드 (최근 {len(stats['recent_trends'])}개):")
            for trend in stats['recent_trends'][-5:]:  # 최근 5개만 표시
                status = "❌" if trend['needs_correction'] else "✅"
                print(f"  {status} {trend['statement']} - {trend['truth_percentage']:.1%}")
    
    def interactive_mode(self) -> None:
        """대화형 모드"""
        print("🤖 AI 진실성 탐지기 대화형 모드")
        print("=" * 40)
        print("명령어:")
        print("  analyze <문장> - 문장 분석")
        print("  context <컨텍스트> - 컨텍스트 설정")
        print("  stats - 통계 보기")
        print("  help - 도움말")
        print("  quit - 종료")
        print("-" * 40)
        
        context = None
        
        while True:
            try:
                command = input("\n> ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['quit', 'exit', 'q']:
                    print("👋 안녕히 가세요!")
                    break
                
                elif command.lower() == 'help':
                    print("도움말:")
                    print("  analyze <문장> - 문장을 분석합니다")
                    print("  context <컨텍스트> - 분석 컨텍스트를 설정합니다")
                    print("  stats - 시스템 통계를 보여줍니다")
                    print("  quit - 프로그램을 종료합니다")
                
                elif command.lower() == 'stats':
                    self.show_statistics()
                
                elif command.startswith('context '):
                    context = command[8:].strip()
                    print(f"✅ 컨텍스트 설정: {context}")
                
                elif command.startswith('analyze '):
                    statement = command[8:].strip()
                    if statement:
                        self.analyze_single(statement, context, show_details=True)
                    else:
                        print("❌ 분석할 문장을 입력해주세요.")
                
                else:
                    # 명령어가 없으면 직접 문장으로 간주
                    self.analyze_single(command, context, show_details=True)
            
            except KeyboardInterrupt:
                print("\n👋 안녕히 가세요!")
                break
            except Exception as e:
                print(f"❌ 오류 발생: {e}")

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description="AI Truth Detector - AI 진실성 탐지기",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python cli_interface.py "지구는 평평하다"
  python cli_interface.py --batch statements.txt
  python cli_interface.py --interactive
  python cli_interface.py --stats
        """
    )
    
    parser.add_argument('statement', nargs='?', help='분석할 문장')
    parser.add_argument('--context', '-c', help='분석 컨텍스트')
    parser.add_argument('--batch', '-b', help='일괄 분석할 파일 경로')
    parser.add_argument('--interactive', '-i', action='store_true', help='대화형 모드')
    parser.add_argument('--stats', '-s', action='store_true', help='통계 보기')
    parser.add_argument('--details', '-d', action='store_true', help='상세 정보 출력')
    parser.add_argument('--no-corrections', action='store_true', help='교정 제안 숨기기')
    parser.add_argument('--output', '-o', help='결과를 JSON 파일로 저장')
    
    args = parser.parse_args()
    
    cli = TruthDetectorCLI()
    
    try:
        if args.interactive:
            cli.interactive_mode()
        
        elif args.stats:
            cli.show_statistics()
        
        elif args.batch:
            # 파일에서 문장들 읽기
            try:
                with open(args.batch, 'r', encoding='utf-8') as f:
                    statements = [line.strip() for line in f if line.strip()]
                
                if not statements:
                    print("❌ 파일에 분석할 문장이 없습니다.")
                    sys.exit(1)
                
                cli.analyze_batch(statements, args.context)
                
            except FileNotFoundError:
                print(f"❌ 파일을 찾을 수 없습니다: {args.batch}")
                sys.exit(1)
            except Exception as e:
                print(f"❌ 파일 읽기 오류: {e}")
                sys.exit(1)
        
        elif args.statement:
            cli.analyze_single(
                args.statement, 
                args.context, 
                show_details=args.details,
                show_corrections=not args.no_corrections
            )
        
        else:
            # 인수 없이 실행하면 대화형 모드
            cli.interactive_mode()
    
    except KeyboardInterrupt:
        print("\n👋 프로그램이 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
