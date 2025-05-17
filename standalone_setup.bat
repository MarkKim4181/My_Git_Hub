@echo off
echo ======== 독립 실행형 이미지 텍스트 추출기 설치 스크립트 ========
echo.

REM requests 패키지 설치 (다운로드에 필요)
echo 0. requests 패키지 설치 중...
pip install requests

REM 필요한 패키지 설치
echo 1. 빌드 스크립트 실행 중...
python build_standalone_exe.py

echo.
echo 설치가 완료되었습니다!
echo 실행 파일 위치: dist\이미지_텍스트_추출기_독립실행형\이미지_텍스트_추출기_독립실행형.exe
echo.
echo 이 실행 파일은 다른 PC에서도 Tesseract OCR 설치 없이 바로 실행할 수 있습니다.
echo ===================================================
pause 