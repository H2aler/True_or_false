#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 향상된 웹 연구원 데모
실시간 검색 과정을 한국어로 표시하는 데모입니다.
"""

from ai_enhanced_researcher import AIEnhancedResearcher
import time

def main():
    """메인 데모 함수"""
    print("🔍 AI 향상된 웹 연구원 데모 시작")
    print("=" * 60)
    
    # 진행 상황 콜백 함수
    def progress_callback(progress):
        status_emoji = {
            'started': '🚀',
            'in_progress': '⏳',
            'completed': '✅',
            'failed': '❌'
        }
        print(f"{status_emoji.get(progress.status, '📝')} {progress.step}: {progress.description}")
        if progress.details:
            print(f"   └─ {progress.details}")
        print()
    
    researcher = AIEnhancedResearcher(progress_callback=progress_callback)
    
    # 테스트 질문들
    test_questions = [
        "지구는 둥글까요?",
        "물은 몇 도에서 끓나요?",
        "인공지능은 어떻게 작동하나요?",
        "코로나19는 무엇인가요?",
        "기후변화의 원인은 무엇인가요?"
    ]
    
    print("📚 테스트 질문들:")
    for i, question in enumerate(test_questions, 1):
        print(f"  {i}. {question}")
    
    print("\n" + "=" * 60)
    
    # 사용자 선택
    while True:
        print("\n🔧 테스트 옵션:")
        print("1. 기본 질문 테스트")
        print("2. 사용자 질문 입력")
        print("3. 모든 질문 일괄 테스트")
        print("4. 종료")
        
        choice = input("\n선택하세요 (1-4): ").strip()
        
        if choice == '1':
            # 기본 질문 테스트
            question = test_questions[0]
            print(f"\n❓ 질문: {question}")
            print("-" * 40)
            
            try:
                result = researcher.research_question(question)
                display_result(result)
            except Exception as e:
                print(f"❌ 오류 발생: {e}")
                
        elif choice == '2':
            # 사용자 질문 입력
            question = input("\n질문을 입력하세요: ").strip()
            if not question:
                print("❌ 질문을 입력해주세요.")
                continue
            
            print(f"\n❓ 질문: {question}")
            print("-" * 40)
            
            try:
                result = researcher.research_question(question)
                display_result(result)
            except Exception as e:
                print(f"❌ 오류 발생: {e}")
                
        elif choice == '3':
            # 모든 질문 일괄 테스트
            print(f"\n🔄 모든 질문 일괄 테스트 시작...")
            print("=" * 60)
            
            for i, question in enumerate(test_questions, 1):
                print(f"\n📝 질문 {i}/{len(test_questions)}: {question}")
                print("-" * 40)
                
                try:
                    result = researcher.research_question(question)
                    display_result(result, show_details=False)
                except Exception as e:
                    print(f"❌ 오류 발생: {e}")
                
                if i < len(test_questions):
                    print("\n" + "=" * 60)
                    time.sleep(2)
                    
        elif choice == '4':
            print("\n👋 데모를 종료합니다.")
            break
        else:
            print("❌ 잘못된 선택입니다. 1-4 중에서 선택해주세요.")
            continue
        
        print("=" * 60)
        
        # 계속할지 묻기
        continue_choice = input("\n다른 질문을 분석하시겠습니까? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes', '예', 'ㅇ']:
            break
    
    print("\n🎉 데모가 완료되었습니다!")
    print("AI 향상된 웹 연구원이 실시간 검색 과정을 표시하며")
    print("질문에 답변하는 과정을 확인했습니다.")

def display_result(result, show_details=True):
    """결과 표시"""
    print(f"\n💡 답변:")
    print(f"{result.answer}")
    
    print(f"\n🎯 신뢰도: {result.confidence:.2f}")
    print(f"🔍 추론: {result.reasoning}")
    print(f"📚 소스 수: {len(result.sources)}개")
    print(f"✅ 사실 검증: {len(result.fact_verifications)}개")
    print(f"⏱️ 총 처리 시간: {result.total_processing_time:.2f}초")
    
    if result.limitations:
        print(f"⚠️ 한계점: {', '.join(result.limitations)}")
    
    if show_details:
        print(f"\n📊 검색 진행 과정:")
        for progress in result.search_progress:
            status_emoji = {
                'started': '🚀',
                'in_progress': '⏳',
                'completed': '✅',
                'failed': '❌'
            }
            print(f"  {status_emoji.get(progress.status, '📝')} {progress.step}: {progress.description}")
            if progress.details:
                print(f"     └─ {progress.details}")
        
        print(f"\n📖 주요 참고 소스:")
        for i, source in enumerate(result.sources[:3], 1):
            print(f"  {i}. {source.title}")
            print(f"     도메인: {source.domain}")
            print(f"     검색 엔진: {source.search_engine}")
            print(f"     키워드: {source.search_keyword}")
            print(f"     신뢰도: {source.credibility_score:.2f}")
            print(f"     처리 시간: {source.processing_time:.2f}초")
            print(f"     URL: {source.url}")
            print()

if __name__ == "__main__":
    main()
