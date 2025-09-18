#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 웹 연구원 데모
AI가 인터넷에서 정보를 검색하고 진실성을 검증하여 질문에 답변하는 데모입니다.
"""

from ai_web_researcher import AIWebResearcher
from ai_advanced_researcher import AIAdvancedResearcher
import time

def main():
    """메인 데모 함수"""
    print("🔍 AI 웹 연구원 데모 시작")
    print("=" * 60)
    
    # 기본 연구원과 고급 연구원 초기화
    basic_researcher = AIWebResearcher()
    advanced_researcher = AIAdvancedResearcher()
    
    # 테스트 질문들
    test_questions = [
        "지구는 둥글까요?",
        "물은 몇 도에서 끓나요?",
        "1 + 1은 얼마인가요?",
        "코로나19는 무엇인가요?",
        "인공지능은 어떻게 작동하나요?",
        "기후변화의 원인은 무엇인가요?",
        "DNA는 무엇인가요?",
        "태양계에는 몇 개의 행성이 있나요?"
    ]
    
    print("📚 테스트 질문들:")
    for i, question in enumerate(test_questions, 1):
        print(f"  {i}. {question}")
    
    print("\n" + "=" * 60)
    
    # 사용자 선택
    while True:
        print("\n🔧 연구원 선택:")
        print("1. 기본 연구원 (빠른 분석)")
        print("2. 고급 연구원 (상세한 분석)")
        print("3. 사용자 질문 입력")
        print("4. 종료")
        
        choice = input("\n선택하세요 (1-4): ").strip()
        
        if choice == '1':
            print("\n🔍 기본 연구원으로 분석 중...")
            researcher = basic_researcher
            research_type = "기본"
        elif choice == '2':
            print("\n🔍 고급 연구원으로 분석 중...")
            researcher = advanced_researcher
            research_type = "고급"
        elif choice == '3':
            question = input("\n질문을 입력하세요: ").strip()
            if not question:
                print("❌ 질문을 입력해주세요.")
                continue
            
            print("\n🔍 고급 연구원으로 분석 중...")
            researcher = advanced_researcher
            research_type = "고급"
        elif choice == '4':
            print("\n👋 데모를 종료합니다.")
            break
        else:
            print("❌ 잘못된 선택입니다. 1-4 중에서 선택해주세요.")
            continue
        
        # 질문 선택 또는 입력
        if choice in ['1', '2']:
            print("\n📝 질문을 선택하세요:")
            for i, question in enumerate(test_questions, 1):
                print(f"  {i}. {question}")
            
            try:
                q_choice = int(input(f"\n질문 번호를 입력하세요 (1-{len(test_questions)}): "))
                if 1 <= q_choice <= len(test_questions):
                    selected_question = test_questions[q_choice - 1]
                else:
                    print("❌ 잘못된 번호입니다.")
                    continue
            except ValueError:
                print("❌ 숫자를 입력해주세요.")
                continue
        else:
            selected_question = question
        
        print(f"\n❓ 선택된 질문: {selected_question}")
        print(f"🔬 연구원 타입: {research_type}")
        print("-" * 40)
        
        try:
            # 연구 수행
            start_time = time.time()
            result = researcher.research_question(selected_question)
            end_time = time.time()
            
            # 결과 표시
            print(f"\n💡 답변:")
            print(f"{result.answer}")
            
            print(f"\n🎯 신뢰도: {result.confidence:.2f}")
            print(f"🔍 추론: {result.reasoning}")
            print(f"📚 참고 소스: {len(result.sources)}개")
            
            if hasattr(result, 'fact_checks'):
                print(f"✅ 사실 검증: {len(result.fact_checks)}개")
            
            if hasattr(result, 'limitations') and result.limitations:
                print(f"⚠️ 한계점: {', '.join(result.limitations)}")
            
            print(f"⏱️ 처리 시간: {end_time - start_time:.2f}초")
            
            # 상세 소스 정보
            if result.sources:
                print(f"\n📖 주요 참고 소스:")
                for i, source in enumerate(result.sources[:3], 1):
                    print(f"  {i}. {source.title}")
                    print(f"     도메인: {getattr(source, 'domain', source.source)}")
                    print(f"     신뢰도: {source.credibility_score:.2f}")
                    print(f"     URL: {source.url}")
                    print()
            
            # 사실 검증 상세 정보
            if hasattr(result, 'fact_verifications') and result.fact_verifications:
                print(f"🔍 사실 검증 상세:")
                for i, verification in enumerate(result.fact_verifications, 1):
                    print(f"  {i}. {verification.statement}")
                    print(f"     검증됨: {'예' if verification.is_verified else '아니오'}")
                    print(f"     신뢰도: {verification.confidence:.2f}")
                    print(f"     방법: {verification.verification_method}")
                    print()
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        
        print("=" * 60)
        
        # 계속할지 묻기
        continue_choice = input("\n다른 질문을 분석하시겠습니까? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes', '예', 'ㅇ']:
            break
    
    print("\n🎉 데모가 완료되었습니다!")
    print("AI 웹 연구원이 인터넷에서 정보를 검색하고 진실성을 검증하여")
    print("질문에 답변하는 과정을 확인했습니다.")

if __name__ == "__main__":
    main()
