@echo off
chcp 65001 >nul
echo ============================================================
echo 🤖 AI 진실성 탐지기 - 버전 통합 실행 시스템
echo ============================================================
echo.

REM 가상환경 활성화
if exist "ai_truth_env\Scripts\activate.bat" (
    echo 가상환경 활성화 중...
    call ai_truth_env\Scripts\activate.bat
) else (
    echo 가상환경을 찾을 수 없습니다. 기본 Python을 사용합니다.
)

REM 필요한 패키지 설치 확인
echo 필요한 패키지 설치 확인 중...
python -c "import flask, flask_cors, flask_restx, flask_jwt_extended, flask_socketio" 2>nul
if errorlevel 1 (
    echo 필요한 패키지를 설치합니다...
    pip install flask flask-cors flask-restx flask-jwt-extended flask-socketio
)

echo.
echo 통합 실행 시스템을 시작합니다...
echo.

REM 통합 실행 스크립트 실행
python run_versions.py

pause
