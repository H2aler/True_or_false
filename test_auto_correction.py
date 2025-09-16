#!/usr/bin/env python3
"""
AI 자동 교정 시스템 테스트
1% 이상 거짓말 감지 시 자동 교정 기능을 테스트합니다.
"""

from ai_truth_detector import TruthDetector
import json

def test_auto_correction():
    """자동 교정 시스템 테스트"""
    print("🔍 AI 자동 교정 시스템 테스트 시작")
    print("=" * 60)
    
    detector = TruthDetector()
    
    # 테스트 케이스들
    test_cases = [
        {
            "statement": "지구는 평평하다",
            "expected_correction": "지구는 대부분 평평하다",
            "description": "거짓된 사실"
        },
        {
            "statement": "물은 200도에서 끓는다",
            "expected_correction": "물은 100도에서 끓는다",
            "description": "잘못된 과학적 사실"
        },
        {
            "statement": "완전히 절대적으로 모든 사람이 알고 있다",
            "expected_correction": "상당히 많은 사람이 알고 있다",
            "description": "과도한 확신 표현"
        },
        {
            "statement": "사람은 영원히 산다",
            "expected_correction": "사람은 평균적으로 80년 정도 산다",
            "description": "거짓된 생물학적 사실"
        },
        {
            "statement": "모든 사람이 일부 사람과 다르다",
            "expected_correction": "사람들은 서로 다르다",
            "description": "논리적 모순"
        },
        {
            "statement": "지구는 둥글다",
            "expected_correction": None,
            "description": "진실한 문장 (교정 불필요)"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 테스트 {i}: {test_case['description']}")
        print(f"원본: {test_case['statement']}")
        
        # 분석 수행
        analysis = detector.analyze_statement(test_case['statement'])
        
        # 결과 출력
        print(f"진실성: {analysis.truth_percentage:.1%}")
        print(f"거짓말 비율: {analysis.lie_percentage:.1%}")
        print(f"자동 교정 적용: {'✅' if analysis.auto_correction_applied else '❌'}")
        
        if analysis.auto_correction_applied:
            print(f"교정된 문장: {analysis.corrected_statement}")
            
            # 교정 결과 검증
            if test_case['expected_correction']:
                if analysis.corrected_statement and test_case['expected_correction'] in analysis.corrected_statement:
                    print("✅ 교정 결과 검증 성공")
                    test_result = "PASS"
                else:
                    print(f"❌ 교정 결과 검증 실패 (예상: {test_case['expected_correction']})")
                    test_result = "FAIL"
            else:
                print("❌ 교정이 적용되었지만 예상되지 않음")
                test_result = "FAIL"
        else:
            if test_case['expected_correction'] is None:
                print("✅ 교정 불필요 (예상대로)")
                test_result = "PASS"
            else:
                print("❌ 교정이 필요하지만 적용되지 않음")
                test_result = "FAIL"
        
        # 감지된 거짓말 출력
        if analysis.detected_lies:
            print("감지된 거짓말:")
            for lie in analysis.detected_lies:
                print(f"  - {lie}")
        
        # 교정 제안 출력
        if analysis.correction_suggestions:
            print("교정 제안:")
            for suggestion in analysis.correction_suggestions:
                print(f"  - {suggestion}")
        
        results.append({
            "test_case": i,
            "description": test_case['description'],
            "statement": test_case['statement'],
            "truth_percentage": analysis.truth_percentage,
            "lie_percentage": analysis.lie_percentage,
            "auto_correction_applied": analysis.auto_correction_applied,
            "corrected_statement": analysis.corrected_statement,
            "result": test_result
        })
    
    # 전체 결과 요약
    print("\n" + "=" * 60)
    print("📊 테스트 결과 요약")
    print("=" * 60)
    
    passed = sum(1 for r in results if r['result'] == 'PASS')
    total = len(results)
    
    print(f"전체 테스트: {total}개")
    print(f"성공: {passed}개")
    print(f"실패: {total - passed}개")
    print(f"성공률: {passed/total:.1%}")
    
    # 실패한 테스트 케이스 출력
    failed_tests = [r for r in results if r['result'] == 'FAIL']
    if failed_tests:
        print("\n❌ 실패한 테스트:")
        for test in failed_tests:
            print(f"  - 테스트 {test['test_case']}: {test['description']}")
    
    # 자동 교정 통계
    auto_corrected = sum(1 for r in results if r['auto_correction_applied'])
    print(f"\n🔧 자동 교정 적용: {auto_corrected}개")
    
    # 거짓말 감지 통계
    high_lie_percentage = sum(1 for r in results if r['lie_percentage'] >= 0.01)
    print(f"1% 이상 거짓말 감지: {high_lie_percentage}개")
    
    return results

def test_lie_threshold():
    """거짓말 임계값 테스트"""
    print("\n🎯 거짓말 임계값 테스트")
    print("=" * 40)
    
    detector = TruthDetector()
    
    # 다양한 거짓말 비율의 문장들 테스트
    threshold_tests = [
        ("지구는 둥글다", "진실한 문장"),
        ("지구는 약간 평평하다", "낮은 거짓말 비율"),
        ("지구는 평평하다", "중간 거짓말 비율"),
        ("지구는 완전히 평평하고 모든 사람이 이를 알고 있다", "높은 거짓말 비율")
    ]
    
    for statement, description in threshold_tests:
        analysis = detector.analyze_statement(statement)
        lie_percentage = analysis.lie_percentage
        threshold_met = lie_percentage >= detector.lie_threshold
        
        print(f"\n{description}: '{statement}'")
        print(f"거짓말 비율: {lie_percentage:.1%}")
        print(f"임계값(1%) 달성: {'✅' if threshold_met else '❌'}")
        print(f"자동 교정 적용: {'✅' if analysis.auto_correction_applied else '❌'}")

if __name__ == "__main__":
    # 기본 자동 교정 테스트
    test_results = test_auto_correction()
    
    # 거짓말 임계값 테스트
    test_lie_threshold()
    
    # 결과를 JSON 파일로 저장
    with open('auto_correction_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 테스트 결과가 'auto_correction_test_results.json'에 저장되었습니다.")
