#!/usr/bin/env python3
"""
API 테스트 스위트
AI 진실성 탐지기 Enterprise Edition의 모든 API 엔드포인트를 테스트합니다.
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

class APITestSuite:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.auth_token = None
        
    def log_test(self, test_name: str, success: bool, message: str = "", response_time: float = 0):
        """테스트 결과를 로깅합니다."""
        result = {
            "test_name": test_name,
            "success": success,
            "message": message,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message} ({response_time:.3f}s)")
        
    def make_request(self, method: str, endpoint: str, **kwargs) -> tuple:
        """HTTP 요청을 보내고 응답 시간을 측정합니다."""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, **kwargs)
            elif method.upper() == "POST":
                response = self.session.post(url, **kwargs)
            elif method.upper() == "PUT":
                response = self.session.put(url, **kwargs)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, **kwargs)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response_time = time.time() - start_time
            return response, response_time
            
        except Exception as e:
            response_time = time.time() - start_time
            return None, response_time
            
    def test_health_check(self):
        """헬스 체크 API 테스트"""
        print("\n🔍 헬스 체크 API 테스트")
        response, response_time = self.make_request("GET", "/api/health")
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_test("Health Check", True, f"Status: {data.get('status')}", response_time)
        else:
            self.log_test("Health Check", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def test_version_api(self):
        """버전 API 테스트"""
        print("\n🔍 버전 API 테스트")
        response, response_time = self.make_request("GET", "/api/v1/version")
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_test("Version API", True, f"Version: {data.get('version')}", response_time)
        else:
            self.log_test("Version API", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def test_system_status(self):
        """시스템 상태 API 테스트"""
        print("\n🔍 시스템 상태 API 테스트")
        response, response_time = self.make_request("GET", "/api/v1/system/status")
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_test("System Status", True, f"Status: {data.get('status')}", response_time)
        else:
            self.log_test("System Status", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def test_detectors_api(self):
        """탐지기 API 테스트"""
        print("\n🔍 탐지기 API 테스트")
        response, response_time = self.make_request("GET", "/api/v1/detectors")
        
        if response and response.status_code == 200:
            data = response.json()
            detector_count = len(data.get('detectors', []))
            self.log_test("Detectors API", True, f"Detectors count: {detector_count}", response_time)
        else:
            self.log_test("Detectors API", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def test_analysis_api(self):
        """분석 API 테스트"""
        print("\n🔍 분석 API 테스트")
        test_data = {
            "statement": "이것은 테스트 문장입니다.",
            "context": "테스트 컨텍스트",
            "analysis_mode": "all"
        }
        
        response, response_time = self.make_request(
            "POST", 
            "/api/analyze", 
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_test("Analysis API", True, f"Analysis completed", response_time)
        else:
            self.log_test("Analysis API", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def test_ai_self_analysis_api(self):
        """AI 자체 분석 API 테스트"""
        print("\n🔍 AI 자체 분석 API 테스트")
        test_data = {
            "statement": "AI가 자신을 분석하는 테스트입니다.",
            "context": "AI 자체 분석 테스트 컨텍스트"
        }
        
        response, response_time = self.make_request(
            "POST", 
            "/api/ai-self-analysis", 
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_test("AI Self Analysis API", True, f"Self analysis completed", response_time)
        else:
            self.log_test("AI Self Analysis API", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def test_research_question_api(self):
        """연구 질문 API 테스트"""
        print("\n🔍 연구 질문 API 테스트")
        test_data = {
            "question": "토끼는 동물인가요?",
            "research_depth": "medium"
        }
        
        response, response_time = self.make_request(
            "POST", 
            "/api/research-question", 
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_test("Research Question API", True, f"Research completed", response_time)
        else:
            self.log_test("Research Question API", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def test_fact_verification_api(self):
        """사실 검증 API 테스트"""
        print("\n🔍 사실 검증 API 테스트")
        test_data = {
            "statement": "지구는 둥글다",
            "verification_level": "high"
        }
        
        response, response_time = self.make_request(
            "POST", 
            "/api/verify-fact", 
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_test("Fact Verification API", True, f"Fact verification completed", response_time)
        else:
            self.log_test("Fact Verification API", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def test_ml_analysis_api(self):
        """머신러닝 분석 API 테스트"""
        print("\n🔍 머신러닝 분석 API 테스트")
        test_data = {
            "statement": "머신러닝을 사용한 진실성 분석 테스트입니다.",
            "context": "머신러닝 분석 테스트 컨텍스트"
        }
        
        response, response_time = self.make_request(
            "POST", 
            "/api/ml-analyze", 
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_test("ML Analysis API", True, f"ML analysis completed", response_time)
        else:
            self.log_test("ML Analysis API", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def test_ml_status_api(self):
        """머신러닝 상태 API 테스트"""
        print("\n🔍 머신러닝 상태 API 테스트")
        response, response_time = self.make_request("GET", "/api/ml-status")
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_test("ML Status API", True, f"ML status retrieved", response_time)
        else:
            self.log_test("ML Status API", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def test_consistency_analysis_api(self):
        """일관성 분석 API 테스트"""
        print("\n🔍 일관성 분석 API 테스트")
        test_data = {
            "statement": "토끼는 동물입니다.",
            "context": "일관성 분석 테스트 컨텍스트"
        }
        
        response, response_time = self.make_request(
            "POST", 
            "/api/consistent-analyze", 
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_test("Consistency Analysis API", True, f"Consistency analysis completed", response_time)
        else:
            self.log_test("Consistency Analysis API", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def test_batch_analysis_api(self):
        """배치 분석 API 테스트"""
        print("\n🔍 배치 분석 API 테스트")
        test_data = {
            "statements": [
                "첫 번째 테스트 문장입니다.",
                "두 번째 테스트 문장입니다.",
                "세 번째 테스트 문장입니다."
            ],
            "context": "배치 분석 테스트 컨텍스트",
            "analysis_mode": "all"
        }
        
        response, response_time = self.make_request(
            "POST", 
            "/api/batch-analyze", 
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_test("Batch Analysis API", True, f"Batch analysis completed", response_time)
        else:
            self.log_test("Batch Analysis API", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def test_metrics_api(self):
        """메트릭 API 테스트"""
        print("\n🔍 메트릭 API 테스트")
        response, response_time = self.make_request("GET", "/api/metrics")
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_test("Metrics API", True, f"Metrics retrieved", response_time)
        else:
            self.log_test("Metrics API", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def test_export_api(self):
        """내보내기 API 테스트"""
        print("\n🔍 내보내기 API 테스트")
        response, response_time = self.make_request("GET", "/api/export")
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_test("Export API", True, f"Export completed", response_time)
        else:
            self.log_test("Export API", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def test_swagger_docs(self):
        """Swagger 문서 API 테스트"""
        print("\n🔍 Swagger 문서 API 테스트")
        response, response_time = self.make_request("GET", "/api/docs/")
        
        if response and response.status_code == 200:
            self.log_test("Swagger Docs", True, f"Documentation accessible", response_time)
        else:
            self.log_test("Swagger Docs", False, f"Status code: {response.status_code if response else 'No response'}", response_time)
            
    def run_all_tests(self):
        """모든 테스트를 실행합니다."""
        print("🚀 API 테스트 스위트 시작")
        print("=" * 50)
        
        start_time = time.time()
        
        # 기본 API 테스트
        self.test_health_check()
        self.test_version_api()
        self.test_system_status()
        self.test_detectors_api()
        self.test_swagger_docs()
        
        # 분석 API 테스트
        self.test_analysis_api()
        self.test_ai_self_analysis_api()
        self.test_research_question_api()
        self.test_fact_verification_api()
        
        # 머신러닝 API 테스트
        self.test_ml_analysis_api()
        self.test_ml_status_api()
        
        # 고급 분석 API 테스트
        self.test_consistency_analysis_api()
        self.test_batch_analysis_api()
        
        # 유틸리티 API 테스트
        self.test_metrics_api()
        self.test_export_api()
        
        total_time = time.time() - start_time
        
        # 결과 요약
        print("\n" + "=" * 50)
        print("📊 테스트 결과 요약")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"총 테스트: {total_tests}")
        print(f"성공: {passed_tests} ✅")
        print(f"실패: {failed_tests} ❌")
        print(f"성공률: {(passed_tests/total_tests)*100:.1f}%")
        print(f"총 실행 시간: {total_time:.3f}초")
        
        # 실패한 테스트 상세 정보
        if failed_tests > 0:
            print("\n❌ 실패한 테스트:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test_name']}: {result['message']}")
        
        # 결과를 JSON 파일로 저장
        with open("api_test_results.json", "w", encoding="utf-8") as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 상세 결과가 'api_test_results.json'에 저장되었습니다.")
        
        return passed_tests == total_tests

def main():
    """메인 함수"""
    print("AI 진실성 탐지기 Enterprise Edition - API 테스트 스위트")
    print("=" * 60)
    
    # 테스트 스위트 실행
    test_suite = APITestSuite()
    success = test_suite.run_all_tests()
    
    if success:
        print("\n🎉 모든 테스트가 성공적으로 완료되었습니다!")
        sys.exit(0)
    else:
        print("\n⚠️ 일부 테스트가 실패했습니다. 로그를 확인해주세요.")
        sys.exit(1)

if __name__ == "__main__":
    main()
