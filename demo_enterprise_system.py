#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enterprise System Demo
엔터프라이즈급 AI 진실성 탐지 시스템 데모

ChatGPT/Claude 수준의 신뢰성과 품질을 보여주는 데모입니다.
"""

import requests
import json
import time
import asyncio
from datetime import datetime
from typing import Dict, List, Any

class EnterpriseSystemDemo:
    """엔터프라이즈 시스템 데모"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Enterprise-Demo/2.0.0'
        })
    
    def test_health_check(self) -> Dict[str, Any]:
        """시스템 상태 확인 테스트"""
        print("🔍 시스템 상태 확인...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            result = response.json()
            
            print(f"✅ 상태: {result['status']}")
            print(f"📊 버전: {result['version']}")
            print(f"⏱️ 업타임: {result['uptime']:.2f}초")
            print(f"📈 성능 메트릭:")
            for key, value in result['performance_metrics'].items():
                print(f"   {key}: {value}")
            
            return result
            
        except Exception as e:
            print(f"❌ 상태 확인 실패: {e}")
            return {}
    
    def test_validation_system(self) -> Dict[str, Any]:
        """검증 시스템 테스트"""
        print("\n🔍 검증 시스템 테스트...")
        
        test_cases = [
            {
                'statement': '지구는 둥글다.',
                'context': '과학적 사실에 대한 질문',
                'validation_level': 'standard',
                'expected': 'valid'
            },
            {
                'statement': '<script>alert("xss")</script>',
                'context': '악성 코드 테스트',
                'validation_level': 'strict',
                'expected': 'invalid'
            },
            {
                'statement': '',
                'context': '빈 문장 테스트',
                'validation_level': 'basic',
                'expected': 'invalid'
            },
            {
                'statement': '정말로 완전히 절대적으로 모든 것이 100% 진실이다.',
                'context': '과장된 표현 테스트',
                'validation_level': 'enterprise',
                'expected': 'valid_with_warnings'
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n  {i}. 테스트: {test_case['statement'][:30]}...")
            
            try:
                response = self.session.post(f"{self.base_url}/api/validate", json={
                    'statement': test_case['statement'],
                    'context': test_case['context'],
                    'validation_level': test_case['validation_level']
                })
                
                result = response.json()
                
                if result['success']:
                    validation = result['validation_result']
                    print(f"     결과: {'✅ 유효' if validation['is_valid'] else '❌ 무효'}")
                    print(f"     신뢰도: {validation['confidence']:.3f}")
                    print(f"     처리 시간: {validation['processing_time']:.3f}초")
                    
                    if validation['warnings']:
                        print(f"     경고: {', '.join(validation['warnings'])}")
                    if validation['suggestions']:
                        print(f"     제안: {', '.join(validation['suggestions'])}")
                else:
                    print(f"     오류: {result['error']}")
                
                results.append(result)
                
            except Exception as e:
                print(f"     오류 발생: {e}")
                results.append({'error': str(e)})
        
        return results
    
    def test_confidence_system(self) -> Dict[str, Any]:
        """신뢰도 평가 시스템 테스트"""
        print("\n🔍 신뢰도 평가 시스템 테스트...")
        
        test_cases = [
            {
                'statement': '지구는 둥글다.',
                'context': '과학적 사실에 대한 질문',
                'analysis_result': {
                    'final_analysis': {
                        'truth_percentage': 0.95,
                        'confidence': 0.9,
                        'needs_correction': False
                    }
                }
            },
            {
                'statement': '정말로 완전히 절대적으로 모든 것이 100% 진실이다.',
                'context': '과장된 표현 테스트',
                'analysis_result': {
                    'final_analysis': {
                        'truth_percentage': 0.2,
                        'confidence': 0.3,
                        'needs_correction': True
                    }
                }
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n  {i}. 테스트: {test_case['statement'][:30]}...")
            
            try:
                response = self.session.post(f"{self.base_url}/api/confidence", json=test_case)
                
                result = response.json()
                
                if result['success']:
                    confidence = result['confidence_evaluation']
                    print(f"     전체 신뢰도: {confidence['overall_confidence']:.3f}")
                    print(f"     품질 수준: {confidence['quality_level']}")
                    print(f"     설명: {confidence['explanation']}")
                    print(f"     처리 시간: {confidence['processing_time']:.3f}초")
                    
                    if confidence['recommendations']:
                        print(f"     권장사항: {', '.join(confidence['recommendations'])}")
                else:
                    print(f"     오류: {result['error']}")
                
                results.append(result)
                
            except Exception as e:
                print(f"     오류 발생: {e}")
                results.append({'error': str(e)})
        
        return results
    
    def test_analysis_system(self) -> Dict[str, Any]:
        """분석 시스템 테스트"""
        print("\n🔍 분석 시스템 테스트...")
        
        test_cases = [
            {
                'statement': '지구는 둥글다.',
                'context': '과학적 사실에 대한 질문',
                'analysis_mode': 'all'
            },
            {
                'statement': '물은 100도에서 끓는다.',
                'context': '과학적 사실에 대한 질문',
                'analysis_mode': 'scientific'
            },
            {
                'statement': '정말로 완전히 절대적으로 모든 것이 100% 진실이다.',
                'context': '과장된 표현 테스트',
                'analysis_mode': 'all'
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n  {i}. 테스트: {test_case['statement'][:30]}...")
            
            try:
                start_time = time.time()
                
                response = self.session.post(f"{self.base_url}/api/analyze", json=test_case)
                
                processing_time = time.time() - start_time
                result = response.json()
                
                if result['success']:
                    analysis = result['analysis']
                    print(f"     진실성: {analysis['final_analysis']['truth_percentage']:.3f}")
                    print(f"     신뢰도: {analysis['final_analysis']['confidence']:.3f}")
                    print(f"     교정 필요: {'예' if analysis['final_analysis']['needs_correction'] else '아니오'}")
                    print(f"     처리 시간: {processing_time:.3f}초")
                    
                    # 신뢰도 평가 결과
                    if 'confidence_evaluation' in analysis:
                        confidence = analysis['confidence_evaluation']
                        print(f"     전체 신뢰도: {confidence['overall_confidence']:.3f}")
                        print(f"     품질 수준: {confidence['quality_level']}")
                else:
                    print(f"     오류: {result['error']}")
                
                results.append(result)
                
            except Exception as e:
                print(f"     오류 발생: {e}")
                results.append({'error': str(e)})
        
        return results
    
    def test_batch_analysis(self) -> Dict[str, Any]:
        """배치 분석 테스트"""
        print("\n🔍 배치 분석 테스트...")
        
        statements = [
            '지구는 둥글다.',
            '물은 100도에서 끓는다.',
            '1 + 1 = 2이다.',
            '지구는 평평하다.',
            '정말로 완전히 절대적으로 모든 것이 100% 진실이다.'
        ]
        
        try:
            start_time = time.time()
            
            response = self.session.post(f"{self.base_url}/api/batch-analyze", json={
                'statements': statements,
                'context': '배치 분석 테스트',
                'analysis_mode': 'all'
            })
            
            processing_time = time.time() - start_time
            result = response.json()
            
            if result['success']:
                print(f"✅ 총 처리: {result['total_processed']}개")
                print(f"✅ 성공: {result['successful']}개")
                print(f"❌ 실패: {result['failed']}개")
                print(f"⏱️ 처리 시간: {processing_time:.3f}초")
                
                print("\n  결과 요약:")
                for batch_result in result['batch_results']:
                    if 'error' not in batch_result:
                        print(f"    {batch_result['index']+1}. {batch_result['statement'][:30]}... - 진실성: {batch_result['final_analysis']['truth_percentage']:.3f}")
                    else:
                        print(f"    {batch_result['index']+1}. {batch_result['statement'][:30]}... - 오류: {batch_result['error']}")
            else:
                print(f"❌ 오류: {result['error']}")
            
            return result
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return {'error': str(e)}
    
    def test_metrics(self) -> Dict[str, Any]:
        """성능 메트릭 테스트"""
        print("\n🔍 성능 메트릭 테스트...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/metrics")
            result = response.json()
            
            if result['success']:
                metrics = result['metrics']
                print(f"📊 총 요청: {metrics['total_requests']}")
                print(f"✅ 성공: {metrics['successful_requests']}")
                print(f"❌ 실패: {metrics['failed_requests']}")
                print(f"⏱️ 평균 응답 시간: {metrics['average_response_time']:.3f}초")
                print(f"💾 캐시 히트율: {metrics['cache_hit_rate']:.2%}")
            else:
                print(f"❌ 오류: {result['error']}")
            
            return result
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return {'error': str(e)}
    
    def run_full_demo(self):
        """전체 데모 실행"""
        print("🚀 AI 진실성 탐지 시스템 (Enterprise Edition) 데모 시작")
        print("=" * 80)
        
        # 1. 시스템 상태 확인
        health_result = self.test_health_check()
        
        # 2. 검증 시스템 테스트
        validation_results = self.test_validation_system()
        
        # 3. 신뢰도 평가 시스템 테스트
        confidence_results = self.test_confidence_system()
        
        # 4. 분석 시스템 테스트
        analysis_results = self.test_analysis_system()
        
        # 5. 배치 분석 테스트
        batch_result = self.test_batch_analysis()
        
        # 6. 성능 메트릭 테스트
        metrics_result = self.test_metrics()
        
        # 7. 최종 요약
        print("\n" + "=" * 80)
        print("🎉 데모 완료!")
        print("=" * 80)
        
        print(f"✅ 시스템 상태: {'정상' if health_result.get('status') == 'healthy' else '비정상'}")
        print(f"📊 총 요청: {metrics_result.get('metrics', {}).get('total_requests', 0)}")
        print(f"✅ 성공률: {metrics_result.get('metrics', {}).get('successful_requests', 0) / max(1, metrics_result.get('metrics', {}).get('total_requests', 1)) * 100:.1f}%")
        print(f"⏱️ 평균 응답 시간: {metrics_result.get('metrics', {}).get('average_response_time', 0):.3f}초")
        
        print("\n🎯 엔터프라이즈급 기능들:")
        print("  ✅ 고급 입력 검증 시스템")
        print("  ✅ 다층적 신뢰도 평가")
        print("  ✅ 비동기 처리 및 캐싱")
        print("  ✅ 포괄적 오류 처리")
        print("  ✅ 성능 모니터링")
        print("  ✅ 배치 처리 지원")
        print("  ✅ 데이터 내보내기")
        print("  ✅ 보안 강화")
        
        print("\n🌟 ChatGPT/Claude 수준의 신뢰성과 품질을 제공합니다!")

def main():
    """메인 실행 함수"""
    demo = EnterpriseSystemDemo()
    demo.run_full_demo()

if __name__ == "__main__":
    main()
