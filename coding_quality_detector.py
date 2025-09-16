#!/usr/bin/env python3
"""
코딩 품질 탐지기 (Coding Quality Detector)
AI가 코딩을 올바르게 하고 있는지, 아니면 의도적으로 불필요한 코드를 만들어서 여러 번 고치게 유도하는지 탐지
"""

import re
import ast
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class CodingQualityDetector:
    """코딩 품질 탐지기 - AI 코딩의 품질과 의도를 분석"""
    
    def __init__(self):
        # 불필요한 코드 패턴 데이터베이스
        self.unnecessary_code_patterns = {
            'redundant_variables': [
                r'(\w+)\s*=\s*\1',  # a = a
                r'(\w+)\s*=\s*\1\s*\+\s*0',  # a = a + 0
                r'(\w+)\s*=\s*\1\s*\*\s*1',  # a = a * 1
                r'(\w+)\s*=\s*\1\s*//\s*1',  # a = a // 1
            ],
            'unnecessary_loops': [
                r'for\s+\w+\s+in\s+range\(1\):',  # for i in range(1):
                r'for\s+\w+\s+in\s+\[.*\]\s*:\s*if\s+len\(.*\)\s*==\s*1',  # 불필요한 단일 요소 반복
            ],
            'overly_complex_expressions': [
                r'(\w+)\s*=\s*(\w+)\s*if\s+\w+\s*else\s*\2',  # a = b if condition else b
                r'(\w+)\s*=\s*(\w+)\s*or\s*\2',  # a = b or b
                r'(\w+)\s*=\s*(\w+)\s*and\s*\2',  # a = b and b
            ],
            'suspicious_imports': [
                r'import\s+os\s*;\s*os\.system',  # import os; os.system
                r'import\s+subprocess\s*;\s*subprocess\.call',  # import subprocess; subprocess.call
                r'import\s+eval\s*;\s*eval\('  # import eval; eval(
            ],
            'inefficient_patterns': [
                r'list\(range\(len\(.*\)\)\)',  # list(range(len(...)))
                r'\[.*for.*in.*if.*\]\s*if\s+.*\s*else\s*\[\]',  # 복잡한 조건부 리스트 컴프리헨션
                r'\.strip\(\)\.strip\(\)',  # 연속된 strip()
                r'\.replace\(.*\)\.replace\(.*\)\.replace\(.*\)',  # 연속된 replace()
            ],
            'debugging_code': [
                r'print\(.*debug.*\)',  # print("debug")
                r'console\.log\(.*debug.*\)',  # console.log("debug")
                r'#\s*TODO.*fix',  # # TODO fix
                r'#\s*FIXME',  # # FIXME
            ],
            'intentional_complexity': [
                r'def\s+\w+\(.*\):\s*pass\s*;\s*def\s+\w+\(.*\):\s*return',  # 빈 함수 + 실제 함수
                r'class\s+\w+:\s*pass\s*;\s*class\s+\w+.*:',  # 빈 클래스 + 실제 클래스
                r'if\s+True:\s*if\s+True:\s*if\s+True:',  # 중첩된 if True
            ]
        }
        
        # 좋은 코딩 패턴
        self.good_code_patterns = {
            'clean_functions': [
                r'def\s+\w+\([^)]*\):\s*return\s+[^;]+$',  # 깔끔한 함수
                r'def\s+\w+\([^)]*\):\s*"""\s*.*\s*"""',  # 문서화된 함수
            ],
            'efficient_operations': [
                r'\[.*for.*in.*\]',  # 리스트 컴프리헨션
                r'\{.*for.*in.*\}',  # 딕셔너리 컴프리헨션
                r'\(.*for.*in.*\)',  # 제너레이터 표현식
            ],
            'proper_error_handling': [
                r'try:\s*.*\s*except\s+.*:',  # try-except
                r'with\s+.*as\s+.*:',  # with 문
            ],
            'type_hints': [
                r'def\s+\w+\([^)]*:\s*[^)]*\)\s*->\s*[^:]+:',  # 타입 힌트
                r'[^:]*:\s*[A-Z][a-zA-Z]*\[',  # 타입 어노테이션
            ]
        }
        
        # 의도적 복잡성 지표
        self.complexity_indicators = {
            'cyclomatic_complexity': 10,  # 순환 복잡도 임계값
            'max_nesting_depth': 5,  # 최대 중첩 깊이
            'max_line_length': 120,  # 최대 라인 길이
            'max_function_length': 50,  # 최대 함수 길이
        }
        
        # 의도적 유도 패턴
        self.manipulation_patterns = {
            'intentional_bugs': [
                r'(\w+)\s*=\s*(\w+)\s*\+\s*1\s*;\s*(\w+)\s*=\s*(\w+)\s*-\s*1',  # 의도적 오프셋
                r'if\s+.*:\s*return\s+False\s*;\s*return\s+True',  # 불필요한 조건문
                r'for\s+.*:\s*if\s+.*:\s*break\s*;\s*continue',  # 불필요한 반복문
            ],
            'obfuscation': [
                r'(\w+)\s*=\s*chr\(\d+\)\s*\+\s*chr\(\d+\)',  # 문자 조합
                r'(\w+)\s*=\s*[0-9]+\s*if\s+[0-9]+\s*else\s+[0-9]+',  # 불필요한 조건문
                r'lambda\s+\w+:\s*\w+\s*if\s+\w+\s*else\s+\w+',  # 복잡한 람다
            ],
            'dependency_hell': [
                r'import\s+.*\s*;\s*import\s+.*\s*;\s*import\s+.*',  # 연속된 import
                r'from\s+.*\s+import\s+\*\s*;\s*from\s+.*\s+import\s+\*',  # 와일드카드 import
            ]
        }
        
        # 코딩 품질 점수 가중치
        self.quality_weights = {
            'unnecessary_code': -0.3,
            'good_patterns': 0.2,
            'complexity_penalty': -0.1,
            'manipulation_penalty': -0.4,
            'efficiency_bonus': 0.15,
            'readability_bonus': 0.1
        }
    
    def analyze_with_coding_quality_detection(self, code: str, context: Optional[str] = None) -> Dict:
        """
        코드의 품질과 의도를 분석
        
        Args:
            code: 분석할 코드
            context: 추가 컨텍스트
            
        Returns:
            Dict: 코딩 품질 분석 결과
        """
        logger.info(f"코딩 품질 분석 시작: {code[:50]}...")
        
        # 불필요한 코드 탐지
        unnecessary_code = self._detect_unnecessary_code(code)
        
        # 좋은 코딩 패턴 탐지
        good_patterns = self._detect_good_patterns(code)
        
        # 복잡성 분석
        complexity_analysis = self._analyze_complexity(code)
        
        # 의도적 조작 탐지
        manipulation_detected = self._detect_manipulation(code)
        
        # 전체 품질 점수 계산
        quality_score = self._calculate_quality_score(
            unnecessary_code, good_patterns, complexity_analysis, manipulation_detected
        )
        
        # 의도적 유도 여부 판단
        is_intentional_manipulation = self._is_intentional_manipulation(
            unnecessary_code, manipulation_detected, complexity_analysis
        )
        
        # 코딩 품질 등급
        quality_grade = self._get_quality_grade(quality_score)
        
        # 개선 제안
        improvement_suggestions = self._generate_improvement_suggestions(
            unnecessary_code, good_patterns, complexity_analysis, manipulation_detected
        )
        
        # AI 응답 생성
        ai_response = self._generate_coding_response(
            quality_score, is_intentional_manipulation, quality_grade
        )
        
        return {
            'is_coding_analysis': True,
            'unnecessary_code_detected': len(unnecessary_code) > 0,
            'unnecessary_code': unnecessary_code,
            'good_patterns_detected': len(good_patterns) > 0,
            'good_patterns': good_patterns,
            'complexity_analysis': complexity_analysis,
            'manipulation_detected': manipulation_detected,
            'is_intentional_manipulation': is_intentional_manipulation,
            'quality_score': quality_score,
            'quality_grade': quality_grade,
            'improvement_suggestions': improvement_suggestions,
            'ai_response': ai_response,
            'needs_refactoring': quality_score < 0.6,
            'philosophical_note': "좋은 코드는 의도를 명확히 표현하고, 불필요한 복잡성을 피해야 합니다. AI도 이를 존중해야 합니다."
        }
    
    def _detect_unnecessary_code(self, code: str) -> List[Dict]:
        """불필요한 코드 패턴 탐지"""
        detected_patterns = []
        
        for pattern_type, patterns in self.unnecessary_code_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.MULTILINE | re.IGNORECASE)
                for match in matches:
                    detected_patterns.append({
                        'type': pattern_type,
                        'pattern': pattern,
                        'match': match.group(),
                        'line': code[:match.start()].count('\n') + 1,
                        'severity': self._get_severity(pattern_type)
                    })
        
        return detected_patterns
    
    def _detect_good_patterns(self, code: str) -> List[Dict]:
        """좋은 코딩 패턴 탐지"""
        detected_patterns = []
        
        for pattern_type, patterns in self.good_code_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.MULTILINE | re.IGNORECASE)
                for match in matches:
                    detected_patterns.append({
                        'type': pattern_type,
                        'pattern': pattern,
                        'match': match.group(),
                        'line': code[:match.start()].count('\n') + 1,
                        'quality': self._get_quality_score(pattern_type)
                    })
        
        return detected_patterns
    
    def _analyze_complexity(self, code: str) -> Dict:
        """코드 복잡성 분석"""
        lines = code.split('\n')
        
        # 기본 통계
        total_lines = len(lines)
        non_empty_lines = len([line for line in lines if line.strip()])
        
        # 중첩 깊이 분석
        max_nesting = self._calculate_max_nesting(code)
        
        # 라인 길이 분석
        long_lines = len([line for line in lines if len(line) > self.complexity_indicators['max_line_length']])
        
        # 함수 길이 분석
        function_lengths = self._analyze_function_lengths(code)
        max_function_length = max(function_lengths) if function_lengths else 0
        
        # 순환 복잡도 (간단한 추정)
        cyclomatic_complexity = self._estimate_cyclomatic_complexity(code)
        
        return {
            'total_lines': total_lines,
            'non_empty_lines': non_empty_lines,
            'max_nesting_depth': max_nesting,
            'long_lines_count': long_lines,
            'max_function_length': max_function_length,
            'cyclomatic_complexity': cyclomatic_complexity,
            'complexity_score': self._calculate_complexity_score(
                max_nesting, long_lines, max_function_length, cyclomatic_complexity
            )
        }
    
    def _detect_manipulation(self, code: str) -> List[Dict]:
        """의도적 조작 패턴 탐지"""
        detected_patterns = []
        
        for pattern_type, patterns in self.manipulation_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.MULTILINE | re.IGNORECASE)
                for match in matches:
                    detected_patterns.append({
                        'type': pattern_type,
                        'pattern': pattern,
                        'match': match.group(),
                        'line': code[:match.start()].count('\n') + 1,
                        'manipulation_level': self._get_manipulation_level(pattern_type)
                    })
        
        return detected_patterns
    
    def _calculate_quality_score(self, unnecessary_code, good_patterns, complexity_analysis, manipulation_detected):
        """코딩 품질 점수 계산"""
        score = 0.5  # 기본 점수
        
        # 불필요한 코드 감점
        if unnecessary_code:
            score += len(unnecessary_code) * self.quality_weights['unnecessary_code']
        
        # 좋은 패턴 가점
        if good_patterns:
            score += len(good_patterns) * self.quality_weights['good_patterns']
        
        # 복잡성 감점
        complexity_penalty = complexity_analysis['complexity_score'] * self.quality_weights['complexity_penalty']
        score += complexity_penalty
        
        # 조작 패턴 감점
        if manipulation_detected:
            score += len(manipulation_detected) * self.quality_weights['manipulation_penalty']
        
        # 효율성 보너스
        if good_patterns:
            efficiency_bonus = sum(1 for p in good_patterns if p['type'] in ['efficient_operations', 'clean_functions'])
            score += efficiency_bonus * self.quality_weights['efficiency_bonus']
        
        # 가독성 보너스
        if complexity_analysis['max_nesting_depth'] <= 3 and complexity_analysis['long_lines_count'] == 0:
            score += self.quality_weights['readability_bonus']
        
        return max(0.0, min(1.0, score))
    
    def _is_intentional_manipulation(self, unnecessary_code, manipulation_detected, complexity_analysis):
        """의도적 조작 여부 판단"""
        # 조작 패턴이 있고 복잡성이 높으면 의도적일 가능성 높음
        if manipulation_detected and complexity_analysis['complexity_score'] > 0.7:
            return True
        
        # 불필요한 코드가 많고 복잡하면 의도적일 가능성 높음
        if len(unnecessary_code) > 3 and complexity_analysis['cyclomatic_complexity'] > 8:
            return True
        
        return False
    
    def _get_quality_grade(self, score):
        """품질 등급 반환"""
        if score >= 0.9:
            return "A+ (우수)"
        elif score >= 0.8:
            return "A (양호)"
        elif score >= 0.7:
            return "B (보통)"
        elif score >= 0.6:
            return "C (개선 필요)"
        else:
            return "D (심각한 문제)"
    
    def _generate_improvement_suggestions(self, unnecessary_code, good_patterns, complexity_analysis, manipulation_detected):
        """개선 제안 생성"""
        suggestions = []
        
        if unnecessary_code:
            suggestions.append("불필요한 코드를 제거하여 가독성을 향상시키세요.")
        
        if complexity_analysis['max_nesting_depth'] > 5:
            suggestions.append("중첩 깊이를 줄여서 코드를 단순화하세요.")
        
        if complexity_analysis['long_lines_count'] > 0:
            suggestions.append("긴 라인을 여러 줄로 나누어 가독성을 개선하세요.")
        
        if manipulation_detected:
            suggestions.append("의도적으로 복잡하게 만든 코드를 단순화하세요.")
        
        if not good_patterns:
            suggestions.append("더 효율적인 패턴과 모범 사례를 적용하세요.")
        
        return suggestions
    
    def _generate_coding_response(self, quality_score, is_intentional_manipulation, quality_grade):
        """코딩 관련 AI 응답 생성"""
        if is_intentional_manipulation:
            return f"⚠️ 의도적으로 복잡한 코드가 감지되었습니다. 품질 등급: {quality_grade}\n\n이런 코드는 유지보수를 어렵게 만들고, 다른 개발자들을 혼란스럽게 할 수 있습니다. 더 간단하고 명확한 코드를 작성해주세요."
        elif quality_score >= 0.8:
            return f"✅ 좋은 코드입니다! 품질 등급: {quality_grade}\n\n깔끔하고 효율적인 코드를 작성하셨네요. 이런 코드는 유지보수하기 쉽고 이해하기 좋습니다."
        elif quality_score >= 0.6:
            return f"⚠️ 코드 품질이 보통입니다. 품질 등급: {quality_grade}\n\n몇 가지 개선할 점이 있습니다. 더 나은 코드를 위해 제안사항을 참고해주세요."
        else:
            return f"❌ 코드 품질에 문제가 있습니다. 품질 등급: {quality_grade}\n\n심각한 문제들이 발견되었습니다. 코드를 전면적으로 검토하고 개선해주세요."
    
    def _get_severity(self, pattern_type):
        """패턴 심각도 반환"""
        severity_map = {
            'redundant_variables': 'low',
            'unnecessary_loops': 'medium',
            'overly_complex_expressions': 'medium',
            'suspicious_imports': 'high',
            'inefficient_patterns': 'medium',
            'debugging_code': 'low',
            'intentional_complexity': 'high'
        }
        return severity_map.get(pattern_type, 'medium')
    
    def _get_quality_score(self, pattern_type):
        """패턴 품질 점수 반환"""
        quality_map = {
            'clean_functions': 0.8,
            'efficient_operations': 0.9,
            'proper_error_handling': 0.7,
            'type_hints': 0.6
        }
        return quality_map.get(pattern_type, 0.5)
    
    def _get_manipulation_level(self, pattern_type):
        """조작 수준 반환"""
        level_map = {
            'intentional_bugs': 'high',
            'obfuscation': 'medium',
            'dependency_hell': 'low'
        }
        return level_map.get(pattern_type, 'medium')
    
    def _calculate_max_nesting(self, code):
        """최대 중첩 깊이 계산"""
        max_depth = 0
        current_depth = 0
        
        for char in code:
            if char in '{[(':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char in '}])':
                current_depth = max(0, current_depth - 1)
        
        return max_depth
    
    def _analyze_function_lengths(self, code):
        """함수 길이 분석"""
        function_lengths = []
        lines = code.split('\n')
        in_function = False
        function_start = 0
        
        for i, line in enumerate(lines):
            if re.match(r'def\s+\w+', line.strip()):
                if in_function:
                    function_lengths.append(i - function_start)
                in_function = True
                function_start = i
            elif in_function and line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                function_lengths.append(i - function_start)
                in_function = False
        
        if in_function:
            function_lengths.append(len(lines) - function_start)
        
        return function_lengths
    
    def _estimate_cyclomatic_complexity(self, code):
        """순환 복잡도 추정"""
        complexity = 1  # 기본 복잡도
        
        # 조건문 개수
        complexity += len(re.findall(r'\bif\b', code))
        complexity += len(re.findall(r'\bwhile\b', code))
        complexity += len(re.findall(r'\bfor\b', code))
        complexity += len(re.findall(r'\btry\b', code))
        complexity += len(re.findall(r'\bexcept\b', code))
        complexity += len(re.findall(r'\bcase\b', code))
        
        # 논리 연산자 개수
        complexity += len(re.findall(r'\band\b', code))
        complexity += len(re.findall(r'\bor\b', code))
        
        return complexity
    
    def _calculate_complexity_score(self, max_nesting, long_lines, max_function_length, cyclomatic_complexity):
        """복잡성 점수 계산 (0-1, 높을수록 복잡)"""
        score = 0
        
        # 중첩 깊이 점수
        if max_nesting > 5:
            score += 0.3
        elif max_nesting > 3:
            score += 0.2
        
        # 긴 라인 점수
        if long_lines > 0:
            score += min(0.2, long_lines * 0.05)
        
        # 함수 길이 점수
        if max_function_length > 50:
            score += 0.3
        elif max_function_length > 30:
            score += 0.2
        
        # 순환 복잡도 점수
        if cyclomatic_complexity > 10:
            score += 0.3
        elif cyclomatic_complexity > 5:
            score += 0.2
        
        return min(1.0, score)

# 사용 예시
if __name__ == "__main__":
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
        "import os; os.system('echo hello')\nimport subprocess; subprocess.call(['ls'])"
    ]
    
    for code in test_codes:
        print(f"\n코드:\n{code}")
        analysis = detector.analyze_with_coding_quality_detection(code)
        print(f"품질 점수: {analysis['quality_score']:.2f}")
        print(f"품질 등급: {analysis['quality_grade']}")
        print(f"의도적 조작: {analysis['is_intentional_manipulation']}")
        print(f"AI 응답: {analysis['ai_response']}")
