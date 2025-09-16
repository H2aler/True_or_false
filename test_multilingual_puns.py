#!/usr/bin/env python3
"""
다국어 말장난 탐지기 테스트
"""

from puns_detector import PunsDetector

def test_multilingual_puns():
    detector = PunsDetector()
    
    # 테스트 문장들
    test_statements = [
        # 한글 말장난
        "개는 개고 고양이는 고양이다",
        "바나나는 바나나가 아니다",
        
        # 다국어 말장난 (한글-영어 혼합)
        "개는 dog고 고양이는 cat이다",
        "banana는 바나나가 아니다",
        
        # 영어 말장난
        "dog is dog and cat is cat",
        "banana is not banana",
        
        # 일반 문장 (말장난 아님)
        "오늘 날씨가 좋다",
        "The weather is nice today"
    ]
    
    print('🌍 다국어 말장난 탐지 테스트')
    print('=' * 60)
    
    for i, statement in enumerate(test_statements, 1):
        print(f'\n테스트 {i}: {statement}')
        analysis = detector.analyze_with_puns_detection(statement)
        
        if analysis['is_pun_detected']:
            print(f'✅ 말장난 감지! 이해도: {analysis["pun_understanding"]:.1%}')
            print(f'📝 유형: {analysis["pun_types"]}')
            print(f'💬 AI 응답: {analysis["pun_response"][:100]}...')
            
            # 다국어 말장난 특별 표시
            multilingual_puns = [p for p in analysis['detected_puns'] if p.get('multilingual', False)]
            if multilingual_puns:
                print('🌍 다국어 말장난 감지됨!')
                for pun in multilingual_puns:
                    print(f'   - {pun.get("korean_word", "")}는 {pun.get("english_word", "")}이다')
        else:
            print('❌ 말장난 미감지')
    
    print('\n' + '=' * 60)
    print('🎯 다국어 말장난 테스트 완료!')

if __name__ == "__main__":
    test_multilingual_puns()
