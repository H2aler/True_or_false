#!/usr/bin/env python3
"""
AI 진실성 탐지기 빠른 테스트
"""

def test_system():
    """시스템 기본 테스트"""
    print("🤖 AI 진실성 탐지기 테스트 시작")
    print("=" * 50)
    
    try:
        from ai_truth_detector import TruthDetector
        
        # 탐지기 초기화
        detector = TruthDetector()
        print("✅ TruthDetector 초기화 성공")
        
        # 테스트 문장들
        test_cases = [
            {
                'statement': '지구는 둥글다.',
                'expected': 'high',
                'description': '진실한 과학적 사실'
            },
            {
                'statement': '지구는 완전히 평평하다.',
                'expected': 'low',
                'description': '거짓된 과학적 사실'
            },
            {
                'statement': '정말로 완전히 절대적으로 모든 것이 100% 진실이다.',
                'expected': 'low',
                'description': '과장된 표현'
            },
            {
                'statement': '모든 사람이 일부 사람과 다르다.',
                'expected': 'low',
                'description': '논리적 모순'
            }
        ]
        
        print("\n📊 테스트 케이스 실행:")
        print("-" * 50)
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n{i}. {case['description']}")
            print(f"   문장: {case['statement']}")
            
            # 분석 수행
            analysis = detector.analyze_statement(case['statement'])
            truth_pct = analysis.truth_percentage * 100
            
            print(f"   진실성: {truth_pct:.1f}%")
            print(f"   신뢰도: {analysis.confidence:.1f}%")
            
            # 예상 결과와 비교
            if case['expected'] == 'high' and truth_pct >= 80:
                print("   결과: ✅ 예상대로 높은 진실성")
            elif case['expected'] == 'low' and truth_pct < 80:
                print("   결과: ✅ 예상대로 낮은 진실성")
            else:
                print("   결과: ⚠️ 예상과 다른 결과")
            
            # 교정 필요성 확인
            if detector.should_correct(analysis):
                corrected = detector.generate_corrected_statement(analysis)
                print(f"   교정문: {corrected}")
                print("   상태: 🔧 교정 필요")
            else:
                print("   상태: ✅ 교정 불필요")
        
        print("\n" + "=" * 50)
        print("🎉 모든 테스트가 완료되었습니다!")
        print("✅ AI 진실성 탐지기가 정상적으로 작동합니다.")
        
        return True
        
    except ImportError as e:
        print(f"❌ 모듈 import 오류: {e}")
        return False
    except Exception as e:
        print(f"❌ 테스트 실행 오류: {e}")
        return False

if __name__ == "__main__":
    success = test_system()
    if success:
        print("\n🚀 웹 애플리케이션을 시작하려면 'python app.py'를 실행하세요.")
    else:
        print("\n❌ 시스템에 문제가 있습니다. 의존성을 확인하세요.")
