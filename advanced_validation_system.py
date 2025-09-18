#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Validation System
고급 검증 및 신뢰도 시스템

ChatGPT/Claude 수준의 입력 검증, 오류 처리, 신뢰도 평가를 제공합니다.
"""

import re
import json
import logging
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import hashlib
import asyncio
from concurrent.futures import ThreadPoolExecutor
import traceback

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ValidationLevel(Enum):
    """검증 수준"""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    ENTERPRISE = "enterprise"

class ConfidenceLevel(Enum):
    """신뢰도 수준"""
    VERY_LOW = 0.0
    LOW = 0.25
    MEDIUM = 0.5
    HIGH = 0.75
    VERY_HIGH = 0.95
    MAXIMUM = 1.0

@dataclass
class ValidationResult:
    """검증 결과"""
    is_valid: bool
    confidence: float
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    validation_level: ValidationLevel
    processing_time: float
    timestamp: datetime

@dataclass
class AnalysisRequest:
    """분석 요청"""
    statement: str
    context: str
    analysis_mode: str
    validation_level: ValidationLevel
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: str = ""
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if not self.request_id:
            self.request_id = self._generate_request_id()

    def _generate_request_id(self) -> str:
        """요청 ID 생성"""
        content = f"{self.statement}|{self.context}|{self.analysis_mode}|{self.timestamp.isoformat()}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()[:16]

class AdvancedValidationSystem:
    """고급 검증 시스템"""
    
    def __init__(self):
        self.validation_rules = self._initialize_validation_rules()
        self.confidence_weights = self._initialize_confidence_weights()
        self.error_patterns = self._initialize_error_patterns()
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def _initialize_validation_rules(self) -> Dict[ValidationLevel, Dict[str, Any]]:
        """검증 규칙 초기화"""
        return {
            ValidationLevel.BASIC: {
                'min_length': 1,
                'max_length': 1000,
                'allowed_chars': r'[\w\s가-힣.,!?;:()\-\[\]{}"\']+',
                'required_fields': ['statement'],
                'timeout': 5.0
            },
            ValidationLevel.STANDARD: {
                'min_length': 3,
                'max_length': 2000,
                'allowed_chars': r'[\w\s가-힣.,!?;:()\-\[\]{}"\'\n\t]+',
                'required_fields': ['statement'],
                'forbidden_patterns': [r'<script.*?>', r'javascript:', r'data:'],
                'timeout': 10.0
            },
            ValidationLevel.STRICT: {
                'min_length': 5,
                'max_length': 5000,
                'allowed_chars': r'[\w\s가-힣.,!?;:()\-\[\]{}"\'\n\t]+',
                'required_fields': ['statement'],
                'forbidden_patterns': [r'<script.*?>', r'javascript:', r'data:', r'<iframe.*?>'],
                'content_validation': True,
                'timeout': 15.0
            },
            ValidationLevel.ENTERPRISE: {
                'min_length': 10,
                'max_length': 10000,
                'allowed_chars': r'[\w\s가-힣.,!?;:()\-\[\]{}"\'\n\t]+',
                'required_fields': ['statement'],
                'forbidden_patterns': [r'<script.*?>', r'javascript:', r'data:', r'<iframe.*?>', r'<object.*?>'],
                'content_validation': True,
                'semantic_validation': True,
                'timeout': 30.0
            }
        }
    
    def _initialize_confidence_weights(self) -> Dict[str, float]:
        """신뢰도 가중치 초기화"""
        return {
            'input_validation': 0.2,
            'content_quality': 0.3,
            'context_relevance': 0.2,
            'processing_success': 0.2,
            'response_quality': 0.1
        }
    
    def _initialize_error_patterns(self) -> Dict[str, List[str]]:
        """오류 패턴 초기화"""
        return {
            'security': [
                r'<script.*?>.*?</script>',
                r'javascript:',
                r'data:text/html',
                r'<iframe.*?>',
                r'<object.*?>',
                r'<embed.*?>'
            ],
            'malicious': [
                r'rm\s+-rf',
                r'sudo\s+',
                r'chmod\s+777',
                r'wget\s+',
                r'curl\s+',
                r'nc\s+'
            ],
            'spam': [
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                r'[0-9]{3}-[0-9]{3,4}-[0-9]{4}'
            ],
            'inappropriate': [
                r'\b(?:fuck|shit|damn|hell|bitch|asshole)\b',
                r'\b(?:hate|kill|die|murder|suicide)\b'
            ]
        }
    
    async def validate_request(self, request: AnalysisRequest) -> ValidationResult:
        """요청 검증"""
        start_time = datetime.now()
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # 1. 기본 검증
            basic_validation = await self._validate_basic(request)
            errors.extend(basic_validation['errors'])
            warnings.extend(basic_validation['warnings'])
            suggestions.extend(basic_validation['suggestions'])
            
            # 2. 보안 검증
            security_validation = await self._validate_security(request)
            errors.extend(security_validation['errors'])
            warnings.extend(security_validation['warnings'])
            
            # 3. 내용 품질 검증
            content_validation = await self._validate_content_quality(request)
            warnings.extend(content_validation['warnings'])
            suggestions.extend(content_validation['suggestions'])
            
            # 4. 맥락 관련성 검증
            context_validation = await self._validate_context_relevance(request)
            warnings.extend(context_validation['warnings'])
            suggestions.extend(context_validation['suggestions'])
            
            # 5. 신뢰도 계산
            confidence = self._calculate_confidence(request, errors, warnings)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return ValidationResult(
                is_valid=len(errors) == 0,
                confidence=confidence,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                validation_level=request.validation_level,
                processing_time=processing_time,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"검증 중 오류 발생: {str(e)}")
            logger.error(traceback.format_exc())
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return ValidationResult(
                is_valid=False,
                confidence=0.0,
                errors=[f"검증 시스템 오류: {str(e)}"],
                warnings=[],
                suggestions=["시스템 관리자에게 문의하세요."],
                validation_level=request.validation_level,
                processing_time=processing_time,
                timestamp=datetime.now()
            )
    
    async def _validate_basic(self, request: AnalysisRequest) -> Dict[str, List[str]]:
        """기본 검증"""
        errors = []
        warnings = []
        suggestions = []
        
        rules = self.validation_rules[request.validation_level]
        
        # 길이 검증
        if len(request.statement) < rules['min_length']:
            errors.append(f"문장이 너무 짧습니다. 최소 {rules['min_length']}자 이상 입력해주세요.")
        elif len(request.statement) > rules['max_length']:
            errors.append(f"문장이 너무 깁니다. 최대 {rules['max_length']}자 이하로 입력해주세요.")
        
        # 문자 검증
        if not re.match(rf"^{rules['allowed_chars']}$", request.statement, re.DOTALL):
            errors.append("허용되지 않는 문자가 포함되어 있습니다.")
        
        # 금지 패턴 검증
        if 'forbidden_patterns' in rules:
            for pattern in rules['forbidden_patterns']:
                if re.search(pattern, request.statement, re.IGNORECASE):
                    errors.append(f"금지된 패턴이 감지되었습니다: {pattern}")
        
        # 문장 품질 검증
        if request.validation_level in [ValidationLevel.STRICT, ValidationLevel.ENTERPRISE]:
            quality_issues = self._check_content_quality(request.statement)
            warnings.extend(quality_issues)
        
        return {
            'errors': errors,
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    async def _validate_security(self, request: AnalysisRequest) -> Dict[str, List[str]]:
        """보안 검증"""
        errors = []
        warnings = []
        
        # 보안 패턴 검증
        for category, patterns in self.error_patterns.items():
            for pattern in patterns:
                if re.search(pattern, request.statement, re.IGNORECASE):
                    if category == 'security':
                        errors.append(f"보안 위험이 감지되었습니다: {pattern}")
                    elif category == 'malicious':
                        errors.append(f"악성 코드가 감지되었습니다: {pattern}")
                    elif category == 'spam':
                        warnings.append(f"스팸으로 의심되는 내용이 감지되었습니다: {pattern}")
                    elif category == 'inappropriate':
                        warnings.append(f"부적절한 내용이 감지되었습니다: {pattern}")
        
        return {
            'errors': errors,
            'warnings': warnings
        }
    
    async def _validate_content_quality(self, request: AnalysisRequest) -> Dict[str, List[str]]:
        """내용 품질 검증"""
        warnings = []
        suggestions = []
        
        # 문장 구조 검증
        if not request.statement.strip().endswith(('.', '!', '?')):
            warnings.append("문장이 적절한 마침표로 끝나지 않았습니다.")
            suggestions.append("문장 끝에 마침표(.), 느낌표(!), 또는 물음표(?)를 추가해주세요.")
        
        # 중복 단어 검증
        words = request.statement.lower().split()
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        
        for word, count in word_count.items():
            if count > 3 and len(word) > 2:
                warnings.append(f"'{word}' 단어가 {count}번 반복되었습니다.")
                suggestions.append("반복되는 단어를 줄여보세요.")
        
        # 문장 길이 검증
        sentences = re.split(r'[.!?]+', request.statement)
        for i, sentence in enumerate(sentences):
            if len(sentence.split()) > 50:
                warnings.append(f"{i+1}번째 문장이 너무 깁니다 ({len(sentence.split())}단어).")
                suggestions.append("긴 문장을 여러 개의 짧은 문장으로 나누어보세요.")
        
        return {
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    async def _validate_context_relevance(self, request: AnalysisRequest) -> Dict[str, List[str]]:
        """맥락 관련성 검증"""
        warnings = []
        suggestions = []
        
        # 문맥과 문장의 관련성 검증
        if request.context and request.statement:
            context_words = set(request.context.lower().split())
            statement_words = set(request.statement.lower().split())
            
            # 공통 단어 비율 계산
            common_words = context_words.intersection(statement_words)
            if len(common_words) == 0:
                warnings.append("문맥과 문장 사이에 공통 단어가 없습니다.")
                suggestions.append("문맥과 관련된 내용으로 문장을 수정해보세요.")
            elif len(common_words) / len(statement_words) < 0.1:
                warnings.append("문맥과 문장의 관련성이 낮습니다.")
                suggestions.append("문맥과 더 관련된 내용으로 문장을 수정해보세요.")
        
        return {
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    def _check_content_quality(self, text: str) -> List[str]:
        """내용 품질 검사"""
        issues = []
        
        # 빈 문장 검사
        if not text.strip():
            issues.append("빈 문장입니다.")
        
        # 단일 문자 반복 검사
        if len(set(text.replace(' ', ''))) < 3:
            issues.append("내용이 너무 단조롭습니다.")
        
        # 의미 있는 단어 비율 검사
        words = text.split()
        meaningful_words = [w for w in words if len(w) > 2 and w.isalpha()]
        if len(meaningful_words) / len(words) < 0.5:
            issues.append("의미 있는 단어의 비율이 낮습니다.")
        
        return issues
    
    def _calculate_confidence(self, request: AnalysisRequest, errors: List[str], warnings: List[str]) -> float:
        """신뢰도 계산"""
        base_confidence = 1.0
        
        # 오류에 따른 신뢰도 감소
        error_penalty = len(errors) * 0.2
        warning_penalty = len(warnings) * 0.05
        
        # 검증 수준에 따른 가중치
        level_weights = {
            ValidationLevel.BASIC: 0.5,
            ValidationLevel.STANDARD: 0.7,
            ValidationLevel.STRICT: 0.85,
            ValidationLevel.ENTERPRISE: 0.95
        }
        
        level_weight = level_weights[request.validation_level]
        
        # 최종 신뢰도 계산
        confidence = (base_confidence - error_penalty - warning_penalty) * level_weight
        
        return max(0.0, min(1.0, confidence))

class AdvancedErrorHandler:
    """고급 오류 처리 시스템"""
    
    def __init__(self):
        self.error_categories = {
            'validation': '입력 검증 오류',
            'processing': '처리 중 오류',
            'security': '보안 관련 오류',
            'timeout': '시간 초과 오류',
            'system': '시스템 오류',
            'network': '네트워크 오류',
            'unknown': '알 수 없는 오류'
        }
    
    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """오류 처리"""
        error_type = type(error).__name__
        error_message = str(error)
        
        # 오류 분류
        category = self._categorize_error(error)
        
        # 사용자 친화적 메시지 생성
        user_message = self._generate_user_message(category, error_message)
        
        # 기술적 세부사항
        technical_details = {
            'error_type': error_type,
            'error_message': error_message,
            'category': category,
            'context': context or {},
            'timestamp': datetime.now().isoformat(),
            'traceback': traceback.format_exc()
        }
        
        # 로깅
        logger.error(f"{category}: {error_message}", extra=technical_details)
        
        return {
            'success': False,
            'error': user_message,
            'category': category,
            'technical_details': technical_details,
            'suggestions': self._get_error_suggestions(category)
        }
    
    def _categorize_error(self, error: Exception) -> str:
        """오류 분류"""
        error_type = type(error).__name__
        
        if 'Validation' in error_type or 'ValueError' in error_type:
            return 'validation'
        elif 'Timeout' in error_type or 'timeout' in str(error).lower():
            return 'timeout'
        elif 'Security' in error_type or 'security' in str(error).lower():
            return 'security'
        elif 'Network' in error_type or 'Connection' in error_type:
            return 'network'
        elif 'System' in error_type or 'OS' in error_type:
            return 'system'
        else:
            return 'unknown'
    
    def _generate_user_message(self, category: str, error_message: str) -> str:
        """사용자 친화적 메시지 생성"""
        base_messages = {
            'validation': '입력한 내용을 확인해주세요.',
            'processing': '처리 중 문제가 발생했습니다.',
            'security': '보안상의 이유로 요청이 거부되었습니다.',
            'timeout': '요청 처리 시간이 초과되었습니다.',
            'system': '시스템에 일시적인 문제가 발생했습니다.',
            'network': '네트워크 연결에 문제가 있습니다.',
            'unknown': '예상치 못한 오류가 발생했습니다.'
        }
        
        return base_messages.get(category, '오류가 발생했습니다.')
    
    def _get_error_suggestions(self, category: str) -> List[str]:
        """오류별 제안사항"""
        suggestions = {
            'validation': [
                '입력 형식을 확인해주세요.',
                '필수 항목이 모두 입력되었는지 확인해주세요.',
                '허용되지 않는 문자가 포함되어 있지 않은지 확인해주세요.'
            ],
            'processing': [
                '잠시 후 다시 시도해주세요.',
                '입력 내용을 간단히 수정해보세요.',
                '문제가 지속되면 관리자에게 문의하세요.'
            ],
            'security': [
                '보안 정책을 확인해주세요.',
                '의심스러운 내용이 포함되어 있지 않은지 확인해주세요.',
                '필요시 관리자에게 문의하세요.'
            ],
            'timeout': [
                '입력 내용을 간단히 수정해보세요.',
                '네트워크 연결을 확인해주세요.',
                '잠시 후 다시 시도해주세요.'
            ],
            'system': [
                '잠시 후 다시 시도해주세요.',
                '시스템이 복구될 때까지 기다려주세요.',
                '문제가 지속되면 관리자에게 문의하세요.'
            ],
            'network': [
                '인터넷 연결을 확인해주세요.',
                '네트워크 설정을 확인해주세요.',
                '잠시 후 다시 시도해주세요.'
            ],
            'unknown': [
                '잠시 후 다시 시도해주세요.',
                '문제가 지속되면 관리자에게 문의하세요.',
                '오류 코드를 기록해두세요.'
            ]
        }
        
        return suggestions.get(category, ['문제가 지속되면 관리자에게 문의하세요.'])

def main():
    """메인 실행 함수"""
    print("🔍 고급 검증 시스템 테스트")
    print("=" * 60)
    
    validation_system = AdvancedValidationSystem()
    error_handler = AdvancedErrorHandler()
    
    # 테스트 요청들
    test_requests = [
        AnalysisRequest(
            statement="지구는 둥글다.",
            context="과학적 사실에 대한 질문",
            analysis_mode="all",
            validation_level=ValidationLevel.STANDARD
        ),
        AnalysisRequest(
            statement="<script>alert('xss')</script>",
            context="악성 코드 테스트",
            analysis_mode="all",
            validation_level=ValidationLevel.STRICT
        ),
        AnalysisRequest(
            statement="",
            context="빈 문장 테스트",
            analysis_mode="all",
            validation_level=ValidationLevel.BASIC
        )
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n{i}. 테스트 요청: {request.statement[:50]}...")
        print(f"   검증 수준: {request.validation_level.value}")
        
        try:
            # 비동기 검증 실행
            import asyncio
            result = asyncio.run(validation_system.validate_request(request))
            
            print(f"   결과: {'✅ 유효' if result.is_valid else '❌ 무효'}")
            print(f"   신뢰도: {result.confidence:.3f}")
            print(f"   처리 시간: {result.processing_time:.3f}초")
            
            if result.errors:
                print(f"   오류: {', '.join(result.errors)}")
            if result.warnings:
                print(f"   경고: {', '.join(result.warnings)}")
            if result.suggestions:
                print(f"   제안: {', '.join(result.suggestions)}")
                
        except Exception as e:
            error_result = error_handler.handle_error(e, {'request': request.__dict__})
            print(f"   오류 처리: {error_result['error']}")
            print(f"   제안: {', '.join(error_result['suggestions'])}")

if __name__ == "__main__":
    main()
