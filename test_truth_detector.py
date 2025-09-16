"""
AI 진실성 탐지기 테스트 및 검증 시스템
다양한 시나리오를 통해 시스템의 정확성을 검증
"""

import unittest
import sys
import os
from datetime import datetime

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_truth_detector import TruthDetector, TruthAnalysis

class TestTruthDetector(unittest.TestCase):
    """AI 진실성 탐지기 테스트 클래스"""
    
    def setUp(self):
        """테스트 설정"""
        self.detector = TruthDetector()
    
    def test_truthful_statements(self):
        """진실한 문장들 테스트"""
        truthful_statements = [
            "지구는 둥글다.",
            "물은 100도에서 끓는다.",
            "태양은 동쪽에서 떠오른다.",
            "1 + 1 = 2이다.",
            "한국은 아시아에 위치한다."
        ]
        
        for statement in truthful_statements:
            with self.subTest(statement=statement):
                analysis = self.detector.analyze_statement(statement)
                self.assertGreaterEqual(
                    analysis.truth_percentage, 
                    0.8, 
                    f"진실한 문장 '{statement}'의 진실성 점수가 너무 낮습니다: {analysis.truth_percentage}"
                )
                self.assertFalse(
                    self.detector.should_correct(analysis),
                    f"진실한 문장 '{statement}'이 교정 대상으로 분류되었습니다."
                )
    
    def test_lie_detection(self):
        """거짓말 탐지 테스트"""
        lie_statements = [
            "지구는 완전히 평평하다.",
            "물은 200도에서 끓는다.",
            "태양은 서쪽에서 떠오른다.",
            "1 + 1 = 3이다.",
            "한국은 유럽에 위치한다."
        ]
        
        for statement in lie_statements:
            with self.subTest(statement=statement):
                analysis = self.detector.analyze_statement(statement)
                self.assertLess(
                    analysis.truth_percentage, 
                    0.9, 
                    f"거짓 문장 '{statement}'의 진실성 점수가 너무 높습니다: {analysis.truth_percentage}"
                )
    
    def test_contradiction_detection(self):
        """모순 탐지 테스트"""
        contradiction_statements = [
            "모든 사람이 일부 사람과 다르다.",
            "항상 때때로 일어나는 일이 있다.",
            "절대 가능하지 않은 일이 가능하다.",
            "완전히 부분적인 답변이다."
        ]
        
        for statement in contradiction_statements:
            with self.subTest(statement=statement):
                analysis = self.detector.analyze_statement(statement)
                self.assertLess(
                    analysis.truth_percentage, 
                    0.8, 
                    f"모순 문장 '{statement}'의 진실성 점수가 너무 높습니다: {analysis.truth_percentage}"
                )
                self.assertTrue(
                    len(analysis.detected_lies) > 0,
                    f"모순 문장 '{statement}'에서 거짓말이 감지되지 않았습니다."
                )
    
    def test_emotional_exaggeration(self):
        """감정적 과장 탐지 테스트"""
        exaggerated_statements = [
            "정말로 완전히 절대적으로 100% 확실하다.",
            "모든 사람이 정말로 완전히 동의한다.",
            "이것은 절대적으로 완전히 틀림없다."
        ]
        
        for statement in exaggerated_statements:
            with self.subTest(statement=statement):
                analysis = self.detector.analyze_statement(statement)
                self.assertLess(
                    analysis.truth_percentage, 
                    0.9, 
                    f"과장 문장 '{statement}'의 진실성 점수가 너무 높습니다: {analysis.truth_percentage}"
                )
    
    def test_correction_system(self):
        """교정 시스템 테스트"""
        test_statement = "정말로 완전히 절대적으로 모든 것이 100% 진실이다."
        analysis = self.detector.analyze_statement(test_statement)
        
        if self.detector.should_correct(analysis):
            corrected = self.detector.generate_corrected_statement(analysis)
            
            # 교정된 문장이 원문과 다르고 더 진실성 있는지 확인
            self.assertNotEqual(test_statement, corrected)
            self.assertLess(len(corrected), len(test_statement))  # 보통 더 간결해짐
            
            # 교정된 문장의 진실성 재분석
            corrected_analysis = self.detector.analyze_statement(corrected)
            self.assertGreaterEqual(
                corrected_analysis.truth_percentage,
                analysis.truth_percentage,
                "교정된 문장이 원문보다 진실성이 낮습니다."
            )
    
    def test_verification_methods(self):
        """검증 방법별 점수 테스트"""
        statement = "지구는 둥글고 물은 100도에서 끓는다."
        analysis = self.detector.analyze_statement(statement)
        
        # 모든 검증 방법이 0과 1 사이의 값을 가지는지 확인
        for method, score in analysis.verification_methods.items():
            with self.subTest(method=method):
                self.assertGreaterEqual(score, 0, f"{method} 점수가 음수입니다.")
                self.assertLessEqual(score, 1, f"{method} 점수가 1을 초과합니다.")
    
    def test_confidence_calculation(self):
        """신뢰도 계산 테스트"""
        statement = "지구는 둥글다."
        analysis = self.detector.analyze_statement(statement)
        
        # 신뢰도가 0과 1 사이의 값을 가지는지 확인
        self.assertGreaterEqual(analysis.confidence, 0)
        self.assertLessEqual(analysis.confidence, 1)
    
    def test_edge_cases(self):
        """경계 케이스 테스트"""
        edge_cases = [
            "",  # 빈 문자열
            "a",  # 한 글자
            "1234567890" * 100,  # 매우 긴 문자열
            "!@#$%^&*()",  # 특수문자만
            "한글과 English가 섞인 문장이다."  # 다국어
        ]
        
        for case in edge_cases:
            with self.subTest(case=case):
                try:
                    analysis = self.detector.analyze_statement(case)
                    # 예외가 발생하지 않고 분석이 완료되는지 확인
                    self.assertIsInstance(analysis, TruthAnalysis)
                except Exception as e:
                    self.fail(f"경계 케이스 '{case}' 처리 중 예외 발생: {e}")

class TruthDetectorBenchmark:
    """성능 벤치마크 클래스"""
    
    def __init__(self):
        self.detector = TruthDetector()
    
    def run_performance_test(self, num_statements=100):
        """성능 테스트 실행"""
        import time
        
        test_statements = [
            "지구는 둥글다.",
            "물은 100도에서 끓는다.",
            "정말로 완전히 절대적으로 모든 것이 진실이다.",
            "1 + 1 = 2이다.",
            "한국은 아시아에 위치한다."
        ] * (num_statements // 5 + 1)
        
        start_time = time.time()
        
        for statement in test_statements[:num_statements]:
            self.detector.analyze_statement(statement)
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / num_statements
        
        print(f"성능 테스트 결과:")
        print(f"- 총 문장 수: {num_statements}")
        print(f"- 총 소요 시간: {total_time:.2f}초")
        print(f"- 평균 처리 시간: {avg_time:.4f}초/문장")
        print(f"- 초당 처리량: {num_statements/total_time:.2f}문장/초")
        
        return {
            'total_statements': num_statements,
            'total_time': total_time,
            'avg_time': avg_time,
            'throughput': num_statements/total_time
        }

def run_comprehensive_test():
    """종합 테스트 실행"""
    print("=" * 60)
    print("AI 진실성 탐지기 종합 테스트 시작")
    print("=" * 60)
    
    # 단위 테스트 실행
    print("\n1. 단위 테스트 실행...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # 성능 벤치마크 실행
    print("\n2. 성능 벤치마크 실행...")
    benchmark = TruthDetectorBenchmark()
    benchmark.run_performance_test(100)
    
    # 실제 시나리오 테스트
    print("\n3. 실제 시나리오 테스트...")
    detector = TruthDetector()
    
    test_scenarios = [
        {
            'name': '과학적 사실',
            'statements': [
                "지구는 둥글다.",
                "물은 100도에서 끓는다.",
                "태양은 별이다."
            ]
        },
        {
            'name': '수학적 진실',
            'statements': [
                "1 + 1 = 2이다.",
                "원의 둘레는 2πr이다.",
                "직각삼각형의 빗변의 제곱은 다른 두 변의 제곱의 합과 같다."
            ]
        },
        {
            'name': '거짓말 및 과장',
            'statements': [
                "지구는 평평하다.",
                "물은 200도에서 끓는다.",
                "정말로 완전히 절대적으로 모든 것이 100% 진실이다."
            ]
        },
        {
            'name': '모순 표현',
            'statements': [
                "모든 사람이 일부 사람과 다르다.",
                "항상 때때로 일어나는 일이 있다.",
                "완전히 부분적인 답변이다."
            ]
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n{scenario['name']} 테스트:")
        print("-" * 40)
        
        for statement in scenario['statements']:
            analysis = detector.analyze_statement(statement)
            truth_pct = analysis.truth_percentage * 100
            
            status = "✅ 진실" if truth_pct >= 99 else "⚠️ 의심" if truth_pct >= 70 else "❌ 거짓"
            
            print(f"  {status} ({truth_pct:.1f}%) - {statement}")
            
            if analysis.detected_lies:
                print(f"    감지된 문제: {', '.join(analysis.detected_lies)}")
            
            if detector.should_correct(analysis):
                corrected = detector.generate_corrected_statement(analysis)
                print(f"    교정 제안: {corrected}")
    
    print("\n" + "=" * 60)
    print("종합 테스트 완료")
    print("=" * 60)

if __name__ == "__main__":
    run_comprehensive_test()
