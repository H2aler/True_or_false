#!/usr/bin/env python3
"""
코딩 품질 탐지기 테스트
"""

from coding_quality_detector import CodingQualityDetector

def test_coding_detector():
    detector = CodingQualityDetector()
    
    # 테스트 코드들
    test_codes = [
        # 좋은 코드
        "def calculate_sum(numbers):\n    return sum(numbers)",
        
        # 불필요한 코드
        "a = 5\na = a + 0\nb = a\nb = b * 1",
        
        # 의도적으로 복잡한 코드
        "def complex_function(x):\n    if True:\n        if True:\n            if True:\n                return x if x else x",
        
        # 조작 패턴
        "import os; os.system('echo hello')\nimport subprocess; subprocess.call(['ls'])",
        
        # 효율적인 코드
        "numbers = [1, 2, 3, 4, 5]\nsquared = [n**2 for n in numbers if n % 2 == 0]"
    ]
    
    print('💻 AI 코딩 품질 분석 테스트')
    print('=' * 60)
    
    for i, code in enumerate(test_codes, 1):
        print(f'\n테스트 {i}:')
        print(f'코드:\n{code}')
        analysis = detector.analyze_with_coding_quality_detection(code)
        
        print(f'품질 점수: {analysis["quality_score"]:.2f}')
        print(f'품질 등급: {analysis["quality_grade"]}')
        print(f'불필요한 코드: {analysis["unnecessary_code_detected"]}')
        print(f'의도적 조작: {analysis["is_intentional_manipulation"]}')
        print(f'AI 응답: {analysis["ai_response"][:100]}...')
    
    print('\n' + '=' * 60)
    print('🎯 코딩 품질 테스트 완료!')

if __name__ == "__main__":
    test_coding_detector()
