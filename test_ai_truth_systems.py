#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Truth Systems Test
AI 진실성 시스템 테스트

AI가 자신의 거짓말을 감지하고 교정하는 모든 시스템을 테스트합니다.
"""

import sys
import time
import subprocess
from pathlib import Path

def run_script(script_name: str, description: str):
    """스크립트 실행"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"📁 스크립트: {script_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ 실행 성공!")
            print("\n📋 출력:")
            print(result.stdout)
        else:
            print("❌ 실행 실패!")
            print(f"오류 코드: {result.returncode}")
            print(f"오류 메시지: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ 실행 시간 초과 (30초)")
    except Exception as e:
        print(f"❌ 실행 중 오류 발생: {e}")

def main():
    """메인 테스트 함수"""
    print("🤖 AI 진실성 시스템 종합 테스트")
    print("=" * 60)
    print("이 테스트는 AI가 자신의 거짓말을 감지하고 교정하는")
    print("모든 시스템을 순차적으로 실행합니다.")
    print("=" * 60)
    
    # 테스트할 스크립트들
    test_scripts = [
        ("ai_self_truth_detector.py", "AI 자체 진실성 탐지기 - 기본 버전"),
        ("ai_real_time_truth_monitor.py", "AI 실시간 진실성 모니터 - 실시간 버전"),
        ("ai_meta_truth_system.py", "AI 메타-진실성 시스템 - 고급 버전")
    ]
    
    # 각 스크립트 실행
    for script_name, description in test_scripts:
        if Path(script_name).exists():
            run_script(script_name, description)
            time.sleep(2)  # 스크립트 간 간격
        else:
            print(f"\n❌ 스크립트를 찾을 수 없습니다: {script_name}")
    
    print(f"\n{'='*60}")
    print("🎉 모든 테스트 완료!")
    print("=" * 60)
    print("📊 테스트 요약:")
    print("1. AI 자체 진실성 탐지기 - 기본적인 거짓말 감지 및 교정")
    print("2. AI 실시간 진실성 모니터 - 실시간 모니터링 및 자동 교정")
    print("3. AI 메타-진실성 시스템 - 고급 메타-인지 및 자기 성찰")
    print("\n💡 각 시스템은 AI가 스스로 자신의 출력을 분석하고")
    print("   1% 이상 거짓말이 감지되면 자동으로 교정합니다.")
    print("=" * 60)

if __name__ == "__main__":
    main()
