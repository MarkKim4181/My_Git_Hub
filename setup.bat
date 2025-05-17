@echo off
echo ======== 이미지 텍스트 추출기 설치 스크립트 ========
echo.

REM 필요한 패키지 설치
echo 1. 필요한 패키지 설치 중...
pip install -r requirements.txt

REM EXE 파일 생성
echo.
echo 2. EXE 파일 생성 중...
python build_exe.py

echo.
echo 설치가 완료되었습니다!
echo 실행 파일 위치: dist\이미지_텍스트_추출기\이미지_텍스트_추출기.exe
echo.
echo ===================================================
pause 