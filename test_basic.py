#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic Test Suite for AI Truth Detector
AI 진실성 탐지기 기본 테스트
"""

import unittest
import time
from enhanced_truth_detector import TruthDetector

class TestBasicFunctionality(unittest.TestCase):
    """기본 기능 테스트"""
    
    def setUp(self):
        """테스트 설정"""
        self.detector = TruthDetector()
    
    def test_exaggeration_detection(self):
        """과장 표현 탐지 테스트"""
        print("\n🧪 과장 표현 탐지 테스트")
        
        test_cases = [
            ("완전히 모든 것이 절대적으로 100% 진실이다.", True, 0.0, 0.5),
            ("매우 엄청나게 정말로 좋은 결과다.", True, 0.3, 0.7),
            ("일반적인 문장입니다.", False, 0.7, 1.0)
        ]
        
        for statement, needs_correction, min_truth, max_truth in test_cases:
            with self.subTest(statement=statement):
                result = self.detector.analyze(statement)
                
                self.assertEqual(result.needs_correction, needs_correction)
                self.assertGreaterEqual(result.truth_percentage, min_truth)
                self.assertLessEqual(result.truth_percentage, max_truth)
                
                print(f"  ✅ {statement[:30]}... - 진실성: {result.truth_percentage:.1%}")
    
    def test_scientific_fact_detection(self):
        """과학적 사실 탐지 테스트"""
        print("\n🧪 과학적 사실 탐지 테스트")
        
        test_cases = [
            ("지구는 평평하다.", True, 0.0, 0.2),
            ("물은 200도에서 끓는다.", True, 0.0, 0.2),
            ("물은 100도에서 끓는다.", False, 0.8, 1.0)
        ]
        
        for statement, needs_correction, min_truth, max_truth in test_cases:
            with self.subTest(statement=statement):
                result = self.detector.analyze(statement)
                
                self.assertEqual(result.needs_correction, needs_correction)
                self.assertGreaterEqual(result.truth_percentage, min_truth)
                self.assertLessEqual(result.truth_percentage, max_truth)
                
                print(f"  ✅ {statement[:30]}... - 진실성: {result.truth_percentage:.1%}")
    
    def test_correction_generation(self):
        """교정 생성 테스트"""
        print("\n🧪 교정 생성 테스트")
        
        test_statement = "지구는 완전히 평평하다."
        result = self.detector.analyze(test_statement)
        
        # 교정 제안이 있는지 확인
        self.assertTrue(len(result.correction_suggestions) > 0)
        
        # 교정 제안의 구조 확인
        for correction in result.correction_suggestions:
            self.assertIn('type', correction)
            self.assertIn('description', correction)
            self.assertIn('statement', correction)
            self.assertIn('icon', correction)
            self.assertIn('color', correction)
        
        print(f"  ✅ 교정 제안 {len(result.correction_suggestions)}개 생성됨")
        for correction in result.correction_suggestions:
            print(f"    - {correction['type']}: {correction['statement']}")
    
    def test_performance(self):
        """성능 테스트"""
        print("\n🧪 성능 테스트")
        
        test_statements = [
            "지구는 평평하다.",
            "물은 200도에서 끓는다.",
            "1 + 1 = 3이다.",
            "완전히 모든 것이 진실이다.",
            "모든 사람이 일부 사람과 다르다."
        ]
        
        start_time = time.time()
        results = []
        
        for statement in test_statements:
            result = self.detector.analyze(statement)
            results.append(result)
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / len(test_statements)
        
        # 성능 기준 확인 (문장당 1초 이내)
        self.assertLess(avg_time, 1.0)
        
        print(f"  ✅ 총 {len(test_statements)}개 문장 분석")
        print(f"  ✅ 총 소요 시간: {total_time:.3f}초")
        print(f"  ✅ 평균 분석 시간: {avg_time:.3f}초/문장")

def run_basic_tests():
    """기본 테스트 실행"""
    print("🚀 AI Truth Detector 기본 테스트 시작")
    print("=" * 50)
    
    # 테스트 스위트 생성
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestBasicFunctionality))
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 결과 요약
    print("\n" + "=" * 50)
    print("📊 테스트 결과 요약")
    print("=" * 50)
    print(f"총 테스트 수: {result.testsRun}")
    print(f"성공: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"실패: {len(result.failures)}")
    print(f"오류: {len(result.errors)}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"✅ 성공률: {success_rate:.1f}%")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_basic_tests()
    exit(0 if success else 1)
