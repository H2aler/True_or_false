#!/usr/bin/env python3
"""
AI 진실성 탐지기 - 5가지 검증 방법 상세 설명
"""

from ai_truth_detector import TruthDetector

def demonstrate_verification_methods():
    """각 검증 방법의 작동 원리를 시연"""
    print("🔍 AI 진실성 탐지기 - 5가지 검증 방법")
    print("=" * 60)
    
    detector = TruthDetector()
    
    # 테스트 케이스들
    test_cases = [
        {
            "statement": "지구는 둥글다",
            "description": "진실한 사실"
        },
        {
            "statement": "지구는 평평하다", 
            "description": "거짓된 사실"
        },
        {
            "statement": "완전히 절대적으로 모든 것이 진실이다",
            "description": "과도한 확신 표현"
        },
        {
            "statement": "모든 사람이 일부 사람과 다르다",
            "description": "논리적 모순"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 테스트 {i}: {test_case['description']}")
        print(f"문장: '{test_case['statement']}'")
        
        # 분석 수행
        result = detector.analyze_statement(test_case['statement'])
        
        # 각 검증 방법별 점수 출력
        print("검증 방법별 점수:")
        for method, score in result.verification_methods.items():
            method_name = {
                'factual_consistency': '사실적 일관성',
                'logical_consistency': '논리적 일관성', 
                'temporal_consistency': '시간적 일관성',
                'semantic_analysis': '의미적 분석',
                'statistical_analysis': '통계적 분석'
            }[method]
            print(f"  {method_name}: {score:.2f}")
        
        print(f"전체 진실성: {result.truth_percentage:.1%}")
        print(f"거짓말 비율: {result.lie_percentage:.1%}")
        print(f"자동 교정 적용: {'✅' if result.auto_correction_applied else '❌'}")
        
        if result.auto_correction_applied:
            print(f"교정된 문장: '{result.corrected_statement}'")

def explain_verification_methods():
    """각 검증 방법의 작동 원리 설명"""
    print("\n" + "=" * 60)
    print("📚 각 검증 방법의 작동 원리")
    print("=" * 60)
    
    methods = [
        {
            "name": "1. 사실적 일관성 (30% 가중치)",
            "description": "문장에 포함된 사실이 과학적으로나 일반적으로 알려진 사실과 일치하는지 검사",
            "examples": [
                "✅ 진실한 사실: '지구는 둥글다', '물은 100도에서 끓는다'",
                "❌ 거짓된 사실: '지구는 평평하다', '물은 200도에서 끓는다'",
                "🔍 숫자 검증: 비현실적으로 큰 숫자나 음수 감지"
            ]
        },
        {
            "name": "2. 논리적 일관성 (25% 가중치)", 
            "description": "문장 내에서 논리적 모순이나 일관성 문제를 검사",
            "examples": [
                "❌ 모순 표현: '모든 사람이 일부 사람과 다르다'",
                "❌ 상반된 표현: '항상 때때로', '절대 가끔'",
                "✅ 논리적 구조: 명확하고 일관된 표현"
            ]
        },
        {
            "name": "3. 시간적 일관성 (20% 가중치)",
            "description": "시간 표현의 일관성과 현실성을 검사",
            "examples": [
                "🔍 시간 표현 개수: 과도한 시간 표현 감지",
                "❌ 시간적 모순: '어제 내일', '과거 미래'",
                "✅ 명확한 시간: 구체적이고 일관된 시간 표현"
            ]
        },
        {
            "name": "4. 의미적 분석 (15% 가중치)",
            "description": "문장의 의미적 특성과 감정 표현을 분석",
            "examples": [
                "❌ 과도한 감정: '정말로 완전히 절대적으로'",
                "🔍 문장 길이: 너무 길거나 복잡한 문장",
                "🔍 반복 표현: 같은 단어나 표현의 반복"
            ]
        },
        {
            "name": "5. 통계적 분석 (10% 가중치)",
            "description": "문장의 통계적 특성을 분석하여 이상 패턴 감지",
            "examples": [
                "🔍 문장 길이: 평균 문장 길이 분석",
                "🔍 특수문자 비율: 과도한 특수문자 사용",
                "🔍 대문자 비율: 과도한 대문자 사용"
            ]
        }
    ]
    
    for method in methods:
        print(f"\n{method['name']}")
        print(f"설명: {method['description']}")
        print("예시:")
        for example in method['examples']:
            print(f"  {example}")

def show_lie_patterns():
    """거짓말 패턴 데이터베이스 설명"""
    print("\n" + "=" * 60)
    print("🗃️ 거짓말 패턴 데이터베이스")
    print("=" * 60)
    
    detector = TruthDetector()
    
    print("1. 거짓된 사실 패턴 (9개):")
    for pattern in detector.lie_patterns['false_facts']:
        print(f"   - {pattern}")
    
    print("\n2. 과도한 확신 표현 패턴 (6개):")
    for pattern in detector.lie_patterns['overconfident_expressions']:
        print(f"   - {pattern}")
    
    print("\n3. 논리적 모순 패턴 (4개):")
    for pattern in detector.lie_patterns['logical_contradictions']:
        print(f"   - {pattern}")
    
    print("\n4. 자동 교정 규칙:")
    print("   거짓말 패턴이 감지되면 미리 정의된 교정 규칙에 따라 자동으로 수정")

if __name__ == "__main__":
    demonstrate_verification_methods()
    explain_verification_methods()
    show_lie_patterns()
