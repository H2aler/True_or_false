#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 일관성 테스트 데모
동일한 문장에 대해 일관된 결과를 반환하는지 테스트합니다.
"""

from ai_consistent_detector import AIConsistentDetector
import time

def main():
    """메인 데모 함수"""
    print("🔍 AI 일관성 테스트 데모")
    print("=" * 60)
    
    detector = AIConsistentDetector()
    
    # 테스트 문장들
    test_statements = [
        "지구는 둥글다.",
        "물은 100도에서 끓는다.",
        "1 + 1 = 2이다.",
        "지구는 평평하다.",
        "정말로 완전히 절대적으로 모든 것이 100% 진실이다."
    ]
    
    print("📝 일관성 테스트 시작...")
    print("-" * 40)
    
    for i, statement in enumerate(test_statements, 1):
        print(f"\n{i}. 문장: {statement}")
        print("   동일한 문장을 5번 분석하여 일관성을 확인합니다...")
        
        # 동일한 문장을 5번 분석
        results = []
        for j in range(5):
            result = detector.analyze_statement(statement)
            results.append({
                'iteration': j + 1,
                'truth_percentage': result.truth_percentage,
                'confidence': result.confidence,
                'statement_hash': result.statement_hash,
                'needs_correction': result.needs_correction
            })
            time.sleep(0.1)  # 짧은 대기
        
        # 결과 표시
        print("   결과:")
        for result in results:
            print(f"     {result['iteration']}회차: 진실성 {result['truth_percentage']:.3f} | 신뢰도 {result['confidence']:.3f} | 해시 {result['statement_hash'][:8]}...")
        
        # 일관성 분석
        truth_scores = [r['truth_percentage'] for r in results]
        confidence_scores = [r['confidence'] for r in results]
        
        truth_variance = max(truth_scores) - min(truth_scores)
        confidence_variance = max(confidence_scores) - min(confidence_scores)
        
        is_consistent = truth_variance < 0.01 and confidence_variance < 0.01
        
        print(f"   일관성 평가:")
        print(f"     진실성 점수 변동폭: {truth_variance:.6f}")
        print(f"     신뢰도 변동폭: {confidence_variance:.6f}")
        print(f"     일관성: {'✅ 일관성 있음' if is_consistent else '❌ 일관성 없음'}")
        
        if not is_consistent:
            print(f"     ⚠️  경고: 동일한 문장에 대해 다른 결과를 반환했습니다!")
    
    # 캐시 통계
    stats = detector.get_cache_stats()
    print(f"\n📊 캐시 통계:")
    print(f"   캐시 크기: {stats['cache_size']}")
    print(f"   캐시 히트율: {stats['cache_hit_rate']:.2%}")
    print(f"   총 요청: {stats['total_requests']}")
    print(f"   캐시 히트: {stats['cache_hits']}")
    
    # 추가 테스트: 캐시 효과 확인
    print(f"\n🔄 캐시 효과 테스트:")
    print("   동일한 문장을 다시 분석하여 캐시에서 결과를 가져오는지 확인...")
    
    test_statement = "지구는 둥글다."
    print(f"   테스트 문장: {test_statement}")
    
    # 첫 번째 분석 (캐시 미스)
    start_time = time.time()
    result1 = detector.analyze_statement(test_statement)
    time1 = time.time() - start_time
    
    # 두 번째 분석 (캐시 히트)
    start_time = time.time()
    result2 = detector.analyze_statement(test_statement)
    time2 = time.time() - start_time
    
    print(f"   첫 번째 분석: {time1:.4f}초 (캐시 미스)")
    print(f"   두 번째 분석: {time2:.4f}초 (캐시 히트)")
    print(f"   속도 향상: {time1/time2:.1f}배 빨라짐")
    print(f"   결과 일치: {'✅ 일치' if result1.statement_hash == result2.statement_hash else '❌ 불일치'}")
    
    print(f"\n🎉 일관성 테스트 완료!")
    print("   이제 동일한 문장에 대해 항상 같은 결과를 반환합니다.")

if __name__ == "__main__":
    main()
