#!/usr/bin/env python3
"""
말장난 탐지기 테스트
"""

from puns_detector import PunsDetector

def test_puns_detector():
    detector = PunsDetector()
    
    # 말장난 테스트 문장들
    test_statements = [
        '개는 개고 고양이는 고양이다',
        '바나나는 바나나가 아니다', 
        '물은 물이지만 얼음은 물이 아니다',
        '사과는 사과지만 사과는 사과가 아니다',
        '시간은 시간이지만 시간은 시간이 아니다'
    ]
    
    print('🎭 AI 말장난 이해 능력 테스트')
    print('=' * 50)
    
    for statement in test_statements:
        print(f'\n문장: {statement}')
        analysis = detector.analyze_with_puns_detection(statement)
        
        if analysis['is_pun_detected']:
            print(f'✅ 말장난 감지! 이해도: {analysis["pun_understanding"]:.1%}')
            print(f'📝 유형: {analysis["pun_types"]}')
            print(f'💬 AI 응답: {analysis["pun_response"][:100]}...')
        else:
            print('❌ 말장난 미감지')
    
    print('\n' + '=' * 50)
    print('🎯 테스트 완료!')

if __name__ == "__main__":
    test_puns_detector()
